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


@pytest.fixture(scope="session")
def p3(puzzle):
    """The P3 computation with the default pinned seeds (fit, spans, boxed, tuning, dps=60
    recomputation), run once per session (~70 s)."""
    from puzzles.flavor_puzzle.solutions import step_3

    return step_3.run_p3(puzzle, seeds=step_3.DEFAULT_SEEDS)
