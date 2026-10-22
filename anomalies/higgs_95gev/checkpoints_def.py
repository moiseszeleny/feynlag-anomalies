"""Checkpoint objects for ``ladder.ipynb``.

Builds ``check_1`` from a live feynlag-models ``sm`` bundle (``make_check_1``), ``check_2``
from the loaded ``Anomaly`` (``make_check_2``), ``check_3`` from the ``sm_singlet_z2`` fields
(``make_check_3``) and ``check_4`` from the singlet candidate at its override (``make_check_4``), with :mod:`checkpoints.core` and
:mod:`anomalies.higgs_95gev.solutions`. ``ladder.ipynb`` imports from this module only, never
from ``solutions/`` directly. Every expected value comes from a solution function or from
``anomaly.yaml``; none is typed here.
"""

from __future__ import annotations

from checkpoints import Checkpoint, exact_match, numeric_tolerance

from anomalies.higgs_95gev.solutions import step_1, step_2, step_3, step_4

#: the mass window of the excesses (GeV), for the notebook's step-1 check
WINDOW_GEV = step_1.WINDOW_GEV
#: the mass of the excess the step-4 candidates reproduce (GeV) and the singlet mixing used there
TARGET_MASS_GEV = step_4.TARGET_MASS_GEV
SIN_THETA = step_4.SIN_THETA

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


# --- step 3: how many operators couple a gauge singlet to the SM? ------------
def make_check_3(bundle) -> Checkpoint:
    """Step 3 asks for the number of terms coupling S to H up to dimension 4, without the Z2."""
    expected = len(step_3.portal_terms(bundle))
    return exact_match(
        "step_3",
        expected=expected,
        hints=[
            "S carries no gauge charge, so any gauge-invariant SM combination can multiply it. "
            "Which is the lowest-dimension one?",
            "H†H has dimension 2. Multiply it by S, then by S S, and keep the dimension <= 4. "
            "Can S pair with two SM fermions instead?",
            f"{expected}: S H†H (dim 3) and S S H†H (dim 4). No SM fermion pair is a gauge singlet, "
            "so suggest_yukawa gives no S psi-bar psi term.",
        ],
    )


# --- step 4: the singlet candidate at 95 GeV ----------------------------------
def make_check_4(bundle) -> Checkpoint:
    """Step 4 asks for the mass of the singlet-like state in the override's spectrum."""
    expected = step_4.singlet_spectrum(bundle)["MH2"]
    return numeric_tolerance(
        "step_4",
        expected=expected,
        rel_tol=1e-6,
        hints=[
            "The model labels its CP-even states by mixing, not by mass: h1 = cos(theta) h + "
            "sin(theta) s is always the h-like one.",
            "With the singlet lighter than the Higgs boson, which of MH1, MH2 is singlet-like? "
            "Read it from the bundle: bundle.values()[bundle.extra['MH2'].s].",
            f"MH2 = {expected:.4g} GeV, the singlet-like h2.",
        ],
    )
