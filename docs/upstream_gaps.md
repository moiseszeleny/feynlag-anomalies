# Proposed gaps in `feynlag` / `feynlag-models`

Issues discovered here that block work in `feynlag-anomalies` but belong upstream. Per `CLAUDE.md`
hard rule 4, nothing in either sibling repo is edited from this repo — these are proposals for the
user to act on (or not) in those repos directly.

## Open

### UG-2 — no per-component LaTeX names for field components (`feynlag`)

**Repo**: `feynlag`. **Discovered**: 2026-09-26, while rendering the neutrino_mass ladder's
SymPy output.

**Symptom**: a field's `tex=` argument only covers the whole field (`Field._repr_latex_`, e.g.
`L`). Its components are bare `IndexedBase`/`Symbol` objects named after `component_names`
(`nuL`, `eL`, `Gp`, `H0`), so `sympy.latex` of any operator, Lagrangian piece or mass matrix
prints those raw names. The same holds for components built inside `feynlag-models` models, which
this repo cannot rename.

**Workaround here**: `feynlag_anomalies/latex.py` maps names to LaTeX through SymPy's
`symbol_names` printer setting (render only). It works because feynlag's `Bilinear`/Dirac
`_latex` methods print their legs via `printer.doprint`. But every downstream repo needs its own
name map, kept in sync with each model's component names.

**Proposal**: a `component_tex=[...]` argument on `Field` (next to `component_names`), stored so
that `sympy.latex` picks it up without a caller-side map. For example, the component symbols
could carry a `_latex` override, or feynlag could expose a `symbol_names` dict for a model.
feynlag-models would then set it once per field. Not acted on without the user's approval.

## Resolved

### UG-1 — `feynlag-models` git dependency ships no model data files (packaging gap)

**Repo**: `feynlag-models`. **Discovered**: 2026-09-22, while verifying this session's build
(`uv sync --all-extras` + `uv run pytest`).

**Symptom**: installing `feynlag-models` as a normal (non-editable) dependency — exactly how
`feynlag-anomalies`' own `pyproject.toml` declares it
(`feynlag-models @ git+https://github.com/moiseszeleny/feynlag-models.git@2197f429...`), and how
anyone cloning `feynlag-anomalies` from GitHub would install it — builds and installs the
`feynlag_models` and `models` Python packages successfully, but every non-`.py` file under
`models/<id>/` (`metadata.yaml`, `README.md`, `NEXT_STEPS.md`, `outputs/`) is silently missing
from the installed package. `feynlag_models.MODELS_DIR` (`Path(__file__).resolve().parent.parent`)
correctly points at the installed package's `models/` directory, but that directory only contains
`__init__.py`/`model.py`/`tests/` — no `metadata.yaml`. Any call into
`feynlag_models.registry.build(model_id)` (or `.metadata(model_id)`) then fails:

```
FileNotFoundError: [Errno 2] No such file or directory:
  '<venv>/lib/python3.13/site-packages/models/seesaw_type1/metadata.yaml'
```

**Root cause** (confirmed by inspection, not guessed): `feynlag-models/pyproject.toml` has no
`[tool.setuptools.package-data]` / `include_package_data` declaration and no `MANIFEST.in`.
setuptools' default wheel build only bundles `.py` files for packages found via
`[tool.setuptools.packages.find]` — every non-Python file under `models/<id>/` is dropped.

**Confirmed not a workaround-able issue from this repo**: a local-path editable install
(`uv pip install -e ../feynlag-models`) does work around it (an editable install just points
imports back at the real source tree, so `metadata.yaml` etc. are found) — this repo's own tests
were verified against that local editable install after finding this gap. But that only works when
a local sibling checkout of `feynlag-models` exists on disk; it is not available to CI on GitHub
Actions or to anyone who `pip install`s this repo normally. An editable VCS install
(`uv pip install -e "git+https://...#egg=feynlag-models"`) — which *would* work in CI — is not
supported by `uv` (`error: Editable must refer to a local directory, not a Git URL`), so there is
no CI-viable workaround from this repo's side.

**Consequence for `feynlag-anomalies`**: `.github/workflows/fast.yml`, `anomalies/neutrino_mass`'s
`test_seesaw_bundle.py`/`test_checkpoints_pass.py::test_check_4_passes_with_canonical_answer`, and
`tests/test_schema.py::test_every_anomaly_validates[neutrino_mass]` will all fail on a clean
`uv sync` until this is fixed upstream. They were verified passing locally only via the
editable-install workaround above (see the end-of-session report for the exact verification run).

**Proposed fix** (in `feynlag-models`, needs the user's approval before anyone applies it): add a
`[tool.setuptools.package-data]` entry (e.g. `"models" = ["*/metadata.yaml", "*/README.md",
"*/NEXT_STEPS.md", "*/outputs/**"]`) or `include_package_data = true` + a `MANIFEST.in`, and
confirm with a clean (non-editable) install + `uv run pytest` after the fix.

**Status**: resolved on 2026-09-25 by feynlag-models PR #11 (merge `1dc5c11`), which adds
`[tool.setuptools.package-data]` for `models/*/metadata.yaml`, `README.md`, `NEXT_STEPS.md` and
`outputs/`. Checked there from a fresh venv with the built wheel installed non-editable, and here
after pinning `feynlag-models` to `1dc5c11`: a plain `uv sync` lists all six models.
