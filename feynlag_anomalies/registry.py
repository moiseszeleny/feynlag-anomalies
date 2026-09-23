"""Discover anomaly fichas and load their ``anomaly.yaml``. Mirrors the shape of
``feynlag_models.registry`` on the sibling repo (a deliberate convention match, not a shared
package — the two are not coupled)."""

from __future__ import annotations

from . import ANOMALIES_DIR
from .loader import load as _load
from .schema import Anomaly


def anomaly_dirs() -> list:
    """Every ``anomalies/<id>/`` directory holding an ``anomaly.yaml``."""
    return sorted(
        p for p in ANOMALIES_DIR.iterdir() if p.is_dir() and (p / "anomaly.yaml").exists()
    )


def anomaly_ids() -> list[str]:
    return [p.name for p in anomaly_dirs()]


def load(anomaly_id: str, check_models: bool = True) -> Anomaly:
    return _load(ANOMALIES_DIR / anomaly_id, check_models=check_models)
