"""Step 3-4: importing feynlag-models' seesaw_type1 and reading off its mass spectrum.

The order-of-magnitude checks below use seesaw_type1's own benchmark (yv=1e-6, MR=1000 GeV,
chosen in feynlag-models/models/seesaw_type1/metadata.yaml so that m_nu ~ 0.03 eV) -- this is
feynlag-models' own already-verified benchmark data, not a value invented in this repo.
"""


def test_bundle_builds(seesaw_bundle):
    assert seesaw_bundle.id == "seesaw_type1"
    assert {"MN1", "MN2", "mDsym", "Mnu"} <= seesaw_bundle.extra.keys()


def test_bundle_has_two_majorana_mass_eigenstates(seesaw_bundle):
    assert len(seesaw_bundle.extra["masses"]) == 2


def test_light_mass_matches_benchmark_order_of_magnitude(seesaw_bundle):
    values = seesaw_bundle.values()
    mn1 = values[seesaw_bundle.extra["MN1"].s]
    # ~0.03 eV = 3e-11 GeV; a generous order-of-magnitude window, not a precision pin (that
    # belongs to feynlag-models' own L2 tests, not this repo).
    assert 1e-12 < mn1 < 1e-9
