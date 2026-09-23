"""Staged-hint checkpoints for ``ladder.ipynb`` exercises.

A :class:`Checkpoint` wraps a check function plus a list of staged hints (1 -> 2 -> 3, per the
kickoff spec's ladder template, §5). A notebook calls the checkpoint on the reader's answer; a
wrong answer nudges toward ``.hint()`` without leaking the expected value into the notebook's own
source.

The ``expected`` value passed into :func:`numeric_tolerance`/:func:`exact_match` must always come
from a loaded ``Anomaly`` object or a ``solutions/`` function -- never a bare literal typed into a
notebook cell or into an anomaly's ``checkpoints_def.py`` -- per the "no number lives only in
prose" rule (kickoff spec §4).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class Checkpoint:
    name: str
    check_fn: Callable[[Any], tuple[bool, str]]
    hints: list[str] = field(default_factory=list)
    _hint_level: int = field(default=0, init=False, repr=False)

    def __call__(self, respuesta: Any) -> bool:
        ok, message = self.check_fn(respuesta)
        suffix = f" -- {message}" if message else ""
        if ok:
            print(f"[{self.name}] correct{suffix}")
        else:
            nudge = " Call .hint() for a nudge." if self.hints else ""
            print(f"[{self.name}] not yet{suffix}.{nudge}")
        return ok

    def hint(self, level: int | None = None) -> str:
        """Reveal the next staged hint (or jump to ``level``, 1-indexed)."""
        if not self.hints:
            raise ValueError(f"checkpoint {self.name!r} has no hints defined")
        if level is not None:
            if not 1 <= level <= len(self.hints):
                raise ValueError(f"hint level must be between 1 and {len(self.hints)}")
            self._hint_level = level
        else:
            self._hint_level = min(self._hint_level + 1, len(self.hints))
        text = self.hints[self._hint_level - 1]
        print(f"[{self.name}] hint {self._hint_level}/{len(self.hints)}: {text}")
        return text


def numeric_tolerance(
    name: str, expected: float, rel_tol: float = 1e-2, hints: list[str] | None = None
) -> Checkpoint:
    """Checkpoint factory: passes if ``respuesta`` is within ``rel_tol`` of ``expected``."""

    def check_fn(respuesta: Any) -> tuple[bool, str]:
        try:
            value = float(respuesta)
        except (TypeError, ValueError):
            return False, f"expected a number, got {respuesta!r}"
        ok = abs(value) <= rel_tol if expected == 0 else abs(value - expected) / abs(expected) <= rel_tol
        return ok, f"got {value:.6g}"

    return Checkpoint(name=name, check_fn=check_fn, hints=list(hints or []))


def exact_match(name: str, expected: Any, hints: list[str] | None = None) -> Checkpoint:
    """Checkpoint factory: passes iff ``respuesta == expected``."""

    def check_fn(respuesta: Any) -> tuple[bool, str]:
        return respuesta == expected, f"got {respuesta!r}"

    return Checkpoint(name=name, check_fn=check_fn, hints=list(hints or []))
