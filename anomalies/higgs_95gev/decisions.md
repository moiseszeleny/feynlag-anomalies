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
  - *Signal strengths $`\mu`$ for the diphoton and bb̄ channels, looked for on 2026-10-15 and not
    found in a primary source.* `[decision, needs approval]`
    - CMS (arXiv:2405.18149) and ATLAS (arXiv:2407.07546) print p-values and 95% CL upper limits in
      the paper text, not a best-fit $`\mu`$. The CMS maximum observed limit is 73 fb at 95.4 GeV.
      `[cited]` The CMS results are tabulated in HEPData (doi:10.17182/hepdata.150508). It blocked
      automated access (HTTP 403), so the user downloaded Figures 5a, 5b and 6a to 6d, kept locally
      in the untracked `anomalies/higgs_95gev/data/`. They hold observed and expected 95% CL limits
      only: at 95.4 GeV, 0.0734 pb observed vs 0.0279 pb expected (0.593 vs 0.224 normalised to the
      SM-like Higgs cross section). The 73.4 fb matches the paper's 73 fb. `[cited]` No best-fit
      $`\mu`$ is in them. A fit table, if CMS tabulated one (for example the local p-value figure),
      was not among the downloads.
    - The LEP paper (hep-ex/0306033) gives no $`\mu`$. The value $`0.117 \pm 0.057`$ appears only
      in Janot (arXiv:2407.10948), as inferred from a phenomenology paper, and Janot argues it is
      internally inconsistent. It is second-hand, so it is not recorded.
    - A CMS diphoton $`\mu`$ near 0.3 turned up in a web-search summary of a secondary source. It
      was not checked against a collaboration document, so it is not recorded.
    - The record therefore carries two `observables[]` rows at `TODO_VERIFY`, which A0 allows, so
      the gap is explicit. The diphoton significances sit in `significance:`, which holds one
      channel.
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
