"""Specs for load_settings."""

import pytest

from agentgate.config import Settings, load_settings


def test_builds_settings_from_environment() -> None:
    env = {
        "AGENTGATE_COMMIT_HASH": "abc1234",
        "DATABASE_URL": "postgresql://user:pass@localhost:5432/agentgate",
    }

    settings = load_settings(env)

    assert settings == Settings(
        commit_hash="abc1234",
        database_url="postgresql://user:pass@localhost:5432/agentgate",
    )


def test_missing_database_url_raises_and_names_the_variable() -> None:
    env = {"AGENTGATE_COMMIT_HASH": "abc1234"}

    with pytest.raises(ValueError, match="DATABASE_URL"):
        load_settings(env)


def test_missing_commit_hash_raises_and_names_the_variable() -> None:
    env = {"DATABASE_URL": "postgresql://user:pass@localhost:5432/agentgate"}

    with pytest.raises(ValueError, match="AGENTGATE_COMMIT_HASH"):
        load_settings(env)
