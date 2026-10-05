"""Feed the canonical solutions through checkpoints_def's Checkpoint objects, so CI catches a
feynlag/feynlag-models API drift even if nbmake is skipped."""

from puzzles.flavor_puzzle import checkpoints_def as cd
from puzzles.flavor_puzzle.solutions import step_1, step_2


def test_check_1_passes_with_canonical_solution(sm_ckm_bundle):
    assert cd.make_check_1(sm_ckm_bundle)(step_1.sm_yukawas(sm_ckm_bundle)["yt"]) is True


def test_check_2_passes_with_canonical_solution(sm_ckm_bundle):
    span = step_1.free_parameter_log10_span(step_1.sm_free_parameters(sm_ckm_bundle))
    assert cd.make_check_2(sm_ckm_bundle)(span) is True


def test_check_3_passes_with_canonical_solution(sm_ckm_bundle):
    A = step_2.wolfenstein(step_2.ckm_numeric(sm_ckm_bundle))["A"]
    assert cd.make_check_3(sm_ckm_bundle)(A) is True


def test_check_1_rejects_a_wrong_answer(sm_ckm_bundle):
    assert cd.make_check_1(sm_ckm_bundle)(1.0) is False
