import pytest


@pytest.fixture(scope="session")
def seesaw_bundle():
    """Build feynlag-models' seesaw_type1 once per test session (a model build costs 10-60s,
    per feynlag-models/CLAUDE.md -- this mirrors that repo's own session-scoped fixture pattern).
    """
    from feynlag_models.registry import build

    return build("seesaw_type1")


@pytest.fixture(scope="session")
def seesaw_2n_bundle():
    """feynlag-models' seesaw_type1_2n (three generations, two nu_R): the step-6 fit model."""
    from feynlag_models.registry import build

    return build("seesaw_type1_2n")


@pytest.fixture(scope="session")
def step6_fit(seesaw_2n_bundle):
    """The step-6 fit against the sourced observables, run once per session (~5 s)."""
    from anomalies.neutrino_mass.solutions import step_6
    from feynlag_anomalies.registry import load

    observed = step_6.observed_from_anomaly(load("neutrino_mass"))
    return step_6.run_fit(seesaw_2n_bundle, observed), observed
