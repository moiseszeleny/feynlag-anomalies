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
