r"""Physics-style LaTeX for feynlag / feynlag-models expressions (render only).

Every field component, parameter and physical boson carries its own LaTeX name upstream (feynlag's
``TexSymbol``; ``docs/upstream_gaps.md``, UG-2), so plain ``sympy.latex`` already prints ``\nu_L``,
``G^+``, ``{\lambda}``. What this module adds is one rule with no upstream equivalent: the conjugate
of a positively charged symbol prints as its antiparticle (``G^-``, not ``\overline{G^+}``), read
from the symbol's own tex. Expressions are never modified.
"""

from __future__ import annotations

import re

from feynlag import TexSymbol
from sympy.printing.latex import LatexPrinter

#: a trailing positive-charge superscript, ``^+`` or ``^{+}``
_PLUS = re.compile(r"\^(\{\+\}|\+)$")


def antiparticle_tex(tex: str) -> str | None:
    """``G^-`` for ``G^+`` (or ``G^{-}`` for ``G^{+}``); ``None`` if ``tex`` has no ``+`` charge."""
    m = _PLUS.search(tex)
    if m is None:
        return None
    return tex[:m.start()] + ("^{-}" if m[1] == "{+}" else "^-")


class _Printer(LatexPrinter):
    def _print_conjugate(self, expr, exp=None):
        arg = expr.args[0]
        tex = antiparticle_tex(self._print(arg)) if isinstance(arg, TexSymbol) else None
        if tex is None:
            return super()._print_conjugate(expr, exp)
        return tex if exp is None else rf"\left({tex}\right)^{{{exp}}}"


def latex(expr, **settings) -> str:
    """``sympy.latex(expr)``, with a charged conjugate printed by its antiparticle's name."""
    return _Printer(settings).doprint(expr)
