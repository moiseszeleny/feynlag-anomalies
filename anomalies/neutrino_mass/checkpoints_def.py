"""Checkpoint objects for ``ladder.ipynb``.

Builds ``check_0`` .. ``check_5`` from :mod:`checkpoints.core` plus
:mod:`anomalies.neutrino_mass.solutions` and, for step 4, a live ``feynlag-models``
``seesaw_type1`` bundle. ``ladder.ipynb`` imports from this module only -- never from
``solutions/`` directly -- keeping exercises and worked solutions separated (kickoff spec §4).

Step 6's checkpoint is built from the loaded ``Anomaly`` (``make_check_6``), so the measured
values it compares against come from ``anomaly.yaml`` and are never re-typed here.
"""

from __future__ import annotations

from checkpoints import Checkpoint, exact_match, numeric_tolerance

from anomalies.neutrino_mass.solutions import step_0, step_1, step_2

# --- step 0: dimensional estimate -------------------------------------------
# Illustrative parameters for the exercise (not measured anomaly data, so not subject to the
# TODO_VERIFY sourcing rule): an O(1) Yukawa, the electroweak scale (as in feynlag's own test
# fixtures, e.g. tests/test_majorana.py), and a GUT-ish heavy scale.
_P0_Y, _P0_V, _P0_M = 1.0, 246.0, 1e14
_p0_expected = step_0.m_nu_estimate(_P0_Y, _P0_V, _P0_M)

check_0 = numeric_tolerance(
    "step_0",
    expected=_p0_expected,
    rel_tol=0.2,
    hints=[
        "m_nu should come from a Yukawa coupling y, the electroweak scale v, and a heavy mass M.",
        "Try m_nu ~ y^2 v^2 / M (see solutions/step_0.py's docstring for the shape).",
        f"With y={_P0_Y}, v={_P0_V} GeV, M={_P0_M:.0e} GeV, m_nu should come out around "
        f"{_p0_expected:.3g} GeV.",
    ],
)

# --- step 1: SM structural test ("does a dim<=4 term exist?") --------------
_p1_expected = step_1.count_dim4_yukawa_terms()

check_1 = exact_match(
    "step_1",
    expected=_p1_expected,
    hints=[
        "Call feynlag.suggest.suggest_yukawa on the minimal SM lepton content (Ll, eR, H, no "
        "nu_R) at max_dim=4, and count the terms it returns.",
        "The only dimension<=4 invariant you should find is the charged-lepton Yukawa.",
        f"suggest_yukawa returns exactly {_p1_expected} term(s) at max_dim=4 for this field "
        "content -- so no dim<=4 neutrino-mass term exists.",
    ],
)

# --- step 2: lowest-dimension EFT operator ----------------------------------
_p2_expected = step_2.weinberg_operator_present()

check_2 = exact_match(
    "step_2",
    expected=_p2_expected,
    hints=[
        "Repeat the step-1 call but raise max_dim to 5.",
        "Look at the .label of each returned SuggestedTerm.",
        "One new term appears, labeled with 'Weinberg' in it -- that's the dimension-5 operator.",
    ],
)

# --- step 3: minimal tree-level UV completion -------------------------------
check_3 = exact_match(
    "step_3",
    expected="seesaw_type1",
    hints=[
        "Which feynlag-models model_id extends the SM with exactly one gauge-singlet fermion?",
        "It's the minimal tree-level completion of the Weinberg operator: type-I seesaw (fewest "
        "fields, smallest representation, fewest parameters).",
        "The model_id is 'seesaw_type1' (see feynlag_models.registry.model_ids()).",
    ],
)


def make_check_4(bundle) -> Checkpoint:
    """Build step 4's checkpoint from a live ``seesaw_type1`` ``ModelBundle``.

    Asks how many Majorana mass eigenstates the (single-generation) bundle produces -- the part
    directly instantiated by this model. The general 3-flavour rank-counting argument (why 2
    heavy states are needed once 2 Delta m^2 are measured) is left as the reader's own derivation
    feeding into step 5 -- see ``decisions.md``.
    """
    expected = len(bundle.extra["masses"])
    return exact_match(
        "step_4",
        expected=expected,
        hints=[
            "Look at bundle.extra['masses'] (or ['U'], ['D']) -- how many entries does it have?",
            "A single Weyl nu_R pairs with the one active nu_L component from a 2x2 Takagi "
            "diagonalization.",
            f"There are {expected} Majorana mass eigenstates (light + heavy) in this bundle.",
        ],
    )


# --- step 5: minimal extension needed for a real fit ------------------------
check_5 = exact_match(
    "step_5",
    expected=True,
    hints=[
        "Two independently measured Delta m^2 require rank >= 2 in the light-neutrino mass "
        "matrix -- how many nu_R does that need?",
        "One nu_R gives rank 1 (a single light mass) -- not enough for two Delta m^2.",
        "At least two nu_R are needed; that's exactly what model_requests/seesaw_type1_nN.md "
        "requests. Answer True once you've read it.",
    ],
)


# --- step 6: stage-1 chi2 against the measured oscillation parameters -------
def make_check_6(anomaly) -> Checkpoint:
    """Step 6 asks for the fitted ratio Delta m^2_31 / Delta m^2_21.

    A rank-1 light sector (one nu_R) cannot produce two independent splittings, so this ratio is
    what the two-nu_R model has to get right; the expected value is the measured one, read from
    the loaded ``Anomaly`` (NuFIT 6.0, see ``anomaly.yaml`` ``sources``).
    """
    from anomalies.neutrino_mass.solutions.step_6 import FIT_OBSERVABLES

    by_name = {o.name: o.value for o in anomaly.observables}
    expected = by_name[FIT_OBSERVABLES[1]] / by_name[FIT_OBSERVABLES[0]]
    return numeric_tolerance(
        "step_6",
        expected=expected,
        rel_tol=1e-3,
        hints=[
            "Build seesaw_type1_2n with feynlag_models.registry.build and fit its six Yukawas "
            "to the five observables with solutions/step_6.run_fit.",
            "Take the ratio of the fitted predictions fit['predicted'] for Delta m^2_31 and "
            "Delta m^2_21.",
            f"The measured ratio is {expected:.4g}; a converged fit reproduces it (all pulls ~0).",
        ],
    )
