"""Checkpoint objects for ``ladder.ipynb``.

Builds ``check_1`` from a live feynlag-models ``sm`` bundle (``make_check_1``) and ``check_2``
from the loaded ``Anomaly`` (``make_check_2``), with :mod:`checkpoints.core` and
:mod:`anomalies.higgs_95gev.solutions`. ``ladder.ipynb`` imports from this module only, never
from ``solutions/`` directly. Every expected value comes from a solution function or from
``anomaly.yaml``; none is typed here.
"""

from __future__ import annotations

from checkpoints import Checkpoint, exact_match, numeric_tolerance

from anomalies.higgs_95gev.solutions import step_1, step_2

#: the mass window of the excesses (GeV), for the notebook's step-1 check
WINDOW_GEV = step_1.WINDOW_GEV

# --- step 1: how many physical scalars does the SM have? ---------------------
def make_check_1(bundle) -> Checkpoint:
    """Step 1 asks for the number of physical (massive) neutral scalars after EWSB."""
    expected = step_1.physical_neutral_scalar_count(bundle)
    return exact_match(
        "step_1",
        expected=expected,
        hints=[
            "Count real degrees of freedom: the Higgs doublet has two complex components.",
            "Three of them are eaten by W+, W- and Z. Check with the model's scalar mass matrices "
            "(bundle.model.mass_matrix on (h, G0), and on G+ with charged=True): how many "
            "eigenvalues are nonzero?",
            f"4 - 3 = {expected}: the neutral matrix is diag(2 lambda v^2, 0) and the charged one "
            "is 0.",
        ],
    )


# --- step 2: the ditau sigma x B as a signal strength -------------------------
def make_check_2(anomaly) -> Checkpoint:
    """Step 2 asks for mu_tautau = [sigma B]_obs / (sigma_ggF B_tautau)_SM-like at 95 GeV."""
    expected = step_2.mu_tautau(anomaly)["mu"]
    return numeric_tolerance(
        "step_2",
        expected=expected,
        rel_tol=1e-3,
        hints=[
            "A signal strength is a ratio to what an SM-like Higgs boson of the same mass gives "
            "in the same channel.",
            "Take the CMS ditau sigma x B from anomaly.observables and divide it by "
            "sigma_ggF x B(tau tau) from anomaly.sm_prediction.sm_reference_values.",
            f"The SM-like denominator is {step_2.sm_like_sigma_br(anomaly):.4g} pb, so "
            f"mu_tautau = {expected:.3g}.",
        ],
    )
