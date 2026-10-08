"""Pins a number quoted in decisions.md against the froggatt_nielsen model."""

import pytest
from feynlag_models import registry


def test_fn_lepton_placeholder_gives_me_22_mev():
    """decisions.md (2026-10-08, P3 prep): at froggatt_nielsen's benchmark the placeholder lepton
    charges give m_e = 22.09 MeV, which is why P3 fits quarks only."""
    fn = registry.load("froggatt_nielsen")
    masses, _ = fn.benchmark_flavour(registry.build("froggatt_nielsen"))
    assert masses["lepton"][0] == pytest.approx(0.02209, abs=5e-6)  # GeV
