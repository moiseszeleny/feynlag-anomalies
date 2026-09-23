"""Unit tests for checkpoints.core.Checkpoint, independent of any specific anomaly."""

import pytest

from checkpoints import exact_match, numeric_tolerance


def test_numeric_tolerance_passes_within_tolerance():
    cp = numeric_tolerance("cp", expected=10.0, rel_tol=0.1)
    assert cp(10.5) is True


def test_numeric_tolerance_fails_outside_tolerance():
    cp = numeric_tolerance("cp", expected=10.0, rel_tol=0.1)
    assert cp(20.0) is False


def test_numeric_tolerance_rejects_non_numeric_answer():
    cp = numeric_tolerance("cp", expected=10.0)
    assert cp("not a number") is False


def test_exact_match_passes_and_fails():
    cp = exact_match("cp", expected="seesaw_type1")
    assert cp("seesaw_type1") is True
    assert cp("something_else") is False


def test_hint_staging_advances_one_level_at_a_time():
    cp = exact_match("cp", expected=1, hints=["hint one", "hint two", "hint three"])
    assert cp.hint() == "hint one"
    assert cp.hint() == "hint two"
    assert cp.hint() == "hint three"
    assert cp.hint() == "hint three"  # stays at the last hint rather than raising


def test_hint_level_jump():
    cp = exact_match("cp", expected=1, hints=["hint one", "hint two", "hint three"])
    assert cp.hint(level=3) == "hint three"
    with pytest.raises(ValueError):
        cp.hint(level=4)


def test_hint_without_any_hints_raises():
    cp = exact_match("cp", expected=1)
    with pytest.raises(ValueError):
        cp.hint()
