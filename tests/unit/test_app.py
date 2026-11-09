"""Specs for the Week 1 HTTP endpoints. These fail until create_app is implemented."""

from fastapi.testclient import TestClient

from agentgate.api.app import create_app
from agentgate.config import Settings

SETTINGS = Settings(commit_hash="abc1234", database_url="postgresql://unused")


def test_health_returns_200() -> None:
    client = TestClient(create_app(SETTINGS))

    assert client.get("/health").status_code == 200


def test_version_returns_commit_hash() -> None:
    client = TestClient(create_app(SETTINGS))

    response = client.get("/version")

    assert response.status_code == 200
    assert "abc1234" in response.text
