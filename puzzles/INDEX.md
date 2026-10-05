# Puzzle catalog

Theoretical problems the SM is consistent with but does not explain. Experimental tensions live in
[`anomalies/`](../anomalies/INDEX.md). Only rows with a real `maturity` value have a directory;
the others are planned. Their `missing_protection` entries are preliminary guesses for triage.

| id | missing protection (preliminary) | status | maturity | notes |
|---|---|---|---|---|
| `flavor_puzzle` | `no_flavor_organizing_symmetry` | open | **P2** | pilot. SM quantifier computed from `sm_ckm`: 5.54 orders of magnitude (Huang–Zhou masses at M_Z, PDG 2024 CKM). Froggatt–Nielsen requested (`model_requests/froggatt_nielsen.md`). Cross-linked to `neutrino_mass`. |
| `hierarchy_problem` | `no_scalar_mass_protection` | — | — | planned. Needs a loop-level fine-tuning quantifier. Check whether feynlag provides one before starting. |
| `strong_cp` | `no_theta_protection` | — | — | planned. θ̄ is bounded by the neutron EDM, so it will carry a sourced experimental bound. |
| `cosmological_constant` | — | — | — | planned. Mostly conceptual. Its quantifier needs careful definition. |
| `charge_quantization` | — | — | — | planned (why hypercharges are commensurate; GUT / anomaly-cancellation arguments). |
| `baryon_asymmetry` | — | — | — | planned. Has a sourced observable (η_B), so it may belong in `anomalies/` instead. Decide when built. |

See [`docs/maturity.md`](../docs/maturity.md) for the P0-P4 scale and
[`docs/protections.md`](../docs/protections.md) for the missing-protection rows.
