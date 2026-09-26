"""Step 7 -- confront the step-6 fit with non-oscillation bounds: cosmology, 0nubetabeta, beta decay.

Everything is computed from the fitted ``seesaw_type1_2n`` Yukawas; no model is declared here.
The light-neutrino matrix comes from feynlag's own seesaw formula, ``m_nu = -m_D M_R^-1 m_D^T``
with ``m_D = y v / sqrt2`` (feynlag-models CONVENTIONS.md). ``m_betabeta = |(m_nu)_ee|`` and
``m_beta = sqrt((m_nu m_nu^dagger)_ee)`` are basis-independent, so no PMNS phase convention
enters; the Takagi route (``OscillationPredictor.spectrum``) is the independent cross-check.
Heavy-state contributions to 0nubetabeta are suppressed by the active-sterile mixing squared and
are not included.
"""

from __future__ import annotations

import math

import numpy as np
import sympy as sp

from fit.stage1 import upper_limit_cut

from .step_6 import FIT_OBSERVABLES, OscillationPredictor

_GEV_TO_EV = 1e9
_FLAVORS = ("e", "mu", "tau")


def light_matrix(bundle, yv: dict) -> np.ndarray:
    """The 3x3 light-neutrino Majorana matrix in eV, from the fitted Yukawas ``{name: value}``."""
    from feynlag import seesaw_light_mass

    bench = bundle.benchmark
    n_nuR = len({name[-1] for name in yv})
    m_D = sp.Matrix(3, n_nuR, lambda a, k: yv[f"yv_{_FLAVORS[a]}{k + 1}"] * bench["v"] / math.sqrt(2))
    M_R = sp.diag(*[bench[f"MR{k + 1}"] for k in range(n_nuR)])
    return np.array(seesaw_light_mass(m_D, M_R).tolist(), dtype=float) * _GEV_TO_EV


def m_betabeta(m: np.ndarray) -> float:
    """Effective Majorana mass ``|(m_nu)_ee|``."""
    return float(abs(m[0, 0]))


def m_beta(m: np.ndarray) -> float:
    """Effective electron-neutrino mass ``sqrt((m_nu m_nu^dagger)_ee)``."""
    return float(math.sqrt((m @ m.conj().T)[0, 0].real))


def mbb_branches(masses_eV, predicted: dict) -> tuple[float, float]:
    """``(constructive, destructive)``: ``|m2 s12^2 c13^2 +- m3 s13^2|`` with m_1 = 0.

    These are the two CP-conserving values (Majorana phases 0 or pi). With real Yukawas and
    positive M_R, ``m_nu = -(m_D M_R^-1/2)(m_D M_R^-1/2)^T`` is negative semidefinite, so all light
    eigenvalues share one sign and only the constructive branch is reachable; the destructive one
    needs complex Yukawas.
    """
    s12 = math.sin(math.radians(predicted[FIT_OBSERVABLES[2]]))
    s13 = math.sin(math.radians(predicted[FIT_OBSERVABLES[3]]))
    a = masses_eV[1] * s12**2 * (1 - s13**2)
    b = masses_eV[2] * s13**2
    return abs(a + b), abs(a - b)


def takagi_cross_check(bundle, yv: dict) -> dict:
    """``m_betabeta`` and ``m_beta`` from the exact Takagi masses and mixing (light states only)."""
    predictor = OscillationPredictor(bundle)
    masses, U = predictor.spectrum([yv[n] for n in predictor.names])
    Ue = [complex(U[0, i]) for i in range(3)]
    return {
        "m_betabeta": abs(sum(Ue[i] ** 2 * masses[i] for i in range(3))),
        "m_beta": math.sqrt(sum(abs(Ue[i]) ** 2 * masses[i] ** 2 for i in range(3))),
    }


def predictions(bundle, fit: dict) -> dict:
    """``{quantity: value in eV}`` for every ``Constraint.quantity``, from a step-6 fit."""
    m = light_matrix(bundle, fit["yv"])
    return {"sum_m_nu": float(sum(fit["masses_eV"])), "m_betabeta": m_betabeta(m), "m_beta": m_beta(m)}


def confront(preds: dict, anomaly) -> list[dict]:
    """One row per ``anomaly.constraints`` entry: prediction, limits and the stage-1 verdict."""
    return [
        {
            "name": c.name,
            "quantity": c.quantity,
            "prediction": preds[c.quantity],
            "limit": c.upper_limit,
            "strongest": c.upper_limit_strongest,
            "cl": c.confidence_level,
            "passes": upper_limit_cut(preds[c.quantity], c.upper_limit),
            "passes_strongest": (None if c.upper_limit_strongest is None
                                 else upper_limit_cut(preds[c.quantity], c.upper_limit_strongest)),
            "notes": c.notes,
        }
        for c in anomaly.constraints
    ]
