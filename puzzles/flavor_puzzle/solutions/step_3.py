"""Step 3 (P3) -- stage-1 fit of feynlag-models' ``froggatt_nielsen`` to the quark data, and the
constrained-minimum span of its O(1) coefficients.

The model is imported through the registry; nothing here declares a Lagrangian. It is built at
its metadata benchmark with ``v = v_F = 246 GeV`` (``puzzle.yaml``), and its symbolic quark
Yukawas ``extra["Yu"]``, ``extra["Yd"]`` (``Y_ij = |c_ij| e^{i arg c_ij} eps^n_ij``) are
lambdified once. The fit loop diagonalises them with numpy's SVD (~0.1 ms a point); every
reported point is recomputed with the model's own ``mass_basis`` / ``ckm`` (feynlag's numeric
``diagonalize_svd``) at ``dps=60`` (:func:`recompute_with_model`).

Decisions this follows are in ``decisions.md`` (2026-10-08):

* quarks only; 10 observables: the six quark masses at M_Z and the PDG CKM sines plus delta;
* eps is free and outside the span. Because every power has the form ``n_ij = a_i + b_j``, the
  map ``eps -> eps/k, |c_ij| -> |c_ij| k^n_ij`` leaves every prediction unchanged
  (:func:`flat_direction`): the data cannot fix eps, so the fit holds it at :data:`EPS_REF` and
  only the span minimisation moves it;
* 8 of the 18 phases are removed by field rephasings (:data:`FIXED_PHASES`), leaving 10;
* span rule: min of ``log10(max|c| / min|c|)`` over the 18 quark ``|c|`` subject to
  ``chi2 <= chi2_min + delta``; delta = 1 headline, delta = 4 sensitivity; a boxed variant with
  every ``|c|`` in [1/3, 3]; and the tuning measure ``max |d ln O / d ln|c||`` at the
  minimum-span point, flagged above :data:`TUNING_FLAG`.

Importing this module is cheap (no model build).
"""

from __future__ import annotations

import math

import numpy as np
import sympy as sp

from fit.stage1 import _reject_sentinel, chi2_gaussian, minimize_chi2

MODEL_ID = "froggatt_nielsen"

#: ``puzzle.yaml`` ``sm_quantities[].name`` of the ten fitted observables, in order
MASS_OBSERVABLES = ("m_u(M_Z)", "m_c(M_Z)", "m_t(M_Z)", "m_d(M_Z)", "m_s(M_Z)", "m_b(M_Z)")
CKM_OBSERVABLES = ("sin theta_12", "sin theta_13", "sin theta_23", "delta")
OBSERVABLES = MASS_OBSERVABLES + CKM_OBSERVABLES

#: the quark coefficient blocks of the model, in the order the parameter vector uses
SECTORS = ("cu", "cd")
ENTRIES = tuple(f"{s}{i}{j}" for s in SECTORS for i in (1, 2, 3) for j in (1, 2, 3))
#: phases set to zero by the 8 independent field rephasings (Q_i, u_j, d_j minus baryon number):
#: arg c^u_{i3} (3), arg c^u_{3j} for j = 1, 2 (2), arg c^d_{3j} (3)
FIXED_PHASES = ("cu13", "cu23", "cu33", "cu31", "cu32", "cd31", "cd32", "cd33")
FREE_PHASES = tuple(e for e in ENTRIES if e not in FIXED_PHASES)

EPS_REF = 0.2           #: reference eps for the fit (a gauge choice, see flat_direction)
DELTAS = (1.0, 4.0)     #: delta chi2: 1 is the headline, 4 the sensitivity check
BOX = (1 / 3, 3.0)      #: the boxed-variant range for every |c|
TUNING_FLAG = 10.0      #: flag the minimum-span point if max |d ln O / d ln|c|| exceeds this
LN_C_BOUND = math.log(1e3)
DEFAULT_SEEDS = (0, 1, 2, 3)  #: pinned seeds of the default test suite and the notebook
FULL_SEEDS = tuple(range(32))  #: the full multi-start run (slow test)
DPS = 60


# --- inputs -----------------------------------------------------------------------------------
def fn_benchmark(puzzle) -> dict:
    """``froggatt_nielsen``'s metadata benchmark with ``v`` replaced by the sourced ``v_F``."""
    from feynlag_models.registry import metadata

    bench = dict(metadata(MODEL_ID)["benchmark"]["inputs"])
    by_name = {q.name: q for q in puzzle.sm_quantities}
    bench["v"] = _reject_sentinel("v_F", by_name["v_F"].value)
    return bench


def observed_from_puzzle(puzzle) -> dict:
    """``{name: (value, sigma)}`` of the ten fitted observables, from ``puzzle.yaml``."""
    by_name = {q.name: q for q in puzzle.sm_quantities}
    return {n: (_reject_sentinel(n, by_name[n].value),
                _reject_sentinel(f"{n}.uncertainty", by_name[n].uncertainty))
            for n in OBSERVABLES}


# --- CKM angles from a matrix -------------------------------------------------------------------
def ckm_angles(V) -> dict:
    """PDG standard-parametrization ``sin theta_12, sin theta_13, sin theta_23, delta``.

    The sines come from ``|V_us|``, ``|V_ub|``, ``|V_cb|``; ``sin delta`` from the Jarlskog
    invariant ``J = Im(V_us V_cb V_ub* V_cs*) = c12 c23 c13^2 s12 s23 s13 sin delta`` and
    ``cos delta`` from ``|V_td|^2 = s12^2 s23^2 + c12^2 c23^2 s13^2 - 2 s12 s23 c12 c23 s13 cos
    delta`` (both rephasing invariant). ``delta`` is returned in [0, 2 pi).
    """
    V = np.asarray(V, dtype=complex)
    s13 = abs(V[0, 2])
    c13 = math.sqrt(1.0 - s13**2)
    s12, s23 = abs(V[0, 1]) / c13, abs(V[1, 2]) / c13
    c12, c23 = math.sqrt(1.0 - s12**2), math.sqrt(1.0 - s23**2)
    J = (V[0, 1] * V[1, 2] * np.conj(V[0, 2]) * np.conj(V[1, 1])).imag
    base = c12 * c23 * s12 * s23 * s13
    sin_d = J / (base * c13**2)
    cos_d = (s12**2 * s23**2 + c12**2 * c23**2 * s13**2 - abs(V[2, 0]) ** 2) / (2 * base)
    delta = math.atan2(sin_d, cos_d) % (2 * math.pi)
    return {"sin theta_12": s12, "sin theta_13": s13, "sin theta_23": s23, "delta": delta}


# --- the predictor ------------------------------------------------------------------------------
class FNQuarkPredictor:
    """The ten quark observables of a ``froggatt_nielsen`` bundle as a function of
    ``(eps, |c|, arg c)``, through numpy's SVD of the bundle's own lambdified Yukawas."""

    def __init__(self, bundle):
        e = bundle.extra
        values = bundle.values()
        self.bundle = bundle
        self.eps = e["eps"].s
        by_name = {p.name: p.s for p in e["c_params"]}
        self.abs_syms = [by_name[f"{n}_abs"] for n in ENTRIES]
        self.arg_syms = [by_name[f"{n}_arg"] for n in ENTRIES]
        self.powers = {"cu": e["powers"]["up"], "cd": e["powers"]["down"]}
        self.n = np.array([int(self.powers[n[:2]][int(n[2]) - 1, int(n[3]) - 1]) for n in ENTRIES])
        self._Y = sp.lambdify([self.eps, *self.abs_syms, *self.arg_syms], [e["Yu"], e["Yd"]], "numpy")
        self.w = float(e["ew"].v.s.subs(values)) / math.sqrt(2)
        self.benchmark_abs = np.array([float(values[s]) for s in self.abs_syms])
        self.benchmark_eps = float(values[self.eps])

    # parameter layout -------------------------------------------------------------------------
    @staticmethod
    def full_args(free_args) -> np.ndarray:
        """All 18 phases from the 10 free ones (the 8 rephasing-fixed ones are zero)."""
        args = dict(zip(FREE_PHASES, free_args))
        return np.array([args.get(n, 0.0) for n in ENTRIES])

    def yukawas(self, eps, abs_c, args):
        Yu, Yd = self._Y(eps, *abs_c, *args)
        return np.array(Yu, dtype=complex), np.array(Yd, dtype=complex)

    def spectrum(self, eps, abs_c, args):
        """``(m_up, m_down, V)``: masses ascending in GeV, ``V = U_L^u† U_L^d`` (rows u, c, t)."""
        Yu, Yd = self.yukawas(eps, abs_c, args)
        Uu, su, _ = np.linalg.svd(Yu)
        Ud, sd, _ = np.linalg.svd(Yd)
        V = Uu[:, ::-1].conj().T @ Ud[:, ::-1]
        return self.w * su[::-1], self.w * sd[::-1], V

    def __call__(self, eps, abs_c, args) -> dict:
        mu, md, V = self.spectrum(eps, abs_c, args)
        return {**dict(zip(MASS_OBSERVABLES, [*mu, *md])), **ckm_angles(V)}


def flat_direction(predictor, eps, abs_c, k):
    """``(eps / k, |c_ij| k^n_ij)``: the exact symmetry of every prediction (n_ij = a_i + b_j)."""
    return eps / k, np.asarray(abs_c) * k ** predictor.n


# --- recomputation with the model's own functions ------------------------------------------------
def recompute_with_model(predictor, eps, abs_c, args, dps=DPS) -> dict:
    """The ten observables at a point, with ``models.froggatt_nielsen.model.mass_basis`` / ``ckm``
    (feynlag's numeric ``diagonalize_svd``) at ``dps`` digits, instead of numpy."""
    from feynlag_models.registry import load

    model = load(MODEL_ID)
    e = predictor.bundle.extra
    values = dict(predictor.bundle.values())
    values[predictor.eps] = sp.Float(float(eps), dps)
    values.update({s: sp.Float(float(a), dps) for s, a in zip(predictor.abs_syms, abs_c)})
    values.update({s: sp.Float(float(a), dps) for s, a in zip(predictor.arg_syms, args)})
    mu = [predictor.w * float(y) for y in model.mass_basis(e["Yu"], values, dps)[2]]
    md = [predictor.w * float(y) for y in model.mass_basis(e["Yd"], values, dps)[2]]
    V = model.ckm(e["Yu"], e["Yd"], values, dps)
    return {**dict(zip(MASS_OBSERVABLES, [*mu, *md])), **ckm_angles(V)}


# --- the fit -------------------------------------------------------------------------------------
def _unpack_fit(x):
    return np.exp(x[:18]), FNQuarkPredictor.full_args(x[18:])


def run_fit(predictor, observed, seeds, eps=EPS_REF) -> dict:
    """Multi-start stage-1 chi2 fit of the 18 ``ln|c|`` and 10 free phases at fixed ``eps``.

    Each seed draws ``ln|c|`` uniform in [-1, 1] and phases uniform in [0, 2 pi). Returns the best
    fit plus every start's result (``"starts"``), each with ``eps``, ``abs_c``, ``args``.
    """
    lo = np.r_[np.full(18, -LN_C_BOUND), np.full(10, -np.inf)]
    hi = np.r_[np.full(18, LN_C_BOUND), np.full(10, np.inf)]
    starts = []
    for seed in seeds:
        rng = np.random.default_rng(seed)
        x0 = np.r_[rng.uniform(-1, 1, 18), rng.uniform(0, 2 * math.pi, 10)]
        res = minimize_chi2(lambda x: predictor(eps, *_unpack_fit(x)), x0, observed,
                            bounds=(lo, hi), x_scale=1.0, max_nfev=4000)
        abs_c, args = _unpack_fit(res["x"])
        starts.append({**res, "seed": seed, "eps": eps, "abs_c": abs_c, "args": args})
    best = min(starts, key=lambda r: r["chi2"])
    return {**best, "starts": sorted(starts, key=lambda r: r["chi2"])}


# --- the constrained-minimum span -----------------------------------------------------------------
def log10_span(abs_c) -> float:
    a = np.abs(np.asarray(abs_c, dtype=float))
    return math.log10(a.max() / a.min())


def minimize_span(predictor, observed, fit, delta, box=None) -> dict:
    """Min of ``log10(max|c| / min|c|)`` over the 18 quark ``|c|`` subject to
    ``chi2 <= fit["chi2"] + delta``, with eps free (it moves the |c| along the flat direction).

    Solved as ``min (u - l)`` with ``l <= ln|c_k| <= u`` and the chi2 constraint (SLSQP),
    started from every fit start. ``box=(lo, hi)`` also bounds every ``|c|``; if no start can
    reach the chi2 limit inside the box, the result has ``feasible=False`` and the best chi2
    found there. Returns the best point with ``eps``, ``abs_c``, ``args``, ``chi2``, ``span``.
    """
    from scipy.optimize import minimize

    limit = fit["chi2"] + delta
    lnc_lo, lnc_hi = (math.log(box[0]), math.log(box[1])) if box else (-LN_C_BOUND, LN_C_BOUND)

    def unpack(z):
        return math.exp(z[0]), np.exp(z[3:21]), FNQuarkPredictor.full_args(z[21:])

    def chi2(z):
        return chi2_gaussian(predictor(*unpack(z)), observed)

    cons = [{"type": "ineq", "fun": lambda z: limit - chi2(z)},
            {"type": "ineq", "fun": lambda z: z[3:21] - z[1]},
            {"type": "ineq", "fun": lambda z: z[2] - z[3:21]}]
    bounds = ([(math.log(1e-3), math.log(0.99)), (None, None), (None, None)]
              + [(lnc_lo, lnc_hi)] * 18 + [(None, None)] * 10)
    results = []
    for start in fit["starts"]:
        lnc = np.clip(np.log(start["abs_c"]), lnc_lo, lnc_hi)
        free = [dict(zip(ENTRIES, start["args"]))[n] for n in FREE_PHASES]
        z0 = np.r_[math.log(start["eps"]), lnc.min(), lnc.max(), lnc, free]
        res = minimize(lambda z: z[2] - z[1], z0, method="SLSQP", bounds=bounds,
                       constraints=cons, options={"maxiter": 500, "ftol": 1e-10})
        eps, abs_c, args = unpack(res.x)
        c2 = chi2(res.x)
        results.append({"eps": eps, "abs_c": abs_c, "args": args, "chi2": c2,
                        "span": log10_span(abs_c), "feasible": c2 <= limit + 1e-6,
                        "seed": start["seed"], "success": bool(res.success)})
    feasible = [r for r in results if r["feasible"]]
    if feasible:
        best = min(feasible, key=lambda r: r["span"])
    else:
        best = min(results, key=lambda r: r["chi2"])
    return {**best, "delta": delta, "box": box, "limit": limit,
            "spans": sorted(r["span"] for r in feasible)}


# --- the tuning measure ---------------------------------------------------------------------------
def tuning_measure(predictor, eps, abs_c, args, h=1e-6) -> dict:
    """``max |d ln O / d ln|c_k||`` over the ten observables and 18 ``|c|`` (central differences).

    Also returns the full sensitivity matrix (rows: observables, columns: ENTRIES) and each
    entry's largest sensitivity, used to check that every ``|c|`` is constrained.
    """
    S = np.zeros((len(OBSERVABLES), len(ENTRIES)))
    for k in range(len(ENTRIES)):
        up, dn = np.array(abs_c, dtype=float), np.array(abs_c, dtype=float)
        up[k] *= math.exp(h)
        dn[k] *= math.exp(-h)
        Ou, Od = predictor(eps, up, args), predictor(eps, dn, args)
        S[:, k] = (np.log([Ou[o] for o in OBSERVABLES]) - np.log([Od[o] for o in OBSERVABLES])) / (2 * h)
    per_entry = np.abs(S).max(axis=0)
    return {"max": float(np.abs(S).max()), "matrix": S, "per_entry": dict(zip(ENTRIES, per_entry)),
            "flagged": bool(np.abs(S).max() > TUNING_FLAG)}


def constrained_entries(tuning, rel=1e-2) -> list[str]:
    """Entries whose largest sensitivity is at least ``rel`` times the largest of all."""
    top = max(tuning["per_entry"].values())
    return [n for n, s in tuning["per_entry"].items() if s >= rel * top]


# --- everything P3 reports ------------------------------------------------------------------------
def run_p3(puzzle, seeds, bundle=None) -> dict:
    """Fit, spans at each delta, the boxed variant, the tuning measure and the dps=60 recomputation."""
    from feynlag_models.registry import build

    bundle = bundle or build(MODEL_ID, benchmark=fn_benchmark(puzzle))
    predictor = FNQuarkPredictor(bundle)
    observed = observed_from_puzzle(puzzle)
    fit = run_fit(predictor, observed, seeds)
    spans = {d: minimize_span(predictor, observed, fit, d) for d in DELTAS}
    boxed = {d: minimize_span(predictor, observed, fit, d, box=BOX) for d in DELTAS}
    head = spans[DELTAS[0]]
    tuning = tuning_measure(predictor, head["eps"], head["abs_c"], head["args"])
    recomputed = {
        "fit": recompute_with_model(predictor, fit["eps"], fit["abs_c"], fit["args"]),
        "span": recompute_with_model(predictor, head["eps"], head["abs_c"], head["args"]),
    }
    return {"bundle": bundle, "predictor": predictor, "observed": observed, "fit": fit,
            "spans": spans, "boxed": boxed, "tuning": tuning, "recomputed": recomputed}
