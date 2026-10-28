"""Step 3 -- lowest-dimension operators: a gauge singlet talks to the SM only through H†H.

The fields are taken from feynlag-models' ``sm_singlet_z2`` bundle (``registry.build``, L3): the
SM doublet ``H`` (``bundle.extra["ew"].H``) and the real singlet ``S`` (``bundle.extra["S"]``).
Nothing here declares a field or a Lagrangian. feynlag's ``suggest_potential`` enumerates the
gauge-invariant scalar terms up to dimension 4 and ``suggest_yukawa`` the fermion bilinears; the
operator list below is what feynlag computes, not a list typed by hand.

- Without a symmetry on S, the terms that couple S to the SM are the Higgs portals
  ``S H†H`` (dim 3) and ``S² H†H`` (dim 4); ``suggest_yukawa`` gives no ``S ψ̄ψ`` term, because no
  pair of SM fermions forms a gauge singlet.
- With the model's Z2 (``S → −S``) the odd terms (``S³``, ``S H†H``) drop out. ``S² H†H`` then
  gives the trilinear ``2 v_S s H†H`` once ``S = v_S + s``, so the singlet still mixes with h.

The dimension-1 tadpole ``S`` (``min_dim=1``) is removable by a shift of S and is left out, as in
feynlag's default window.
"""

from __future__ import annotations

import sympy as sp

MODEL_ID = "sm_singlet_z2"
#: the portal operators feynlag must return, by label (``SuggestedTerm.label``)
PORTAL_LABELS = ("S (H†H)", "S S (H†H)")


def build_singlet(benchmark=None):
    """The ``sm_singlet_z2`` bundle from the feynlag-models registry."""
    from feynlag_models.registry import build

    return build(MODEL_ID) if benchmark is None else build(MODEL_ID, benchmark=benchmark)


def fields(bundle):
    """``(H, S)`` as the model declares them."""
    return bundle.extra["ew"].H, bundle.extra["S"]


def potential_terms(bundle, with_z2: bool = False, max_dim: int = 4):
    """feynlag's invariant scalar terms in ``(H, S)``, with or without the model's Z2."""
    from feynlag import suggest_potential

    H, S = fields(bundle)
    groups = [bundle.extra["Z2"]] if with_z2 else []
    return suggest_potential([H, S], bundle.pieces.gauge_groups, discrete_groups=groups,
                             max_dim=max_dim)


def couples_s_to_sm(term, bundle) -> bool:
    """True for a term with both S and a component of H."""
    H, S = fields(bundle)
    syms = term.expr.free_symbols
    return S.components[0] in syms and any(c in syms for c in H.components)


def portal_terms(bundle, with_z2: bool = False):
    """The terms coupling S to the SM, ``{label: dim}``."""
    return {t.label: t.dim for t in potential_terms(bundle, with_z2) if couples_s_to_sm(t, bundle)}


def yukawa_terms(bundle, with_singlet: bool = True):
    """feynlag's fermion bilinears with the SM fermions and ``[H]`` or ``[H, S]``."""
    from feynlag import suggest_yukawa

    H, S = fields(bundle)
    scalars = [H, S] if with_singlet else [H]
    return suggest_yukawa(list(bundle.pieces.fermions.values()), scalars,
                          bundle.pieces.gauge_groups)


def singlet_fermion_terms(bundle):
    """The Yukawa terms containing S: none at dim <= 4."""
    s = fields(bundle)[1].components[0]
    return [t for t in yukawa_terms(bundle) if s in t.expr.free_symbols]


def z2_trilinear(bundle):
    """The coefficient of the fluctuation ``s`` in ``S² H†H`` after ``S → v_S + s``.

    Returns ``(term_expr, coefficient)``; the coefficient is ``2 v_S H†H``.
    """
    s0 = fields(bundle)[1].components[0]
    term = next(t for t in potential_terms(bundle, with_z2=True) if t.label == PORTAL_LABELS[1])
    vS = bundle.extra["vS"].s
    shifted = sp.expand(term.expr.subs(s0, vS + s0, simultaneous=True))
    return term.expr, sp.factor(shifted.coeff(s0, 1))
