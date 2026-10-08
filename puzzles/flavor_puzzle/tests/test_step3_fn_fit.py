"""Step 3 (P3): froggatt_nielsen fitted to the quark data, and the constrained-minimum span."""

import math

import numpy as np
import pytest

from fit.stage1 import chi2_gaussian
from puzzles.flavor_puzzle.solutions import step_1, step_2, step_3


@pytest.fixture(scope="module")
def predictor(p3):
    return p3["predictor"]


def _random_point(seed=7):
    rng = np.random.default_rng(seed)
    return 0.2, np.exp(rng.uniform(-1, 1, 18)), rng.uniform(0, 2 * math.pi, 18)


# --- the machinery ------------------------------------------------------------------------------
def test_ckm_angles_round_trip_on_sm_ckm(puzzle, sm_ckm_bundle):
    """The angle and delta extraction recovers sm_ckm's PDG 2024 Eq. (12.28) inputs."""
    angles = step_3.ckm_angles(step_2.ckm_numeric(sm_ckm_bundle))
    q = {s.name: s.value for s in puzzle.sm_quantities}
    for name in step_3.CKM_OBSERVABLES:
        assert angles[name] == pytest.approx(q[name], rel=1e-10)


def test_fit_is_built_with_v_F(puzzle, predictor):
    v_F = {s.name: s.value for s in puzzle.sm_quantities}["v_F"]
    assert predictor.w == pytest.approx(v_F / math.sqrt(2), rel=1e-15)


def test_numpy_path_matches_model_dps60(predictor):
    """The fast numpy SVD agrees with models.froggatt_nielsen.model.mass_basis / ckm at dps=60."""
    point = _random_point()
    fast, slow = predictor(*point), step_3.recompute_with_model(predictor, *point)
    for name in step_3.OBSERVABLES:
        assert fast[name] == pytest.approx(slow[name], rel=1e-10)


def test_eps_flat_direction_is_exact(predictor):
    """eps -> eps/k, |c_ij| -> |c_ij| k^n_ij leaves every prediction unchanged (n_ij = a_i + b_j),
    so the data cannot fix eps."""
    eps, abs_c, args = _random_point()
    base = predictor(eps, abs_c, args)
    for k in (0.5, 1.9):
        moved = predictor(*step_3.flat_direction(predictor, eps, abs_c, k), args)
        for name in step_3.OBSERVABLES:
            assert moved[name] == pytest.approx(base[name], rel=1e-10)


def test_eight_fixed_phases_are_a_rephasing_gauge(predictor):
    """Any 18 phases can be rephased (Q_i, u_j, d_j) to zero the 8 FIXED_PHASES, with the same
    predictions: the gauge choice loses nothing."""
    eps, abs_c, args = _random_point()
    a = dict(zip(step_3.ENTRIES, args))
    phi_u = {3: a["cu33"], 1: a["cu31"], 2: a["cu32"]}
    phi_Q = {3: 0.0, 1: phi_u[3] - a["cu13"], 2: phi_u[3] - a["cu23"]}
    phi_d = {j: a[f"cd3{j}"] for j in (1, 2, 3)}
    shifted = []
    for n in step_3.ENTRIES:
        i, j = int(n[2]), int(n[3])
        shifted.append(a[n] + phi_Q[i] - (phi_u[j] if n.startswith("cu") else phi_d[j]))
    shifted = dict(zip(step_3.ENTRIES, shifted))
    assert all(abs(math.remainder(shifted[n], 2 * math.pi)) < 1e-12 for n in step_3.FIXED_PHASES)
    base, gauged = predictor(eps, abs_c, args), predictor(eps, abs_c, [shifted[n] for n in step_3.ENTRIES])
    for name in step_3.OBSERVABLES:
        assert gauged[name] == pytest.approx(base[name], rel=1e-10)


def test_sm_limit_gives_the_quark_only_sm_span(puzzle, sm_ckm_bundle):
    """step_3's span function on the SM's own quark parameters gives sm_reference_values.quarks_only."""
    span = step_3.log10_span(list(step_1.sm_quark_parameters(sm_ckm_bundle).values()))
    assert span == pytest.approx(puzzle.quantifier.sm_reference_values["quarks_only"], abs=5e-4)


# --- the fit and the span (default pinned seeds) ---------------------------------------------------
def test_fit_reproduces_the_data(p3):
    """chi2_min ~ 0 and every pull ~ 0, also when recomputed with the model at dps=60. With 28 free
    parameters and 10 observables this shows the model accommodates the data, not that the data
    prefer it."""
    fit = p3["fit"]
    assert fit["chi2"] < 1e-6
    assert max(abs(p) for p in fit["pulls"].values()) < 1e-3
    assert chi2_gaussian(p3["recomputed"]["fit"], p3["observed"]) < 1e-6


@pytest.mark.parametrize("delta", step_3.DELTAS)
def test_minimum_span_respects_the_chi2_limit(p3, delta):
    res = p3["spans"][delta]
    assert res["feasible"]
    assert res["chi2"] <= p3["fit"]["chi2"] + delta + 1e-6
    assert res["span"] == pytest.approx(step_3.log10_span(res["abs_c"]), abs=1e-12)


def test_minimum_span_point_recomputed_with_model(p3):
    """The headline (delta = 1) point, recomputed at dps=60, still satisfies the chi2 limit."""
    head = p3["spans"][1.0]
    assert chi2_gaussian(p3["recomputed"]["span"], p3["observed"]) <= head["limit"] + 1e-6


def test_larger_delta_never_gives_a_larger_span(p3):
    assert p3["spans"][4.0]["span"] <= p3["spans"][1.0]["span"] + 1e-3


def test_fn_span_is_below_the_quark_only_sm_span(puzzle, p3):
    assert p3["spans"][1.0]["span"] < puzzle.quantifier.sm_reference_values["quarks_only"]


@pytest.mark.parametrize("delta", step_3.DELTAS)
def test_boxed_variant_stays_in_the_box(p3, delta):
    res = p3["boxed"][delta]
    lo, hi = step_3.BOX
    assert res["feasible"]
    assert np.all(res["abs_c"] >= lo * (1 - 1e-9)) and np.all(res["abs_c"] <= hi * (1 + 1e-9))


def test_tuning_measure_and_constrained_set(p3):
    """The tuning measure is reported and flagged consistently; every one of the 18 quark |c|
    enters some observable (all of them enter m_u m_c m_t ~ |det c| at leading order)."""
    tuning = p3["tuning"]
    assert tuning["flagged"] == (tuning["max"] > step_3.TUNING_FLAG)
    assert len(step_3.constrained_entries(tuning)) == 18


# --- the full multi-start run ----------------------------------------------------------------------
@pytest.mark.slow
@pytest.mark.timeout(3600)  # ~17 min for 32 starts, plus the 4 pinned seeds
def test_full_multistart_is_stable(puzzle):
    """32 starts: the two smallest feasible spans agree within 0.02 at each delta, and the default
    pinned seeds land within 0.02 of the full run's minimum."""
    full = step_3.run_p3(puzzle, seeds=step_3.FULL_SEEDS)
    assert full["fit"]["chi2"] < 1e-6
    default = step_3.run_p3(puzzle, seeds=step_3.DEFAULT_SEEDS, bundle=full["bundle"])
    for delta in step_3.DELTAS:
        spans = full["spans"][delta]["spans"]
        assert len(spans) >= 2 and spans[1] - spans[0] < 0.02
        assert default["spans"][delta]["span"] - spans[0] < 0.02
