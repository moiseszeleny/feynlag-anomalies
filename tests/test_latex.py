"""feynlag_anomalies.latex: symbols carry their own names upstream (UG-2); this module only prints
a charged conjugate by its antiparticle's name. Render only."""

import re

import sympy as sp
from feynlag import TexSymbol

from feynlag_anomalies.latex import latex


def _weinberg():
    from feynlag import suggest_yukawa

    from anomalies.neutrino_mass.solutions.step_1 import build_sm_lepton_fields

    Ll, eR, H, groups = build_sm_lepton_fields()
    terms = suggest_yukawa([Ll, eR], [H], list(groups), max_dim=5)
    return next(t for t in terms if "Weinberg" in t.label).expr


def test_weinberg_operator_renders_physics_names():
    out = latex(_weinberg())
    assert r"\nu_L" in out and "H^0" in out and "G^+" in out
    assert r"\overline{\nu_L}" in out  # the Majorana conjugate leg nuLbar
    assert "G^-" in out and r"\overline{G^+}" not in out
    assert not re.search(r"\b(nuL|eL|Gp|H0)\b", out)


def test_rendering_does_not_modify_the_expression():
    expr = _weinberg()
    before = sp.srepr(expr)
    latex(expr)
    assert sp.srepr(expr) == before


def test_conjugate_goldstone_power_has_no_double_superscript():
    Gp = TexSymbol("Gp", "G^+")
    assert latex(sp.conjugate(Gp) ** 2) == r"\left(G^-\right)^{2}"
    assert latex(sp.conjugate(TexSymbol("Hp", "H^{+}"))) == "H^{-}"


def test_seesaw_2n_parameters():
    from feynlag_models.registry import build

    out = latex(build("seesaw_type1_2n").extra["Mnu"])
    assert r"y^\nu_{\mu1}" in out and "M_1" in out
    assert "yv" not in out and "MR" not in out


def test_step5_matrix_names():
    from anomalies.neutrino_mass.solutions.step_5 import light_mass_matrix

    out = latex(light_mass_matrix(1))
    assert r"m^D_{\mu 1}" in out and "M_{1}" in out
    assert "mD" not in out and "MR" not in out


def test_uncharged_conjugates_print_as_sympy_does():
    for s in (sp.Symbol("x"), TexSymbol("X", r"\chi"), TexSymbol("Z", "Z^0")):
        assert latex(sp.conjugate(s)) == sp.latex(sp.conjugate(s))
