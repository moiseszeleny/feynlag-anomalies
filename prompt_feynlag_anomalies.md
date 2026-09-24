# Kickoff prompt — `feynlag-anomalies` project

> Paste this entire text as the first message in Claude Code, opened in an empty folder that will be the new repository (with `feynlag` and `feynlag-models` cloned as sibling folders or installed in the environment). Also save a copy as `docs/PROJECT_BRIEF.md` inside the repo.

---

## 0. Role and mode of work

You are my research-and-development collaborator for a new repository, `feynlag-anomalies` (working name). I am a theoretical physicist (BSM phenomenology, extended scalar sector, neutrinos, LFV) and the author of `feynlag` (a Python/SymPy pipeline: gauge invariance, EWSB, mass matrices, vertices, UFO/LaTeX export, round-trip with MadGraph) and of `feynlag-models` (a verified library of minimal SM extensions with a maturity scale L0–L4).

**Before writing code:** explore the repos, read the documentation listed in §2, and present me with a plan (use plan mode). Do not start building until I approve it. If anything in this prompt contradicts what you find in the repos, stop and ask me.

## 1. Project goal

Build a verifiable, pedagogical library that, for every anomaly or measurement suggesting physics beyond the SM:

1. **Explains the anomaly**: what is measured, who measures it, what its significance is, and what its current status is.
2. **Explains, by calculation, why the SM doesn't describe it**, and identifies *which SM protection* blocks it.
3. **Builds a ladder of minimal extensions** that could describe it: dimensional estimate → EFT → UV completion → model in `feynlag-models` → confrontation with constraints.

**Audience:** colleagues and graduate students. Pedagogical principle: *a theoretical physicist learns by calculating, and the calculation generates the criteria for later decisions*. Each rung of the ladder must be a calculation the reader executes, which then motivates the next rung.

**Downstream uses:** a source for papers (reviews, phenomenological studies) and for outreach. Design it so the content can be reused, not just read.

**Thematic scope:** collider (Higgs and resonances), flavor, electroweak precision, neutrinos (including short-baseline anomalies: LSND/MiniBooNE/MicroBooNE, gallium, reactors), dark matter (direct, relic), cosmology (H₀, ΔN_eff, etc.), and X17 (ATOMKI/PADME/MEG II).

## 2. Relationship to `feynlag-models`: no-duplication rule

First read, in `feynlag-models`: `README.md`, `CLAUDE.md`, `CONVENTIONS.md`, `GENEALOGY.md`, `FEYNLAG_GAPS.md`, and `REPORT.md`. Also review `feynlag`'s documentation and public API.

| Lives in `feynlag-anomalies` | Lives in `feynlag-models` |
|---|---|
| Anomaly records: data, sources, status | Model declaration and `Model.validate()` |
| Tests for "why the SM can't" | Spectrum, vertices, UFO, round-trip |
| Minimal candidates (referenced by `model_id`) | Tests against the literature (L2) |
| Benchmark points, scans, fits, χ² | `GENEALOGY.md` |
| Pedagogical notebooks (ladders) | — |

Rules:
- **This repo never declares a Lagrangian.** It imports models from `feynlag-models` by `model_id`.
- If an anomaly needs a model that doesn't exist, or a variant (for example, more generations), write a **model request** in `model_requests/<id>.md`: fields, quantum numbers, symmetries, motivation, what calculation requires it, and the minimum level required. **Do not modify `feynlag-models` without my explicit approval.**
- Only models with maturity **≥ L2** are fit or scanned.
- Any `feynlag` gaps you discover (for example, loops or matching to Wilson coefficients) are documented as a proposal for `FEYNLAG_GAPS.md`, not patched here.

## 3. Concepts that structure the whole repo

### 3.1 Three types of "the SM can't explain it" (`sm_failure_type` field)
- `structural`: fields or terms are missing (ν mass, DM candidate, baryogenesis). It is **proven** with feynlag: enumeration of invariants, counting of states.
- `resonance`: a new state at a mass where the SM has nothing (95 GeV, 146 GeV eμ). The work is in the significance (local vs. global, look-elsewhere) and the coherence across channels.
- `quantitative`: the SM contributes, but the prediction differs from the measurement (R(D*), b→sℓℓ, CAA, M_W, g−2). The SM prediction usually requires QCD or loops that feynlag doesn't compute, and must be **cited and tagged**.

### 3.2 SM protection taxonomy (`docs/protections.md` and `sm_protection` field)
Accidental symmetries (B, L_e, L_μ, L_τ); field content; GIM; chiral/helicity suppression; custodial symmetry (ρ = 1); loop suppression; CKM hierarchy; others you find. Each anomaly maps to the protection(s) that must be broken, and that guides the family of extensions.

### 3.3 Anomaly maturity scale (parallel to L0–L4)
- **A0**: record with verified data and primary sources.
- **A1**: SM argument (executable structural test or a cited, tagged prediction) and identified protection.
- **A2**: lowest-dimension EFT operator and minimal candidate(s) with `model_id` (or a model request).
- **A3**: stage-1 scan or fit (Gaussian χ² with constraints).
- **A4**: fit with real likelihoods (stages 2–3).

### 3.4 Closed status vocabulary
`established` · `live` · `weakened` · `resolved` (closed case, kept as pedagogical material) · `hint` (preliminary, pending confirmation). Always dated and justified. Mandatory `tensions_with_other_data` field (e.g., ATOMKI vs. MEG II/PADME, LSND/MiniBooNE vs. MicroBooNE, CDF vs. ATLAS/CMS on M_W).

## 4. The record (data schema)

One folder per anomaly: `anomalies/<anomaly_id>/` with:
- `anomaly.yaml`, validated by a schema (pydantic or jsonschema) with at least: `id`, `title`, `sector`, `observables[]` (name, measured value, statistical and systematic uncertainties, units), `sm_prediction` (value, uncertainty, `provenance: computed|cited`, reference), `significance` (local, global, method), `experiments[]`, `sources[]` (arXiv / DOI / HEPData / PDG, **consultation date**), `status`, `status_date`, `status_rationale`, `tensions_with_other_data`, `sm_failure_type`, `sm_protection[]`, `eft_operators[]`, `candidate_models[]` (model_id or model_request), `maturity` (A0–A4), `falsifiers[]` (what future measurement would rule out each candidate), `changelog[]`.
- `ladder.ipynb`: the pedagogical ladder (§5).
- `solutions/`: checkpoint solutions (kept separate from the exercises).
- `decisions.md`: a decision log, one line per rung ("I chose X because calculation Y gave Z").
- `tests/`: the record's tests.

**No number lives only in prose**: every numeric value used in notebooks or docs is read from `anomaly.yaml`.

## 5. Pedagogical ladder (`ladder.ipynb` template)

Each rung ends with a **checkpoint** `check_<step>(answer)` that validates what the reader computes, and offers **staged hints** (1 → 2 → 3).

0. **Back-of-envelope estimate**: dimensional analysis of the scale or coupling required.
1. **Try it with the SM**: enumerate invariants with feynlag, or reproduce and cite the prediction. Name the protection at work.
2. **EFT before a model**: lowest-dimension SMEFT/WET operator and estimate of Λ.
3. **From the operator to the fields**: tree-level UV completions (reference: de Blas, Criado, Pérez-Victoria, Santiago, arXiv:1711.10391). Choose the minimal one with an explicit criterion (fewer fields → smaller representations → fewer parameters → no ad hoc symmetries) and import it from `feynlag-models`.
4. **Predict before running**: the reader writes down what they expect (number of physical scalars, Goldstones, new vertices, mixings) and then compares against feynlag.
5. **Break it on purpose**: try a non-minimal or incorrect choice and show, by calculation, why it fails.
6. **Confront with constraints**: stage-1 χ². If there's tension, that motivates the next rung of the genealogy.

Planned curricular order, where each anomaly adds a new skill: neutrinos → 95 GeV → 146 GeV eμ → g−2 (closed case) → flavor → cosmology.

## 6. Fits to data (from simple to complete)

- **Stage 1 (implement now):** Gaussian χ² with summary values and hard cuts (perturbativity, unitarity, vacuum stability). Only `lambdify` + NumPy/SciPy. Common module `fit/stage1.py`, reusable by every record.
- **Stage 2 (interface design only, not implementation):** HiggsTools (collider), flavio/smelli (flavor, via matching to WCxf, which would be a new `feynlag` gap), micrOMEGAs (relic abundance and direct detection via UFO/CalcHEP).
- **Stage 3 (future):** HEPData, pyhf, and CLASS for cosmology.
- Don't install heavy tools (micrOMEGAs, CLASS, HiggsTools) without asking me.

## 7. Verifiability rules (non-negotiable)

1. **Don't use experimental values from memory.** Every number is obtained from a primary source (arXiv, HEPData, PDG, an official collaboration note) and recorded with its reference and consultation date. If you can't verify it, mark `TODO_VERIFY` and don't use it in calculations.
2. **Dated status.** Your knowledge may be out of date. Verify each anomaly's current status in the literature before writing it down. Examples that require explicit verification: muon g−2 (Fermilab 2025 final result vs. the 2025 lattice-based White Paper), M_W (CDF vs. ATLAS/CMS), the 95 GeV excess (CMS/ATLAS γγ, ττ, LEP bb̄), the 146 GeV eμ excess (CMS), the anomalous LZ event (September 2026; take the details from the preprint, not from press coverage), X17 (PADME, MEG II), MicroBooNE.
3. **Tag `computed` vs. `cited`** on every prediction and every claim in the notebooks.
4. **Automated tests (pytest):** schema validation for every record; SM structural tests (e.g., "no ν mass term of dimension ≤ 4 exists with SM field content"); checkpoints against solutions; notebook execution in CI (nbmake or nbval).
5. **Regression test against the literature** before any original result: reproduce a published benchmark of the model used.
6. **"Explains the anomaly"** is only claimed with a code-computed metric (Δχ² or pull) and the list of satisfied constraints.
7. **Reproducibility:** pinned environment (`pyproject.toml`), CI, frozen versions designed for a Zenodo DOI, `CHANGELOG`.
8. Follow `feynlag-models/CONVENTIONS.md` (metric, potential, signs). If there is ambiguity, ask.

## 8. Tasks for this first session

1. **Exploration and plan** (wait for my approval): summary of the relevant feynlag API, status of the models in `feynlag-models`, and a plan for the repo's structure.
2. **Repo skeleton:** `pyproject.toml`, folder structure, `README.md`, `CLAUDE.md` (operational rules for this repo, derived from this prompt), `docs/PROJECT_BRIEF.md` (a copy of this prompt), `docs/protections.md`, `docs/maturity.md`, basic CI.
3. **Record schema + validator + schema tests.**
4. **`checkpoints` module** (helpers for exercises with staged hints) and **`fit/stage1.py` module**.
5. **Full pilot: `neutrino_mass`, up to A2** (and A3 if it's straightforward):
   - Step 0: m_ν ~ y²v²/M.
   - Step 1: feynlag test for the absence of a mass term at dimension ≤ 4; protection = no ν_R + accidental L.
   - Step 2: Weinberg operator (dimension 5).
   - Step 3: tree-level completions (type I, II, III seesaw); the minimal one is type I → `seesaw_type1`.
   - Step 4: the reader predicts how many light massive ν there are with 1 N and verifies it against the rank of the mass matrix.
   - Step 5: two measured Δm² require at least 2 N. Draft `model_requests/seesaw_type1_nN.md` (or the corresponding variant per `feynlag-models`).
   - Step 6: if feasible, stage-1 χ² with oscillation data (values from a verified global fit, e.g. NuFIT, with version and date).
6. **A0 stubs** for `higgs_95gev` and `emu_146gev`, with verified primary sources; and an `anomalies/INDEX.md` with the full candidate catalog (every sector from §1), indicating sector, type, preliminary status, and sources to verify.

## 9. What not to do

- Don't declare models or Lagrangians in this repo.
- Don't modify `feynlag` or `feynlag-models` without approval.
- Don't invent or recall experimental values, significances, or references from memory.
- Don't delete resolved anomalies: they move to `status: resolved` as pedagogical cases.
- Don't advance to fitting stages 2–3 in this session.

## 10. At the end of the session, report to me

- What got done and at what A0–A4 level each record stands.
- Tests that pass or fail.
- Model requests generated and feynlag gaps detected.
- Values marked `TODO_VERIFY` and decisions that need my judgment.
- A concrete proposal for the next session.
