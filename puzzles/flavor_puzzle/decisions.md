# Decisions — `flavor_puzzle`

One dated line per ladder step, tagged as in `anomalies/neutrino_mass/decisions.md`:
`[feynlag-verified: test]`, `[physics judgment]` or `[decision, needs approval]`.

- **2026-10-04 — P0** (record): puzzle stated as the unexplained hierarchy of the nine
  charged-fermion Yukawa eigenvalues and the CKM parameters. Lepton mixing is cross-linked through
  `related_anomalies: [neutrino_mass]` and is not duplicated here. `[physics judgment]`
- **2026-10-04 — P0** (quantifier): `free_parameter_log10_span`, the log10 range of the
  dimensionless free parameters a theory needs. It was chosen because the same definition applies
  to the SM and to a flavor model, so P3 can report a before/after on one number. It is blind to
  how many parameters there are and to whether the O(1) coefficients are tuned. Revisit at P1 if
  that turns out to matter. `[physics judgment]`
- **2026-10-04 — P0** (common scale): Yukawas to be compared at MS-bar μ = M_Z, a standard
  choice that sits below any flavor-model scale, so running up to it is part of P3, not P1.
  `[physics judgment]`
- **Next (P1)**: source the masses and the CKM fit (PDG) plus a published running to M_Z, then
  compute the SM quantifier in `solutions/` from `feynlag_models.registry` model `sm_ckm` (L3). Add
  a regression test against the published running before trusting it.
- **Next (P2)**: `model_requests/froggatt_nielsen.md` (a U(1)_FN flavon and its charges).
  `[decision, needs approval]` (hard rule 4).
