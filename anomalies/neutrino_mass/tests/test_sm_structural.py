"""Step 1: no dimension<=4 neutrino-mass term exists for minimal SM lepton content."""

from anomalies.neutrino_mass.solutions.step_1 import count_dim4_yukawa_terms


def test_no_dim4_neutrino_mass_term():
    assert count_dim4_yukawa_terms() == 1
