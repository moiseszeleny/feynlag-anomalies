# Decisions — `neutrino_mass`

One dated line per ladder step (kickoff spec §5), tagged `[feynlag-verified: test]` (backed by
a passing test in this repo or in `feynlag`/`feynlag-models`), `[physics judgment]` (a reasoned
choice not itself pinned by a test), or `[decision, needs approval]` (something that changes scope
or touches a sibling repo and needs the user's sign-off before acting on it).

- **2026-09-22 — Step 0** (dimensional estimate): `m_nu ~ y^2 v^2 / M` implemented in
  `solutions/step_0.py::m_nu_estimate`. `[physics judgment]` — the standard seesaw-scale
  dimensional estimate, not itself a feynlag computation.
- **2026-09-22 — Step 1** (SM structural test): `feynlag.suggest.suggest_yukawa` on minimal SM
  lepton content (`Ll`, `eR`, no `ν_R`) at `max_dim=4` returns exactly one term (the
  charged-lepton Yukawa) — no dimension-≤4 neutrino-mass term exists. Protection identified:
  `field_content` (no ν_R) + `accidental_symmetry` (SM's accidental lepton number).
  `[feynlag-verified: test]` — `tests/test_sm_structural.py::test_no_dim4_neutrino_mass_term`,
  mirroring feynlag's own `tests/test_suggest.py::test_sm_lepton_yukawa` precedent.
- **2026-09-22 — Step 2** (EFT operator): same call at `max_dim=5` surfaces exactly one
  additional term, labeled `Weinberg`, confirming the dimension-5 Weinberg operator
  `(LH)(LH)/Λ` is the minimal SM-lepton EFT operator generating a Majorana neutrino mass.
  `[feynlag-verified: test]` — `tests/test_weinberg_dim5.py::test_weinberg_operator_appears_at_dim5`,
  mirroring `feynlag`'s own `tests/test_majorana.py::test_suggest_weinberg_dim5`.
- **2026-09-22 — Step 3** (UV completion, choice of minimal model): type-I seesaw chosen over
  type-II/III per de Blas–Criado–Pérez-Victoria–Santiago (arXiv:1711.10391) — fewest new fields,
  smallest representation (a gauge singlet), fewest parameters, no ad hoc symmetries. Imported as
  `feynlag_models.registry.build("seesaw_type1")`. `[physics judgment]`, the minimality argument
  itself is not re-derived here (it is feynlag-models' own stated rationale for this model, see
  its `README.md`); the import is `[feynlag-verified: test]` —
  `tests/test_seesaw_bundle.py::test_bundle_builds`.
- **2026-09-22 — Step 4** (predict before running): read off `bundle.extra["MN1"]` (light),
  `["MN2"]` (heavy), `["mDsym"]` (Dirac mass) and confirm the benchmark
  (`yv=1e-6`, `M_R=1000 GeV` → `m_ν ≈ 0.03 eV`, per `feynlag-models/models/seesaw_type1/
  metadata.yaml`'s own benchmark description) reproduces via `bundle.values()`.
  **Caveat, `[physics judgment]`**: `seesaw_type1` is single-generation, so "how many light
  massive neutrinos result from one ν_R" is only trivially answerable (one) from this bundle; the
  general 3-flavour rank-counting argument (why 2 heavy states are needed once 2 Δm² are
  measured) is posed as the reader's own derivation feeding directly into step 5, not literally
  instantiated by this model.
- **2026-09-22 — Step 5** (breaking it on purpose / minimal extension request): two
  independently measured Δm² require rank ≥2 in the light-neutrino mass matrix, hence ≥2 ν_R.
  Filed `model_requests/seesaw_type1_nN.md` requesting the n-generation variant.
  `[decision, needs approval]` — no change made to `feynlag-models`; the request is filed for the
  user's review per `CLAUDE.md` hard rule 4.
- **2026-09-22 — Step 6** (stage-1 χ² against oscillation data): **SKIPPED — blocked.** A
  genuine χ² fit needs two independent light masses from the model, which `seesaw_type1` as it
  exists cannot provide (rank-1 light sector). Forcing a degenerate one-observable χ² would
  overclaim what a real 2-flavour oscillation fit requires (resolved with the user before
  building, see the approved plan). `neutrino_mass` therefore stays at **maturity A2**, not A3,
  this session; step 6 unblocks once `model_requests/seesaw_type1_nN.md` is approved and built.
  `[decision, needs approval]`.
