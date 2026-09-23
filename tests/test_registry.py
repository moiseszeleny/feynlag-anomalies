from feynlag_anomalies.registry import anomaly_dirs, anomaly_ids


def test_anomaly_ids_match_directory_names():
    for d in anomaly_dirs():
        assert d.name in anomaly_ids()


def test_expected_pilot_anomalies_present():
    ids = set(anomaly_ids())
    assert {"neutrino_mass", "higgs_95gev", "emu_146gev"} <= ids
