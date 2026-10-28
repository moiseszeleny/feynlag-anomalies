"""Step 3: the singlet's lowest operators, computed by feynlag on the sm_singlet_z2 fields."""

import sympy as sp

from anomalies.higgs_95gev.solutions import step_3


def test_portals_without_z2(singlet_bundle):
    # S H†H (dim 3) and S² H†H (dim 4) are the only terms coupling S to H
    assert step_3.portal_terms(singlet_bundle) == {"S (H†H)": 3, "S S (H†H)": 4}


def test_full_potential_without_z2(singlet_bundle):
    labels = {t.label: t.dim for t in step_3.potential_terms(singlet_bundle)}
    assert labels == {"(H†H)": 2, "S S": 2, "S (H†H)": 3, "(H†H) (H†H)": 4, "S S S": 3,
                      "S S (H†H)": 4, "S S S S": 4}


def test_z2_removes_the_odd_terms(singlet_bundle):
    labels = {t.label for t in step_3.potential_terms(singlet_bundle, with_z2=True)}
    assert labels == {"(H†H)", "S S", "(H†H) (H†H)", "S S (H†H)", "S S S S"}
    assert step_3.portal_terms(singlet_bundle, with_z2=True) == {"S S (H†H)": 4}


def test_no_singlet_yukawa(singlet_bundle):
    # adding S changes nothing in the fermion sector: no S psi-bar psi at dim <= 4
    assert step_3.singlet_fermion_terms(singlet_bundle) == []
    with_s = {t.label for t in step_3.yukawa_terms(singlet_bundle)}
    without = {t.label for t in step_3.yukawa_terms(singlet_bundle, with_singlet=False)}
    assert with_s == without and len(without) == 3


def test_z2_portal_gives_the_trilinear(singlet_bundle):
    term, coeff = step_3.z2_trilinear(singlet_bundle)
    H, S = step_3.fields(singlet_bundle)
    s0 = S.components[0]
    HdH = sp.expand(term / s0**2)
    assert sp.simplify(coeff - 2 * singlet_bundle.extra["vS"].s * HdH) == 0
    assert all(c in HdH.free_symbols for c in H.components)
