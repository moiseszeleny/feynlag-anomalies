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


@pytest.fixture(scope="session")
def singlet_bundle():
    """feynlag-models' sm_singlet_z2 at its own benchmark (step 3 uses only its fields)."""
    from anomalies.higgs_95gev.solutions import step_3

    return step_3.build_singlet()


@pytest.fixture(scope="session")
def singlet_candidate(anomaly):
    """sm_singlet_z2 at the step-4 override (h2 singlet-like at 95 GeV)."""
    from anomalies.higgs_95gev.solutions import step_4

    return step_4.build_singlet_candidate(anomaly)


@pytest.fixture(scope="session")
def thdm_aligned(anomaly):
    """thdm_type2 at the tan beta = 1.5 point whose labels the model keeps, and its inversion."""
    from anomalies.higgs_95gev.solutions import step_4

    return step_4.build_thdm_candidate(anomaly, step_4.THDM_ALIGNED_POINT)
