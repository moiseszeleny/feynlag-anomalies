"""Step 5 -- a mixing angle from ``tan 2 alpha`` is a convention plus a branch (the UG-4 lesson).

Everything here acts on a plain real symmetric matrix ``M = [[a, b], [b, d]]``: no field, no
model and no Lagrangian is declared (CLAUDE.md hard rule 1). The rotation has feynlag-models'
orientation, new = R . old with ``R(alpha) = [[c, s], [-s, c]]`` (CONVENTIONS.md, ``rotation_2x2``),
so ``R M R^T`` is the mass matrix of the rotated states.

- ``(R M R^T)_12 = (d - a)/2 sin 2alpha + b cos 2alpha``, so ``tan 2alpha = 2b/(a - d)`` and the
  condition is unchanged under ``alpha -> alpha + pi/2``, which swaps the two diagonal entries.
  The condition fixes alpha only modulo ``pi/2``.
- The principal branch, ``alpha = atan(2b/(a - d))/2`` (feynlag's ``diagonalize_orthogonal_2x2``),
  has ``|alpha| <= pi/4``, so ``|cos alpha| >= |sin alpha|``: the first rotated state is the one
  closest to the first basis state. It labels by mixing. Its eigenvalue is the larger one when
  ``a > d`` and the smaller one when ``a < d``.
- Gunion--Haber (hep-ph/0207010, Eqs. (14)-(17)) fix alpha from both ``sin 2alpha`` and
  ``cos 2alpha`` with ``m_H >= m_h`` and take ``-pi/2 <= alpha <= pi/2``; that is the principal
  branch only when ``M11 > M22``. Their footnote 10: ``alpha -> alpha +- pi`` is ``h -> -h``,
  ``H -> -H``, so the branch left after mass ordering is a field sign.

The adapters at the end hand the candidates' CP-even blocks to these functions; they reuse
:mod:`step_4` and add no physics.
"""

from __future__ import annotations

import math

import numpy as np
import sympy as sp

from anomalies.higgs_95gev.solutions import step_4

#: two plain matrices, one per regime
DEMO_A_GT_D = ((3.0, 1.0), (1.0, 1.0))
DEMO_A_LT_D = ((1.0, 1.0), (1.0, 3.0))


# --- symbolic: the generic matrix -------------------------------------------------------------
def symmetric_2x2():
    """``(a, b, d, M)`` with ``M = [[a, b], [b, d]]``, real symbols."""
    a, b, d = sp.symbols("a b d", real=True)
    return a, b, d, sp.Matrix([[a, b], [b, d]])


def rotation(alpha):
    """``R(alpha) = [[cos, sin], [-sin, cos]]``, new = R . old."""
    c, s = sp.cos(alpha), sp.sin(alpha)
    return sp.Matrix([[c, s], [-s, c]])


def rotated(M, alpha):
    """``R(alpha) M R(alpha)^T``, the mass matrix of the rotated states."""
    R = rotation(alpha)
    return R * M * R.T


def offdiagonal(M, alpha):
    """The (1, 2) entry of :func:`rotated`, as ``(d - a)/2 sin 2alpha + b cos 2alpha``."""
    return sp.simplify(sp.trigsimp(rotated(M, alpha)[0, 1]))


def principal_angle(a, b, d):
    """``atan(2b/(a - d))/2``: symbolic for symbols, a float for numbers (``a != d``)."""
    if all(isinstance(x, (int, float)) for x in (a, b, d)):
        return 0.5 * math.atan(2 * b / (a - d))
    return sp.atan(2 * b / (a - d)) / 2


def first_entry_by_regime():
    """The principal branch's first diagonal entry in each regime.

    Returns ``{+1: (computed, closed), -1: (computed, closed)}`` for ``a = d + sign delta``,
    ``delta > 0``. ``computed`` is ``(R M R^T)_11`` at the principal angle, simplified, and
    ``closed`` is ``(a + d)/2 + sign sqrt((a - d)^2 + 4 b^2)/2`` in the same variables.
    """
    a, b, d, M = symmetric_2x2()
    delta = sp.Symbol("delta", positive=True)
    entry = rotated(M, principal_angle(a, b, d))[0, 0]
    out = {}
    for sign in (1, -1):
        computed = sp.simplify(sp.expand_trig(entry.subs(a, d + sign * delta)))
        closed = (2 * d + sign * delta) / 2 + sign * sp.sqrt(delta**2 + 4 * b**2) / 2
        out[sign] = (computed, closed)
    return out


# --- numeric: which state comes first ----------------------------------------------------------
def branch_report(M) -> dict:
    """The principal branch on a numeric ``M``.

    Returns ``alpha``, the ``first`` and ``second`` diagonal entries of ``R M R^T``, whether the
    first is the lighter, and ``overlap``: ``|cos alpha|``, the first state's component along the
    first basis state.
    """
    M = np.asarray(M, dtype=float)
    alpha = principal_angle(float(M[0, 0]), float(M[0, 1]), float(M[1, 1]))
    c, s = math.cos(alpha), math.sin(alpha)
    R = np.array([[c, s], [-s, c]])
    D = R @ M @ R.T
    return {"alpha": alpha, "first": float(D[0, 0]), "second": float(D[1, 1]),
            "offdiagonal": float(D[0, 1]), "first_is_lighter": bool(D[0, 0] < D[1, 1]),
            "overlap": abs(c)}


def mass_ordered_shift(M, first: str = "heavier") -> float:
    """What to add to the principal alpha to put the ``first`` ("heavier"/"lighter") state first.

    0 when the principal branch already does; otherwise ``+pi/2`` or ``-pi/2``, whichever keeps
    the result in ``[-pi/2, pi/2]`` (Gunion--Haber's range; the two differ by ``pi``, a field
    sign).
    """
    if first not in ("heavier", "lighter"):
        raise ValueError(f"first must be 'heavier' or 'lighter', not {first!r}")
    r = branch_report(M)
    if r["first_is_lighter"] == (first == "lighter"):
        return 0.0
    return math.pi / 2 if r["alpha"] <= 0 else -math.pi / 2


def closed_form_roots(M) -> tuple[float, float]:
    """``(a + d)/2 -+ sqrt((a - d)^2 + 4b^2)/2``: the minus root, then the plus root."""
    M = np.asarray(M, dtype=float)
    a, b, d = M[0, 0], M[0, 1], M[1, 1]
    r = math.sqrt((a - d) ** 2 + 4 * b**2) / 2
    return (a + d) / 2 - r, (a + d) / 2 + r


# --- the candidates' CP-even blocks ------------------------------------------------------------
def singlet_mass_matrix(anomaly) -> np.ndarray:
    """``sm_singlet_z2``'s (h, s) block at the step-4 override (GeV^2)."""
    from feynlag_models.registry import load

    base = load(step_4.SINGLET_ID).benchmark_point()
    o = step_4.singlet_override(base, step_4.TARGET_MASS_GEV, step_4.heavy_mass(anomaly))
    v, vS = base["v"], base["vS"]
    m12 = o["lamHS"] * v * vS
    return np.array([[o["MH"] ** 2, m12], [m12, 2 * o["lamS"] * vS**2]])


def thdm_block(anomaly, point: dict = step_4.THDM_POINT) -> dict:
    """``thdm_type2``'s (rho1, rho2) block at a step-4 point, from the Gunion--Haber inversion."""
    from feynlag_models.registry import load

    v = load(step_4.THDM_ID).benchmark_point()["v"]
    return step_4.thdm_gh_inversion(v, step_4.TARGET_MASS_GEV, step_4.heavy_mass(anomaly),
                                    point["tanb"], point["sin_bma"], point["mA"], point["mHp"],
                                    point["m12sq"])
