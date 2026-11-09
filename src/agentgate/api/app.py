"""
FastAPI app: GET /health and GET /version.
"""

from fastapi import FastAPI

from agentgate.config import Settings


def create_app(settings: Settings) -> FastAPI:
    """Build the FastAPI app from the given settings.

    Contract:
    - Takes settings as an argument. Does not read the environment or globals.
    - GET /health returns 200 while the process is up, with body {"message": "200"}.
    - GET /version returns 200 with body {"message": settings.commit_hash}.

    Failure modes: none defined yet.

    Learn: FastAPI application factories; FastAPI's TestClient.
    """

    app = FastAPI()

    @app.get("/health")
    def health() -> dict[str,str]:
      return {"message": "200"}

    @app.get("/version")
    def version() -> dict[str,str]:
      return {"message": settings.commit_hash}

    return app