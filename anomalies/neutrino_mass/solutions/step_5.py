"""Step 5 -- rank of the light-neutrino mass matrix for n right-handed neutrinos.

A generic ``n_gen x n_nuR`` Dirac mass ``m_D`` and a diagonal ``M_R`` go through feynlag's own
seesaw formula ``m_nu = -m_D M_R^-1 m_D^T``. These are plain SymPy matrices, not a model: no
fields or Lagrangian are declared here.
"""

from __future__ import annotations

import sympy as sp


def light_mass_matrix(n_nuR: int, n_gen: int = 3) -> sp.Matrix:
    """The ``n_gen x n_gen`` seesaw light-neutrino matrix for generic ``m_D`` and diagonal ``M_R``."""
    from feynlag import seesaw_light_mass

    flavors = ("e", "mu", "tau", *(f"f{a}" for a in range(3, n_gen)))
    m_D = sp.Matrix(n_gen, n_nuR, lambda a, k: sp.Symbol(f"mD_{flavors[a]}{k + 1}"))
    M_R = sp.diag(*[sp.Symbol(f"MR{k + 1}", positive=True) for k in range(n_nuR)])
    return seesaw_light_mass(m_D, M_R)


def light_rank(n_nuR: int, n_gen: int = 3) -> int:
    """Rank of the ``n_gen x n_gen`` seesaw light-neutrino matrix with ``n_nuR`` singlets."""
    return light_mass_matrix(n_nuR, n_gen).rank(simplify=True)
