# Model request: `seesaw_type1_nN` (n-generation type-I seesaw)

**Requested by**: `anomalies/neutrino_mass` (step 5 of `ladder.ipynb`)
**Status**: fulfilled on 2026-09-25 by `feynlag-models`' `seesaw_type1_2n` (PR #9, maturity L2).
The id is lowercase because the metadata schema requires `^[a-z0-9_]+$`. It has three lepton
generations (the rank argument needs n_L ≥ 2, and `sm.pieces` offers only 1 or 3) and two
ν_R. Used by `anomalies/neutrino_mass` step 6.
**Minimum level requested**: L2 (literature-checked masses/mixings/vertices — matching what the
existing single-generation `seesaw_type1` already reaches; UFO/L3 is blocked upstream by
`feynlag-models/FEYNLAG_GAPS.md` FG-3, no Majorana UFO export path in `feynlag`, so L2 is the
realistic ceiling for this variant too).

## Motivation

`feynlag-models`' existing `seesaw_type1` model (`models/seesaw_type1/`) has exactly one
right-handed neutrino `ν_R` (`nflavors=1`), giving a single physical light-neutrino mass. Neutrino
oscillation experiments measure **two independent** mass-squared splittings (Δm²₂₁ and
Δm²₃₁/Δm²₃₂ — solar and atmospheric), which is only possible with at least **two** massive light
states. A rank argument on the seesaw mass matrix (step 5 of the `neutrino_mass` ladder) shows
that reproducing two independent Δm² values requires **at least two** right-handed neutrinos.

Without this variant, `neutrino_mass` cannot progress past maturity A2 in `feynlag-anomalies`: a
real stage-1 χ² fit (step 6, A3) against two measured Δm² values is not possible against a
single-light-mass model without either overclaiming (fitting one observable and calling it a
global fit) or leaving one Δm² unconstrained.

## Requested field content

Extend `nuR` from `nflavors=1` to `nflavors=2` (minimal choice — 2 heavy Majorana states is the
minimum needed to fit 2 independent light Δm², following the same "minimal extension" logic as
the existing `seesaw_type1` choosing type-I over type-II/III per de Blas–Criado–Pérez-Victoria–
Santiago, arXiv:1711.10391). No new gauge or discrete symmetries beyond what `seesaw_type1`
already declares (SM gauge group; the same accidental/explicitly-broken lepton number as
`seesaw_type1`'s `metadata.yaml`).

- `nuR`: `WeylFermion`, SM gauge singlet, right-chirality, **`nflavors=2`** (was 1 in
  `seesaw_type1`).
- Yukawa `−y_ν,ij L̄_i H̃ ν_R,j` becomes a genuine 3×2 (flavor × generation) Dirac-mass matrix
  after EWSB, not a single number.
- Majorana mass term `−½ (M_R)_jk ν_R,jᵀ C ν_R,k` becomes a symmetric 2×2 matrix, in general with
  off-diagonal entries (or diagonal-only as the minimal/simplest benchmark choice — left to the
  implementer's judgment when this is approved).

## Quantum numbers

Identical to `seesaw_type1`'s existing `nuR` entry in `metadata.yaml` (`su3: 1, su2: 1, u1y: "0"`,
global `U1_L` charge `1`, explicitly broken by the Majorana mass term), just with `generations: 2`
instead of `1`.

## What calculation requires it

Step 6 of `anomalies/neutrino_mass/ladder.ipynb`: a diagonal Gaussian χ² (via `fit/stage1.py`)
against two independently measured Δm² values from a global neutrino-oscillation fit (e.g. NuFIT —
version and consultation date to be sourced when this record's `TODO_VERIFY` values are resolved).
This is not implementable against a model whose light-neutrino sector has rank 1.

## Notes

- This request does **not** ask for a build to happen — per `CLAUDE.md` hard rule 4, no change to
  `feynlag-models` is made without the user's explicit approval.
- `feynlag-models/FEYNLAG_GAPS.md` FG-3 (no Majorana UFO export path in `feynlag`) will still cap
  this variant at L2, same as the existing `seesaw_type1` — flagging this up front so approving
  the model request doesn't come with an implicit expectation of L3/UFO output.
