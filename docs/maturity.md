# Anomaly maturity scale (A0-A4)

This scale tracks how far an anomaly's *ficha* (`anomalies/<id>/`) has progressed. It runs
parallel to, but is a different axis from, `feynlag-models`' model maturity scale (L0-L4, tracked
per `model_id`, not per anomaly) — do not conflate the two. A candidate model referenced by an
anomaly must independently satisfy its own L-level requirements (e.g. `feynlag-models` maturity
≥ L2 before it can be fit or scanned here, per `CLAUDE.md` hard rule 7).

| level | requirement |
|---|---|
| **A0** | Ficha exists with data and verified primary sources (`observables[]`, `sources[]` filled in, or explicitly `TODO_VERIFY`). |
| **A1** | An SM argument exists: either an executable structural test (via `feynlag`) or a cited, provenance-tagged SM prediction, plus an identified `sm_protection`. |
| **A2** | The lowest-dimension EFT operator is identified and at least one minimal candidate model is referenced by `model_id` (or a `model_requests/<id>.md` is filed if none exists). |
| **A3** | A stage-1 fit or scan has been run (Gaussian χ² via `fit/stage1.py`, with hard cuts) against a candidate model at feynlag-models maturity ≥ L2. |
| **A4** | A fit or scan has been run with real (non-Gaussian-summary) likelihoods, stage 2-3 tooling (HiggsTools, flavio/smelli, micrOMEGAs, pyhf, CLASS...). Not attempted before stage-2/3 tooling is approved and installed. |

An anomaly's `maturity` field in `anomaly.yaml` must be evidenced by what actually exists in its
directory (tests passing, notebook peldaños completed) — do not advance the field without the
corresponding work, and do not force a peldaño (e.g. a χ² fit needing a model capability that does
not yet exist) just to claim a higher level; document the block in `decisions.md` instead.
