"""Pydantic schema for ``anomalies/<id>/anomaly.yaml``.

Every numeric field that could come from an experimental measurement is typed as
``Verifiable = float | Literal["TODO_VERIFY"]`` — the sentinel is a first-class value, not an
error, so an anomaly.yaml can be committed honestly before every number has a verified primary
source. ``feynlag_anomalies.loader`` is the boundary that keeps the sentinel out of any real
calculation (``fit/stage1.py`` raises if it receives one).

This module only validates shape and closed vocabularies. Cross-file checks (id == directory
name, ``candidate_models[].model_id`` exists in the feynlag-models registry, maturity vs. model
maturity) live in ``feynlag_anomalies.loader`` because they need to look outside a single YAML
file.
"""

from __future__ import annotations

from datetime import date
from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field

TODO_VERIFY = "TODO_VERIFY"

Verifiable = Union[float, Literal["TODO_VERIFY"]]
DateOrTodo = Union[date, Literal["TODO_VERIFY"]]

SECTORS = Literal[
    "collider",
    "flavor",
    "electroweak_precision",
    "neutrinos",
    "dark_matter",
    "cosmology",
    "x17",
]

STATUSES = Literal["established", "live", "weakened", "resolved", "hint"]
SM_FAILURE_TYPES = Literal["structural", "resonance", "quantitative"]
PROVENANCES = Literal["computed", "cited"]
MATURITIES = Literal["A0", "A1", "A2", "A3", "A4"]
SOURCE_KINDS = Literal["arxiv", "doi", "hepdata", "pdg", "other"]

ID_PATTERN = r"^[a-z0-9_]+$"


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Observable(_Strict):
    name: str
    value: Verifiable
    stat_uncertainty: Verifiable
    sys_uncertainty: Verifiable | None = None
    units: str


class SMPrediction(_Strict):
    value: Verifiable
    uncertainty: Verifiable | None = None
    provenance: PROVENANCES
    reference: str | None = None


class Significance(_Strict):
    local: Verifiable | None = None
    global_: Verifiable | None = Field(default=None, alias="global")
    method: str | None = None

    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class Experiment(_Strict):
    name: str
    notes: str | None = None


class Source(_Strict):
    kind: SOURCE_KINDS
    identifier: str
    consulted_on: DateOrTodo


class EFTOperator(_Strict):
    name: str
    dimension: int
    expression: str | None = None


class CandidateModel(_Strict):
    model_id: str | None = None
    model_request: str | None = None
    notes: str | None = None

    def model_post_init(self, __context) -> None:
        if not self.model_id and not self.model_request:
            raise ValueError("CandidateModel needs at least one of model_id or model_request")


class ChangelogEntry(_Strict):
    date: DateOrTodo
    note: str
    author: str | None = None


class Anomaly(_Strict):
    id: str = Field(pattern=ID_PATTERN)
    title: str
    sector: SECTORS
    observables: list[Observable] = Field(default_factory=list)
    sm_prediction: SMPrediction
    significance: Significance | None = None
    experiments: list[Experiment] = Field(default_factory=list)
    sources: list[Source] = Field(default_factory=list)
    status: STATUSES
    status_date: DateOrTodo
    status_rationale: str
    tensions_with_other_data: list[str] = Field(default_factory=list)
    sm_failure_type: SM_FAILURE_TYPES
    sm_protection: list[str] = Field(default_factory=list)
    eft_operators: list[EFTOperator] = Field(default_factory=list)
    candidate_models: list[CandidateModel] = Field(default_factory=list)
    maturity: MATURITIES
    falsifiers: list[str] = Field(default_factory=list)
    changelog: list[ChangelogEntry] = Field(default_factory=list)
