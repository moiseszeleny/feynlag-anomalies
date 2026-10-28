"""Step 2 -- the CMS ditau sigma x B on the signal-strength scale of the diphoton channel.

CMS ditau (arXiv:2208.02717) reports ``sigma(gg -> phi) x B(phi -> tau tau)`` in pb for a generic
scalar ``phi``. CMS diphoton reports a signal strength ``mu``, a ratio to an SM-like Higgs boson of
the same mass. To put the two on one scale, divide the ditau number by the same product for an
SM-like Higgs boson at 95 GeV:

    mu_tautau = [sigma x B]_obs
                / (sigma_ggF,SM-like(95 GeV, 13 TeV) x B_SM-like(H -> tau tau, 95 GeV)).

Both SM-like inputs are cited from the LHC Higgs Working Group tables and stored in
``anomaly.yaml`` ``sm_prediction.sm_reference_values`` (keys below); the ratio is computed here.

Uncertainties, kept apart (decisions.md, 2026-10-16):

* experimental: the stage-1 symmetrised CMS error (``stat_uncertainty`` of the ditau row, the
  mean of +3.9/-3.1 pb), propagated linearly, ``d mu = d(sigma B) / (sigma_SM B_SM)``;
* theory normalisation: the symmetrised ggF scale error, the ggF PDF+alpha_s error, the
  symmetrised B(tau tau) error and a missing-NLO-EW term, added in quadrature as relative errors
  on the denominator. The ggF table gives no NLO EW factor below 100 GeV, so none is applied; its
  size at 100 GeV (``1 + delta_EW = 1.0418``) is taken as a symmetric uncertainty instead.

The theory error is reported separately (``sys_uncertainty`` of the derived row) rather than
folded into the experimental one, so a later fit can treat it as a correlated nuisance.

The derived ``mu_tautau`` row and the ditau ``sigma x B`` row are the same measurement. A fit
must use one or the other, never both: :data:`EXCLUSIVE_WITH` records the pair.
"""

from __future__ import annotations

import math

from fit.stage1 import _reject_sentinel

DITAU_ROW = "sigma(gg -> phi) x B(phi -> tau tau) at m_phi = 95 GeV (CMS ditau)"
MU_TAUTAU_ROW = "signal strength mu_tautau at 95 GeV (CMS ditau, normalised to SM-like ggF x B)"
DIPHOTON_ROW = "signal strength mu at 95.4 GeV (CMS diphoton, best fit)"
#: observables rows that hold the same measurement; a fit selects at most one of each pair
EXCLUSIVE_WITH = {MU_TAUTAU_ROW: DITAU_ROW}

#: ``sm_prediction.sm_reference_values`` keys
SIGMA = "sigma_ggF_95GeV_13TeV_pb"
SIGMA_SCALE_UP = "sigma_ggF_95GeV_13TeV_scale_up_pct"
SIGMA_SCALE_DOWN = "sigma_ggF_95GeV_13TeV_scale_down_pct"
SIGMA_PDF = "sigma_ggF_95GeV_13TeV_pdf_alphas_pct"
BR = "BR_tautau_95GeV"
BR_UP = "BR_tautau_95GeV_up_pct"
BR_DOWN = "BR_tautau_95GeV_down_pct"
EW_100 = "sigma_ggF_100GeV_13TeV_EW_factor"
KEYS = (SIGMA, SIGMA_SCALE_UP, SIGMA_SCALE_DOWN, SIGMA_PDF, BR, BR_UP, BR_DOWN, EW_100)


def sm_inputs(anomaly) -> dict[str, float]:
    """The SM-like inputs from ``sm_prediction.sm_reference_values``; raises on ``TODO_VERIFY``."""
    ref = anomaly.sm_prediction.sm_reference_values
    return {k: _reject_sentinel(f"sm_prediction.sm_reference_values.{k}", ref[k]) for k in KEYS}


def observable(anomaly, name):
    (o,) = [o for o in anomaly.observables if o.name == name]
    return o


def sm_like_sigma_br(anomaly) -> float:
    """``sigma_ggF x B(tau tau)`` for an SM-like Higgs boson at 95 GeV, 13 TeV, in pb."""
    s = sm_inputs(anomaly)
    return s[SIGMA] * s[BR]


def theory_components_pct(anomaly) -> dict[str, float]:
    """The relative theory errors on the SM-like denominator, in percent, symmetrised."""
    s = sm_inputs(anomaly)
    return {
        "ggF scale": (s[SIGMA_SCALE_UP] + s[SIGMA_SCALE_DOWN]) / 2,
        "ggF PDF+alpha_s": s[SIGMA_PDF],
        "B(tau tau)": (s[BR_UP] + s[BR_DOWN]) / 2,
        "missing NLO EW": (s[EW_100] - 1) * 100,
    }


def theory_rel_uncertainty(anomaly) -> float:
    """Relative theory error on the SM-like denominator: the components in quadrature."""
    return math.sqrt(sum(x**2 for x in theory_components_pct(anomaly).values())) / 100


def mu_tautau(anomaly) -> dict[str, float]:
    """The ditau signal strength with its experimental and theory errors."""
    ditau = observable(anomaly, DITAU_ROW)
    sigma_b = _reject_sentinel(DITAU_ROW, ditau.value)
    d_sigma_b = _reject_sentinel(f"{DITAU_ROW} stat_uncertainty", ditau.stat_uncertainty)
    denom = sm_like_sigma_br(anomaly)
    mu = sigma_b / denom
    return {
        "mu": mu,
        "exp_uncertainty": d_sigma_b / denom,
        "theory_uncertainty": mu * theory_rel_uncertainty(anomaly),
        "sm_like_sigma_br_pb": denom,
    }
