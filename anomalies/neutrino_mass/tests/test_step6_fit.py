"""Step 6: stage-1 chi2 of seesaw_type1_2n against NuFIT 6.0 (normal ordering)."""

import math

import numpy as np
import pytest

from anomalies.neutrino_mass.solutions import step_6
from feynlag_anomalies.registry import load
from feynlag_models.registry import metadata


def _rotation(i, j, theta):
    R = np.eye(3)
    c, s = math.cos(theta), math.sin(theta)
    R[i, i] = R[j, j] = c
    R[i, j], R[j, i] = s, -s
    return R


def test_fit_model_is_at_least_L2():
    """CLAUDE.md hard rule 7: only fit a candidate model at feynlag-models maturity >= L2."""
    assert metadata(step_6.MODEL_ID)["maturity_level"] >= 2


def test_fit_observables_are_sourced():
    """Every fitted observable holds a number, not the TODO_VERIFY sentinel."""
    observed = step_6.observed_from_anomaly(load("neutrino_mass"))
    assert set(observed) == set(step_6.FIT_OBSERVABLES)
    assert all(isinstance(v, float) and isinstance(s, float) and s > 0 for v, s in observed.values())


def test_predictor_inverts_ibarra_ross_eq_6(seesaw_2n_bundle):
    """Regression against a published parametrisation: Yukawas built with the two-nu_R
    Casas-Ibarra form (Ibarra-Ross, arXiv:hep-ph/0312138v2, Eq. (6); R = first two rows of their
    Eq. (5), + reflection, real z and U, <H0> = v/sqrt2) give back the input m2, m3 and angles.
    The inputs are arbitrary, not oscillation data."""
    m2, m3 = 0.01e-9, 0.05e-9                                        # GeV (0.01, 0.05 eV)
    t12, t13, t23 = (math.radians(a) for a in (33.0, 8.5, 45.0))
    z = 0.3
    U = _rotation(1, 2, t23) @ _rotation(0, 2, t13) @ _rotation(0, 1, t12)
    b = seesaw_2n_bundle.benchmark
    M1, M2, vev = b["MR1"], b["MR2"], b["v"] / math.sqrt(2)
    col1 = math.sqrt(M1) * (math.sqrt(m2) * math.cos(z) * U[:, 1] + math.sqrt(m3) * math.sin(z) * U[:, 2])
    col2 = math.sqrt(M2) * (-math.sqrt(m2) * math.sin(z) * U[:, 1] + math.sqrt(m3) * math.cos(z) * U[:, 2])
    yv = np.column_stack([col1, col2]).ravel() / vev                # yv_e1, yv_e2, yv_mu1, ...
    pred = step_6.OscillationPredictor(seesaw_2n_bundle)(yv)
    names = step_6.FIT_OBSERVABLES
    assert pred[names[0]] == pytest.approx((m2 * 1e9) ** 2, rel=1e-9)
    assert pred[names[1]] == pytest.approx((m3 * 1e9) ** 2, rel=1e-9)
    for name, angle in zip(names[2:], (33.0, 8.5, 45.0)):
        assert pred[name] == pytest.approx(angle, abs=1e-8)


def test_fit_accommodates_nufit(step6_fit):
    """The fit converges with every pull ~0: the model can reproduce both splittings and the
    three angles. ndof = -1 (six Yukawas, five observables), so this is not a goodness-of-fit test."""
    fit, _ = step6_fit
    assert fit["success"]
    assert fit["ndof"] == -1
    assert fit["chi2"] < 1e-6
    assert all(abs(p) < 1e-3 for p in fit["pulls"].values())
    assert fit["perturbative"]


def test_lightest_neutrino_is_massless(step6_fit):
    """The rank-2 prediction survives the fit: m1 = 0, so sum m_nu = m2 + m3 = sqrt(Dm21) + sqrt(Dm31)."""
    fit, observed = step6_fit
    m1, m2, m3 = fit["masses_eV"]
    assert m1 == 0.0
    assert fit["sum_m_nu_eV"] == pytest.approx(
        math.sqrt(observed[step_6.FIT_OBSERVABLES[0]][0]) + math.sqrt(observed[step_6.FIT_OBSERVABLES[1]][0]),
        rel=1e-6)


def test_sm_is_excluded_by_the_splittings(step6_fit):
    """Massless SM neutrinos: chi2 over the two splittings alone is (7.49/0.19)^2 + (2.513/0.020)^2."""
    fit, _ = step6_fit
    assert fit["chi2_sm_dm2"] > 1e4
    assert fit["chi2_model_dm2"] < 1e-6
