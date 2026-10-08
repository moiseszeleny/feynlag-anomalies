"""Step 1 -- the SM's flavor parameters from feynlag-models' ``sm_ckm`` and the quantifier.

The model is imported through the registry; nothing here declares a Lagrangian. ``sm_ckm`` is
built at a benchmark whose masses, vev and CKM inputs are the sourced ``sm_quantities`` of
``puzzle.yaml``, and the Yukawas are read from the model's own relation y_f = sqrt(2) m_f / v
(``bundle.pieces.yukawa_params``), never re-typed here.

Importing this module is cheap (no model build): ``feynlag_anomalies.loader`` imports it to check
that ``quantifier.implementation`` resolves.
"""

from __future__ import annotations

import math
from collections.abc import Mapping

from fit.stage1 import _reject_sentinel

MODEL_ID = "sm_ckm"

#: ``puzzle.yaml`` ``sm_quantities[].name`` -> ``sm_ckm`` benchmark key
MASS_INPUTS = {
    "m_u(M_Z)": "MU", "m_c(M_Z)": "MC", "m_t(M_Z)": "MT",
    "m_d(M_Z)": "MD", "m_s(M_Z)": "MS", "m_b(M_Z)": "MB",
    "m_e(M_Z)": "ME", "m_mu(M_Z)": "MMU", "m_tau(M_Z)": "MTA",
}
VEV_INPUT = {"v_F": "v"}
CKM_INPUTS = {"sin theta_12": "s12", "sin theta_13": "s13", "sin theta_23": "s23", "delta": "deltaCP"}

#: Yukawa parameter names of ``sm_ckm``, grouped by sector
SECTORS = {
    "up": ("yu", "yc", "yt"),
    "down": ("yd", "ys", "yb"),
    "lepton": ("ye", "ymu", "ytau"),
}
YUKAWAS = tuple(y for names in SECTORS.values() for y in names)
#: CKM angles of ``sm_ckm`` whose sines enter the quantifier (the phase deltaCP does not)
CKM_ANGLES = {"s12": "th12", "s13": "th13", "s23": "th23"}


def free_parameter_log10_span(params: Mapping[str, float]) -> float:
    """The puzzle's quantifier: log10(max |c| / min |c|) over the free parameters ``params``."""
    values = [abs(float(c)) for c in params.values()]
    if not values or min(values) == 0.0:
        raise ValueError("the span needs at least one parameter and no zeros")
    return math.log10(max(values) / min(values))


def sm_benchmark(puzzle) -> dict:
    """``sm_ckm``'s metadata benchmark with masses, v and CKM inputs taken from ``puzzle``.

    Every other input (gauge couplings, M_H, widths) stays at the model benchmark; none of them
    enters the Yukawas or the CKM matrix. Raises on the ``TODO_VERIFY`` sentinel.
    """
    from feynlag_models.registry import metadata

    bench = dict(metadata(MODEL_ID)["benchmark"]["inputs"])
    by_name = {q.name: q for q in puzzle.sm_quantities}
    for name, key in {**MASS_INPUTS, **VEV_INPUT, **CKM_INPUTS}.items():
        bench[key] = _reject_sentinel(name, by_name[name].value)
    return bench


def sm_yukawas(bundle) -> dict[str, float]:
    """``{name: y_f}`` evaluated from the bundle's own Yukawa parameters at its benchmark."""
    values = bundle.params.numeric()
    ys = bundle.pieces.yukawa_params
    return {name: values[ys[name].symbol] for name in YUKAWAS}


def sm_ckm_sines(bundle) -> dict[str, float]:
    """``{s12, s13, s23}`` as sines of the bundle's CKM angles."""
    values = bundle.params.numeric()
    by_name = {p.name: p for p in bundle.extra["ckm_params"]}
    return {key: math.sin(values[by_name[angle].symbol]) for key, angle in CKM_ANGLES.items()}


def sm_free_parameters(bundle) -> dict[str, float]:
    """The SM's dimensionless flavor parameters the quantifier runs over."""
    return {**sm_yukawas(bundle), **sm_ckm_sines(bundle)}


def sm_quark_parameters(bundle) -> dict[str, float]:
    """The quark-only free parameters: the six quark Yukawas and the three CKM sines.

    This is the SM's footing for comparison with a model fitted to quarks only (P3).
    """
    yukawas = sm_yukawas(bundle)
    quarks = {name: yukawas[name] for name in SECTORS["up"] + SECTORS["down"]}
    return {**quarks, **sm_ckm_sines(bundle)}


def sector_spans(yukawas: Mapping[str, float]) -> dict[str, float]:
    """The quantifier restricted to each sector's three Yukawas."""
    return {sector: free_parameter_log10_span({n: yukawas[n] for n in names})
            for sector, names in SECTORS.items()}
