# AgentGate

An LLM gateway: one HTTP API in front of several model backends, with routing,
resilience, rate limits, and an eval harness that gates changes in CI.

Status: Week 1 of 12. The skeleton, health endpoints, container, and CI are in
place. Routing, backends, and the rest arrive week by week; see `CHANGELOG.md`.

## Layout

```
src/agentgate/   application code (api/, config.py, ...)
tests/           unit tests (mirror src/agentgate)
deploy/          Caddy config for the VM
docs/            architecture notes and ADRs
```

## Development

Requires Python 3.12 and [uv](https://docs.astral.sh/uv/).

```
uv sync          # install dependencies
make check       # lint, types, import rules, tests
make run         # serve on http://127.0.0.1:8000
```

With Docker: `cp .env.example .env`, set `POSTGRES_PASSWORD`, then `docker compose up`.

## Endpoints

- `GET /health`: liveness.
- `GET /version`: the commit hash the image was built from.
