"""Step 1: the Yukawas from sm_ckm and the SM value of the quantifier."""

import math
import re

import pytest

from fit.stage1 import Stage1Error
from puzzles.flavor_puzzle.solutions import step_1


def test_yukawas_match_published_definition(puzzle, sm_ckm_bundle):
    """sm_ckm's y_f = sqrt(2) m_f / v reproduces Huang-Zhou's definition m_f = y_f v_F / sqrt(2)
    (arXiv:2009.04851, Table 2 caption), computed here directly from the sourced masses."""
    q = {s.name: s.value for s in puzzle.sm_quantities}
    v_F = q["v_F"]
    yukawas = step_1.sm_yukawas(sm_ckm_bundle)
    # MASS_INPUTS and YUKAWAS list the fermions in the same order (u, c, t, d, s, b, e, mu, tau)
    for mass_name, y_name in zip(step_1.MASS_INPUTS, step_1.YUKAWAS):
        assert yukawas[y_name] == pytest.approx(math.sqrt(2) * q[mass_name] / v_F, rel=1e-12)


def test_ckm_sines_round_trip(puzzle, sm_ckm_bundle):
    q = {s.name: s.value for s in puzzle.sm_quantities}
    sines = step_1.sm_ckm_sines(sm_ckm_bundle)
    for name, key in step_1.CKM_INPUTS.items():
        if key in sines:
            assert sines[key] == pytest.approx(q[name], rel=1e-12)


def test_quantifier_sm_value_matches_yaml(puzzle, sm_ckm_bundle):
    span = step_1.free_parameter_log10_span(step_1.sm_free_parameters(sm_ckm_bundle))
    assert span == pytest.approx(puzzle.quantifier.sm_value, abs=5e-4)


def test_quark_only_sm_value_matches_yaml(puzzle, sm_ckm_bundle):
    """The quark-only SM reference (six quark Yukawas + three CKM sines), the footing of the
    quark-only P3 fit, is pinned against the value recorded in puzzle.yaml."""
    params = step_1.sm_quark_parameters(sm_ckm_bundle)
    assert set(params) == {"yu", "yc", "yt", "yd", "ys", "yb", "s12", "s13", "s23"}
    span = step_1.free_parameter_log10_span(params)
    assert span == pytest.approx(puzzle.quantifier.sm_reference_values["quarks_only"], abs=5e-4)
    assert max(params, key=params.get) == "yt" and min(params, key=params.get) == "yu"


def test_span_is_set_by_top_and_electron(sm_ckm_bundle):
    params = step_1.sm_free_parameters(sm_ckm_bundle)
    assert max(params, key=params.get) == "yt"
    assert min(params, key=params.get) == "ye"


def test_sector_spans_ordered(sm_ckm_bundle):
    spans = step_1.sector_spans(step_1.sm_yukawas(sm_ckm_bundle))
    assert spans["up"] > spans["lepton"] > spans["down"]


def test_sentinel_rejected(puzzle):
    broken = puzzle.model_copy(deep=True)
    broken.sm_quantities[0].value = "TODO_VERIFY"
    with pytest.raises(Stage1Error, match=re.escape(broken.sm_quantities[0].name)):
        step_1.sm_benchmark(broken)


def test_span_rejects_zero():
    with pytest.raises(ValueError):
        step_1.free_parameter_log10_span({"a": 1.0, "b": 0.0})
