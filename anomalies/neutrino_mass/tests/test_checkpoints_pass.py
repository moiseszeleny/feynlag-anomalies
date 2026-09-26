"""Feed the canonical solutions through checkpoints_def's Checkpoint objects.

Runs the same assertions ladder.ipynb's checkpoints make, without executing the notebook -- so
CI catches a feynlag/feynlag-models API drift even if nbmake is skipped.
"""

from anomalies.neutrino_mass import checkpoints_def as cd
from anomalies.neutrino_mass.solutions import step_0, step_1, step_2, step_5


def test_check_0_passes_with_canonical_solution():
    answer = step_0.m_nu_estimate(cd._P0_Y, cd._P0_V, cd._P0_M)
    assert cd.check_0(answer) is True


def test_check_1_passes_with_canonical_solution():
    assert cd.check_1(step_1.count_dim4_yukawa_terms()) is True


def test_check_2_passes_with_canonical_solution():
    assert cd.check_2(step_2.weinberg_operator_present()) is True


def test_check_3_passes_with_canonical_answer():
    assert cd.check_3("seesaw_type1") is True


def test_check_4_passes_with_canonical_answer(seesaw_bundle):
    check_4 = cd.make_check_4(seesaw_bundle)
    assert check_4(len(seesaw_bundle.extra["masses"])) is True


def test_check_5_passes_with_canonical_solution():
    assert cd.check_5(step_5.light_rank(1)) is True


def test_light_rank_counts_right_handed_neutrinos():
    """One nu_R gives a rank-1 light sector (one Delta m^2); two give rank 2 (both)."""
    assert step_5.light_rank(1) == 1
    assert step_5.light_rank(2) == 2


def test_light_mass_matrix_is_an_outer_product_for_one_nu_R():
    m = step_5.light_mass_matrix(1)
    assert m.shape == (3, 3) and m.rank(simplify=True) == 1 and m == m.T


def test_check_6_passes_with_canonical_answer(step6_fit):
    from anomalies.neutrino_mass.solutions.step_6 import FIT_OBSERVABLES
    from feynlag_anomalies.registry import load

    fit, _ = step6_fit
    answer = fit["predicted"][FIT_OBSERVABLES[1]] / fit["predicted"][FIT_OBSERVABLES[0]]
    assert cd.make_check_6(load("neutrino_mass"))(answer) is True
