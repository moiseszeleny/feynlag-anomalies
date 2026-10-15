"""Step 4: the familon bound on v_phi from K+ -> pi+ a (NA62), at the P3 points."""

import math

import pytest

from puzzles.flavor_puzzle.solutions import step_4

# Pinned at the stored Delta = 1 point (puzzles/flavor_puzzle/reference_point_delta1.json): the
# minimum span is unique but the point reaching it is not, so a fresh fit's point (and its
# coupling) can differ by platform. The Delta = 4 and best-fit points are fresh-fit points and are
# only used in point-independent checks (mass form = charge form, the loose spread check).
GHAT_DELTA1 = 0.1616245      # v_phi / |F^V_sd| at the stored Delta = 1 point
V_PHI_MIN_DELTA1 = 1.317917e11  # GeV


@pytest.fixture(scope="module")
def bounds(p3, puzzle):
    from puzzles.flavor_puzzle.solutions import step_3

    pts = {"delta1": step_3.load_reference_point(), "delta4": p3["spans"][4.0], "bestfit": p3["fit"]}
    return {k: step_4.bound_at(p3["predictor"], pt, puzzle) for k, pt in pts.items()}


def test_charges_reproduce_the_powers(bounds):
    """n_ij = q(Q_i) - q(d_j) at the benchmark charges, the premise of the Goldstone form."""
    assert all(b["charges_match_powers"] for b in bounds.values())


@pytest.mark.parametrize("point", ["delta1", "delta4", "bestfit"])
def test_mass_form_equals_goldstone_charge_form(bounds, point):
    """|G_sd + G_ds*| / (2 (m_s - m_d)) from the model's mass basis equals |(X_L + X_R)_sd| / 2
    from the rotated U(1)_FN charges: the conversion to arXiv:2002.04623 Eq. (17) is consistent
    with a being the U(1)_FN Goldstone, and no running-mass scale enters."""
    b = bounds[point]
    assert b["ghat_mass"] == pytest.approx(b["ghat_charge"], rel=1e-10)


def test_coupling_at_the_reported_point(bounds):
    assert bounds["delta1"]["ghat_mass"] == pytest.approx(GHAT_DELTA1, rel=1e-6)


def test_rate_formula_reproduces_the_paper_worked_number(puzzle):
    """arXiv:2002.04623 Table III: F^V_sd > 6.8e11 GeV from BR(K+ -> pi+ a) < 7.3e-11 (E949), with
    their f_+(0) = 0.9706 (Table IV). Eqs. (5), (6) with PDG 2024 kaon inputs give 6.73e11, within
    rounding of the quoted 6.8 (2% tolerance)."""
    kin = {**step_4.kaon_inputs(puzzle), "f_plus": 0.9706}
    assert step_4.F_min(7.3e-11, kin) == pytest.approx(6.8e11, rel=0.02)


def test_bound_on_v_phi(bounds):
    b = bounds["delta1"]
    assert b["br_max"] == pytest.approx(4.96e-11, rel=1e-12)
    assert b["v_phi_min"] == pytest.approx(V_PHI_MIN_DELTA1, rel=1e-6)
    assert b["Lambda_min"] == pytest.approx(b["v_phi_min"] / (math.sqrt(2) * b["eps"]), rel=1e-12)


def test_cut_passes_above_and_fails_below_the_bound(bounds, puzzle):
    """The hard cut admits every v_phi above the bound, so the fit survives the constraint."""
    b = bounds["delta1"]
    assert step_4.familon_cut(1.01 * b["v_phi_min"], b["ghat_mass"], puzzle)
    assert step_4.familon_cut(1e3 * b["v_phi_min"], b["ghat_mass"], puzzle)
    assert not step_4.familon_cut(0.99 * b["v_phi_min"], b["ghat_mass"], puzzle)


def test_model_benchmark_v_phi_is_excluded(p3, bounds, puzzle):
    """The model's benchmark v_phi = 2.83 TeV is far below the bound: not a viable point."""
    v_bench = float(p3["bundle"].benchmark["vphi"])
    b = bounds["delta1"]
    assert not step_4.familon_cut(v_bench, b["ghat_mass"], puzzle)
    assert b["v_phi_min"] / v_bench > 1e7


def test_spread_over_points(bounds):
    """Regression check on these three stored points only (Delta = 1, Delta = 4, best fit): their
    bounds agree within a factor 5. It says nothing about other points of the chi2 <= chi2_min + 1
    region, where a tuned alignment of (X_L + X_R)_sd can make the coupling much smaller."""
    vs = [b["v_phi_min"] for b in bounds.values()]
    assert max(vs) / min(vs) < 5


def test_sentinel_rejected(puzzle):
    from fit.stage1 import Stage1Error

    broken = puzzle.model_copy(deep=True)
    [c for c in broken.constraints if c.quantity == step_4.CONSTRAINT_QUANTITY][0].upper_limit = "TODO_VERIFY"
    with pytest.raises(Stage1Error):
        step_4.br_limit(broken)


def test_u1_fn_is_qcd_anomalous_with_the_model_charges():
    """The U(1)_FN-SU(3)_c^2 anomaly coefficient, computed from froggatt_nielsen's benchmark charges
    (via the registry), is nonzero: a is massless only at tree level, an axiflavon with QCD."""
    from feynlag_models.registry import metadata

    bench = metadata("froggatt_nielsen")["benchmark"]["inputs"]
    coeff = step_4.colour_anomaly_coefficient(bench)
    assert coeff == int(coeff) and coeff != 0
