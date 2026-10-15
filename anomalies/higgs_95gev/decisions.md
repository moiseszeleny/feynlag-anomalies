# Decisions — `higgs_95gev`

- **2026-09-22**: A0 stub created. No literature search performed this session (out of scope for
  the repo-bootstrap session). `[decision, needs approval]` — next session should run a primary
  literature pass (CMS/ATLAS diphoton and ditau channels, LEP bb̄) before advancing past A0.
- **2026-10-15 — A0 literature pass.** Every number in `anomaly.yaml` was read from the paper's own
  text (PDF full text, or the abstract page where stated), not from review articles. `[cited]`
  - *CMS diphoton*, arXiv:2405.18149: local (global) 2.9σ (1.3σ) at 95.4 GeV. The 2016 data alone
    give 3.3σ, up from 2.8σ in arXiv:1811.08459. Recorded under `significance:`.
  - *ATLAS diphoton*, arXiv:2407.07546: no significant excess. Largest model-dependent deviation
    is 1.7σ local at 95.4 GeV. Recorded in `experiments[]` and as a tension.
  - *CMS ditau*, arXiv:2208.02717: 2.6σ (2.3σ) at 95 GeV and 3.1σ (2.7σ) at 100 GeV, local
    (global). The only channel with an entry in `observables[]`: $`\sigma B`$ at 95 GeV, 7.8 pb
    with errors +3.9/−3.1, symmetrised to 3.5.
  - *LEP bb̄*, arXiv:hep-ex/0306033: $`1-{\rm CL}_b \approx 0.02`$, i.e. 2.3σ, near 98 GeV. The paper
    itself says the signal behind it is about an order of magnitude below the SM Higgs rate.
    Janot, arXiv:2407.10948, argues the LEP data disfavour a 95 GeV scalar as its cause. That is
    one author's reanalysis. It is not a collaboration result. `[physics judgment]`
  - *No later result found.* A web search on 2026-10-15 found no Run 3 or 2026 collaboration
    result on this excess. Absence from a search is not proof, so this is not claimed as a fact
    about the experiments. `[decision]`
- **2026-10-15 — what stays open.**
  - The best-fit signal strengths $`\mu`$ for the diphoton and bb̄ channels were not read, so the
    record has no signal-strength observable for them. The diphoton significances sit in
    `significance:`, which holds one channel. `[decision, needs approval]`
  - The ditau $`\sigma B`$ is given in pb for a generic $`\phi`$, not as a ratio to an SM-like
    Higgs cross section, so it cannot be compared with the diphoton channel yet. A comparison needs
    a cross-section ratio at 95 GeV, which is A1 work.
  - `sm_prediction` is the background-only expectation of the cited searches (0.0 for the new
    signal), because the SM has no scalar near 95 GeV. No SM argument was written. That is A1.
  - Status is `hint`: three channels at 2 to 3σ, none significant alone, ATLAS weaker, and a
    disfavouring LEP reanalysis. `[physics judgment]`
  - Not read and therefore not cited: combined ATLAS+CMS significances quoted in phenomenology
    papers. They are not collaboration numbers.
- **Maturity stays A0.** `sm_protection`, `eft_operators` and `candidate_models` are untouched.
