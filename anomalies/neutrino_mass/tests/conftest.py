import pytest


@pytest.fixture(scope="session")
def seesaw_bundle():
    """Build feynlag-models' seesaw_type1 once per test session (a model build costs 10-60s,
    per feynlag-models/CLAUDE.md -- this mirrors that repo's own session-scoped fixture pattern).
    """
    from feynlag_models.registry import build

    return build("seesaw_type1")
