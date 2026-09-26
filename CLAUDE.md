# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

`feynlag-anomalies` is a verifiable, pedagogical library. For each measurement or anomaly that
suggests physics beyond the Standard Model, it (1) explains what is measured and its current
status, (2) proves or cites, by calculation, why the SM does not describe it and which SM
protection blocks it, and (3) builds a ladder of minimal extensions: dimensional estimate → EFT
operator → tree-level UV completion → confrontation with data. Full requirements are in
`docs/PROJECT_BRIEF.md` (the original kickoff prompt).

This repo depends on two sibling repos, both read-only from here:
- `feynlag` (`../lagrangian`, pip package `feynlag`) — the SymPy engine: field declaration, gauge
  invariance, EWSB, mass matrices, Feynman rules, UFO/LaTeX export.
- `feynlag-models` (`../feynlag-models`, pip package `feynlag-models`) — the verified library of
  minimal SM extensions (`sm`, `sm_ckm`, `sm_singlet_z2`, `seesaw_type1`, `thdm_type2`, maturity
  L0-L4), consumed here by `model_id`.

## Commands

- `uv sync --all-extras` — install/update the environment.
- `uv run pytest -q` — fast suite (schema validation, checkpoints, stage1, structural tests).
- `uv run pytest --nbmake anomalies -q` — execute every `ladder.ipynb` top-to-bottom; a notebook
  that raises (a failed checkpoint) is a test failure.
- `uv run pytest -q anomalies/neutrino_mass` — one anomaly's tests only.
- `uv run jupyter nbconvert --to notebook --execute --inplace anomalies/<id>/ladder.ipynb` —
  refresh a notebook's stored outputs after editing it (nbmake runs in memory and never saves).

## Architecture

`anomalies/<id>/anomaly.yaml` is parsed and validated by `feynlag_anomalies.schema.Anomaly`
(pydantic) plus cross-file checks in `feynlag_anomalies.loader`. `anomalies/<id>/ladder.ipynb` is
the pedagogical notebook; it imports checkpoint objects from the anomaly's own
`checkpoints_def.py` (built from `checkpoints.core.Checkpoint` + `solutions/`), never from
`solutions/` directly, and reads every numeric value from the loaded `Anomaly` object rather than
inlining literals. Notebooks show SymPy objects with `IPython.display.display` (as
`Math(... + sp.latex(expr))` when paired with a label) and keep `print` for plain text and
numeric tables. `fit/stage1.py` runs Gaussian χ² fits against `feynlag_models` model bundles.
Candidate models are consumed exclusively through `feynlag_models.registry`.

## Hard rules

1. **Never declare a `feynlag.Model` or a Lagrangian in this repo.** All physics-model content
   (fields, symmetries, Lagrangians) lives in `feynlag-models`. This repo only imports models by
   `model_id` and computes on top of them (structural tests, EFT operators, fits, notebooks).
2. **Always import candidate models via `feynlag_models.registry.{load,build,metadata,model_ids}`.**
   Never `import models.<id>.model` directly.
3. **Never create a top-level Python package or bare module literally named `models` anywhere in
   this repository.** `feynlag_models.registry.load()` does
   `importlib.import_module("models.<id>.model")`, where `models` is a separate top-level package
   (not namespaced under `feynlag_models`). A local `models` package here would collide with it in
   `sys.modules`.
4. **Never modify `feynlag` or `feynlag-models`.** If a `feynlag` capability is missing, or a
   `feynlag-models` packaging/tooling issue blocks this repo, write it up as a *proposed* gap in
   `docs/upstream_gaps.md` — do not edit `feynlag-models/FEYNLAG_GAPS.md` directly. If an anomaly
   needs a model that does not exist, or a variant of one, write `model_requests/<id>.md` (fields,
   quantum numbers, symmetries, motivation, the calculation that requires it, minimum
   feynlag-models maturity level needed) instead of building it here. Neither action is taken
   without the user's explicit approval.
5. **No experimental number from memory.** Every measured value needs a primary source (arXiv,
   HEPData, PDG, an official collaboration note) and a consultation date in `sources[]`. If a
   value cannot be verified in this session, it is written as the literal sentinel `TODO_VERIFY`
   and must not be consumed by `fit/stage1.py` (which raises, naming the field, if it receives the
   sentinel).
6. **Tag every prediction/claim `computed` or `cited`** (`sm_prediction.provenance` in the schema;
   the same discipline extends to notebook prose).
7. **Only fit or scan a `candidate_models[]` entry whose feynlag-models maturity is ≥ L2**
   (`feynlag_models.registry.metadata(model_id)["maturity_level"]`).
8. **Stage-2/3 fitting tools (HiggsTools, flavio/smelli, micrOMEGAs, pyhf, CLASS, HEPData) are
   interface-design-only in this phase** — do not install or wire them up without asking first.
9. `status` is a closed vocabulary: `established | live | weakened | resolved | hint`, always
   dated (`status_date`) and justified (`status_rationale`).
10. **Never delete a resolved anomaly folder.** It moves to `status: resolved` and stays as
    pedagogical material.
11. Follow `feynlag-models/CONVENTIONS.md` (metric, potential signs, rotation conventions) for any
    symbolic work that touches feynlag/feynlag-models objects directly. If a convention is
    ambiguous, ask rather than guess.

## Verifiability discipline (see `docs/PROJECT_BRIEF.md` §7 for the full text)

- Re-check the current status of any anomaly against the literature before writing it down — prior
  knowledge may be stale. Cases the kickoff prompt explicitly flags as needing a fresh check: muon
  g−2 (Fermilab 2025 final vs. the 2025 lattice White Paper), M_W (CDF vs. ATLAS/CMS), the 95 GeV
  and 146 GeV eμ excesses, the September 2026 LZ anomalous event (read the preprint, not press
  coverage), X17, MicroBooNE.
- A regression test against a published benchmark is expected before trusting any new numeric
  result derived here.
- "Explains the anomaly" is only claimed once a code-computed metric (Δχ² or pull) and the list of
  satisfied constraints back it up — never as prose alone.
