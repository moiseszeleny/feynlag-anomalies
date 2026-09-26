"""Stage-1 fitting: Gaussian chi2 + hard cuts, pure numpy/scipy/sympy.lambdify.

Only the "etapa 1" tooling from the kickoff spec (§6) is implemented here: a diagonal Gaussian
chi2 against summary values, plus a perturbativity cut and a single-quartic vacuum-stability cut.
Stage 2 (HiggsTools, flavio/smelli, micrOMEGAs) and stage 3 (HEPData, pyhf, CLASS) are explicitly
out of scope this session -- not even their interfaces are designed here, per the kickoff spec's
"no instales herramientas pesadas sin preguntar."

Every function that consumes a measured/predicted number rejects the ``TODO_VERIFY`` sentinel
(see ``feynlag_anomalies.schema.TODO_VERIFY``) with a clear, field-naming error -- this is the
concrete mechanism that keeps an unverified value out of a fit.
"""

from __future__ import annotations

import math
from typing import Callable, Mapping

import numpy as np
import sympy as sp

TODO_VERIFY = "TODO_VERIFY"


class Stage1Error(ValueError):
    """Raised when stage-1 fitting code receives an unverified (TODO_VERIFY) value."""


def _reject_sentinel(name: str, value) -> float:
    if isinstance(value, str):
        raise Stage1Error(f"{name!r} holds the unverified sentinel {value!r} -- cannot fit with it")
    return float(value)


def combine_uncertainties(stat: float, syst: float | None = None) -> float:
    """Quadrature sum of statistical and systematic uncertainty.

    Ignores possible correlations between observables -- a stage-1 simplification; revisit with a
    full covariance at stage 2/3 if a fit needs it.
    """
    stat = _reject_sentinel("stat", stat)
    syst = 0.0 if syst is None else _reject_sentinel("syst", syst)
    return math.sqrt(stat**2 + syst**2)


def chi2_gaussian(
    predicted: Mapping[str, float], observed: Mapping[str, tuple[float, float]]
) -> float:
    """Diagonal Gaussian chi2: sum_i ((predicted_i - observed_i) / sigma_i)**2.

    ``observed`` maps each observable name to ``(central_value, uncertainty)``.
    """
    total = 0.0
    for key, (center, sigma) in observed.items():
        if key not in predicted:
            raise KeyError(f"no prediction for observable {key!r}")
        pred = _reject_sentinel(f"predicted[{key!r}]", predicted[key])
        center = _reject_sentinel(f"observed[{key!r}].center", center)
        sigma = _reject_sentinel(f"observed[{key!r}].sigma", sigma)
        total += ((pred - center) / sigma) ** 2
    return total


def predict(
    bundle_values: Mapping[sp.Symbol, float], observable_exprs: Mapping[str, sp.Expr]
) -> dict[str, float]:
    """Evaluate each observable expression at a ModelBundle's numeric values.

    ``bundle_values`` is typically ``ModelBundle.values()`` (``{symbol: number}``);
    ``observable_exprs`` maps an observable name to a sympy expression in those symbols.
    """
    predicted = {}
    for name, expr in observable_exprs.items():
        free = sorted(expr.free_symbols, key=lambda s: s.name)
        missing = [s for s in free if s not in bundle_values]
        if missing:
            raise KeyError(f"observable {name!r}: no value for symbols {missing}")
        fn = sp.lambdify(free, expr, "numpy")
        predicted[name] = float(fn(*(bundle_values[s] for s in free)))
    return predicted


def scan(
    build_fn: Callable[..., object],
    param_grid: Mapping[str, np.ndarray],
    observable_exprs: Mapping[str, sp.Expr],
    observed: Mapping[str, tuple[float, float]],
) -> np.ndarray:
    """Grid-scan chi2 over a candidate model's benchmark parameters.

    ``build_fn(benchmark=...)`` should return a ``feynlag_models`` ``ModelBundle`` (typically
    ``functools.partial(feynlag_models.registry.build, model_id)``); ``param_grid`` maps
    benchmark parameter names to arrays of values to scan; the grid is the outer product of all
    of them.

    Known limitation: feynlag-models' own CLAUDE.md documents model builds at 10-60s each (its
    own test fixtures are session-scoped for exactly this reason) -- a naive grid scan over more
    than a handful of points is likely impractical. This function does not special-case rebuilding
    only the ``ExternalParameter`` values without rebuilding the whole model; that would need
    feynlag-models internals not explored this session.
    """
    names = list(param_grid)
    grids = np.meshgrid(*(param_grid[n] for n in names), indexing="ij")
    shape = grids[0].shape
    chi2 = np.empty(shape, dtype=float)
    for idx in np.ndindex(shape):
        point = {n: g[idx] for n, g in zip(names, grids)}
        bundle = build_fn(benchmark=point)
        predicted = predict(bundle.values(), observable_exprs)
        chi2[idx] = chi2_gaussian(predicted, observed)
    return chi2


def minimize_chi2(
    predict_fn: Callable[[np.ndarray], Mapping[str, float]],
    x0,
    observed: Mapping[str, tuple[float, float]],
    bounds=(-np.inf, np.inf),
    **least_squares_kwargs,
) -> dict:
    """Minimize the diagonal Gaussian chi2 over a parameter vector, without rebuilding a model.

    ``predict_fn(x)`` returns ``{observable: prediction}`` for the parameter vector ``x``
    (typically by substituting ``x`` into a bundle's symbolic matrices, which is far cheaper than
    ``scan``'s rebuild per point). The residuals handed to ``scipy.optimize.least_squares`` are
    the pulls, so the returned ``chi2`` equals ``chi2_gaussian`` at the optimum.

    Returns ``{"x", "chi2", "predicted", "pulls", "ndof", "success", "message"}``; ``ndof`` is
    ``n_observables - n_parameters`` and may be <= 0 (an underdetermined fit shows only that the
    model *can* accommodate the data).
    """
    from scipy.optimize import least_squares

    obs = {k: (_reject_sentinel(f"observed[{k!r}].center", c),
               _reject_sentinel(f"observed[{k!r}].sigma", s)) for k, (c, s) in observed.items()}
    names = list(obs)

    def residuals(x):
        pred = predict_fn(x)
        return np.array([(float(pred[k]) - obs[k][0]) / obs[k][1] for k in names])

    res = least_squares(residuals, np.asarray(x0, dtype=float), bounds=bounds,
                        **least_squares_kwargs)
    predicted = dict(predict_fn(res.x))
    pulls = {k: (float(predicted[k]) - obs[k][0]) / obs[k][1] for k in names}
    return {
        "x": res.x,
        "chi2": chi2_gaussian(predicted, obs),
        "predicted": predicted,
        "pulls": pulls,
        "ndof": len(names) - len(res.x),
        "success": bool(res.success),
        "message": res.message,
    }


def perturbativity_cut(couplings: Mapping[str, float], bound: float = 4 * math.pi) -> bool:
    """True iff every named coupling satisfies ``|value| < bound`` (default ``4*pi``)."""
    return all(abs(_reject_sentinel(name, value)) < bound for name, value in couplings.items())


def bfb_single_quartic(lam: float) -> bool:
    """Bounded-from-below cut for a single quartic coupling: ``lam > 0``.

    Only the single-scalar case is generic enough to implement here; multi-scalar copositivity
    conditions (2HDM, singlet extensions, ...) are model-specific and out of scope for a generic
    helper -- write a model-specific vacuum-stability check instead of extending this one.
    """
    return _reject_sentinel("lam", lam) > 0


def unitarity_cut(*args, **kwargs) -> bool:
    """Partial-wave unitarity bound -- NOT implemented this session.

    Bounds like |Re a_0| < 1/2 (Lee-Quigg-Thacker-style) need per-process, per-model research
    (which 2->2 channel, which partial wave) that should not be fabricated in a skeleton pass.
    Open item: implement per-model when a real anomaly needs it; see docs/maturity.md.
    """
    raise NotImplementedError(
        "unitarity_cut is not implemented -- needs per-process partial-wave research, "
        "see module docstring"
    )
