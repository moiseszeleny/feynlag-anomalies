"""Shared, anomaly-independent helpers for feynlag-anomalies.

Nothing here contains the physics of any single anomaly; that lives in
``anomalies/<id>/``. Nothing here declares a feynlag Lagrangian or model; candidate
models are always consumed through ``feynlag_models.registry``.
"""

from pathlib import Path

__version__ = "0.1.0"

#: repository root (the directory holding ``pyproject.toml``)
ROOT = Path(__file__).resolve().parent.parent
ANOMALIES_DIR = ROOT / "anomalies"
