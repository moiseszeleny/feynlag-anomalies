"""Step 2 -- the CKM hierarchy in powers of the Cabibbo angle.

The CKM matrix is ``sm_ckm``'s ``V_expr`` (feynlag's ``standard_ckm``) evaluated at the bundle
benchmark. The Wolfenstein parameters follow the phase-convention-independent definitions of
PDG 2024, CKM review, Eq. (12.4).
"""

from __future__ import annotations

import math
from collections.abc import Mapping

import numpy as np


def ckm_numeric(bundle) -> np.ndarray:
    """The 3x3 complex CKM matrix at the bundle benchmark."""
    V = bundle.extra["V_expr"].subs(bundle.params.numeric()).evalf()
    return np.array(V.tolist(), dtype=complex)


def wolfenstein(V: np.ndarray) -> dict[str, float]:
    """``{lambda, A, rho_bar, eta_bar}`` from a CKM matrix (PDG Eq. 12.4).

    lambda = |V_us| / sqrt(|V_ud|^2 + |V_us|^2), A lambda^2 = lambda |V_cb / V_us| and
    rho_bar + i eta_bar = -(V_ud V_ub^*) / (V_cd V_cb^*).
    """
    Vud, Vus, Vub = V[0]
    Vcd, Vcb = V[1, 0], V[1, 2]
    lam = abs(Vus) / math.sqrt(abs(Vud) ** 2 + abs(Vus) ** 2)
    A = abs(Vcb) / (lam * abs(Vus))
    z = -(Vud * np.conj(Vub)) / (Vcd * np.conj(Vcb))
    return {"lambda": float(lam), "A": float(A), "rho_bar": float(z.real), "eta_bar": float(z.imag)}


def lambda_powers(params: Mapping[str, float], lam: float) -> dict[str, float]:
    """``{name: n}`` with c = lambda^n, i.e. n = log c / log lambda, for each parameter."""
    return {name: math.log(abs(c)) / math.log(lam) for name, c in params.items()}
