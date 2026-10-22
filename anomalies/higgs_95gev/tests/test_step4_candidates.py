"""Step 4: the candidate spectra re-derived by the feynlag-models bundles (no fit)."""

import math

import numpy as np
import pytest

from anomalies.higgs_95gev.solutions import step_2, step_4


def test_singlet_rederives_the_target_point(singlet_candidate, anomaly):
    s = step_4.singlet_spectrum(singlet_candidate)
    assert s["MH2"] == pytest.approx(step_4.TARGET_MASS_GEV, rel=1e-9)
    assert s["MH1"] == pytest.approx(step_4.heavy_mass(anomaly), rel=1e-9)
    assert math.sin(s["theta"]) == pytest.approx(step_4.SIN_THETA, rel=1e-9)


def test_singlet_h2_is_the_singlet_like_state(singlet_candidate):
    # the model labels by mixing, not by mass: with the singlet lighter, h2 is the light state
    s = step_4.singlet_spectrum(singlet_candidate)
    assert s["MH2"] < s["MH1"]
    assert s["h2_singlet_fraction"] > s["h2_doublet_fraction"]
    assert s["h2_singlet_fraction"] == pytest.approx(1 - step_4.SIN_THETA**2, rel=1e-9)


def test_singlet_override_matrix_by_hand(anomaly):
    from feynlag_models.registry import load

    base = load(step_4.SINGLET_ID).benchmark_point()
    o = step_4.singlet_override(base, step_4.TARGET_MASS_GEV, step_4.heavy_mass(anomaly))
    v, vS = base["v"], base["vS"]
    M = np.array([[o["MH"] ** 2, o["lamHS"] * v * vS], [o["lamHS"] * v * vS, 2 * o["lamS"] * vS**2]])
    assert sorted(np.sqrt(np.linalg.eigvalsh(M))) == pytest.approx(
        [step_4.TARGET_MASS_GEV, step_4.heavy_mass(anomaly)], rel=1e-12)


def test_universal_mu_is_sin2theta(singlet_candidate, anomaly):
    theta = step_4.singlet_spectrum(singlet_candidate)["theta"]
    assert step_4.universal_mu(theta) == pytest.approx(step_4.SIN_THETA**2, rel=1e-9)
    needed = step_4.sin2theta_needed(anomaly, [step_2.DIPHOTON_ROW, step_2.MU_TAUTAU_ROW])
    assert set(needed) == {step_2.DIPHOTON_ROW, step_2.MU_TAUTAU_ROW}


def test_thdm_inversion_is_consistent():
    p = step_4.THDM_POINT
    inv = step_4.thdm_gh_inversion(246.2184581018163, 95.0, 125.2, p["tanb"], p["sin_bma"],
                                   p["mA"], p["mHp"], p["m12sq"])
    assert sorted(np.sqrt(np.linalg.eigvalsh(inv["M"]))) == pytest.approx([95.0, 125.2])
    assert step_4.thdm_bounded_from_below(inv)
    # the regime of UG-4: M11 < M22, i.e. alpha_GH > pi/4
    assert inv["M"][0, 0] < inv["M"][1, 1] and inv["alpha_GH"] > math.pi / 4


@pytest.mark.xfail(strict=True, reason="UG-4: thdm_type2 puts the lighter CP-even state in the H "
                   "slot when M11 < M22 (principal-branch alpha)")
def test_thdm_inverted_hierarchy_labels(anomaly):
    bundle, _ = step_4.build_thdm_candidate(anomaly)
    s = step_4.thdm_spectrum(bundle)
    # Gunion-Haber labelling: m_H >= m_h, so H is the 125 GeV state and h the 95 GeV one
    assert s["MHH"] == pytest.approx(step_4.heavy_mass(anomaly), rel=1e-6)
    assert s["MH0"] == pytest.approx(step_4.TARGET_MASS_GEV, rel=1e-6)
