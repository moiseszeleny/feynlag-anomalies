"""Step 1: the SM has one physical scalar, with m_h^2 = 2 lambda v^2, and none near 95 GeV."""

import sympy as sp

from anomalies.higgs_95gev.solutions import step_1


def test_single_physical_scalar(sm_bundle):
    """Four real doublet dof, three eaten Goldstones, one massive neutral scalar."""
    spec = step_1.scalar_spectrum(sm_bundle)
    assert step_1.doublet_real_dof(sm_bundle) == 4
    assert spec["massless"] == len(sm_bundle.goldstones) == 3
    assert spec["massive_charged"] == 0
    assert step_1.physical_neutral_scalar_count(sm_bundle) == 1
    assert step_1.doublet_real_dof(sm_bundle) - spec["massless"] == 1


def test_higgs_mass_is_two_lambda_v_squared(sm_bundle):
    """The model's key result (feynlag-models tests/test_l0_l1.py::test_tadpole_and_higgs_mass)."""
    ew = sm_bundle.extra["ew"]
    assert sp.simplify(step_1.higgs_mass_squared(sm_bundle) - 2 * ew.lam.s * ew.v.s**2) == 0


def test_no_sm_scalar_near_95gev(sm_bundle, anomaly):
    """The only scalar mass equals the MH input, which matches the measured Higgs mass (PDG 2024)
    within 1 GeV; both lie outside 90-100 GeV."""
    (m_h,) = step_1.sm_scalar_masses_gev(sm_bundle)
    assert abs(m_h - sm_bundle.benchmark["MH"]) < 1e-9
    assert step_1.scalars_in_window(sm_bundle) == []
    m_meas, dm = step_1.measured_higgs_mass(anomaly)
    lo, hi = step_1.WINDOW_GEV
    assert abs(m_h - m_meas) < 1.0
    assert m_meas - 5 * dm > hi


def test_measured_mass_sentinel_rejected(anomaly):
    import pytest
    from fit.stage1 import Stage1Error

    broken = anomaly.model_copy(deep=True)
    broken.sm_prediction.sm_reference_values["m_H_measured_GeV"] = "TODO_VERIFY"
    with pytest.raises(Stage1Error, match="m_H_measured_GeV"):
        step_1.measured_higgs_mass(broken)
