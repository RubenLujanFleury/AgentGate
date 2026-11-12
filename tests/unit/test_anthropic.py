"""Specs for the Anthropic adapter. Run: uv run pytest tests/unit/test_anthropic.py -q

The HTTP layer is replaced with httpx2.MockTransport. No network calls happen.
"""

import asyncio
import json
from collections.abc import Callable

import httpx2
import pytest

from agentgate.api.schemas import ChatRequest, ChatResponse, Message
from agentgate.backends.anthropic import AnthropicBackend
from agentgate.backends.errors import BackendError

API_KEY = "sk-test-secret-key"


def _reply(text: str = "hello") -> dict[str, object]:
    return {
        "id": "msg_1",
        "type": "message",
        "role": "assistant",
        "model": "claude-test",
        "content": [{"type": "text", "text": text}],
        "stop_reason": "end_turn",
        "usage": {"input_tokens": 3, "output_tokens": 2},
    }


def _backend(handler: Callable[[httpx2.Request], httpx2.Response]) -> AnthropicBackend:
    client = httpx2.AsyncClient(transport=httpx2.MockTransport(handler))
    return AnthropicBackend(api_key=API_KEY, client=client)


def _request(*messages: Message, max_tokens: int | None = None) -> ChatRequest:
    return ChatRequest(model="claude-test", messages=list(messages), max_tokens=max_tokens)


def test_complete_returns_text_and_usage() -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(200, json=_reply("hello"))

    backend = _backend(handler)
    result = asyncio.run(backend.complete(_request(Message(role="user", content="hi"))))

    assert isinstance(result, ChatResponse)
    assert result.choices[0].message.content == "hello"
    assert result.usage.total_tokens == 5


def test_system_message_moves_to_top_level_field() -> None:
    sent: dict[str, object] = {}

    def handler(request: httpx2.Request) -> httpx2.Response:
        sent.update(json.loads(request.content))
        return httpx2.Response(200, json=_reply())

    backend = _backend(handler)
    asyncio.run(
        backend.complete(
            _request(
                Message(role="system", content="be brief"),
                Message(role="user", content="hi"),
            )
        )
    )

    assert sent["system"] == "be brief"
    assert sent["messages"] == [{"role": "user", "content": "hi"}]


def test_missing_max_tokens_sends_default() -> None:
    sent: dict[str, object] = {}

    def handler(request: httpx2.Request) -> httpx2.Response:
        sent.update(json.loads(request.content))
        return httpx2.Response(200, json=_reply())

    backend = _backend(handler)
    asyncio.run(backend.complete(_request(Message(role="user", content="hi"))))

    assert sent["max_tokens"] == 1024


def test_non_2xx_becomes_backend_error_without_leaking_details() -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(500, text=f"upstream said {API_KEY}")

    backend = _backend(handler)

    with pytest.raises(BackendError) as excinfo:
        asyncio.run(backend.complete(_request(Message(role="user", content="hi"))))

    assert excinfo.value.status_code == 500
    assert API_KEY not in str(excinfo.value)
    assert "upstream said" not in str(excinfo.value)


def test_timeout_becomes_backend_error() -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        raise httpx2.TimeoutException("timed out")

    backend = _backend(handler)

    with pytest.raises(BackendError):
        asyncio.run(backend.complete(_request(Message(role="user", content="hi"))))


def test_malformed_reply_becomes_backend_error() -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(200, json={"unexpected": True})

    backend = _backend(handler)

    with pytest.raises(BackendError):
        asyncio.run(backend.complete(_request(Message(role="user", content="hi"))))


def test_tool_role_is_rejected_before_any_call() -> None:
    calls: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        calls.append(request)
        return httpx2.Response(200, json=_reply())

    backend = _backend(handler)

    with pytest.raises(ValueError):
        asyncio.run(backend.complete(_request(Message(role="tool", content="x"))))
    assert calls == []
