# SM protection taxonomy

Every anomaly's `sm_protection[]` field must reference one or more rows of this table. This is a
skeleton for session 1 — most rows are not yet populated with worked examples/citations; that is
deferred to the session that builds the corresponding anomaly record.

| protection | mechanism (one line) | example anomaly | status |
|---|---|---|---|
| `accidental_symmetry` | A global symmetry ($B$, $`L_e`$, $`L_\mu`$, $`L_\tau`$, or total $L$) that is not imposed but emerges from the SM's gauge symmetry and field content at the renormalizable level. | `neutrino_mass` (accidental lepton number forbids a dim-4 Majorana mass) | seeded |
| `field_content` | The SM simply lacks a field needed to write the term (e.g. no $`\nu_R`$, no dark-matter candidate). | `neutrino_mass` (no $`\nu_R`$, so no dim-4 Dirac mass either) | seeded |
| `gim` | GIM mechanism: flavor-changing neutral currents cancel between up-type (or down-type) quark loops in the limit of degenerate masses, suppressed by mass splittings/CKM factors otherwise. | (flavor anomalies, not yet built) | placeholder |
| `chiral_helicity_suppression` | An amplitude requires a chirality flip, suppressing it by a light fermion mass over the relevant scale. | (not yet built) | placeholder |
| `custodial_symmetry` | An approximate $`SU(2)_{\rm custodial}`$ protects $`\rho = M_W^2/(M_Z^2 \cos^2\theta_W) \approx 1`$ against large corrections. | ($`M_W`$ tension, not yet built) | placeholder |
| `loop_suppression` | The leading SM contribution only arises at loop level (no tree-level diagram), suppressing it by a loop factor. | (g−2, not yet built) | placeholder |
| `ckm_hierarchy` | CKM matrix elements connecting distant generations are hierarchically small, suppressing associated transitions. | (flavor anomalies, not yet built) | placeholder |

Add new rows as needed; do not remove a row once an anomaly references it (breaks the
cross-reference the schema loader checks).

## Missing protections (puzzle direction)

Anomalies ask *which protection blocks an effect*. Puzzles (`puzzles/<id>/`) ask the dual
question: *why does nothing protect or fix a quantity*. A puzzle's `missing_protection[]` refers
to rows of this table.

| missing protection | what is missing (one line) | example puzzle | status |
|---|---|---|---|
| `no_flavor_organizing_symmetry` | The $U(3)^5$ flavor symmetry of the gauge sector is broken only by the Yukawas, and nothing in the SM fixes their pattern or size. | `flavor_puzzle` | seeded |
| `no_scalar_mass_protection` | No chiral or gauge symmetry protects an elementary scalar mass, so $`m_H^2`$ is additively sensitive to heavy scales. | (hierarchy problem, not yet built) | placeholder |
| `no_theta_protection` | $\bar\theta$ is a dimension-4 CP-odd parameter that no SM symmetry sets to zero, yet the neutron EDM bounds it to be tiny. | (strong CP, not yet built) | placeholder |
