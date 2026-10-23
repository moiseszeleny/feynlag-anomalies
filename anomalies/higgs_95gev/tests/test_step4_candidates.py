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
    m12 = o["lamHS"] * v * vS
    M = np.array([[o["MH"] ** 2, m12], [m12, 2 * o["lamS"] * vS**2]])
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


def test_h2_zz_scales_with_sin_theta(singlet_bundle):
    # feynlag-models' test_coupling_rescaling pins h2 W W and h2 f f-bar; h2 Z Z is pinned here
    import sympy as sp
    from feynlag_models.checks import assert_dual_equal

    b, p = singlet_bundle.bosons, singlet_bundle.pieces
    th = singlet_bundle.extra["theta"].s
    g, gp, v = p.gw.s, p.g1.s, p.ew.v.s
    rules = singlet_bundle.model.feynman_rules(singlet_bundle.boson_list, sector="kinetic",
                                               conjugate_map=singlet_bundle.cmap,
                                               simplifier=sp.simplify)
    legs = tuple(sorted((b["h2"], b["Z"], b["Z"]), key=lambda f: f.sort_key()))
    assert_dual_equal(rules[legs], -sp.I * (g**2 + gp**2) * v / 2 * sp.sin(th), msg="h2ZZ")


def test_thdm_aligned_point_keeps_its_labels(thdm_aligned, anomaly):
    bundle, inv = thdm_aligned
    p = step_4.THDM_ALIGNED_POINT
    s = step_4.thdm_spectrum(bundle)
    # alpha_GH < pi/4 (M11 > M22): the model's h is the 95 GeV state and its H the 125 GeV one
    assert inv["alpha_GH"] < math.pi / 4 and inv["M"][0, 0] > inv["M"][1, 1]
    assert s["MH0"] == pytest.approx(step_4.TARGET_MASS_GEV, rel=1e-6)
    assert s["MHH"] == pytest.approx(step_4.heavy_mass(anomaly), rel=1e-6)
    assert s["MA0"] == pytest.approx(p["mA"], rel=1e-6)
    assert s["MHp"] == pytest.approx(p["mHp"], rel=1e-6) and p["mHp"] >= step_4.MHP_MIN_GEV
    # the model's alpha is Gunion-Haber's here, so sin(beta - alpha) of the 95 GeV h is 0.3
    assert math.sin(math.atan(p["tanb"]) - s["alpha"]) == pytest.approx(p["sin_bma"], rel=1e-6)
    assert step_4.thdm_bounded_from_below(inv)


def test_thdm_coupling_scan(anomaly):
    rows = step_4.thdm_coupling_scan(246.2184581018163, step_4.TARGET_MASS_GEV,
                                     step_4.heavy_mass(anomaly))
    assert len(rows) == 15
    # m_H+- >= 580 GeV with a 95 GeV h and a 125 GeV H: every BFB point needs |lambda| > 10.8
    assert min(r["max_abs_lambda"] for r in rows) > 10.8
    # the aligned point is the scan minimum at its (tan beta, sin(beta - alpha))
    p = step_4.THDM_ALIGNED_POINT
    (row,) = [r for r in rows if (r["tanb"], r["sin_bma"]) == (p["tanb"], p["sin_bma"])]
    assert row["labels_kept"] and (row["mA"], row["m12sq"]) == (p["mA"], p["m12sq"])
    assert row["max_abs_lambda"] == pytest.approx(10.9, abs=0.05)
