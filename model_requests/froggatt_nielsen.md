# Model request: `froggatt_nielsen` ($`U(1)_{\rm FN}`$ flavon, three generations)

**Requested by**: `puzzles/flavor_puzzle` (P2; motivated by the $\lambda$-power table in section 4
of `ladder.ipynb`)
**Status**: fulfilled on 2026-10-05 by `feynlag-models`' `froggatt_nielsen` (PR #14, maturity L2),
filed on 2026-10-04 with the user's approval (CLAUDE.md hard rule 4). Design choices: a global
$`U(1)_{\rm FN}`$, spontaneously broken (the flavon phase $a$ is a massless Goldstone); the flavon
has charge $+1$ rather than $-1$ (only differences matter; the map to Leurer–Nir–Seiberg is in the
model's `metadata.yaml`); the integer charges are benchmark inputs, set at the benchmark to the
LNS "master model" (hep-ph/9310320 Eq. 2.5) for quarks and to placeholder lepton charges. The
numeric complex SVD this request anticipated as a gap is FEYNLAG_GAPS FG-6, worked around in
`feynlag_models.flavor` (`ckm_from_yukawas`, `mass_spectrum`). For use by P3 of `puzzles/flavor_puzzle`.
**Minimum level requested**: L2 (literature-checked mass and mixing scaling, below). P3 of the
puzzle is a stage-1 fit, which hard rule 7 gates at L2 or higher. L3/UFO is not needed for P3.

## Motivation

The SM fits the nine charged-fermion masses and the CKM matrix with free Yukawas whose
dimensionless values span **5.54 orders of magnitude** (the puzzle's quantifier
`free_parameter_log10_span`, computed from `sm_ckm` in `puzzles/flavor_puzzle/solutions/step_1.py`).
Section 4 of the notebook shows that every Yukawa is close to $\lambda^n$ with
$0 \lesssim n \lesssim 9$ ($\lambda \approx 0.225$), and that the CKM sines go as $\lambda$,
$\lambda^2$, $\lambda^3$ with $O(1)$ coefficients.

The Froggatt–Nielsen mechanism (Froggatt & Nielsen, Nucl. Phys. B147 (1979) 277,
doi:10.1016/0550-3213(79)90316-X, INSPIRE 131306) turns that observation into a model. A flavour
$`U(1)_{\rm FN}`$ under which the generations carry different charges forbids most renormalizable
Yukawas. A flavon $\phi$, charged under $`U(1)_{\rm FN}`$, gets a vev, and the Yukawas arise from
higher-dimension operators suppressed by $\epsilon = \langle\phi\rangle/\Lambda$ to a power fixed
by the charges. The free parameters become $O(1)$ coefficients $`c_{ij}`$, whose span is the number
P3 will compare with 5.54 orders of magnitude. Leurer, Nir and Seiberg (Nucl. Phys. B398 (1993)
319, hep-ph/9212278) give the systematic analysis of such mass-matrix models and of their mass
and mixing scaling.

Without this model the puzzle cannot pass P2: no candidate in `feynlag-models` addresses flavour
hierarchies. `sm_ckm` only reproduces them with free Yukawas.

## Requested field content

The parent is `sm_ckm` (extends): the same three generations of `Ll`, `eR`, `QL`, `uR`, `dR`
and the Higgs doublet `H`. On top of that:

- `phi` (the flavon $\phi$): complex scalar, SM gauge singlet $(1, 1, 0)$, $`U(1)_{\rm FN}`$ charge
  $-1$ (a convention; only charge differences matter). It gets a vev
  $`\langle\phi\rangle = v_\phi/\sqrt2`$.
- Every SM fermion field gets a $`U(1)_{\rm FN}`$ charge per generation: $`q(Q_{L,i})`$,
  $`q(u_{R,i})`$, $`q(d_{R,i})`$, $`q(L_{L,i})`$, $`q(e_{R,i})`$. $H$ is uncharged (the usual
  minimal choice).

**The charges should be benchmark inputs (integers), not hard-coded**, so that different
assignments are different benchmarks of one model rather than different models. P3 will scan or
compare a few assignments. Their literature values should be checked by the implementer (e.g.
against Leurer–Nir–Seiberg), not taken from this request.

## Symmetries and Lagrangian

$`U(1)_{\rm FN}`$ is spontaneously broken by $\langle\phi\rangle$. Whether it is a global $U(1)$
(with a pseudo-Goldstone flavon in the spectrum), explicitly broken to a discrete $`Z_N`$, or
gauged (anomaly conditions) is left to the implementer's judgment. The choice changes the flavon
phenomenology, not the Yukawa scaling that P3 needs. Please record the choice in the model's
`metadata.yaml`.

Effective Yukawas, the minimal EFT version (heavy FN messengers integrated out at $\Lambda$):

```math
-\mathcal L \supset c^u_{ij} \left(\frac{\phi}{\Lambda}\right)^{n^u_{ij}} \bar Q_i \tilde H u_j
+ c^d_{ij} \left(\frac{\phi}{\Lambda}\right)^{n^d_{ij}} \bar Q_i H d_j
+ c^e_{ij} \left(\frac{\phi}{\Lambda}\right)^{n^e_{ij}} \bar L_i H e_j + \text{h.c.}
```

with $`n_{ij}`$ fixed by $`U(1)_{\rm FN}`$ invariance, e.g.
$`n^u_{ij} = \lvert q(Q_{L,i}) - q(u_{R,j}) \rvert`$ (using $\phi^*$ when the difference is
negative; the sign convention is the implementer's). After symmetry breaking,

```math
y^f_{ij} = c^f_{ij}\, \epsilon^{\,n^f_{ij}}, \qquad \epsilon = \frac{v_\phi}{\sqrt2\,\Lambda} .
```

The $`c_{ij}`$ are complex $O(1)$ parameters. Neutrinos stay massless, as in `sm_ckm`. Lepton
mixing is out of scope for this request.

## What calculation requires it

P3 of `puzzles/flavor_puzzle`:

1. A stage-1 Gaussian $\chi^2$ (`fit/stage1.py`) of the model's masses and CKM magnitudes, as
   functions of $`(\epsilon, c_{ij})`$, against the sourced `sm_quantities` (Huang–Zhou masses at
   $`M_Z`$, PDG 2024 CKM).
2. At the best fit, the quantifier `free_parameter_log10_span` over the model's own free
   parameters $`\{\lvert c_{ij}\rvert\}`$ (and $\epsilon$), compared with the SM's 5.54 orders
   of magnitude.

From the bundle this needs: the symbolic $3\times3$ Yukawa matrices $`Y_u`$, $`Y_d`$, $`Y_e`$ in
terms of $`(\epsilon, c_{ij})`$ and the charges, and a way to get masses and $`V_{\rm CKM}`$ at a
numeric point (a biunitary diagonalisation of the complex $3\times3$ matrices).

## L2 literature checks requested

Mass scaling: for suitably ordered charges, up to $O(1)$ factors,

```math
\frac{m_{f_i}}{v} \sim \epsilon^{\,\lvert q(Q_{L,i}) - q(f_{R,i}) \rvert} .
```

Mixing scaling, for $i \neq j$:

```math
\lvert V_{ij} \rvert \sim \epsilon^{\,\lvert q(Q_{L,i}) - q(Q_{L,j}) \rvert} .
```

Both are checked against Leurer–Nir–Seiberg (or Froggatt–Nielsen), as an $O(1)$-coefficient
scaling at a random point, in the style of the numeric dual checks of `feynlag_models.checks`.

## Anticipated feynlag gaps (for the implementer, not claimed as found)

- **Higher-dimension operators.** The Yukawas have dimension $4 + n$ with $n$ up to about 8.
  `Model.check_invariance` / `validate` take `max_dim`, so the dimension ceiling can be raised.
  Whether the rest of the pipeline (mass matrices, vertex extraction) is exercised at that
  dimension is untested here. An alternative is to substitute the flavon vev in the coefficients
  first and keep only the dimension-4 Yukawas plus the flavon couplings to the needed order.
- **Complex $3\times3$ Dirac diagonalisation.** `feynlag.diagonalize_svd` is symbolic and
  documented for real $M$ ("complex Yukawas can be handled numerically at export time"). A
  generic complex $`Y_u`$, $`Y_d`$ needs a numeric biunitary SVD, analogous to the numeric Takagi
  added for FG-5. If it is missing, it would be an FG entry in `feynlag-models/FEYNLAG_GAPS.md`.

## Notes

- This request does not itself build anything (hard rule 4). Building it happens in
  `feynlag-models`, under that repo's own rules.
- Flavon-mediated flavour-changing neutral currents (meson mixing, $\mu \to e\gamma$) are the
  model's main experimental constraints. A serious confrontation needs stage-2 tools
  (flavio/smelli, hard rule 8). At stage 1, P3 can apply only coarse hard cuts on $\Lambda$ and
  $`v_\phi`$, and will say so.
