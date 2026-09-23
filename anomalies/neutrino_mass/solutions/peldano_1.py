"""Peldano 1 -- SM structural test: no dim<=4 neutrino-mass term.

Reproduces, for this repo's own purposes, the minimal-SM-lepton field construction from feynlag's
own test suite (``tests/test_suggest.py::test_sm_lepton_yukawa`` /
``tests/test_majorana.py::_sm_leptons``): a lepton doublet ``Ll``, a charged-lepton singlet
``eR``, and the Higgs doublet ``H`` -- with **no** right-handed neutrino.
"""

from __future__ import annotations

import sympy as sp

from feynlag import SU2, U1, ExternalParameter, Scalar, WeylFermion


def build_sm_lepton_fields(nflavors: int = 1):
    """Return ``(Ll, eR, H, (SU2L, U1Y))``.

    The gauge coupling values (``gw``, ``g1``) are internal bookkeeping for feynlag's
    gauge-variation machinery, not a physical prediction -- they cancel out of the structural
    "does an invariant term exist" question this peldano asks, so they do not need a
    ``TODO_VERIFY`` sentinel.
    """
    gw = ExternalParameter("gw", 0.6535, positive=True)
    g1 = ExternalParameter("g1", 0.3580, positive=True)
    SU2L = SU2("SU2L", coupling=gw)
    U1Y = U1("U1Y", coupling=g1)
    Ll = WeylFermion(
        "Ll",
        reps={SU2L: 2, U1Y: -sp.Rational(1, 2)},
        chirality="L",
        nflavors=nflavors,
        component_names=["nuL", "eL"],
    )
    eR = WeylFermion(
        "eR", reps={U1Y: -1}, chirality="R", nflavors=nflavors, component_names=["eR"]
    )
    H = Scalar("H", reps={SU2L: 2, U1Y: sp.Rational(1, 2)}, component_names=["Gp", "H0"])
    return Ll, eR, H, (SU2L, U1Y)


def count_dim4_yukawa_terms() -> int:
    """How many gauge-invariant Yukawa/mass terms exist at dimension <=4 for SM leptons alone."""
    from feynlag import suggest_yukawa

    Ll, eR, H, groups = build_sm_lepton_fields()
    terms = suggest_yukawa([Ll, eR], [H], list(groups), max_dim=4)
    return len(terms)
