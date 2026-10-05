# Model request: `froggatt_nielsen` (U(1)_FN flavon, three generations)

**Requested by**: `puzzles/flavor_puzzle` (P2; motivated by the λ-power table in section 4 of
`ladder.ipynb`)
**Status**: filed on 2026-10-04 with the user's approval (CLAUDE.md hard rule 4). Not yet built.
**Minimum level requested**: L2 (literature-checked mass and mixing scaling, below). P3 of the
puzzle is a stage-1 fit, which hard rule 7 gates at ≥ L2. L3/UFO is not needed for P3.

## Motivation

The SM fits the nine charged-fermion masses and the CKM matrix with free Yukawas whose
dimensionless values span **5.54 decades** (the puzzle's quantifier `free_parameter_log10_span`,
computed from `sm_ckm` in `puzzles/flavor_puzzle/solutions/step_1.py`). Section 4 of the
notebook shows that every Yukawa is close to λ^n with 0 ≲ n ≲ 9 (λ ≈ 0.225), and that the CKM
sines go as λ, λ², λ³ with O(1) coefficients.

The Froggatt–Nielsen mechanism (Froggatt & Nielsen, Nucl. Phys. B147 (1979) 277,
doi:10.1016/0550-3213(79)90316-X, INSPIRE 131306) turns that observation into a model. A flavour
U(1)_FN under which the generations carry different charges forbids most renormalizable Yukawas.
A flavon φ, charged under U(1)_FN, gets a vev, and the Yukawas arise from higher-dimension
operators suppressed by ε = ⟨φ⟩/Λ to a power fixed by the charges. The free parameters become
O(1) coefficients c_ij, whose span is the number P3 will compare with 5.54 decades. Leurer, Nir
and Seiberg (Nucl. Phys. B398 (1993) 319, hep-ph/9212278) give the systematic analysis of such
mass-matrix models and of their mass and mixing scaling.

Without this model the puzzle cannot pass P2: no candidate in `feynlag-models` addresses flavour
hierarchies. `sm_ckm` only reproduces them with free Yukawas.

## Requested field content

The parent is `sm_ckm` (extends): the same three generations of `Ll`, `eR`, `QL`, `uR`, `dR`
and the Higgs doublet `H`. On top of that:

- `phi` (flavon): complex scalar, SM gauge singlet `(1, 1, 0)`, U(1)_FN charge −1 (a convention;
  only charge differences matter). It gets a vev ⟨φ⟩ = v_φ/√2.
- Every SM fermion field gets a U(1)_FN charge per generation: `q(QL_i)`, `q(uR_i)`, `q(dR_i)`,
  `q(Ll_i)`, `q(eR_i)`. `H` is uncharged (the usual minimal choice).

**The charges should be benchmark inputs (integers), not hard-coded**, so that different
assignments are different benchmarks of one model rather than different models. P3 will scan or
compare a few assignments. Their literature values should be checked by the implementer (e.g.
against Leurer–Nir–Seiberg), not taken from this request.

## Symmetries and Lagrangian

- U(1)_FN, spontaneously broken by ⟨φ⟩. Whether it is a global U(1) (with a pseudo-Goldstone
  flavon in the spectrum), explicitly broken to a discrete Z_N, or gauged (anomaly conditions)
  is left to the implementer's judgment. The choice changes the flavon phenomenology, not the
  Yukawa scaling that P3 needs. Please record the choice in the model's `metadata.yaml`.
- Effective Yukawas, the minimal EFT version (heavy FN messengers integrated out at Λ):

  ```
  -L ⊃ c^u_ij (φ/Λ)^{n^u_ij} Q̄_i H̃ u_j + c^d_ij (φ/Λ)^{n^d_ij} Q̄_i H d_j
       + c^e_ij (φ/Λ)^{n^e_ij} L̄_i H e_j + h.c.
  ```

  with n_ij fixed by U(1)_FN invariance, e.g. n^u_ij = |q(QL_i) − q(uR_j)| (using φ* when the
  difference is negative; the sign convention is the implementer's). After symmetry breaking,
  y^f_ij = c^f_ij ε^{n^f_ij} with ε = v_φ/(√2 Λ). The c_ij are complex O(1) parameters.
- Neutrinos stay massless, as in `sm_ckm`. Lepton mixing is out of scope for this request.

## What calculation requires it

P3 of `puzzles/flavor_puzzle`:

1. A stage-1 Gaussian χ² (`fit/stage1.py`) of the model's masses and CKM magnitudes, as
   functions of (ε, c_ij), against the sourced `sm_quantities` (Huang–Zhou masses at M_Z, PDG
   2024 CKM).
2. At the best fit, the quantifier `free_parameter_log10_span` over the model's own free
   parameters {|c_ij|} (and ε), compared with the SM's 5.54 decades.

From the bundle this needs: the symbolic 3×3 Yukawa matrices Y_u, Y_d, Y_e in terms of
(ε, c_ij, charges), and a way to get masses and V_CKM at a numeric point (a biunitary
diagonalisation of the complex 3×3 matrices).

## L2 literature checks requested

- Mass scaling: for suitably ordered charges, m_{f_i}/v ∼ ε^{|q(QL_i) − q(f_i)|}, up to O(1)
  factors.
- Mixing scaling: |V_ij| ∼ ε^{|q(QL_i) − q(QL_j)|} for i ≠ j.
- Both checked against Leurer–Nir–Seiberg (or Froggatt–Nielsen), as an O(1)-coefficient scaling
  at a random point, in the style of the numeric dual checks of `feynlag_models.checks`.

## Anticipated feynlag gaps (for the implementer, not claimed as found)

- **Higher-dimension operators.** The Yukawas are dimension 4 + n with n up to about 8.
  `Model.check_invariance` / `validate` take `max_dim`, so the dimension ceiling can be raised.
  Whether the rest of the pipeline (mass matrices, vertex extraction) is exercised at that
  dimension is untested here. An alternative is to substitute the flavon vev in the coefficients
  first and keep only the dimension-4 Yukawas plus the flavon couplings to the needed order.
- **Complex 3×3 Dirac diagonalisation.** `feynlag.diagonalize_svd` is symbolic and documented
  for real M ("complex Yukawas can be handled numerically at export time"). A generic complex
  Y_u, Y_d needs a numeric biunitary SVD, analogous to the numeric Takagi added for FG-5. If it
  is missing, it would be an FG entry in `feynlag-models/FEYNLAG_GAPS.md`.

## Notes

- This request does not itself build anything (hard rule 4). Building it happens in
  `feynlag-models`, under that repo's own rules.
- Flavon-mediated flavour-changing neutral currents (meson mixing, μ → eγ) are the model's main
  experimental constraints. A serious confrontation needs stage-2 tools (flavio/smelli, hard rule
  8). At stage 1, P3 can apply only coarse hard cuts on Λ and v_φ, and will say so.
