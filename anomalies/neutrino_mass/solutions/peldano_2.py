"""Peldano 2 -- lowest-dimension EFT operator: the Weinberg operator."""

from __future__ import annotations

from .peldano_1 import build_sm_lepton_fields


def weinberg_operator_present(max_dim: int = 5) -> bool:
    """True iff ``suggest_yukawa``'s term list at ``max_dim`` includes the Weinberg operator."""
    from feynlag import suggest_yukawa

    Ll, eR, H, groups = build_sm_lepton_fields()
    terms = suggest_yukawa([Ll, eR], [H], list(groups), max_dim=max_dim)
    return any("Weinberg" in t.label for t in terms)


def lambda_estimate(m_nu: float, v: float) -> float:
    """Lambda ~ v^2 / m_nu, from m_nu ~ v^2 / Lambda (Weinberg operator, kappa ~ O(1))."""
    return v**2 / m_nu
