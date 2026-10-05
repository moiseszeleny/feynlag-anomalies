# Anomaly maturity scale (A0-A4)

This scale tracks how far an anomaly's *record* (`anomalies/<id>/`) has progressed. It runs
parallel to, but is a different axis from, `feynlag-models`' model maturity scale (L0-L4, tracked
per `model_id`, not per anomaly) — do not conflate the two. A candidate model referenced by an
anomaly must independently satisfy its own L-level requirements (e.g. `feynlag-models` maturity
L2 or higher before it can be fit or scanned here, per `CLAUDE.md` hard rule 7).

| level | requirement |
|---|---|
| **A0** | Record exists with data and verified primary sources (`observables[]`, `sources[]` filled in, or explicitly `TODO_VERIFY`). |
| **A1** | An SM argument exists: either an executable structural test (via `feynlag`) or a cited, provenance-tagged SM prediction, plus an identified `sm_protection`. |
| **A2** | The lowest-dimension EFT operator is identified and at least one minimal candidate model is referenced by `model_id` (or a `model_requests/<id>.md` is filed if none exists). |
| **A3** | A stage-1 fit or scan has been run (Gaussian $\chi^2$ via `fit/stage1.py`, with hard cuts) against a candidate model at feynlag-models maturity L2 or higher. |
| **A4** | A fit or scan has been run with real (non-Gaussian-summary) likelihoods, stage 2-3 tooling (HiggsTools, flavio/smelli, micrOMEGAs, pyhf, CLASS...). Not attempted before stage-2/3 tooling is approved and installed. |

An anomaly's `maturity` field in `anomaly.yaml` must be evidenced by what actually exists in its
directory (tests passing, notebook steps completed) — do not advance the field without the
corresponding work, and do not force a step (e.g. a $\chi^2$ fit needing a model capability that
does not yet exist) just to claim a higher level; document the block in `decisions.md` instead.

## Puzzle maturity scale (P0-P4)

Records under `puzzles/<id>/` (theoretical problems, not experimental tensions) use a parallel
scale. It is enforced the same way (`feynlag_anomalies.loader.load_puzzle`) and gated by the same
model rule: P3+ needs feynlag-models maturity L2 or higher.

| level | requirement |
|---|---|
| **P0** | `puzzle.yaml` with a precise `statement`, the `sm_quantities[]` it is about (sourced, or explicitly `TODO_VERIFY`), a `quantifier` definition and a `missing_protection`. |
| **P1** | The quantifier is computed in the SM by code: `quantifier.provenance: computed` and `quantifier.implementation` resolve to a callable (the loader checks both), backed by a regression test. |
| **P2** | A mechanism class is identified and at least one candidate model is referenced by `model_id` (or a `model_requests/<id>.md` is filed). |
| **P3** | The quantifier is computed in a candidate model at L2 or higher and compared with the SM value, *and* the model passes the experimental constraints of the linked anomalies (stage-1 $\chi^2$ with hard cuts). |
| **P4** | As P3 with stage-2/3 likelihoods. Blocked until that tooling is approved. |

A model "addresses" a puzzle only with a computed before/after quantifier and the list of
constraints it satisfies, never as prose. Naturalness-type arguments are criteria, not
measurements: they are tagged `cited` unless the number behind them is computed here.
