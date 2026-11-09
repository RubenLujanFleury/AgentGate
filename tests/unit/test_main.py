"""Specs for main(). These fail until main() calls uvicorn.run."""

from typing import Any

import pytest
import uvicorn
from fastapi import FastAPI

from agentgate.__main__ import main


def test_main_serves_the_app_on_all_interfaces_port_8000(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/agentgate")
    monkeypatch.setenv("AGENTGATE_COMMIT_HASH", "abc1234")
    calls: list[tuple[Any, dict[str, Any]]] = []

    def fake_run(app: Any, **kwargs: Any) -> None:
        calls.append((app, kwargs))

    monkeypatch.setattr(uvicorn, "run", fake_run)

    main()

    assert len(calls) == 1
    app, kwargs = calls[0]
    assert isinstance(app, FastAPI)
    assert kwargs["host"] == "0.0.0.0"
    assert kwargs["port"] == 8000
