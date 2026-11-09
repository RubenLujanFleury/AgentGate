# Architecture

Status: Week 1. Only the edge exists so far (`api/app.py`, `config.py`).

The full design is in `Planning Docs/gateway-plan.md` (section 3, architecture)
and the module-by-module allowed-imports table in section 6B. The import rules
are enforced in CI by the `import-linter` contracts in `pyproject.toml`.

Dependencies point inward: HTTP at the edge, logic in the middle, adapters at
the outside. Config is passed into constructors, never read from module globals.

Updated each week; the final version lands in Week 12.
