# feynlag-anomalies

A verifiable, pedagogical library of BSM anomalies. For each measurement or anomaly that suggests
physics beyond the Standard Model, this repo explains what is measured, proves or cites — by
calculation — why the SM fails and which SM protection it violates, and builds a ladder from a
dimensional estimate to a minimal tree-level UV completion imported from
[`feynlag-models`](../feynlag-models) by `model_id`, confronted with data.

**This repo never declares a Lagrangian.** Physics-model content (fields, symmetries, vertices,
UFO export) lives entirely in `feynlag-models`; this repo only imports models and builds
anomaly-facing data, tests, fits, and notebooks on top of them, using
[`feynlag`](../lagrangian) directly only for structural "why can't the SM do this" checks and
EFT-operator enumeration.

## What lives where

| Lives in `feynlag-anomalies` | Lives in `feynlag-models` |
|---|---|
| Anomaly fichas: data, sources, status | Model declaration and `Model.validate()` |
| Tests for "why the SM can't" | Spectrum, vertices, UFO, round-trip |
| Minimal candidates (referenced by `model_id`) | Tests against the literature (L2) |
| Benchmark points, scans, fits, χ² | `GENEALOGY.md` |
| Pedagogical notebooks (ladders) | — |

## Quickstart

```bash
uv sync --all-extras
uv run pytest -q                      # fast suite: schema, checkpoints, stage1, structural tests
uv run pytest --nbmake anomalies -q   # execute every ladder.ipynb top-to-bottom
```

**Known blocker (see [`docs/upstream_gaps.md`](docs/upstream_gaps.md) UG-1)**: a clean `uv sync`
currently cannot build any `feynlag-models` model (`metadata.yaml` and other data files are
missing from that repo's built package, a packaging gap in `feynlag-models` itself, not in this
repo). Until that is fixed upstream, tests that touch a model (`seesaw_type1`, ...) only pass with
a local editable override:

```bash
uv pip install -e ../feynlag-models   # requires a local sibling checkout of feynlag-models
```

Each `ladder.ipynb` ships already solved, so `nbmake` can confirm it runs green in CI end to end;
to work through an anomaly as an exercise, make your own copy of the notebook before reading the
`solutions/` directory it imports from.

## Anomaly catalog

See [`anomalies/INDEX.md`](anomalies/INDEX.md) for the full candidate catalog across every sector
(collider, flavor, electroweak precision, neutrinos, dark matter, cosmology, X17), and the
maturity level (A0-A4, see [`docs/maturity.md`](docs/maturity.md)) of each.

## Further reading

- [`CLAUDE.md`](CLAUDE.md) — operational rules for working in this repo.
- [`docs/PROJECT_BRIEF.md`](docs/PROJECT_BRIEF.md) — the original project kickoff prompt (full
  requirements).
- [`docs/protections.md`](docs/protections.md) — the SM-protection taxonomy.
- [`docs/maturity.md`](docs/maturity.md) — the A0-A4 anomaly maturity scale.
