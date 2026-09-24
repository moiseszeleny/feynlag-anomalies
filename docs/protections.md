# SM protection taxonomy

Every anomaly's `sm_protection[]` field must reference one or more rows of this table. This is a
skeleton for session 1 — most rows are not yet populated with worked examples/citations; that is
deferred to the session that builds the corresponding anomaly record.

| protection | mechanism (one line) | example anomaly | status |
|---|---|---|---|
| `accidental_symmetry` | A global symmetry (B, L_e, L_μ, L_τ, or total L) that is not imposed but emerges from the SM's gauge symmetry and field content at the renormalizable level. | `neutrino_mass` (accidental lepton number forbids a dim-4 Majorana mass) | seeded |
| `field_content` | The SM simply lacks a field needed to write the term (e.g. no ν_R, no dark-matter candidate). | `neutrino_mass` (no ν_R ⟹ no dim-4 Dirac mass either) | seeded |
| `gim` | GIM mechanism: flavor-changing neutral currents cancel between up-type (or down-type) quark loops in the limit of degenerate masses, suppressed by mass splittings/CKM factors otherwise. | (flavor anomalies, not yet built) | placeholder |
| `chiral_helicity_suppression` | An amplitude requires a chirality flip, suppressing it by a light fermion mass over the relevant scale. | (not yet built) | placeholder |
| `custodial_symmetry` | An approximate SU(2)_custodial protects ρ = M_W²/(M_Z² cos²θ_W) ≈ 1 against large corrections. | (M_W tension, not yet built) | placeholder |
| `loop_suppression` | The leading SM contribution only arises at loop level (no tree-level diagram), suppressing it by a loop factor. | (g−2, not yet built) | placeholder |
| `ckm_hierarchy` | CKM matrix elements connecting distant generations are hierarchically small, suppressing associated transitions. | (flavor anomalies, not yet built) | placeholder |

Add new rows as needed; do not remove a row once an anomaly references it (breaks the
cross-reference the schema loader checks).
