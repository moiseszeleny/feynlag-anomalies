# Decisions — `flavor_puzzle`

One dated line per ladder step, tagged as in `anomalies/neutrino_mass/decisions.md`:
`[feynlag-verified: test]`, `[physics judgment]` or `[decision, needs approval]`.

- **2026-10-04 — P0** (record): puzzle stated as the unexplained hierarchy of the nine
  charged-fermion Yukawa eigenvalues and the CKM parameters. Lepton mixing is cross-linked through
  `related_anomalies: [neutrino_mass]` and is not duplicated here. `[physics judgment]`
- **2026-10-04 — P0** (quantifier): `free_parameter_log10_span`, the $`\log_{10}`$ range of the
  dimensionless free parameters a theory needs. It was chosen because the same definition applies
  to the SM and to a flavor model, so P3 can report a before/after on one number. It is blind to
  how many parameters there are and to whether the $O(1)$ coefficients are tuned. Revisit at P1
  if that turns out to matter. `[physics judgment]`
- **2026-10-04 — P0** (common scale): Yukawas to be compared at $\overline{\rm MS}$ $`\mu = M_Z`$, a
  standard choice that sits below any flavor-model scale, so running up to it is part of P3, not
  P1. `[physics judgment]`
- **2026-10-04 — P1** (sources): running masses from Huang & Zhou, arXiv:2009.04851v2 (PRD 103,
  016010), Tables 2 and 3, row "M_Z, Full SM"; CKM from PDG 2024 CKM review Eq. (12.28). Both PDFs
  were read in this session. The masses, not Yukawas, are stored because they are what the
  source prints; $`v_F = 246`$ GeV is stored as the source's definition. `[physics judgment]`
- **2026-10-04 — P1** (input vintage): Huang & Zhou's inputs are PDG-2020 era (e.g.
  $`M_t = 172.4`$ GeV), older than the PDG 2024 CKM fit. The quantifier spans orders of magnitude
  and its inputs move by percent, so the mismatch is immaterial here. Refresh if an updated
  running appears. `[physics judgment]`
- **2026-10-04 — P1** (CKM scale): CKM angles are the low-energy fit, masses are at $`M_Z`$. PDG
  2024 §12.1 states the CKM elements can be treated as constants below $`m_W`$; the running from
  there to $`M_Z`$ is negligible at this precision. `[physics judgment]`, backed by the cited
  statement.
- **2026-10-04 — P1** (free-parameter set): the SM quantifier runs over the nine Yukawas and the
  three CKM sines; $\delta$ is excluded as a phase with no hierarchy content. The CKM sines never
  set the span ($`y_t`$ and $`y_e`$ do), so including them only matters for models whose
  coefficients are compared on the same footing. `[physics judgment]`
- **2026-10-04 — P1** (Yukawas from the model): Yukawas are evaluated from `sm_ckm`'s own
  `yukawa_params` ($`y_f = \sqrt2\, m_f / v`$) at a benchmark overriding masses, $v$ and CKM inputs
  with the sourced values; it matches the source's definition to $10^{-12}$.
  `[feynlag-verified: test]`,
  `tests/test_step1_yukawas.py::test_yukawas_match_published_definition`.
- **2026-10-04 — P1** (quantifier): SM value 5.542 orders of magnitude ($`\log_{10} y_t/y_e`$);
  sector spans up 5.14, lepton 3.55, down 3.03. `[feynlag-verified: test]`,
  `test_quantifier_sm_value_matches_yaml`.
- **2026-10-04 — P1** (regression): $\lambda$, $A$, $\bar\rho$, $\bar\eta$ from `sm_ckm`'s $V$ at
  the Eq. (12.28) angles all fall inside the PDG 2024 Eq. (12.26) $1\sigma$ bands (0.22501, 0.826,
  0.159, 0.352). `[feynlag-verified: test]`,
  `tests/test_step2_ckm.py::test_wolfenstein_regression_pdg2024`.
- **2026-10-04 — P2** (model request): `model_requests/froggatt_nielsen.md` filed with the
  user's approval (hard rule 4). It asks for the EFT version (flavon plus higher-dimension Yukawas,
  messengers integrated out), with parent `sm_ckm` and $`U(1)_{\rm FN}`$ charges as integer
  benchmark inputs, so that charge assignments are benchmarks rather than separate models. It
  requests L2: mass and mixing scaling checked against Froggatt–Nielsen (1979) and
  Leurer–Nir–Seiberg (1993), both verified on INSPIRE/arXiv this session. It flags two likely
  feynlag gaps: dimension $4 + n$ operators and a numeric complex $3\times3$ SVD.
  `[decision, approved]`
- **2026-10-05 — P2** (model built): `feynlag-models`' `froggatt_nielsen` reached L2 (PR #14):
  textures, the determinant charge sum and the mass and CKM scaling are checked against
  Leurer–Nir–Seiberg (hep-ph/9310320 Eqs. 2.2–2.7, 2.19). For P3 the bundle exposes
  `extra["Yu"]`, `extra["Yd"]`, `extra["Ye"]` (symbolic in `extra["eps"]` and the
  $`\lvert c_{ij}\rvert`$, $`\alpha_{ij}`$ parameters in `extra["c_params"]`), and
  `feynlag_models.flavor.ckm_from_yukawas` / `mass_spectrum` give $V$ and the masses at a numeric
  point without rebuilding. `candidate_models` now lists `model_id: froggatt_nielsen`.
- **2026-10-08 — P2** (pin bump): feynlag 0.3.0 and `feynlag-models` `cb0678a` (PR #16), which
  close FG-6 (numeric complex SVD) and FG-7 (the global $U(1)$ charge counter) upstream.
  `feynlag_models.flavor` is deleted, so the entry above is superseded on that point: $V$ and the
  masses at a numeric point now come from `models.froggatt_nielsen.model.mass_basis` / `ckm` /
  `benchmark_flavour`, which use feynlag's `diagonalize_svd(method="numeric")`. The bundle's
  `extra` keys are unchanged. `[feynlag-verified: test]` — full suite and both notebooks pass at
  the new pins.
- **Next (P3)**: once the model reaches L2, fit $`(\epsilon, c_{ij})`$ to the sourced masses and
  CKM with `fit/stage1.py`, then compute `free_parameter_log10_span` over
  $`\{\lvert c_{ij}\rvert\}`$ and compare with 5.54. Flavon FCNC constraints need stage-2 tools;
  stage 1 applies only coarse cuts.
