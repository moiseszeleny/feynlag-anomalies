"""Each checkpoint accepts the canonical answer and rejects a wrong one."""

from anomalies.higgs_95gev import checkpoints_def as cd
from anomalies.higgs_95gev.solutions import step_1, step_2


def test_check_1(sm_bundle):
    check = cd.make_check_1(sm_bundle)
    assert check(step_1.physical_neutral_scalar_count(sm_bundle))
    assert not check(4)


def test_check_2(anomaly):
    check = cd.make_check_2(anomaly)
    mu = step_2.mu_tautau(anomaly)["mu"]
    assert check(mu)
    assert not check(1.1 * mu)
