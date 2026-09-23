"""Unit tests for fit.stage1 -- toy numbers only, model-independent."""

import pytest
import sympy as sp

from fit.stage1 import (
    Stage1Error,
    bfb_single_quartic,
    chi2_gaussian,
    combine_uncertainties,
    perturbativity_cut,
    predict,
    unitarity_cut,
)


def test_combine_uncertainties_quadrature_sum():
    assert combine_uncertainties(3.0, 4.0) == pytest.approx(5.0)


def test_combine_uncertainties_rejects_sentinel():
    with pytest.raises(Stage1Error):
        combine_uncertainties("TODO_VERIFY", 4.0)


def test_chi2_gaussian_zero_at_exact_match():
    assert chi2_gaussian({"x": 1.0}, {"x": (1.0, 0.5)}) == pytest.approx(0.0)


def test_chi2_gaussian_nonzero_away_from_center():
    chi2 = chi2_gaussian({"x": 2.0}, {"x": (1.0, 0.5)})
    assert chi2 == pytest.approx(4.0)


def test_chi2_gaussian_rejects_sentinel():
    with pytest.raises(Stage1Error):
        chi2_gaussian({"x": "TODO_VERIFY"}, {"x": (1.0, 0.5)})


def test_chi2_gaussian_missing_prediction_raises_keyerror():
    with pytest.raises(KeyError):
        chi2_gaussian({}, {"x": (1.0, 0.5)})


def test_predict_evaluates_sympy_expression():
    x, y = sp.symbols("x y")
    predicted = predict({x: 2.0, y: 3.0}, {"sum": x + y})
    assert predicted == {"sum": pytest.approx(5.0)}


def test_perturbativity_cut():
    assert perturbativity_cut({"g": 1.0}) is True
    assert perturbativity_cut({"g": 100.0}) is False


def test_bfb_single_quartic():
    assert bfb_single_quartic(0.13) is True
    assert bfb_single_quartic(-0.1) is False


def test_unitarity_cut_not_implemented():
    with pytest.raises(NotImplementedError):
        unitarity_cut()
