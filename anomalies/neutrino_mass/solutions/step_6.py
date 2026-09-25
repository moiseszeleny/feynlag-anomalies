"""Step 6 -- stage-1 chi2 of feynlag-models' ``seesaw_type1_2n`` against oscillation data.

The model is imported through the registry; nothing here declares a Lagrangian. Its symbolic
5×5 seesaw matrix ``bundle.extra["Mnu"]`` is evaluated at trial Yukawas (``M_1``, ``M_2`` and
``v`` stay at the model benchmark) and diagonalised with feynlag's numeric Takagi, so a fit
point costs milliseconds instead of a model rebuild.
"""

from __future__ import annotations

import math

import numpy as np
import sympy as sp

from fit.stage1 import combine_uncertainties, minimize_chi2, perturbativity_cut

MODEL_ID = "seesaw_type1_2n"
FIT_OBSERVABLES = (
    "Delta m^2_21 (solar)",
    "Delta m^2_31 (atmospheric, normal ordering)",
    "theta_12",
    "theta_13",
    "theta_23",
)
#: fit variables are y / YV_SCALE, so least_squares works with O(1) numbers
YV_SCALE = 1e-6
_GEV_TO_EV = 1e9
_DPS = 30


def observed_from_anomaly(anomaly, names=FIT_OBSERVABLES) -> dict:
    """``{name: (value, sigma)}`` from the loaded ``Anomaly``; the sentinel is rejected downstream."""
    by_name = {o.name: o for o in anomaly.observables}
    return {n: (by_name[n].value,
                combine_uncertainties(by_name[n].stat_uncertainty, by_name[n].sys_uncertainty))
            for n in names}


class OscillationPredictor:
    """Masses and mixing angles of a ``seesaw_type1_2n`` bundle as a function of its Yukawas."""

    def __init__(self, bundle):
        e = bundle.extra
        self.names = [p.name for p in e["yv_params"]]
        self.symbols = [p.s for p in e["yv_params"]]
        fixed = {e["ew"].v.s: sp.Float(bundle.benchmark["v"], _DPS)}
        fixed.update({p.s: sp.Float(bundle.benchmark[p.name], _DPS) for p in e["MR"]})
        self.Mnu = e["Mnu"].subs(fixed)
        self.benchmark_yv = np.array([bundle.benchmark[n] for n in self.names], dtype=float)

    def spectrum(self, yv):
        """``(masses_eV, U)`` from feynlag's numeric Takagi, columns ordered by mass."""
        from feynlag import diagonalize_takagi

        M = self.Mnu.subs({s: sp.Float(float(y), _DPS) for s, y in zip(self.symbols, yv)})
        U, D = diagonalize_takagi(M, method="numeric")
        return [float(D[k, k]) * _GEV_TO_EV for k in range(D.rows)], U

    def __call__(self, yv) -> dict:
        """Δm²_21, Δm²_31 in eV² and θ12, θ13, θ23 in degrees, normal ordering (m1 lightest)."""
        m, U = self.spectrum(yv)
        light = sorted(m[:3])
        if m[:3] != light or m[2] >= m[3]:
            raise ValueError("expected three light states below the heavy ones, ordered by mass")
        s13 = float(abs(U[0, 2]))
        c13sq = 1.0 - s13**2
        s12 = math.sqrt(float(abs(U[0, 1])) ** 2 / c13sq)
        s23 = math.sqrt(float(abs(U[1, 2])) ** 2 / c13sq)
        return {
            FIT_OBSERVABLES[0]: m[1] ** 2 - m[0] ** 2,
            FIT_OBSERVABLES[1]: m[2] ** 2 - m[0] ** 2,
            FIT_OBSERVABLES[2]: math.degrees(math.asin(s12)),
            FIT_OBSERVABLES[3]: math.degrees(math.asin(s13)),
            FIT_OBSERVABLES[4]: math.degrees(math.asin(s23)),
        }


def run_fit(bundle, observed: dict) -> dict:
    """Minimize the Gaussian chi2 over the six Yukawas, starting from the model benchmark.

    Six parameters against five observables: ``ndof = -1``, so chi2_min ≈ 0 shows only that the
    model *can* accommodate the data. The result also carries the SM chi2 over the two Δm²
    (the SM predicts massless neutrinos) and the model's lightest mass, which is exactly 0.
    """
    predictor = OscillationPredictor(bundle)
    fit = minimize_chi2(lambda x: predictor(x * YV_SCALE), predictor.benchmark_yv / YV_SCALE,
                        observed, x_scale="jac")
    yv = fit["x"] * YV_SCALE
    masses, _ = predictor.spectrum(yv)
    dm2 = FIT_OBSERVABLES[:2]
    fit.update(
        yv=dict(zip(predictor.names, yv)),
        perturbative=perturbativity_cut(dict(zip(predictor.names, yv))),
        masses_eV=masses[:3],
        sum_m_nu_eV=sum(masses[:3]),
        chi2_sm_dm2=sum((observed[n][0] / observed[n][1]) ** 2 for n in dm2),
        chi2_model_dm2=sum(fit["pulls"][n] ** 2 for n in dm2),
    )
    return fit
