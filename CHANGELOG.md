# Changelog

One line per week: what shipped, and what slipped.

## Week 1 · 9–15 Nov · Skeleton, VM, and TLS (in progress)

- Shipped: repo layout, FastAPI app stub (`/health`, `/version`), Dockerfile and compose, CI workflow, import-linter rules, Caddy config, ADR 0001.
- Slipped: VM provisioning, DNS, and TLS are not verified yet; the app stubs raise `NotImplementedError` until implemented.
