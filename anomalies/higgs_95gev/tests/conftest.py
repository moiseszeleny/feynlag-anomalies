import pytest


@pytest.fixture(scope="session")
def sm_bundle():
    """feynlag-models' sm, built once per test session through the registry."""
    from anomalies.higgs_95gev.solutions import step_1

    return step_1.build_sm()


@pytest.fixture(scope="session")
def anomaly():
    from feynlag_anomalies.registry import load

    return load("higgs_95gev")
