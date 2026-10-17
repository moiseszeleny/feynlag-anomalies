"""Step 1 -- SM structural test: one physical scalar, at m_h^2 = 2 lambda v^2, none near 95 GeV.

The SM is taken from feynlag-models (``feynlag_models.registry.build("sm")``, L3); nothing here
declares a field or a Lagrangian. After EWSB the Higgs doublet's four real degrees of freedom
split into three would-be Goldstones (eaten by W+-, Z) and one physical neutral scalar ``h``.
The model's own scalar mass matrices give the count and the mass, read here rather than assumed:
the neutral block in the ``(h, G0)`` basis is ``diag(2 lambda v^2, 0)`` and the charged block
``(G+)`` is ``0`` (``models/sm/tests/test_l0_l1.py::test_tadpole_and_higgs_mass`` and
``::test_goldstone_count`` in feynlag-models).

The numeric mass uses the model's benchmark input ``MH`` (a round input, not a measurement):
the SM fixes the *number* of scalars, while their mass is an input; with one scalar, the input
that reproduces the observed boson leaves nothing for 95 GeV.
"""

from __future__ import annotations

import math

import sympy as sp

MODEL_ID = "sm"
#: the mass window of the excess, in GeV (CMS diphoton 95.4, CMS ditau 95-100, LEP ~98)
WINDOW_GEV = (90.0, 100.0)


def build_sm():
    """The ``sm`` bundle from the feynlag-models registry."""
    from feynlag_models.registry import build

    return build(MODEL_ID)


def scalar_mass_matrices(bundle) -> tuple[sp.Matrix, sp.Matrix]:
    """The neutral ``(h, G0)`` and charged ``(G+)`` scalar mass matrices after EWSB."""
    b = bundle.bosons
    neutral = bundle.model.mass_matrix([b["h"], b["G0"]])
    charged = bundle.model.mass_matrix([b["Gp"]], charged=True)
    return neutral, charged


def doublet_real_dof(bundle) -> int:
    """Real degrees of freedom of the Higgs doublet: two complex components."""
    return 2 * len(bundle.extra["ew"].H.components)


def scalar_spectrum(bundle) -> dict:
    """Count massive and massless scalar states from the model's mass matrices.

    A neutral real state counts once, a charged complex state (``G+`` with ``G-``) twice.
    Returns the counts and the symbolic nonzero neutral eigenvalues.
    """
    neutral, charged = scalar_mass_matrices(bundle)
    n_eig = [e for e, m in neutral.eigenvals().items() for _ in range(m)]
    c_eig = [e for e, m in charged.eigenvals().items() for _ in range(m)]
    massive_neutral = [sp.simplify(e) for e in n_eig if sp.simplify(e) != 0]
    massive_charged = [e for e in c_eig if sp.simplify(e) != 0]
    return {
        "massive_neutral": len(massive_neutral),
        "massive_charged": 2 * len(massive_charged),
        "massless": (len(n_eig) - len(massive_neutral)) + 2 * (len(c_eig) - len(massive_charged)),
        "neutral_mass_squared": massive_neutral,
    }


def physical_neutral_scalar_count(bundle) -> int:
    """How many physical (massive) neutral scalars the SM has after EWSB."""
    return scalar_spectrum(bundle)["massive_neutral"]


def higgs_mass_squared(bundle) -> sp.Expr:
    """The one nonzero neutral eigenvalue, symbolically (the model's ``2 lambda v^2``)."""
    (m2,) = scalar_spectrum(bundle)["neutral_mass_squared"]
    return m2


def sm_scalar_masses_gev(bundle) -> list[float]:
    """Masses (GeV) of every physical SM scalar at the model benchmark."""
    values = bundle.values()
    return [math.sqrt(float(m2.subs(values))) for m2 in scalar_spectrum(bundle)["neutral_mass_squared"]]


def scalars_in_window(bundle, window=WINDOW_GEV) -> list[float]:
    """The physical SM scalar masses that fall inside ``window`` (GeV); empty in the SM."""
    lo, hi = window
    return [m for m in sm_scalar_masses_gev(bundle) if lo <= m <= hi]
