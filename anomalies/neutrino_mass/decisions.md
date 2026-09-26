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
- **2026-09-25 — Step 2** (Λ estimate): now that the observables are sourced (NuFIT 6.0), the
  notebook's Λ ~ v²/m_ν estimate uses m_ν = √Δm²_31 from `anomaly.yaml` instead of only step 0's
  illustrative m_ν, giving Λ ~ 10^15 GeV. The stale "no verified Δm²" note was removed.
  `[physics judgment]`, a dimensional estimate with an O(1) Wilson coefficient.
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
- **2026-09-25 — Step 6** (stage-1 χ² against oscillation data): **done**, maturity A2 → A3.
  - Model: `seesaw_type1_2n` from feynlag-models (PR #9, L2), the build requested in step 5. The
    request used the id `seesaw_type1_2N`; the schema requires lowercase. Imported through
    `feynlag_models.registry.build`. `[feynlag-verified: test]` —
    `tests/test_step6_fit.py::test_fit_model_is_at_least_L2`.
  - Data: NuFIT 6.0 (arXiv:2410.05380v2), Table 1, normal ordering, variant "IC24 with SK
    atmospheric data", the paper's comprehensive analysis and the one where normal ordering is
    the best fit. Values read from the arXiv text with `pdftotext` on 2026-09-25. `[physics
    judgment]` for the choice of variant.
  - Two stage-1 simplifications, both recorded in `anomaly.yaml`. NuFIT's asymmetric 1σ errors
    are replaced by the mean of the upper and lower error. NuFIT quotes total errors only, so they
    sit in `stat_uncertainty` with `sys_uncertainty: null`. Correlations between parameters are
    ignored (diagonal χ²). `[physics judgment]`
  - Fit: the six Dirac Yukawas are free, with M₁ = 1 TeV and M₂ = 3 TeV fixed at the model
    benchmark (only y²/M enters the light sector). The observables are Δm²₂₁, Δm²₃₁, θ₁₂, θ₁₃,
    θ₂₃. Each point is evaluated with feynlag's numeric Takagi on the model's own 5×5 matrix, and
    the fit is minimised with `fit.stage1.minimize_chi2`, starting from the model benchmark
    rather than from a data-derived point. The prediction function reproduces the
    Ibarra–Ross Eq. (6) (two-ν_R Casas–Ibarra) inputs exactly. `[feynlag-verified: test]` —
    `tests/test_step6_fit.py::test_predictor_inverts_ibarra_ross_eq_6`.
  - Result: χ²_min ≈ 3×10⁻¹⁴ with every pull below 2×10⁻⁷. With six parameters and five
    observables, ndof = −1, so this shows the model **can** accommodate the data, not that the
    data prefer it. The SM's massless neutrinos give χ² ≈ 1.7×10⁴ over the two splittings alone.
    The structural prediction is m₁ = 0 exactly, so Σm_ν = √Δm²₂₁ + √Δm²₃₁ ≈ 0.059 eV (computed).
    `[feynlag-verified: test]` — `tests/test_step6_fit.py::test_fit_accommodates_nufit`,
    `::test_lightest_neutrino_is_massless`, `::test_sm_is_excluded_by_the_splittings`.
  - δCP is recorded but not fitted: the model's Yukawas are real, so it is CP-conserving by
    construction. Complex Yukawas need a complex Takagi, which feynlag's numeric route does not
    yet do. The confrontation with Σm_ν from cosmology and with 0νββ is not done, and
    `tensions_with_other_data` stays `TODO_VERIFY`. `[physics judgment]`
- **2026-09-25 — Pedagogical pass on `ladder.ipynb`** (no change to any fitted result):
  - Step 5's checkpoint now asks for a computed quantity: the rank of the 3×3 seesaw light matrix
    `-m_D M_R⁻¹ m_Dᵀ` for one ν_R, via `feynlag.seesaw_light_mass` on generic symbolic matrices
    (`solutions/step_5.py::light_rank`). It gives rank 1 for one ν_R and rank 2 for two. The old
    checkpoint only tested that the model-request file existed. `[feynlag-verified: test]` —
    `tests/test_checkpoints_pass.py::test_light_rank_counts_right_handed_neutrinos`.
  - Step 2 takes the Weinberg operator to the vacuum (`G⁺ → 0`, `H⁰ → v/√2`, per
    feynlag-models `CONVENTIONS.md`); only the ν_Lν_L Majorana term survives, ∝ v²/2. Step 4
    links back: M_R/y² = 10¹⁵ GeV at the seesaw_type1 benchmark, the same order as step 2's Λ
    for C = 1. The exact-vs-seesaw light-mass difference (3.1×10⁻¹⁴) matches (m_D/M_R)² (3.0×10⁻¹⁴).
  - Step 6 shows the Casas–Ibarra degeneracy: `run_fit` from `alt_start` (benchmark with signs
    flipped) gives different Yukawas with the same χ² and spectrum. `[feynlag-verified: test]` —
    `tests/test_step6_fit.py::test_fit_yukawas_are_degenerate`. Largest active–sterile mixing at
    the best fit ≈ 1.6×10⁻⁷ (computed).
  - Checkpoint calls are now `assert cd.check_N(...)`: `Checkpoint.__call__` returns a bool and
    never raised, so a wrong answer did not previously fail `pytest --nbmake`.
- **2026-09-26 — `ladder.ipynb` restyled** after feynlag's `examples/DiscreteGroups_Tutorial.ipynb`
  (numbered claim sections, prediction blockquotes, MOVE/peek cells with `ok`/`trace`, Recap).
  Style only: no fitted or checked value changed. New cells compute a hypercharge ledger (§1),
  walk the Weinberg operator into the vacuum term by term (§2.1), and display the symbolic
  one-ν_R light matrix (`solutions/step_5.py::light_mass_matrix`, §5). Every `ok` line is
  backed by an `assert` in the same cell.
