.PHONY: sync test lint typecheck imports check run docker-build

sync:
	uv sync

test:
	uv run pytest

lint:
	uv run ruff check .

typecheck:
	uv run mypy

imports:
	uv run lint-imports

check: lint typecheck imports test

run:
	uv run python -m agentgate

# Multi-arch build. Multi-platform builds need --push to a registry, or a
# per-platform --load, because Docker can't load a multi-arch image locally.
docker-build:
	docker buildx build --platform linux/amd64,linux/arm64 \
		--build-arg GIT_COMMIT=$$(git rev-parse --short HEAD) \
		-t agentgate:dev .
