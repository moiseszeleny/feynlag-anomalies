"""Step 2: the CKM hierarchy, with a regression against PDG 2024."""

import pytest

from puzzles.flavor_puzzle.solutions import step_1, step_2

# Published benchmark, not puzzle data: PDG 2024 CKM review (rpp2024-rev-ckm-matrix, 31 May 2024),
# Eq. (12.26), the global fit for the Wolfenstein parameters, as (central, -1 sigma, +1 sigma).
PDG2024_WOLFENSTEIN = {
    "lambda": (0.22501, 0.00068, 0.00068),
    "A": (0.826, 0.015, 0.016),
    "rho_bar": (0.1591, 0.0094, 0.0094),
    "eta_bar": (0.3523, 0.0071, 0.0073),
}


@pytest.mark.parametrize("name", PDG2024_WOLFENSTEIN)
def test_wolfenstein_regression_pdg2024(sm_ckm_bundle, name):
    """The Eq. (12.28) angles fed through sm_ckm's V land inside the Eq. (12.26) 1-sigma bands."""
    got = step_2.wolfenstein(step_2.ckm_numeric(sm_ckm_bundle))[name]
    central, lo, hi = PDG2024_WOLFENSTEIN[name]
    assert central - lo <= got <= central + hi


def test_ckm_is_unitary(sm_ckm_bundle):
    import numpy as np

    V = step_2.ckm_numeric(sm_ckm_bundle)
    assert np.allclose(V.conj().T @ V, np.eye(3), atol=1e-12)


def test_ckm_sines_scale_as_powers_of_lambda(sm_ckm_bundle):
    """s12 = lambda^1, s23 ~ lambda^2, s13 ~ lambda^3-4: the hierarchy Wolfenstein exhibits."""
    lam = step_2.wolfenstein(step_2.ckm_numeric(sm_ckm_bundle))["lambda"]
    n = step_2.lambda_powers(step_1.sm_ckm_sines(sm_ckm_bundle), lam)
    assert n["s12"] == pytest.approx(1.0, abs=1e-9)
    assert 1.5 < n["s23"] < 2.5
    assert 3.0 < n["s13"] < 4.5
