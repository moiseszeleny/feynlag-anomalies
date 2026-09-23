"""Peldano 2: the dimension-5 Weinberg operator appears only once max_dim is raised to 5."""

from anomalies.neutrino_mass.solutions.peldano_2 import weinberg_operator_present


def test_weinberg_operator_absent_at_dim4():
    assert weinberg_operator_present(max_dim=4) is False


def test_weinberg_operator_appears_at_dim5():
    assert weinberg_operator_present(max_dim=5) is True
