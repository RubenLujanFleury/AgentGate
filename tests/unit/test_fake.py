"""Specs for the scripted fake backend. Run: uv run pytest tests/unit/test_fake.py -q

These also check that FakeBackend satisfies the Backend protocol (the annotated
assignment below is checked by mypy, and the call runs at test time).
"""

import asyncio

import pytest

from agentgate.api.schemas import ChatRequest, ChatResponse, Choice, Message, Usage
from agentgate.backends.base import Backend
from agentgate.backends.fake import FakeBackend

REQUEST = ChatRequest(model="m", messages=[Message(role="user", content="hi")])


def _response(text: str) -> ChatResponse:
    return ChatResponse(
        id="chatcmpl-test",
        created=0,
        model="m",
        choices=[Choice(index=0, message=Message(role="assistant", content=text))],
        usage=Usage(prompt_tokens=1, completion_tokens=1, total_tokens=2),
    )


def test_complete_returns_scripted_response() -> None:
    backend = FakeBackend([_response("hello")])

    result = asyncio.run(backend.complete(REQUEST))

    assert result.choices[0].message.content == "hello"


def test_complete_returns_responses_in_script_order() -> None:
    backend = FakeBackend([_response("first"), _response("second")])

    first = asyncio.run(backend.complete(REQUEST))
    second = asyncio.run(backend.complete(REQUEST))

    assert first.choices[0].message.content == "first"
    assert second.choices[0].message.content == "second"


def test_empty_script_is_rejected() -> None:
    with pytest.raises(ValueError):
        FakeBackend([])


def test_complete_after_script_is_used_up_raises() -> None:
    backend = FakeBackend([_response("only")])
    asyncio.run(backend.complete(REQUEST))

    with pytest.raises(RuntimeError):
        asyncio.run(backend.complete(REQUEST))


def test_fake_satisfies_backend_protocol() -> None:
    backend: Backend = FakeBackend([_response("hi")])

    result = asyncio.run(backend.complete(REQUEST))

    assert result.choices[0].message.content == "hi"
