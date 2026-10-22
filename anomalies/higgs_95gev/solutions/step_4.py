"""Step 4 -- candidate models that put a CP-even scalar at 95 GeV (computed spectra, no fit).

Both models come from feynlag-models through ``registry.build(model_id, benchmark=override)``;
neither is edited (CLAUDE.md hard rule 4). The override benchmarks are solved here, numerically,
from physical-basis targets, and the bundle must re-derive the target masses.

``sm_singlet_z2`` (L3). The CP-even mass matrix in the ``(h, s)`` basis is
``[[2 lam v^2, lamHS v vS], [lamHS v vS, 2 lamS vS^2]]`` (model key result, Robens--Stefaniak
Eq. 7). Its input ``MH`` fixes ``lam = MH^2/(2 v^2)``, the ``(h, h)`` entry, not an eigenvalue,
so a 95 GeV singlet-like state needs ``MH`` below the measured Higgs mass. The model rotates
``(h1, h2) = R(theta) (h, s)`` with the principal-branch ``tan 2 theta``, so **h1 is always the
h-like state** and, with the singlet lighter, the 95 GeV singlet-like state is **h2**
(``MH2``). Every h2 coupling to SM particles is the SM one times ``-sin theta`` (model key result
``test_coupling_rescaling``) and h2 at 95 GeV cannot decay to h1 pairs, so every h2 signal
strength is the same number, ``sin^2 theta``.

``thdm_type2`` (L3). The CP-even block is inverted numerically from the physical basis with
Gunion--Haber Eqs. (10)--(13) (lambda6 = lambda7 = 0, the model's potential). The model labels
``(H, h) = R(alpha) (rho1, rho2)`` with the principal-branch alpha, which coincides with
Gunion--Haber's ``m_H >= m_h`` branch only when ``M11 > M22`` (the model's own conventions_map).
For a 95 GeV ``h`` under a 125 GeV ``H`` with ``alpha_GH > pi/4`` the model swaps the labels: its
``H`` gets 95 GeV. That is UG-4 (``docs/upstream_gaps.md``); the inversion stays here as its
evidence, and nothing works around it.
"""

from __future__ import annotations

import math

import numpy as np

from fit.stage1 import _reject_sentinel

from anomalies.higgs_95gev.solutions import step_1

SINGLET_ID = "sm_singlet_z2"
THDM_ID = "thdm_type2"
#: the mass of the excess the candidates must reproduce (GeV): the mass at which the SM-like
#: reference values of step 2 are tabulated, inside step_1.WINDOW_GEV
TARGET_MASS_GEV = 95.0
#: h-s mixing of the singlet benchmark (illustrative, not fitted)
SIN_THETA = 0.2
#: the 2HDM point used as UG-4 evidence: tan beta, sin(beta - alpha_GH) of the 95 GeV state,
#: m_A, m_H+- (GeV; m_H+- > 580 GeV at 95% CL from B -> X_s gamma, Misiak--Steinhauser
#: arXiv:1702.04571, as cited in feynlag-models' thdm_type2/NEXT_STEPS.md section 2) and m12^2 (GeV^2). Bounded from below; max |lambda_i| = 11.8.
THDM_POINT = {"tanb": 2.0, "sin_bma": 0.3, "mA": 300.0, "mHp": 600.0, "m12sq": 6000.0}


def heavy_mass(anomaly) -> float:
    """The measured Higgs mass (PDG 2024, from the record) for the SM-like state."""
    return step_1.measured_higgs_mass(anomaly)[0]


# --- the singlet ------------------------------------------------------------------------------
def singlet_override(benchmark: dict, m_light: float, m_heavy: float,
                     sin_theta: float = SIN_THETA) -> dict:
    """Benchmark inputs with an s-like state at ``m_light`` and an h-like one at ``m_heavy``.

    ``M = R(theta)^T diag(m_heavy^2, m_light^2) R(theta)`` in the ``(h, s)`` basis, then
    ``MH = sqrt(M11)``, ``lamS = M22/(2 vS^2)``, ``lamHS = M12/(v vS)`` at the model's ``v``, ``vS``.
    """
    v, vS = benchmark["v"], benchmark["vS"]
    c, s = math.sqrt(1 - sin_theta**2), sin_theta
    m11 = m_heavy**2 * c**2 + m_light**2 * s**2
    m22 = m_light**2 * c**2 + m_heavy**2 * s**2
    m12 = (m_heavy**2 - m_light**2) * c * s
    out = dict(benchmark)
    out.update(MH=math.sqrt(m11), lamS=m22 / (2 * vS**2), lamHS=m12 / (v * vS))
    return out


def singlet_spectrum(bundle) -> dict:
    """MH1, MH2, theta and the h2 eigenvector composition at the bundle's benchmark."""
    vals = bundle.values()
    e = bundle.extra
    mh1, mh2, theta = (float(vals[e[k].s]) for k in ("MH1", "MH2", "theta"))
    R = np.array(e["rot"].matrix.subs(e["theta"].s, theta).evalf(), dtype=float)
    return {"MH1": mh1, "MH2": mh2, "theta": theta,
            "h2_singlet_fraction": float(R[1, 1] ** 2),
            "h2_doublet_fraction": float(R[1, 0] ** 2)}


def build_singlet_candidate(anomaly, sin_theta: float = SIN_THETA):
    """``sm_singlet_z2`` at the override putting h2 (singlet-like) at TARGET_MASS_GEV."""
    from feynlag_models.registry import build, load

    base = load(SINGLET_ID).benchmark_point()
    return build(SINGLET_ID, benchmark=singlet_override(
        base, TARGET_MASS_GEV, heavy_mass(anomaly), sin_theta))


def universal_mu(theta: float) -> float:
    """Every h2 signal strength: ``sin^2 theta`` (couplings ``-sin theta`` x SM)."""
    return math.sin(theta) ** 2


def sin2theta_needed(anomaly, rows) -> dict[str, float]:
    """The ``sin^2 theta`` each recorded signal strength would need (displayed, not judged).

    Since every h2 signal strength is ``sin^2 theta``, that is the recorded value itself; a value
    above 1 cannot be reached by mixing alone.
    """
    out = {}
    for name in rows:
        (o,) = [o for o in anomaly.observables if o.name == name]
        out[name] = _reject_sentinel(f"observables[{name!r}].value", o.value)
    return out


# --- the 2HDM (UG-4 evidence) -----------------------------------------------------------------
def thdm_gh_inversion(v: float, m_light: float, m_heavy: float, tanb: float, sin_bma: float,
                      mA: float, mHp: float, m12sq: float) -> dict:
    """lambda_1..5 from the physical basis, Gunion--Haber Eqs. (10)--(13), lambda6 = lambda7 = 0.

    The CP-even states are ``(H, h) = R(alpha) (rho1, rho2)`` with ``m_H = m_heavy >= m_h =
    m_light`` and ``alpha = beta - asin(sin_bma)`` (Gunion--Haber's branch). Returns the lambdas,
    ``alpha_GH`` and the CP-even block ``M``.
    """
    beta = math.atan(tanb)
    sb, cb = math.sin(beta), math.cos(beta)
    alpha = beta - math.asin(sin_bma)
    R = np.array([[math.cos(alpha), math.sin(alpha)], [-math.sin(alpha), math.cos(alpha)]])
    M = R.T @ np.diag([m_heavy**2, m_light**2]) @ R
    lam1 = (M[0, 0] - m12sq * tanb) / (v**2 * cb**2)
    lam2 = (M[1, 1] - m12sq / tanb) / (v**2 * sb**2)
    lam345 = (M[0, 1] + m12sq) / (v**2 * sb * cb)
    lam5 = m12sq / (sb * cb * v**2) - mA**2 / v**2
    lam4 = lam5 - 2 * (mHp**2 - mA**2) / v**2
    lam3 = lam345 - lam4 - lam5
    return {"lam1": lam1, "lam2": lam2, "lam3": lam3, "lam4": lam4, "lam5": lam5,
            "alpha_GH": alpha, "M": M}


def thdm_bounded_from_below(lams: dict) -> bool:
    """Tree-level bounded-from-below conditions for the Z2-symmetric quartics (lambda6 = lambda7 = 0).

    The standard necessary and sufficient conditions, reported for the UG-4 point, not used to
    judge it.
    """
    l1, l2, l3, l4, l5 = (lams[f"lam{k}"] for k in range(1, 6))
    if l1 <= 0 or l2 <= 0:
        return False
    r = math.sqrt(l1 * l2)
    return l3 > -r and l3 + l4 - abs(l5) > -r


def build_thdm_candidate(anomaly, point: dict = THDM_POINT):
    """``thdm_type2`` at the GH-inverted point (95 GeV h under a 125 GeV H)."""
    from feynlag_models.registry import build, load

    base = load(THDM_ID).benchmark_point()
    inv = thdm_gh_inversion(base["v"], TARGET_MASS_GEV, heavy_mass(anomaly), point["tanb"],
                            point["sin_bma"], point["mA"], point["mHp"], point["m12sq"])
    bench = dict(base)
    bench.update(tanb=point["tanb"], m12sq=point["m12sq"],
                 **{f"lam{k}": inv[f"lam{k}"] for k in range(1, 6)})
    return build(THDM_ID, benchmark=bench), inv


def thdm_spectrum(bundle) -> dict:
    vals = bundle.values()
    e = bundle.extra
    return {k: float(vals[e[k].s]) for k in ("MH0", "MHH", "MA0", "MHp", "alpha")}
