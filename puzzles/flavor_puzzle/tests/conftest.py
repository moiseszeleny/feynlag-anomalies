import pytest


@pytest.fixture(scope="session")
def puzzle():
    from feynlag_anomalies.registry import load_puzzle

    return load_puzzle("flavor_puzzle")


@pytest.fixture(scope="session")
def sm_ckm_bundle(puzzle):
    """feynlag-models' sm_ckm at the sourced benchmark of puzzle.yaml (a build costs ~1 s)."""
    from feynlag_models.registry import build

    from puzzles.flavor_puzzle.solutions import step_1

    return build(step_1.MODEL_ID, benchmark=step_1.sm_benchmark(puzzle))
