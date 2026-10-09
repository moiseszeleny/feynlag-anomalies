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
- **2026-10-08 — P3 prep** ($\epsilon$ in the fit): $\epsilon$ is a free fit parameter and is
  excluded from the span. It is the $`U(1)_{\rm FN}`$ order parameter that produces the hierarchy,
  not an $O(1)$ coefficient whose size the model has to explain.
  `[decision, approved by the user]`
- **2026-10-08 — P3 prep** (quarks only): P3 fits quarks only. The lepton FN charges are
  placeholders in the model, and at its benchmark they give $`m_e = 22`$ MeV (recomputed this
  session with `benchmark_flavour`: 22.09 MeV, pinned by
  `tests/test_fn_benchmark.py::test_fn_lepton_placeholder_gives_me_22_mev`). The SM comparison value is recomputed on the same
  footing: six quark Yukawas and three CKM sines give 5.136 orders of magnitude
  ($`\log_{10} y_t/y_u`$), stored as `quantifier.sm_reference_values.quarks_only` and pinned by
  `tests/test_step1_yukawas.py::test_quark_only_sm_value_matches_yaml`. The all-sector 5.542
  stays as `sm_value`. `[decision, approved by the user]`
- **2026-10-08 — P3 prep** (span rule): the model's span is the minimum of
  $`\log_{10}(\max\lvert c\rvert / \min\lvert c\rvert)`$ over the $c$'s, subject to
  $`\chi^2 \leq \chi^2_{\min} + \Delta`$, counting only the $c$'s that some observable
  constrains. The $c$'s are not unique at the best fit (more parameters than observables), so a
  span read off one best-fit point would be arbitrary. $\Delta$ and the constrained set are
  proposed in the P3 design. `[decision, approved by the user]`
- **2026-10-08 — P3 prep** (scale): the FN relation $`y_{ij} = c_{ij}\,\epsilon^{n_{ij}}`$ is
  imposed at $`\mu = M_Z`$, against the Huang–Zhou masses at $`M_Z`$. Running from $`M_Z`$ to
  $\Lambda$ is absorbed into the $c$'s, an effect of about 0.1 in the span, and is stated as a
  stage-1 approximation. `[decision, approved by the user]`
- **2026-10-08 — P3 prep** (familon constraint): the flavon phase $a$ is an exact Goldstone boson
  (global $`U(1)_{\rm FN}`$), with off-diagonal couplings $`n_{ij} M_{ij} / v_\phi`$ to the quarks,
  so $`K^+ \to \pi^+ a`$ bounds $`v_\phi`$. P3 must list it as a hard constraint on $`v_\phi`$. It
  does not enter the stage-1 $\chi^2$, because the Yukawa fit depends only on $\epsilon$ (checked:
  the model's $\epsilon = v_\phi/(\sqrt2\,\Lambda)$, and $`v_\phi`$, $\Lambda$ enter the Yukawas
  only through it). Experimental input, read in the primary source this session: NA62,
  arXiv:2103.15389 (JHEP 06 (2021) 093), $`{\rm BR}(K^+ \to \pi^+ X) < (3\text{–}6)\times10^{-11}`$
  at 90% CL for a stable or invisible $X$ with $`m_X = 0`$–110 MeV (Sec. 8 and conclusions; the
  $`m_X = 0`$ point is only in Fig. 8, so the conservative $6\times10^{-11}$ is the quotable value).
  The bound on $`v_\phi`$ is `TODO_VERIFY`: it needs a cited $`\Gamma(K \to \pi a)`$ formula and the
  model's $`a\,\bar s d`$ coupling, and no number is taken from memory. The 2026 NA62 proceedings
  (arXiv:2604.12649) update only $`K^+ \to \pi^+ \nu\bar\nu`$, not $`K^+ \to \pi^+ X`$. The model's
  benchmark $`v_\phi = 2.83`$ TeV must not be quoted as viable. `[decision, approved by the user]`
- **2026-10-08 — P3 prep** (vev convention): `froggatt_nielsen` is built with $`v = v_F = 246`$
  GeV, overriding the model default of 246.22 GeV, as `sm_benchmark` already does for `sm_ckm`.
  The masses are Huang–Zhou's $`m_f = y_f v_F/\sqrt2`$. `[decision, approved by the user]`
- **2026-10-08 — P3 design** (tuning guard): the minimum span is computed without a box. At the
  minimum-span point the tuning measure
  $`\max \lvert \partial \ln O / \partial \ln\lvert c\rvert \rvert`$ over the ten observables and 18
  quark $`\lvert c\rvert`$ is reported, and flagged if it exceeds 10. The span with every
  $`\lvert c\rvert`$ boxed in $[1/3, 3]$ is reported as a sensitivity variant. Reason: a free
  minimum could lower the span through tuned cancellations among $O(1)$ coefficients; the measure
  detects that, and the box shows how much the answer depends on allowing it.
  `[decision, approved by the user]`
- **2026-10-08 — P3 design** ($\Delta\chi^2$): $\Delta = 1$ is the headline, the 68% profile
  interval of one derived quantity (the span); $\Delta = 4$ is reported as a sensitivity check.
  `[decision, approved by the user]`
- **2026-10-08 — P3 fit** (`solutions/step_3.py`, result; P3 not yet claimed): `froggatt_nielsen`
  built with $v = v_F$, fitted to the 10 quark observables with 18 $`\ln\lvert c\rvert`$ and 10
  free phases at $\epsilon = 0.2$ (the 8 other phases fixed by rephasing). The fit loop uses numpy
  SVD on the bundle's lambdified Yukawas, which agrees with the model's `mass_basis` / `ckm` at
  dps 60 to $10^{-13}$; every reported point is recomputed with the model. The exact flat
  direction $`\epsilon \to \epsilon/k`$, $`\lvert c_{ij}\rvert \to \lvert c_{ij}\rvert k^{n_{ij}}`$
  ($`n_{ij} = a_i + b_j`$ in both sectors) means the data cannot fix $\epsilon$; only the span
  minimisation picks it. Full run, 32 starts (about 17 min):
  - $`\chi^2_{\min} = 1.3\times10^{-23}`$ (28 parameters, 10 observables: the model accommodates
    the data, which is not a preference).
  - Constrained-minimum span: **0.189** orders of magnitude at $\Delta = 1$ (at
    $\epsilon = 0.136$), 0.182 at $\Delta = 4$, against 5.136 for the SM's quarks. At least four
    starts reach the same minimum to $10^{-4}$.
  - Boxed in $`\lvert c\rvert \in [1/3, 3]`$: 0.189 / 0.182 in the full run, equal to the free
    minimum, which already lies inside the box. The default 4-seed run gives 0.1898 / 0.1825
    boxed against 0.1894 / 0.1820 free, within $5\times10^{-4}$ (the notebook table rounds
    0.1898 to 0.190).
  - Tuning measure at the minimum-span point: 0.98 (full run) and 1.06 (the default 4-seed
    point, reproduced on 2026-10-09 with `run_p3(DEFAULT_SEEDS)`: 1.0639), far below the flag
    at 10. The minimum-span point is not unique, so the measure is quoted per point and can
    differ by platform.
  - All 18 quark $`\lvert c\rvert`$ enter some observable (the determinant argument).
  `[feynlag-verified: test]` — `tests/test_step3_fn_fit.py` (default: 4 pinned seeds;
  `test_full_multistart_is_stable` is `slow`). Open before P3 is claimed: an Opus physics review,
  and the familon bound on $`v_\phi`$ (`TODO_VERIFY`).
- **2026-10-09 — P3 review fold-in** (Opus review of PR #14: no physics error, headline numbers
  reproduced, 0.189 confirmed as the constrained minimum). Three low findings:
  - *SM footing.* 5.136 is the SM span at central values, while the FN span is a minimum under
    $`\chi^2 \leq \chi^2_{\min} + 1`$. Under the same rule the quark-only SM span is **5.068**
    (`step_3.sm_quark_span_profiled`: $`m_u`$ up by $1.00\,\sigma$, $`m_t`$ down by
    $0.03\,\sigma$, the rest unmoved; an analytic scan of the $1\sigma$ circle gives the same
    5.0676). Stored as
    `quantifier.sm_reference_values.quarks_only_profiled_delta1` and pinned by
    `tests/test_step3_fn_fit.py::test_sm_quark_span_profiled_matches_yaml`. The gap is 4.947
    orders of magnitude at central values and **4.878** like-for-like. At $\Delta = 4$ the SM
    value is 5.008 against the FN 0.182. `[feynlag-verified: test]`
  - *Conditional headline.* The 0.189 holds for the LNS charge assignment, with $\epsilon$ and
    the integer charges excluded from the span by the user decision of 2026-10-08. As context,
    counting $\epsilon$ as one more $c$ would give at most
    $`\log_{10}(0.958/0.136) = 0.85`$ at the reported point (max $`\lvert c\rvert = 0.958`$,
    $\epsilon = 0.136$, recomputed this session). `[physics judgment]`
  - *Tuning value.* The review quoted 0.9814 for `run_p3(DEFAULT_SEEDS)`; rerun here it gives
    1.0639, and 0.9814 is the full 32-start value already reported above. Both are kept, each
    for its own point, and the notebook outputs were refreshed (they show 1.06). Not changed to
    0.98. `[feynlag-verified: test]`
- **Next (P3)**: an Opus physics review of the fit and of the notebook's section 5. Then the
  familon bound on $`v_\phi`$ from a cited $`\Gamma(K \to \pi a)`$ formula. P3 maturity is
  claimed in `puzzle.yaml` only after both.
