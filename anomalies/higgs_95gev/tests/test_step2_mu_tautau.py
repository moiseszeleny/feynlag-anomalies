"""Step 2: the CMS ditau sigma x B as a signal strength, from the yaml inputs."""

import re

import pytest

from fit.stage1 import Stage1Error
from anomalies.higgs_95gev.solutions import step_2


def test_mu_tautau_matches_the_observables_row(anomaly):
    """The derived row in anomaly.yaml is what step_2 computes from the yaml's own inputs."""
    res = step_2.mu_tautau(anomaly)
    row = step_2.observable(anomaly, step_2.MU_TAUTAU_ROW)
    assert row.value == pytest.approx(res["mu"], abs=5e-4)
    assert row.stat_uncertainty == pytest.approx(res["exp_uncertainty"], abs=5e-4)
    assert row.sys_uncertainty == pytest.approx(res["theory_uncertainty"], abs=5e-4)


def test_mu_tautau_by_hand(anomaly):
    """sigma B / (sigma_ggF B_tautau), with the inputs read back independently of step_2."""
    ref = anomaly.sm_prediction.sm_reference_values
    ditau = step_2.observable(anomaly, step_2.DITAU_ROW)
    denom = ref["sigma_ggF_95GeV_13TeV_pb"] * ref["BR_tautau_95GeV"]
    res = step_2.mu_tautau(anomaly)
    assert res["sm_like_sigma_br_pb"] == pytest.approx(denom, rel=1e-12)
    assert res["mu"] == pytest.approx(ditau.value / denom, rel=1e-12)
    assert res["exp_uncertainty"] / res["mu"] == pytest.approx(
        ditau.stat_uncertainty / ditau.value, rel=1e-12)


def test_theory_error_is_the_quadrature_sum(anomaly):
    """Larger than each symmetrised component, smaller than their linear sum."""
    ref = anomaly.sm_prediction.sm_reference_values
    parts = [(ref[step_2.SIGMA_SCALE_UP] + ref[step_2.SIGMA_SCALE_DOWN]) / 2,
             ref[step_2.SIGMA_PDF], (ref[step_2.BR_UP] + ref[step_2.BR_DOWN]) / 2,
             (ref[step_2.EW_100] - 1) * 100]
    assert list(step_2.theory_components_pct(anomaly).values()) == pytest.approx(parts)
    rel = step_2.theory_rel_uncertainty(anomaly)
    assert max(parts) / 100 < rel < sum(parts) / 100
    assert rel == pytest.approx(sum(x**2 for x in parts) ** 0.5 / 100, rel=1e-12)


def test_derived_row_is_exclusive_with_the_ditau_row(anomaly):
    """The derived mu_tautau row and the sigma x B row are one measurement: both exist, and the
    pair is recorded so that a fit never takes both."""
    names = {o.name for o in anomaly.observables}
    assert step_2.EXCLUSIVE_WITH == {step_2.MU_TAUTAU_ROW: step_2.DITAU_ROW}
    assert set(step_2.EXCLUSIVE_WITH) | set(step_2.EXCLUSIVE_WITH.values()) <= names


@pytest.mark.parametrize("key", [step_2.SIGMA, step_2.BR, step_2.EW_100])
def test_sentinel_rejected(anomaly, key):
    broken = anomaly.model_copy(deep=True)
    broken.sm_prediction.sm_reference_values[key] = "TODO_VERIFY"
    with pytest.raises(Stage1Error, match=re.escape(key)):
        step_2.mu_tautau(broken)


def test_ditau_sentinel_rejected(anomaly):
    broken = anomaly.model_copy(deep=True)
    step_2.observable(broken, step_2.DITAU_ROW).value = "TODO_VERIFY"
    with pytest.raises(Stage1Error, match=re.escape("CMS ditau")):
        step_2.mu_tautau(broken)
