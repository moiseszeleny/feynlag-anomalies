"""Step 4 (P3 constraint) -- the familon bound on v_phi from K+ -> pi+ a.

In ``froggatt_nielsen`` the flavon phase ``a`` is the Goldstone of the global U(1)_FN (a familon):
massless at tree level, and an axiflavon once QCD is included, because U(1)_FN has a colour anomaly
with the LNS charges (:func:`colour_anomaly_coefficient`). Its QCD-induced mass is far below
``m_K - m_pi`` and does not affect K -> pi a. The model states
its one-flavon couplings (``metadata.yaml`` key result, test ``test_flavon_couplings``) as

    -M_ij (h/v + (|n_ij| s + i n_ij a) / v_phi) dbar_L,i d_R,j + h.c.,

so in the mass basis the ``a`` coupling is ``-a dbar_L G d_R + h.c.`` with
``G = R_L (i n o M) R_R^dagger / v_phi`` (``R_L``, ``R_R`` from the model's ``mass_basis``,
``R_L Y R_R^dagger = diag``; ``o`` the entrywise product). The s-bar d terms are
``-a sbar (G_sd P_R + G_ds^* P_L) d``: scalar part ``(G_sd + G_ds^*)/2``, pseudoscalar part
``(G_sd - G_ds^*)/2``. Parity lets only the scalar density mediate K -> pi (0^- -> 0^-).

The rate is Martin Camalich, Pospelov, Vuong, Ziegler, Zupan, arXiv:2002.04623 (PRD 102, 015023):

* Eq. (1)  ``L = d_mu a / (2 f_a) fbar_i gamma^mu (c^V_ij + c^A_ij gamma_5) f_j``,
* Eq. (2)  ``F^V_ij = 2 f_a / c^V_ij``,
* Eq. (5)  ``Gamma(P1 -> P2 a) = kappa_12 f_+(0)^2 / |F^V_ij|^2``,
* Eq. (6)  ``kappa_12 = M1^3 / (16 pi) (1 - M2^2 / M1^2)^3``,
* Eq. (17) the same interaction after the field redefinition (18):
  ``-i a / (2 f_a) fbar_i [(m_i - m_j) c^V_ij + (m_i + m_j) c^A_ij gamma_5] f_j``.

Matching the scalar s-bar d term of Eq. (17) to the model's gives the conversion

    1 / |F^V_sd| = |G_sd + G_ds^*| / (2 (m_s - m_d)).

Because ``a`` is the Goldstone of U(1)_FN with ``n_ij = q(Q_i) - q(d_j)``, the same number is
``|(X_L + X_R)_sd| / (2 v_phi)`` with ``X_L = R_L diag(q_Q) R_L^dagger`` and
``X_R = R_R diag(q_d) R_R^dagger``: the masses drop out, so no running-mass scale enters
(:func:`familon_coupling` returns both forms; a test pins their equality).

The bound: ``BR = Gamma tau_K / hbar <= BR_max`` gives
``v_phi >= ghat f_+(0) sqrt(kappa tau_K / (hbar BR_max))`` with ``ghat = v_phi / |F^V_sd|``,
which depends only on the fitted Yukawas (the P3 fit fixes eps; ``v_phi`` is free and
``Lambda = v_phi / (sqrt2 eps)``). ``hbar`` comes from the exact SI values of ``h`` and ``e``.
"""

from __future__ import annotations

import math

import numpy as np
import sympy as sp

from fit.stage1 import _reject_sentinel, upper_limit_cut

CONSTRAINT_QUANTITY = "br_k_to_pi_a"
INPUTS = {"m_K": "m_K+", "m_pi": "m_pi+", "tau_K": "tau_K+", "f_plus": "f_+(0) K->pi"}
DPS = 60


def hbar_gev_s() -> float:
    """hbar in GeV s from the exact 2019-SI constants (scipy.constants)."""
    from scipy import constants

    return constants.hbar / constants.e * 1e-9


# --- inputs from puzzle.yaml ----------------------------------------------------------------------
def kaon_inputs(puzzle) -> dict:
    """``m_K``, ``m_pi`` (GeV), ``tau_K`` (s), ``f_plus`` from ``sm_quantities``; sentinel-guarded."""
    by_name = {q.name: q for q in puzzle.sm_quantities}
    return {key: _reject_sentinel(name, by_name[name].value) for key, name in INPUTS.items()}


def br_limit(puzzle) -> float:
    """The NA62 upper limit on BR(K+ -> pi+ a) recorded in ``puzzle.yaml`` ``constraints``."""
    (c,) = [c for c in puzzle.constraints if c.quantity == CONSTRAINT_QUANTITY]
    return _reject_sentinel(c.name, c.upper_limit)


# --- the coupling ---------------------------------------------------------------------------------
def familon_coupling(predictor, point, dps=DPS) -> dict:
    """``ghat = v_phi / |F^V_sd|`` at a P3 point (``eps``, ``abs_c``, ``args``), two ways.

    ``ghat_mass``: from ``G v_phi = R_L (i n o M) R_R^dagger`` and the model's masses, as
    ``|G_sd + G_ds^*| v_phi / (2 (m_s - m_d))``. ``ghat_charge``: from the rotated U(1)_FN charges,
    ``|(X_L + X_R)_sd| / 2``. Also returns ``Gv`` (``v_phi G``), the masses and the pseudoscalar
    part, for reporting.
    """
    from feynlag_models.registry import load

    model = load("froggatt_nielsen")
    bundle = predictor.bundle
    e = bundle.extra
    values = dict(bundle.values())
    values[predictor.eps] = sp.Float(float(point["eps"]), dps)
    values.update({s: sp.Float(float(a), dps) for s, a in zip(predictor.abs_syms, point["abs_c"])})
    values.update({s: sp.Float(float(a), dps) for s, a in zip(predictor.arg_syms, point["args"])})
    RL, RR, y = model.mass_basis(e["Yd"], values, dps)
    RL = np.array(RL.evalf(30).tolist(), dtype=complex)
    RR = np.array(RR.evalf(30).tolist(), dtype=complex)
    masses = predictor.w * np.array([float(v) for v in y])
    M = predictor.w * np.array(sp.Matrix(e["Yd"]).subs(values).evalf(30).tolist(), dtype=complex)
    n = np.array(e["powers"]["down"].tolist(), dtype=float)
    Gv = RL @ (1j * n * M) @ RR.conj().T
    scalar = (Gv[1, 0] + np.conj(Gv[0, 1])) / 2
    pseudo = (Gv[1, 0] - np.conj(Gv[0, 1])) / 2
    qQ = np.array([bundle.benchmark[f"qQ{i}"] for i in (1, 2, 3)], dtype=float)
    qd = np.array([bundle.benchmark[f"qd{i}"] for i in (1, 2, 3)], dtype=float)
    XL = RL @ np.diag(qQ) @ RL.conj().T
    XR = RR @ np.diag(qd) @ RR.conj().T
    return {
        "ghat_mass": float(abs(scalar) / (masses[1] - masses[0])),
        "ghat_charge": float(abs(XL[1, 0] + XR[1, 0]) / 2),
        "Gv": Gv, "scalar": complex(scalar), "pseudoscalar": complex(pseudo),
        "m_d": float(masses[0]), "m_s": float(masses[1]),
        "charges_match_powers": bool(np.allclose(n, qQ[:, None] - qd[None, :])),
    }


def colour_anomaly_coefficient(benchmark) -> float:
    """The U(1)_FN-SU(3)_c^2 anomaly coefficient ``sum_generations (2 q_Q - q_u - q_d)``.

    Each quark doublet holds two colour triplets of charge ``q_Q``; ``u_R``, ``d_R`` enter as
    left-handed conjugates with charge ``-q``. Nonzero means U(1)_FN is QCD-anomalous, so ``a`` is
    an axiflavon. feynlag's ``check_anomalies`` skips global groups by design, hence this check.
    """
    q = {f: [float(benchmark[f"q{f}{i}"]) for i in (1, 2, 3)] for f in ("Q", "u", "d")}
    return 2 * sum(q["Q"]) - sum(q["u"]) - sum(q["d"])


# --- the rate and the bound -----------------------------------------------------------------------
def kappa(m_K, m_pi) -> float:
    """arXiv:2002.04623 Eq. (6), in GeV^3."""
    return m_K**3 / (16 * math.pi) * (1 - (m_pi / m_K) ** 2) ** 3


def width(inv_F, m_K, m_pi, f_plus) -> float:
    """arXiv:2002.04623 Eq. (5): ``Gamma(K -> pi a)`` in GeV for ``1/|F^V_sd|`` in 1/GeV."""
    return kappa(m_K, m_pi) * f_plus**2 * inv_F**2


def branching_ratio(ghat, v_phi, kin) -> float:
    """BR(K+ -> pi+ a) at ``v_phi`` (GeV) for the coupling ``ghat = v_phi / |F^V_sd|``."""
    gamma = width(ghat / v_phi, kin["m_K"], kin["m_pi"], kin["f_plus"])
    return gamma * kin["tau_K"] / hbar_gev_s()


def F_min(br_max, kin) -> float:
    """The lower bound on ``|F^V_sd|`` (GeV) from ``BR <= br_max``."""
    return kin["f_plus"] * math.sqrt(kappa(kin["m_K"], kin["m_pi"]) * kin["tau_K"]
                                     / (hbar_gev_s() * br_max))


def v_phi_min(ghat, br_max, kin) -> float:
    """The lower bound on ``v_phi`` (GeV): ``v_phi >= ghat * F_min``."""
    return ghat * F_min(br_max, kin)


def familon_cut(v_phi, ghat, puzzle) -> bool:
    """Hard cut in the style of ``fit/stage1.py``: True iff BR(K+ -> pi+ a) at ``v_phi`` passes the
    NA62 limit recorded in ``puzzle.yaml``. The cut is satisfied by choosing ``v_phi`` above
    :func:`v_phi_min` for the point's coupling ``ghat``; the bound is point dependent."""
    kin = kaon_inputs(puzzle)
    return upper_limit_cut(branching_ratio(ghat, v_phi, kin), br_limit(puzzle))


def bound_at(predictor, point, puzzle) -> dict:
    """Everything reported for one P3 point: coupling, ``v_phi_min`` and ``Lambda_min``."""
    kin, br_max = kaon_inputs(puzzle), br_limit(puzzle)
    coupling = familon_coupling(predictor, point)
    vmin = v_phi_min(coupling["ghat_mass"], br_max, kin)
    return {**coupling, "eps": float(point["eps"]), "v_phi_min": vmin,
            "Lambda_min": vmin / (math.sqrt(2) * float(point["eps"])), "br_max": br_max}
