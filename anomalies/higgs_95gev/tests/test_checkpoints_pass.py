"""Each checkpoint accepts the canonical answer and rejects a wrong one."""

import math

from anomalies.higgs_95gev import checkpoints_def as cd
from anomalies.higgs_95gev.solutions import step_1, step_2, step_3, step_4, step_5


def test_check_1(sm_bundle):
    check = cd.make_check_1(sm_bundle)
    assert check(step_1.physical_neutral_scalar_count(sm_bundle))
    assert not check(4)


def test_check_2(anomaly):
    check = cd.make_check_2(anomaly)
    mu = step_2.mu_tautau(anomaly)["mu"]
    assert check(mu)
    assert not check(1.1 * mu)


def test_check_3(singlet_bundle):
    check = cd.make_check_3(singlet_bundle)
    assert check(len(step_3.portal_terms(singlet_bundle)))
    assert not check(1)


def test_check_4(singlet_candidate):
    check = cd.make_check_4(singlet_candidate)
    s = step_4.singlet_spectrum(singlet_candidate)
    assert check(s["MH2"])
    assert not check(s["MH1"])


def test_check_5(anomaly):
    M = step_5.thdm_block(anomaly)["M"]
    check = cd.make_check_5(M)
    assert check(step_5.mass_ordered_shift(M, first="heavier"))
    assert not check(0.0) and not check(-math.pi / 2)
