# Anomaly catalog

Full candidate catalog across every sector named in the kickoff prompt (§1). Only the three rows
with a real `maturity` value have a directory under `anomalies/`; every other row is a planned
placeholder, not yet created, so this table gives the intended scope without over-promising
fichas that don't exist yet. `sm_failure_type` and `status` on the planned rows are preliminary
guesses for triage only -- to be confirmed (or corrected) when each ficha is actually built.

| id | sector | sm_failure_type (preliminary) | status (preliminary) | maturity | notes |
|---|---|---|---|---|---|
| `neutrino_mass` | neutrinos | structural | established | **A2** | pilot ficha, this session. Peldano 6 blocked on `model_requests/seesaw_type1_nN.md`. |
| `higgs_95gev` | collider | resonance | hint | **A0** | stub, this session. Needs literature pass. |
| `emu_146gev` | collider | resonance | hint | **A0** | stub, this session. Needs literature pass. |
| `muon_g_minus_2` | collider (precision) | quantitative | — | — | planned. Needs verification of Fermilab 2025 final result vs. the 2025 lattice White Paper (see `CLAUDE.md`). |
| `r_d_star` | flavor | quantitative | — | — | planned (R(D*), charged-current lepton universality). |
| `b_to_s_ll` | flavor | quantitative | — | — | planned (b -> s l l, e.g. angular observables / branching ratios). |
| `caa` | flavor | quantitative | — | — | planned (Cabibbo Angle Anomaly). |
| `m_w_mass` | electroweak_precision | quantitative | — | — | planned. Needs verification of CDF vs. ATLAS/CMS tension status (see `CLAUDE.md`). |
| `gallium_anomaly` | neutrinos | quantitative | — | — | planned (short-baseline, radioactive source experiments). |
| `lsnd_miniboone_microboone` | neutrinos | quantitative | — | — | planned (short-baseline sterile-neutrino hints, tension with MicroBooNE). |
| `reactor_anomaly` | neutrinos | quantitative | — | — | planned (reactor antineutrino flux/spectrum deficit). |
| `x17` | x17 | resonance | — | — | planned (ATOMKI/PADME/MEG II). |
| `dark_matter_direct` | dark_matter | — | — | — | planned (direct-detection hints/limits, e.g. the September 2026 LZ event -- read the preprint, not press coverage, per `CLAUDE.md`). |
| `dark_matter_relic` | dark_matter | — | — | — | planned (relic abundance constraints on candidate models). |
| `hubble_tension` | cosmology | quantitative | — | — | planned (H0 early- vs. late-universe tension). |
| `delta_n_eff` | cosmology | — | — | — | planned (ΔN_eff, effective number of relativistic species). |

See [`docs/maturity.md`](../docs/maturity.md) for the A0-A4 scale and
[`docs/protections.md`](../docs/protections.md) for the SM-protection taxonomy referenced by each
ficha's `sm_protection[]` field.
