import copy

import pytest
import yaml

from feynlag_anomalies import ANOMALIES_DIR


@pytest.fixture
def valid_anomaly_dict():
    """A deep copy of neutrino_mass's anomaly.yaml (valid dict form), safe to tamper with."""
    raw = yaml.safe_load((ANOMALIES_DIR / "neutrino_mass" / "anomaly.yaml").read_text())
    return copy.deepcopy(raw)
