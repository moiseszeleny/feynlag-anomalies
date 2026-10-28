"""Step 5: the branch of a 2x2 mixing angle, on a plain matrix and on the candidates' blocks."""

import math

import numpy as np
import pytest
import sympy as sp

from anomalies.higgs_95gev.solutions import step_4, step_5


def test_offdiagonal_fixes_alpha_modulo_half_pi():
    a, b, d, M = step_5.symmetric_2x2()
    al = sp.Symbol("alpha", real=True)
    off = step_5.offdiagonal(M, al)
    assert sp.simplify(off - ((d - a) / 2 * sp.sin(2 * al) + b * sp.cos(2 * al))) == 0
    assert sp.simplify(off.subs(al, step_5.principal_angle(a, b, d))) == 0
    # alpha + pi/2 flips the sign of the off-diagonal entry and swaps the diagonal ones
    shifted = step_5.rotated(M, al + sp.pi / 2)
    D = step_5.rotated(M, al)
    assert sp.simplify(shifted[0, 1] + D[0, 1]) == 0
    assert sp.simplify(shifted[0, 0] - D[1, 1]) == 0 and sp.simplify(shifted[1, 1] - D[0, 0]) == 0


def test_first_entry_by_regime():
    for computed, closed in step_5.first_entry_by_regime().values():
        assert sp.simplify(computed - closed) == 0


@pytest.mark.parametrize("M, lighter_first", [(step_5.DEMO_A_GT_D, False),
                                              (step_5.DEMO_A_LT_D, True)])
def test_demo_regimes(M, lighter_first):
    r = step_5.branch_report(M)
    assert abs(r["alpha"]) <= math.pi / 4 and r["overlap"] >= 1 / math.sqrt(2)
    assert r["offdiagonal"] == pytest.approx(0, abs=1e-12)
    assert r["first_is_lighter"] is lighter_first
    assert sorted([r["first"], r["second"]]) == pytest.approx(sorted(np.linalg.eigvalsh(M)))
    # the shift that puts the other state first swaps the two entries
    want = "heavier" if lighter_first else "lighter"
    alpha = r["alpha"] + step_5.mass_ordered_shift(M, first=want)
    D = np.asarray(step_5.rotated(sp.Matrix(M), alpha).evalf(), dtype=float)
    assert D[0, 0] == pytest.approx(r["second"]) and D[1, 1] == pytest.approx(r["first"])
    assert abs(alpha) <= math.pi / 2


def test_singlet_block_is_in_the_a_gt_d_regime(anomaly, singlet_candidate):
    M = step_5.singlet_mass_matrix(anomaly)
    r = step_5.branch_report(M)
    s = step_4.singlet_spectrum(singlet_candidate)
    assert M[0, 0] > M[1, 1] and not r["first_is_lighter"]
    assert r["alpha"] == pytest.approx(s["theta"], rel=1e-9)
    assert math.sqrt(r["first"]) == pytest.approx(s["MH1"], rel=1e-9)
    # the pinned key result's minus root for h1 is the 95 GeV state, not MH1, in this regime
    minus, plus = step_5.closed_form_roots(M)
    assert math.sqrt(minus) == pytest.approx(s["MH2"], rel=1e-9)
    assert math.sqrt(plus) == pytest.approx(s["MH1"], rel=1e-9)


def test_thdm_blocks_against_the_bundles(anomaly, thdm_aligned):
    swapped = step_4.build_thdm_candidate(anomaly)
    for (bundle, inv), shift in ((swapped, math.pi / 2), (thdm_aligned, 0.0)):
        r = step_5.branch_report(inv["M"])
        t = step_4.thdm_spectrum(bundle)
        # the model's alpha is the principal branch on the same block
        assert r["alpha"] == pytest.approx(t["alpha"], rel=1e-9)
        assert math.sqrt(r["first"]) == pytest.approx(t["MHH"], rel=1e-6)
        assert step_5.mass_ordered_shift(inv["M"], first="heavier") == pytest.approx(shift)
        assert r["alpha"] + shift == pytest.approx(inv["alpha_GH"], rel=1e-9)
    assert step_5.thdm_block(anomaly)["M"] == pytest.approx(swapped[1]["M"])
