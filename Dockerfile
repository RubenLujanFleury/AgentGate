FROM python:3.12-slim

# uv pinned to the version used locally (0.11.7).
COPY --from=ghcr.io/astral-sh/uv:0.11.7 /uv /usr/local/bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Dependencies first, so this layer caches while source changes.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY src ./src
RUN uv sync --frozen --no-dev

ARG GIT_COMMIT=unknown
ENV AGENTGATE_COMMIT_HASH=$GIT_COMMIT

EXPOSE 8000
CMD ["python", "-m", "agentgate"]
