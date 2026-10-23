# Decisions — `higgs_95gev`

- **2026-09-22**: A0 stub created. No literature search performed this session (out of scope for
  the repo-bootstrap session). `[decision, needs approval]` — next session should run a primary
  literature pass (CMS/ATLAS diphoton and ditau channels, LEP bb̄) before advancing past A0.
- **2026-10-15 — A0 literature pass.** Every number in `anomaly.yaml` was read from a paper, not
  from a review article. Full text was read for arXiv:2405.18149, 2407.07546, 2208.02717 and
  hep-ex/0306033. arXiv:2407.10948 (Janot) was read in its abstract and selected passages, not in
  full. arXiv:1811.08459 was not read: the 2.8σ is quoted from arXiv:2405.18149 and 2208.02717, and
  1811.08459 is not in `sources[]`. `[cited]`
  - *CMS diphoton*, arXiv:2405.18149: local (global) 2.9σ (1.3σ) at 95.4 GeV. The 2016 data alone
    give 3.3σ, up from 2.8σ in the earlier analysis (arXiv:1811.08459, quoted here, not read). Recorded under `significance:`.
  - *ATLAS diphoton*, arXiv:2407.07546: no significant excess. Largest model-dependent deviation
    is 1.7σ local at 95.4 GeV. Recorded in `experiments[]` and as a tension.
  - *CMS ditau*, arXiv:2208.02717: 2.6σ (2.3σ) at 95 GeV and 3.1σ (2.7σ) at 100 GeV, local
    (global). The only channel with an entry in `observables[]`: $`\sigma B`$ at 95 GeV, 7.8 pb
    with errors +3.9/−3.1. CMS prints a total error, so the 3.5 in `stat_uncertainty` is its mean,
    a stage-1 symmetrisation, not a statistical error. The schema field name is kept.
  - *LEP bb̄*, arXiv:hep-ex/0306033: $`1-{\rm CL}_b \approx 0.02`$, i.e. 2.3σ, near 98 GeV. The paper
    itself says the signal behind it is about an order of magnitude below the SM Higgs rate.
    Janot, arXiv:2407.10948, argues the LEP data disfavour a 95 GeV scalar as its cause. That is
    one author's reanalysis. It is not a collaboration result. `[physics judgment]`
  - *No later result found.* A web search on 2026-10-15 found no Run 3 or 2026 collaboration
    result on this excess. Absence from a search is not proof, so this is not claimed as a fact
    about the experiments. `[decision]`
- **2026-10-15 — what stays open.**
  - *Signal strengths $`\mu`$ for the diphoton and bb̄ channels.* The diphoton value was found on
    2026-10-16 in a CMS collaboration source (below). The bb̄ value was not found in a primary
    source. `[decision, needs approval]`
    - CMS (arXiv:2405.18149) and ATLAS (arXiv:2407.07546) print p-values and 95% CL upper limits in
      the paper text, not a best-fit $`\mu`$. The CMS maximum observed limit is 73 fb at 95.4 GeV.
      `[cited]` The CMS results are tabulated in HEPData (doi:10.17182/hepdata.150508). It blocked
      automated access (HTTP 403), so the user downloaded Figures 5a, 5b and 6a to 6d, kept locally
      in the untracked `anomalies/higgs_95gev/data/`. They hold observed and expected 95% CL limits
      only: at 95.4 GeV, 0.0734 pb observed vs 0.0279 pb expected (0.593 vs 0.224 normalised to the
      SM-like Higgs cross section). The 73.4 fb, the maximum of the observed curve, is reached at 95.3 to 95.4 GeV in the table
      and matches the paper's 73 fb at 95.4 GeV. `[cited]` The DOI is printed as Ref. [49] of
      arXiv:2405.18149. The INSPIRE id `ins2791038` comes from the doi.org redirect to the HEPData
      record page and from the downloaded filenames, since the files carry no metadata. No best-fit
      $`\mu`$ is in them. A fit table, if CMS tabulated one (for example the local p-value figure),
      was not among the downloads.
    - The LEP paper (hep-ex/0306033) gives no $`\mu`$. The value $`0.117 \pm 0.057`$ appears only
      in Janot (arXiv:2407.10948), as inferred from a phenomenology paper, and Janot argues it is
      internally inconsistent. It is second-hand, so it is not recorded.
    - *CMS diphoton $`\mu`$, found on 2026-10-16.* The CMS public page for CMS-HIG-20-002
      carries supplementary figures. Additional Figures 14 and 15 (downloaded by the user as
      `CMS-HIG-20-002_Figure-aux_014.pdf` and `_015.pdf`, kept in the untracked
      `anomalies/higgs_95gev/data/cms_additional_figures/`) print
      $`\hat\mu_{\rm combined} = 0.33\,^{+0.19}_{-0.12}`$ at $`m_H = 95.4`$ GeV with 132 fb⁻¹, with the
      line $`\mu = \mu_{\rm SM}`$ drawn. The number is in the figure, not in the page text. I read it
      from the rendered plot and from the PDF text, and a reviewer checked it against both. It
      matches a value quoted earlier by a phenomenology paper, which I had not recorded because I
      had not seen it in a CMS document. `[cited]`
    - *Normalisation.* The paper defines its limits "relative to the expected value for an SM-like
      Higgs boson" (arXiv:2405.18149). That $`\hat\mu = 1`$ means an SM-like Higgs boson of the same
      mass is an inference from the figure's $`\mu = \mu_{\rm SM}`$ line. No caption states it.
    - *Caption text, which the PDFs do not carry.* The figure PDFs have no captions. The captions
      are on the CMS page (`cms-results.web.cern.ch/cms-results/public-results/publications/HIG-20-002/`),
      whose raw HTML I downloaded and searched on 2026-10-16. `[cited]`
      - Additional Figure 14: "The χ² probability of the values for the eleven event classes being
        compatible with the overall best-fit signal strength is 68%." The plot has eleven rows.
      - Additional Figure 15: the same sentence for the three years, with probability 6%, so the
        per-year values (2016: 0.77 +0.27/−0.24, 2017: 0.01 ±0.22, 2018: 0.35 +0.18/−0.17, read from
        the figure) are not comfortably consistent.
      - Additional Figure 32: "The best-fit result is ($`\mu_{ggH}`$, $`\mu_{VBF}`$) = (0.47, 0.05)" at
        $`m_H = 95.4`$ GeV, for ggH and VBF production only. The 68% and 95% contours are only in the
        image. This is a two-parameter fit point, not the overall $`\mu`$, and is context only.
    - *Uncertainty.* CMS prints $`+0.19/-0.12`$, a total fit error. The 0.155 in `stat_uncertainty` is
      its mean, a stage-1 symmetrisation, not a statistical error. The schema field name is kept.
    - The LEP bb̄ row stays at `TODO_VERIFY`, which A0 allows, so the gap is explicit. The diphoton
      significances sit in `significance:`, which holds one channel.
  - The ditau $`\sigma B`$ is given in pb for a generic $`\phi`$, not as a ratio to an SM-like
    Higgs cross section, so it cannot be compared with the diphoton channel yet. A comparison needs
    a cross-section ratio at 95 GeV, which is A1 work.
  - `sm_prediction` is the background-only expectation of the cited searches (0.0 for the new
    signal), because the SM has no scalar near 95 GeV. It is a convention, not a number a paper
    states, and `provenance` is a closed vocabulary, so it stays `cited`. No SM argument was
    written. That is A1.
  - Status is `hint`: three channels at 2 to 3σ, none significant alone, ATLAS weaker, and a
    disfavouring LEP reanalysis. `[physics judgment]`
  - Not read and therefore not cited: combined ATLAS+CMS significances quoted in phenomenology
    papers. They are not collaboration numbers.
- **Maturity stays A0.** `sm_protection`, `eft_operators` and `candidate_models` are untouched.
- **2026-10-16 — A1: the SM argument and the ditau signal strength.**
  - *Step 1, SM structural test.* `solutions/step_1.py` builds feynlag-models' `sm` (L3) through
    `feynlag_models.registry.build` and reads its scalar mass matrices after EWSB. The neutral
    block in the $`(h, G^0)`$ basis is $`{\rm diag}(2\lambda v^2, 0)`$ and the charged block
    $`(G^+)`$ is zero. Four real doublet fields minus three Goldstones leaves one physical neutral
    scalar, with $`m_h^2 = 2\lambda v^2`$, the model's key result
    `test_tadpole_and_higgs_mass`. At the model benchmark the only scalar mass is its input
    $`M_H = 125.0`$ GeV, outside 90 to 100 GeV. Tests:
    `tests/test_sm_structural.py::test_single_physical_scalar`,
    `::test_higgs_mass_is_two_lambda_v_squared` and `::test_no_sm_scalar_near_95gev`. `[computed]`
  - *The SM prediction.* `sm_prediction` keeps the value 0.0 (no resonant signal) and is now
    `provenance: computed`, with the step-1 tests as `reference`. The zero follows from the count,
    not from a parameter choice, so `sm_protection` is `field_content`: a second scalar needs a
    new field. `[computed]`
  - *The Z boson is in the window.* $`m_Z`$ = 91.19 GeV at the model benchmark lies in 90 to 100 GeV.
    It is spin 1, so Landau–Yang forbids $`Z \to \gamma\gamma`$, and it is part of the SM
    background in the ditau and $`b\bar b`$ searches. The window test counts scalars only, and
    the notebook says why. `[physics judgment]`
  - *Step 2 inputs.* Both read on 2026-10-16 from LHC Higgs WG primary tables, not from memory or
    a phenomenology paper. `[cited]`
    - $`\sigma_{\rm ggF}`$ at 95 GeV, 13 TeV: 68.25 pb, scale $`+8.6/-8.9`$ %, PDF+$`\alpha_s`$
      ±3.3 %. Source: the twiki `CERNYellowReportPageBSMAt13TeV` (CERN Report 4 update), table
      "Quark-loop induced interaction" (a scalar coupling to gluons through top and bottom loops
      like the SM Higgs), NNLO+NNLL QCD, PDF4LHC15_nnlo_30. The EW correction column is 0 below
      100 GeV (not provided). The same row is in `Higgs_XSBR_YR4_update.xlsx`, sheet
      `YR4 BSM 13TeV`, as 68.25, +8.59/−8.91, 3.25; the twiki's rounded values are recorded.
    - *Why this table.* The same page has a "point-like effective interaction" table, N3LO but in
      the heavy-top limit without a bottom loop, which gives 76.30 pb at 95 GeV. The quark-loop
      table is the one defined as SM-like, so it is the normalisation. `[decision]`
    - $`B(H \to \tau\tau)`$ at 95 GeV: $`8.32 \times 10^{-2}`$, $`+6.94/-6.77`$ %. Source: the
      twiki `CERNYellowReportPageBR2014` (CERN Report 3, 2013 update), "Higgs → 2 fermions"
      table at $`M_H`$ = 95.0 GeV. The CERN Report 4 BR table covers 120 to 130 GeV only.
    - *Cross-check.* The Report 4 xlsx sheet `YR4 BSM Width` lists partial widths at 95 GeV
      without NLO EW corrections and without $`s\bar s`$. Their ratio gives
      $`B(\tau\tau)`$ = 0.0824 and a summed width of $`2.38 \times 10^{-3}`$ GeV, against 0.0832
      and $`2.32 \times 10^{-3}`$ GeV in Report 3. The 1 % difference is well inside the 6.9 % BR
      error. `[computed]`
  - *Storage.* The inputs sit in a new optional field, `sm_prediction.sm_reference_values`
    (schema test `tests/test_schema.py::test_sm_prediction_reference_values`), which mirrors
    `Quantifier.sm_reference_values`. Code reads them from the loaded `Anomaly` and rejects
    `TODO_VERIFY` (`tests/test_step2_mu_tautau.py::test_sentinel_rejected`). `[decision]`
  - *Result.* $`\mu_{\tau\tau} = 7.8 / (68.25 \times 0.0832) = 1.37 \pm 0.62\,({\rm exp}) \pm 0.16\,({\rm theory})`$,
    a new `observables[]` row pinned to `solutions/step_2.py::mu_tautau` by
    `tests/test_step2_mu_tautau.py`. `[computed]`
  - *Errors.* The experimental error is the stage-1 symmetrised 3.5 pb, propagated linearly. The
    theory error adds three relative errors in quadrature: the symmetrised ggF scale error, the
    PDF+$`\alpha_s`$ error and the symmetrised BR error. It is stored in `sys_uncertainty` and
    kept apart from the experimental error, not combined, so that a fit can treat it as a
    correlated normalisation nuisance. The two reports are treated as uncorrelated, which is an
    approximation. `[decision]`
  - *What is not claimed.* The notebook shows $`\mu_{\gamma\gamma}`$ and $`\mu_{\tau\tau}`$
    side by side, with no $`\chi^2`$ (that is A3), and does not say they agree. Ditau is
    $`gg \to \phi`$ only, while the diphoton $`\mu`$ covers all production modes. The ditau
    excess peaks at 100 GeV, not 95 GeV. The cross section and the BR come from two different
    reports. `[decision]`
  - *Still open.* The LEP $`b\bar b`$ signal strength stays `TODO_VERIFY`. `eft_operators` and
    `candidate_models` are A2 work: `sm_singlet_z2` and `thdm_type2`, both L3. `[decision]`
  - **Maturity A1.** An executable structural test via feynlag-models and `sm_protection` are
    in place (`docs/maturity.md`).
- **2026-10-20 — review of PR #18, folded in.** These changes supersede the 2026-10-16 entry
  where the two differ.
  - *Measured Higgs mass.* The "none in 90 to 100 GeV" claim used to rest on the model benchmark
    $`M_H = 125.0`$ GeV, a round input. It now also uses the measured mass, PDG 2024
    $`m_H = 125.20 \pm 0.11`$ GeV ("OUR AVERAGE", read from the Higgs boson listing and the
    summary table on 2026-10-20), stored as `sm_reference_values.m_H_measured_*`. The test
    checks that the benchmark agrees with it to within 1 GeV and that it lies far above the window.
    `[cited]`
  - *Missing NLO EW.* The ggF quark-loop table gives $`1+\delta_{\rm EW}`$ only from 100 GeV up,
    1.0418 at 100 GeV. It is not applied at 95 GeV. Its size, 4.2 %, is added in quadrature to the
    theory error as a symmetric missing-EW term. The theory error grows from 0.16 to 0.17 and
    $`\mu_{\tau\tau}`$ = 1.37 is unchanged. Applying the factor instead would give about 1.32.
    `[decision]`
  - *No double counting.* The derived $`\mu_{\tau\tau}`$ row and the ditau $`\sigma B`$ row are
    the same measurement. `solutions/step_2.py::EXCLUSIVE_WITH` records the pair, and a test
    checks it. The A3 fit must select rows by name and take at most one of the pair. `[decision]`
  - *References checked.* Landau, Dokl. Akad. Nauk SSSR 60 (1948) 207, and Yang, Phys. Rev. 77
    (1950) 242, were checked on INSPIRE on 2026-10-20. `[cited]`
  - *Schema docstring.* `SMPrediction.sm_reference_values` no longer claims a source check. The
    sources are in `sources[]` and the yaml comment names them, but no loader check links a key
    to a source.
- **2026-10-22 — A2: lowest operators and two candidate models.**
  - *Fields from the model.* Step 3 takes $H$ and $S$ from the `sm_singlet_z2` bundle
    (`registry.build`), so no field is declared here. feynlag's `suggest_potential` gives, up to
    dimension 4, the portals $`S H^\dagger H`$ (dim 3) and $`S^2 H^\dagger H`$ (dim 4). With the
    model's $`Z_2`$ only $`S^2 H^\dagger H`$ is left, and with $`S = v_S + s`$ it gives the
    trilinear $`2 v_S\, s\, H^\dagger H`$. `suggest_yukawa` gives no $`S \bar\psi \psi`$ term.
    `[computed]`
  - *Dimension-5 operators.* The $`S G G`$ and $`S F F`$ operators are copied from
    arXiv:1512.04933v3 (Eq. (10); the photon operator from $`S B B`$ and $`S W W`$ in
    Eqs. (13)–(14); loops of heavy states in Eqs. (20)–(21)), read on 2026-10-22. The minimal singlet model has neither; it reaches photons and gluons only through
    its mixing with $h$. `[cited]`
  - *Which singlet state is at 95 GeV.* `sm_singlet_z2` labels its states by mixing, not by
    mass. Its $`\theta`$ is the principal branch of $`\tan 2\theta`$, so $`h_1`$ is always the
    $h$-like state. With the singlet lighter, the 95 GeV state is $`h_2`$, not $`h_1`$ as the A2
    plan said. The model's labels are self-consistent: the $`h_2`$ eigenvector is 96 % singlet at
    $`\sin\theta = 0.2`$ (`test_singlet_h2_is_the_singlet_like_state`). Only its closed-form
    key result $`m^2_{1,2} = \ldots \mp \sqrt{\ldots}`$ assumes $`M_{11} < M_{22}`$; that is
    noted in UG-4. `[computed]`
  - *The singlet benchmark.* The input `MH` fixes the $`(h,h)`$ entry $`2\lambda v^2`$, not an
    eigenvalue. The override is solved from
    $`M = R^T {\rm diag}(m_{125}^2, m_{95}^2) R`$ with the measured $`m_H`$ = 125.20 GeV, which
    gives `MH` = 124.13 GeV. $`\sin\theta = 0.2`$ is illustrative, not fitted. `[decision]`
  - *Universal signal strength.* Every $`h_2`$ coupling is $`-\sin\theta`$ times the SM one,
    because the model substitutes $`h = \cos\theta\, h_1 - \sin\theta\, h_2`$ into every SM
    coupling of $h$. The model's key result `test_coupling_rescaling` pins this for $`h_2 WW`$
    and $`h_2 f\bar f`$ ($t$, $b$, $\tau$). The $`h_2 ZZ`$ coupling is pinned here
    (`test_h2_zz_scales_with_sin_theta`). So $`\mu_{\gamma\gamma} = \mu_{\tau\tau} =
    \mu_{b\bar b} = \sin^2\theta`$. The notebook shows this next to the recorded values, with no
    verdict; that comparison is A3. `[computed]`
  - *Why a CP-even state in the 2HDM, not the CP-odd one.* LEP's $`e^+e^- \to Z\phi`$ needs a
    $`\phi Z Z`$ coupling, and $A$ has none. `[physics judgment]`
  - *The 2HDM labels (UG-4).* The model's $`\alpha`$ is the principal branch, which agrees
    with Gunion–Haber's $`m_H \ge m_h`$ only when $`M_{11} > M_{22}`$. At the inverted point
    ($`\tan\beta = 2`$, $`\sin(\beta-\alpha) = 0.3`$ for the 95 GeV state,
    $`m_A = 300`$ GeV, $`m_{H^\pm} = 600`$ GeV, $`m_{12}^2 = 6000`$ GeV²),
    $`\alpha_{\rm GH} = 0.80 > \pi/4`$, and the model returns its $H$ at 95 GeV and its $h$ at
    125 GeV. A strict xfail (`test_thdm_inverted_hierarchy_labels`) holds the evidence. The
    swap happens when $`\alpha_{\rm GH} > \pi/4`$, which for an exactly aligned 125 GeV state
    means every $`\tan\beta > 1`$. No workaround is used here. `[computed]`
  - *A usable 2HDM point.* At $`\tan\beta = 1.5`$ with the same $`\sin(\beta-\alpha) = 0.3`$,
    $`\alpha_{\rm GH} < \pi/4`$ and the model keeps its labels. The point
    `step_4.THDM_ALIGNED_POINT` ($`m_A = 100`$ GeV, $`m_{H^\pm} = 580`$ GeV,
    $`m_{12}^2 = 8500`$ GeV²) is the minimum of $`\max\lvert\lambda_i\rvert`$ over the scan
    below at that $`(\tan\beta, \sin(\beta-\alpha))`$. It is illustrative, not fitted. The bundle
    re-derives $`m_h = 95`$, $`m_H = 125.20`$, $`m_A`$, $`m_{H^\pm}`$ and
    $`\sin(\beta-\alpha)`$ under its own labels (`test_thdm_aligned_point_keeps_its_labels`).
    `thdm_type2` therefore has a usable point; UG-4 stays open for the inverted-label regime.
    `[computed]`
  - *Couplings near $`4\pi`$ (A3 caveat).* With $`m_{H^\pm} > 580`$ GeV (Misiak–Steinhauser, as
    cited in feynlag-models' `thdm_type2/NEXT_STEPS.md`), `step_4.thdm_coupling_scan` inverts
    the spectrum on a grid at $`m_{H^\pm}`$ = 580 GeV. The grid is
    $`\tan\beta \in \{1, 1.5, 2, 3, 5\}`$, $`\sin(\beta-\alpha) \in \{0.1, 0.3, 0.5\}`$,
    $`m_A`$ from 100 to 800 GeV in steps of 10 and $`m_{12}^2`$ from −20000 to 60000 GeV² in steps
    of 500. It finds no bounded-from-below point with $`\max\lvert\lambda_i\rvert`$ below 10.8
    (`test_thdm_coupling_scan`; an independent review scan found 10.85). The usable point needs
    10.9 and the UG-4 point 11.8, both close to $`4\pi \approx 12.6`$. Recorded for A3, not
    judged here. `[computed]`
  - **Maturity A2.** The lowest-dimension operator is identified, and `sm_singlet_z2` and
    `thdm_type2` are candidates by `model_id`, each with a computed spectrum (`docs/maturity.md`). No $`\chi^2`$, and
    the LEP $`b\bar b`$ row stays `TODO_VERIFY`.
- **2026-10-22 — review of PR #19, folded in.** The entry above already carries these changes.
  - The UG-4 text had lost every `\r` of its LaTeX (`\rho`, `\rm`) to line breaks. It is
    retyped and now cites `CONVENTIONS.md:82`.
  - The $`S B B`$ / $`S W W`$ split ($`1/\Lambda_\gamma = 1/\Lambda_B + 1/\Lambda_W`$) is cited to
    Eqs. (13)–(14) of arXiv:1512.04933v3, not Eq. (10).
  - The coupling scan is now code with a test. The rescaling sentence names what the model pins.
  - `thdm_type2` gained the $`\tan\beta = 1.5`$ point. `[decision]`
