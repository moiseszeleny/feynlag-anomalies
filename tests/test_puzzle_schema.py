"""Validates every puzzles/<id>/puzzle.yaml, plus one negative test per validator rule --
mirroring tests/test_schema.py for anomalies."""

import pytest
import yaml

from feynlag_anomalies.loader import PuzzleValidationError, load_puzzle
from feynlag_anomalies.registry import puzzle_dirs, puzzle_ids
from feynlag_anomalies.schema import Puzzle

# A real callable to point quantifier.implementation at in the positive P1 test.
_RESOLVABLE = "feynlag_anomalies.latex:latex"


def _write(tmp_path, name, data):
    d = tmp_path / name
    d.mkdir(exist_ok=True)
    (d / "puzzle.yaml").write_text(yaml.safe_dump(data))
    return d


@pytest.mark.parametrize("puzzle_dir", puzzle_dirs(), ids=lambda p: p.name)
def test_every_puzzle_validates(puzzle_dir):
    puzzle = load_puzzle(puzzle_dir)
    assert puzzle.id == puzzle_dir.name


def test_expected_pilot_puzzle_present():
    assert "flavor_puzzle" in puzzle_ids()


def test_id_must_match_directory_name(tmp_path, valid_puzzle_dict):
    valid_puzzle_dict["id"] = "not_the_dirname"
    d = _write(tmp_path, "flavor_puzzle", valid_puzzle_dict)
    with pytest.raises(PuzzleValidationError):
        load_puzzle(d)


@pytest.mark.parametrize(
    "field, bad",
    [("status", "established"), ("maturity", "A0"), ("mechanism_classes", ["magic"])],
)
def test_closed_vocabularies(valid_puzzle_dict, field, bad):
    valid_puzzle_dict[field] = bad
    with pytest.raises(Exception):
        Puzzle.model_validate(valid_puzzle_dict)


def test_anomaly_only_field_rejected(valid_puzzle_dict):
    valid_puzzle_dict["sm_failure_type"] = "structural"
    with pytest.raises(Exception):
        Puzzle.model_validate(valid_puzzle_dict)


def test_unknown_related_anomaly_rejected(tmp_path, valid_puzzle_dict):
    valid_puzzle_dict["related_anomalies"] = ["does_not_exist_anywhere"]
    d = _write(tmp_path, "flavor_puzzle", valid_puzzle_dict)
    with pytest.raises(PuzzleValidationError, match="related_anomalies"):
        load_puzzle(d)


def test_sm_quantity_source_must_be_listed(tmp_path, valid_puzzle_dict):
    valid_puzzle_dict["sm_quantities"][0]["source"] = "arXiv:0000.00000"
    d = _write(tmp_path, "flavor_puzzle", valid_puzzle_dict)
    with pytest.raises(PuzzleValidationError, match="not in sources"):
        load_puzzle(d)


def test_p1_requires_quantifier(tmp_path, valid_puzzle_dict):
    valid_puzzle_dict["maturity"] = "P1"
    valid_puzzle_dict["quantifier"] = None
    d = _write(tmp_path, "flavor_puzzle", valid_puzzle_dict)
    with pytest.raises(PuzzleValidationError, match="requires a quantifier"):
        load_puzzle(d)


def test_p1_rejects_cited_quantifier(tmp_path, valid_puzzle_dict):
    valid_puzzle_dict["maturity"] = "P1"
    valid_puzzle_dict["quantifier"].update(provenance="cited", implementation=_RESOLVABLE)
    d = _write(tmp_path, "flavor_puzzle", valid_puzzle_dict)
    with pytest.raises(PuzzleValidationError, match="computed quantifier"):
        load_puzzle(d)


@pytest.mark.parametrize("impl", [None, "feynlag_anomalies.latex:no_such_function", "no_such_module:f"])
def test_p1_rejects_unresolvable_implementation(tmp_path, valid_puzzle_dict, impl):
    valid_puzzle_dict["maturity"] = "P1"
    valid_puzzle_dict["quantifier"]["implementation"] = impl
    d = _write(tmp_path, "flavor_puzzle", valid_puzzle_dict)
    with pytest.raises(PuzzleValidationError, match="implementation"):
        load_puzzle(d)


def test_p1_accepts_resolvable_computed_quantifier(tmp_path, valid_puzzle_dict):
    valid_puzzle_dict["maturity"] = "P1"
    valid_puzzle_dict["quantifier"]["implementation"] = _RESOLVABLE
    d = _write(tmp_path, "flavor_puzzle", valid_puzzle_dict)
    assert load_puzzle(d).maturity == "P1"


def test_unknown_model_id_rejected(tmp_path, valid_puzzle_dict):
    valid_puzzle_dict["candidate_models"] = [{"model_id": "does_not_exist_anywhere"}]
    d = _write(tmp_path, "flavor_puzzle", valid_puzzle_dict)
    with pytest.raises(PuzzleValidationError):
        load_puzzle(d)


def test_low_maturity_model_rejected_for_fit_level_puzzle(tmp_path, valid_puzzle_dict, monkeypatch):
    import feynlag_models.registry as fm_registry

    monkeypatch.setattr(fm_registry, "metadata", lambda model_id: {"maturity_level": 0})
    valid_puzzle_dict["maturity"] = "P3"
    valid_puzzle_dict["quantifier"]["implementation"] = _RESOLVABLE
    valid_puzzle_dict["candidate_models"] = [{"model_id": "sm_ckm"}]
    d = _write(tmp_path, "flavor_puzzle", valid_puzzle_dict)
    with pytest.raises(PuzzleValidationError, match="implies a fit/scan"):
        load_puzzle(d)
