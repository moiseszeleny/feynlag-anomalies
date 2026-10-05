"""Checkpoint objects for ``ladder.ipynb``.

Every checkpoint is built from an ``sm_ckm`` bundle at the sourced benchmark
(``solutions.step_1.sm_benchmark(puzzle)``) plus :mod:`puzzles.flavor_puzzle.solutions`, so the
expected values come from ``puzzle.yaml`` and the model, never from literals typed here.
``ladder.ipynb`` imports from this module only -- never from ``solutions/`` directly.
"""

from __future__ import annotations

from checkpoints import Checkpoint, numeric_tolerance

from puzzles.flavor_puzzle.solutions import step_1, step_2


# --- step 1: the top Yukawa from the model's own relation -------------------
def make_check_1(bundle) -> Checkpoint:
    """Step 1 asks for y_t at mu = M_Z."""
    expected = step_1.sm_yukawas(bundle)["yt"]
    return numeric_tolerance(
        "step_1",
        expected=expected,
        rel_tol=1e-3,
        hints=[
            "The bundle's Yukawas are internal parameters: bundle.pieces.yukawa_params['yt'].",
            "Its expr is sqrt(2) MT / v; evaluate it with bundle.params.numeric().",
            f"With m_t(M_Z) and v_F from puzzle.yaml, y_t comes out at {expected:.4f}.",
        ],
    )


# --- step 2: the quantifier ------------------------------------------------
def make_check_2(bundle) -> Checkpoint:
    """Step 2 asks for the SM value of free_parameter_log10_span."""
    expected = step_1.free_parameter_log10_span(step_1.sm_free_parameters(bundle))
    return numeric_tolerance(
        "step_2",
        expected=expected,
        rel_tol=1e-3,
        hints=[
            "Collect the nine Yukawas and the three CKM sines in one dict.",
            "The span is log10(max / min). Which two parameters set it?",
            f"The largest is y_t and the smallest is y_e, so the span is {expected:.3f} "
            "orders of magnitude.",
        ],
    )


# --- step 3: the CKM hierarchy in powers of lambda -------------------------
def make_check_3(bundle) -> Checkpoint:
    """Step 3 asks for the Wolfenstein A = |V_cb| / (lambda |V_us|)."""
    expected = step_2.wolfenstein(step_2.ckm_numeric(bundle))["A"]
    return numeric_tolerance(
        "step_3",
        expected=expected,
        rel_tol=1e-3,
        hints=[
            "lambda is |V_us| / sqrt(|V_ud|^2 + |V_us|^2), essentially s12.",
            "A lambda^2 = s23, so A is s23 / s12^2 up to tiny corrections.",
            f"A = {expected:.3f}: an O(1) number once the power lambda^2 is pulled out.",
        ],
    )
