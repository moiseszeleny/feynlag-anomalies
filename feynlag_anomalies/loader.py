"""Load and cross-validate ``anomaly.yaml`` and ``puzzle.yaml`` files.

``feynlag_anomalies.schema.Anomaly`` validates shape and closed vocabularies. This module adds
the checks that need to look outside a single YAML file: the ``id`` must match its directory
name, referenced ``model_id``s must exist in the feynlag-models registry, and a fit/scan-level
maturity (A3+) must be backed by a sufficiently mature model (feynlag-models maturity >= L2, per
CLAUDE.md hard rule 7).

Puzzles get the same id and model checks (P3+ is the fit level), plus: ``related_anomalies``
must name existing anomaly records, ``sm_quantities[].source`` must name a ``sources[]`` entry, and
from P1 on the ``quantifier`` must be ``computed`` with an ``implementation`` that resolves to a
callable.
"""

from __future__ import annotations

import importlib
import re
from pathlib import Path

import yaml

from . import ANOMALIES_DIR
from .schema import ID_PATTERN, Anomaly, CandidateModel, Puzzle

_MATURITY_ORDER = {"A0": 0, "A1": 1, "A2": 2, "A3": 3, "A4": 4}
_FIT_LEVEL_MATURITY = "A3"
_PUZZLE_MATURITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "P4": 4}
_PUZZLE_QUANTIFIED_MATURITY = "P1"
_PUZZLE_FIT_LEVEL_MATURITY = "P3"
_MIN_MODEL_LEVEL = 2


class AnomalyValidationError(ValueError):
    """Raised when an anomaly.yaml fails a cross-file check."""


class PuzzleValidationError(ValueError):
    """Raised when a puzzle.yaml fails a cross-file check."""


def load(anomaly_dir: Path, check_models: bool = True) -> Anomaly:
    """Parse and validate ``anomaly_dir/anomaly.yaml``.

    Args:
        anomaly_dir: the ``anomalies/<id>/`` directory.
        check_models: if True (default), cross-check ``candidate_models[].model_id`` against the
            feynlag-models registry. Set False only for tests that intentionally construct an
            anomaly with a fictitious model_id.
    """
    anomaly_dir = Path(anomaly_dir)
    yaml_path = anomaly_dir / "anomaly.yaml"
    if not yaml_path.exists():
        raise AnomalyValidationError(f"{yaml_path} does not exist")

    raw = yaml.safe_load(yaml_path.read_text())
    anomaly = Anomaly.model_validate(raw)

    errors: list[str] = []

    if not re.match(ID_PATTERN, anomaly.id):
        errors.append(f"id {anomaly.id!r} does not match {ID_PATTERN}")
    if anomaly.id != anomaly_dir.name:
        errors.append(f"id {anomaly.id!r} does not match directory name {anomaly_dir.name!r}")

    known_sources = {s.identifier for s in anomaly.sources}
    for c in anomaly.constraints:
        if c.source not in known_sources:
            errors.append(f"constraint {c.name!r} cites source {c.source!r}, not in sources[]")

    if check_models:
        is_fit_level = _MATURITY_ORDER[anomaly.maturity] >= _MATURITY_ORDER[_FIT_LEVEL_MATURITY]
        errors.extend(
            _check_candidate_models(anomaly.candidate_models, anomaly.maturity, is_fit_level)
        )

    if errors:
        raise AnomalyValidationError(f"{yaml_path}: " + "; ".join(errors))
    return anomaly


def load_puzzle(puzzle_dir: Path, check_models: bool = True) -> Puzzle:
    """Parse and validate ``puzzle_dir/puzzle.yaml``.

    Args:
        puzzle_dir: the ``puzzles/<id>/`` directory.
        check_models: as in :func:`load`.
    """
    puzzle_dir = Path(puzzle_dir)
    yaml_path = puzzle_dir / "puzzle.yaml"
    if not yaml_path.exists():
        raise PuzzleValidationError(f"{yaml_path} does not exist")

    raw = yaml.safe_load(yaml_path.read_text())
    puzzle = Puzzle.model_validate(raw)

    errors: list[str] = []

    if puzzle.id != puzzle_dir.name:
        errors.append(f"id {puzzle.id!r} does not match directory name {puzzle_dir.name!r}")

    for anomaly_id in puzzle.related_anomalies:
        if not (ANOMALIES_DIR / anomaly_id / "anomaly.yaml").exists():
            errors.append(f"related_anomalies references unknown anomaly {anomaly_id!r}")

    known_sources = {s.identifier for s in puzzle.sources}
    for q in puzzle.sm_quantities:
        if q.source is not None and q.source not in known_sources:
            errors.append(f"sm_quantities {q.name!r} cites {q.source!r}, not in sources[]")

    order = _PUZZLE_MATURITY_ORDER
    if order[puzzle.maturity] >= order[_PUZZLE_QUANTIFIED_MATURITY]:
        errors.extend(_check_quantifier(puzzle))

    if check_models:
        is_fit_level = order[puzzle.maturity] >= order[_PUZZLE_FIT_LEVEL_MATURITY]
        errors.extend(
            _check_candidate_models(puzzle.candidate_models, puzzle.maturity, is_fit_level)
        )

    if errors:
        raise PuzzleValidationError(f"{yaml_path}: " + "; ".join(errors))
    return puzzle


def _check_quantifier(puzzle: Puzzle) -> list[str]:
    q = puzzle.quantifier
    if q is None:
        return [f"maturity {puzzle.maturity!r} requires a quantifier"]
    errors: list[str] = []
    if q.provenance != "computed":
        errors.append(
            f"maturity {puzzle.maturity!r} requires a computed quantifier, got {q.provenance!r}"
        )
    if not q.implementation:
        errors.append(f"maturity {puzzle.maturity!r} requires quantifier.implementation")
        return errors
    module_name, _, func_name = q.implementation.partition(":")
    try:
        func = getattr(importlib.import_module(module_name), func_name)
    except (ImportError, AttributeError, ValueError) as exc:
        return errors + [f"quantifier.implementation {q.implementation!r} does not resolve ({exc})"]
    if not callable(func):
        errors.append(f"quantifier.implementation {q.implementation!r} is not callable")
    return errors


def _check_candidate_models(
    candidate_models: list[CandidateModel], maturity: str, is_fit_level: bool
) -> list[str]:
    errors: list[str] = []
    model_ids = [cm.model_id for cm in candidate_models if cm.model_id]
    if not model_ids:
        return errors

    from feynlag_models.registry import metadata as fm_metadata
    from feynlag_models.registry import model_ids as fm_model_ids

    known_ids = set(fm_model_ids())

    for model_id in model_ids:
        if model_id not in known_ids:
            errors.append(f"candidate_models references unknown model_id {model_id!r}")
            continue
        if is_fit_level:
            level = fm_metadata(model_id)["maturity_level"]
            if level < _MIN_MODEL_LEVEL:
                errors.append(
                    f"maturity {maturity!r} implies a fit/scan, but candidate "
                    f"model {model_id!r} is only feynlag-models maturity L{level} (< L{_MIN_MODEL_LEVEL})"
                )
    return errors
