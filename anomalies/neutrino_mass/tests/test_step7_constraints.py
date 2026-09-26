"""Step 7: the step-6 fit against cosmology, 0nubetabeta and beta-decay bounds."""

import numpy as np
import pytest

from anomalies.neutrino_mass.solutions import step_6, step_7
from feynlag_anomalies.registry import load


@pytest.fixture(scope="module")
def fits(seesaw_2n_bundle, step6_fit):
    fit, observed = step6_fit
    alt = step_6.run_fit(seesaw_2n_bundle, observed, x0=step_6.alt_start(seesaw_2n_bundle))
    return {"benchmark": fit, "alt": alt}


@pytest.mark.parametrize("start", ["benchmark", "alt"])
def test_light_matrix_is_negative_semidefinite(seesaw_2n_bundle, fits, start):
    """Real Yukawas, positive M_R: m_nu = -A A^T, so every light eigenvalue is <= 0."""
    m = step_7.light_matrix(seesaw_2n_bundle, fits[start]["yv"])
    eig = np.linalg.eigvalsh(m)
    assert np.all(eig <= 1e-12 * np.max(np.abs(eig)))


@pytest.mark.parametrize("start", ["benchmark", "alt"])
def test_mbb_is_the_constructive_branch(seesaw_2n_bundle, fits, start):
    fit = fits[start]
    mbb = step_7.predictions(seesaw_2n_bundle, fit)["m_betabeta"]
    plus, minus = step_7.mbb_branches(fit["masses_eV"], fit["predicted"])
    assert mbb == pytest.approx(plus, rel=1e-6) and minus < plus


@pytest.mark.parametrize("start", ["benchmark", "alt"])
def test_matrix_route_agrees_with_takagi(seesaw_2n_bundle, fits, start):
    """Seesaw formula (to O(theta^2)) vs the exact Takagi masses and mixing."""
    fit = fits[start]
    preds = step_7.predictions(seesaw_2n_bundle, fit)
    exact = step_7.takagi_cross_check(seesaw_2n_bundle, fit["yv"])
    assert preds["m_betabeta"] == pytest.approx(exact["m_betabeta"], rel=1e-6)
    assert preds["m_beta"] == pytest.approx(exact["m_beta"], rel=1e-6)


def test_verdicts(seesaw_2n_bundle, fits):
    rows = step_7.confront(step_7.predictions(seesaw_2n_bundle, fits["benchmark"]), load("neutrino_mass"))
    for r in rows:
        assert r["passes"] == (r["prediction"] <= r["limit"])
    failing = [r["name"] for r in rows if not r["passes"]]
    # only the non-collaboration, prior-dependent cosmology bound is below the NO minimum
    assert len(failing) == 1 and "CMB-SPA" in failing[0]
