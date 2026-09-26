r"""Physics-style LaTeX for feynlag / feynlag-models symbols (render only).

feynlag names doublet components after ``component_names`` (``nuL``, ``Gp``, ...) and offers no
per-component LaTeX hook (see ``docs/upstream_gaps.md``, UG-2), so SymPy prints those raw names.
:func:`latex` maps them to physics notation through SymPy's own ``symbol_names`` printer setting,
and prints the conjugate of a symbol listed in ``CONJ_TEX`` by its own name (``G^-``, not
``\overline{G^+}``).
Expressions are never modified; a name with no rule falls back to SymPy's default rendering.
Extend ``TEX_NAMES`` / ``_PATTERNS`` when a new model brings new names.
"""

from __future__ import annotations

import re

import sympy as sp
from sympy.printing.latex import LatexPrinter

TEX_NAMES = {
    "nuL": r"\nu_L",
    "eL": "e_L",
    "eR": "e_R",
    "nuR": r"\nu_R",
    "Gp": "G^+",
    "H0": "H^0",
    "yv": r"y_\nu",
    "MR": "M_R",
}

#: conjugates with a name of their own, printed instead of ``\overline{...}``
CONJ_TEX = {"Gp": "G^-"}

_FLAVORS = {"e": "e", "mu": r"\mu", "tau": r"\tau"}
_PATTERNS = [
    # seesaw_type1_2n: Dirac Yukawa of lepton flavour a with nu_R number k, and M_R eigenvalues
    (re.compile(r"^yv_(e|mu|tau)(\d+)$"), lambda m: rf"y^\nu_{{{_FLAVORS[m[1]]} {m[2]}}}"),
    (re.compile(r"^MR(\d+)$"), lambda m: rf"M_{{{m[1]}}}"),
]


def tex_name(name: str) -> str | None:
    """LaTeX for a feynlag symbol name, or ``None`` if no rule covers it."""
    if name in TEX_NAMES:
        return TEX_NAMES[name]
    for pattern, render in _PATTERNS:
        if m := pattern.match(name):
            return render(m)
    if name.endswith("bar") and len(name) > 3 and (base := tex_name(name[:-3])):
        return rf"\bar{{{base}}}"
    return None


class _Printer(LatexPrinter):
    def _print_conjugate(self, expr, exp=None):
        arg = expr.args[0]
        if isinstance(arg, sp.Symbol) and arg.name in CONJ_TEX:
            tex = CONJ_TEX[arg.name]
            return tex if exp is None else rf"\left({tex}\right)^{{{exp}}}"
        return super()._print_conjugate(expr, exp)


def latex(expr, **settings) -> str:
    """``sympy.latex(expr)`` with feynlag names rendered in physics notation."""
    names = {s: t for s in sp.sympify(expr).free_symbols
             if isinstance(s, sp.Symbol) and (t := tex_name(s.name))}
    return _Printer({"symbol_names": names, **settings}).doprint(expr)
