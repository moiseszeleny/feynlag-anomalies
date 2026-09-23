"""Load and cross-validate ``anomaly.yaml`` files.

``feynlag_anomalies.schema.Anomaly`` validates shape and closed vocabularies. This module adds
the checks that need to look outside a single YAML file: the ``id`` must match its directory
name, referenced ``model_id``s must exist in the feynlag-models registry, and a fit/scan-level
maturity (A3+) must be backed by a sufficiently mature model (feynlag-models maturity >= L2, per
CLAUDE.md hard rule 7).
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from .schema import ID_PATTERN, Anomaly

_MATURITY_ORDER = {"A0": 0, "A1": 1, "A2": 2, "A3": 3, "A4": 4}
_FIT_LEVEL_MATURITY = "A3"
_MIN_MODEL_LEVEL = 2


class AnomalyValidationError(ValueError):
    """Raised when an anomaly.yaml fails a cross-file check."""


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

    if check_models:
        errors.extend(_check_candidate_models(anomaly))

    if errors:
        raise AnomalyValidationError(f"{yaml_path}: " + "; ".join(errors))
    return anomaly


def _check_candidate_models(anomaly: Anomaly) -> list[str]:
    errors: list[str] = []
    model_ids = [cm.model_id for cm in anomaly.candidate_models if cm.model_id]
    if not model_ids:
        return errors

    from feynlag_models.registry import metadata as fm_metadata
    from feynlag_models.registry import model_ids as fm_model_ids

    known_ids = set(fm_model_ids())
    is_fit_level = _MATURITY_ORDER[anomaly.maturity] >= _MATURITY_ORDER[_FIT_LEVEL_MATURITY]

    for model_id in model_ids:
        if model_id not in known_ids:
            errors.append(f"candidate_models references unknown model_id {model_id!r}")
            continue
        if is_fit_level:
            level = fm_metadata(model_id)["maturity_level"]
            if level < _MIN_MODEL_LEVEL:
                errors.append(
                    f"anomaly maturity {anomaly.maturity!r} implies a fit/scan, but candidate "
                    f"model {model_id!r} is only feynlag-models maturity L{level} (< L{_MIN_MODEL_LEVEL})"
                )
    return errors
