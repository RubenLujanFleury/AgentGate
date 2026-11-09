# 0001. One VM running Docker Compose, not a managed platform

Status: Accepted (Week 1)

## Context

AgentGate needs a public HTTPS endpoint, Postgres with backups, and an
observability stack (OpenTelemetry Collector, Prometheus, Grafana, a trace
backend). The stack has to run on a budget of zero or close to it.

## Decision

Run everything on one Linux VM under Docker Compose. Caddy terminates TLS and
is the only public port besides SSH. The VM is an Oracle Cloud Always Free Arm
instance (2 OCPU, 12 GB), with Hetzner as the fallback.

## Consequences

- Every image must build for `linux/arm64` and `linux/amd64`.
- Oracle can reclaim idle free instances, so a scheduled health check keeps traffic flowing.
- Backups and restore are our responsibility, not a managed service's.
- Moving to a managed platform later is a new ADR that supersedes this one.

## Alternatives considered

- A managed container platform: less to operate, but it hides the deployment
  mechanics this project is meant to demonstrate, and it costs money.
