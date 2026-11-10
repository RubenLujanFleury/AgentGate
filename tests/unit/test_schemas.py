"""Specs for the unified chat schemas. Run: pytest tests/unit/test_schemas.py"""

import pytest
from pydantic import ValidationError

from agentgate.api.schemas import ChatRequest, ChatResponse, Message


def test_request_accepts_minimal_valid_body() -> None:
    req = ChatRequest.model_validate(
        {"model": "m", "messages": [{"role": "user", "content": "hi"}]}
    )

    assert req.temperature == 1
    assert req.max_tokens is None


def test_request_rejects_missing_messages() -> None:
    with pytest.raises(ValidationError):
        ChatRequest.model_validate({"model": "m"})


def test_request_rejects_empty_messages() -> None:
    with pytest.raises(ValidationError):
        ChatRequest.model_validate({"model": "m", "messages": []})


def test_request_rejects_bad_role() -> None:
    with pytest.raises(ValidationError):
        ChatRequest.model_validate(
            {"model": "m", "messages": [{"role": "bot", "content": "hi"}]}
        )


def test_request_rejects_out_of_range_temperature() -> None:
    with pytest.raises(ValidationError):
        ChatRequest.model_validate(
            {"model": "m", "messages": [{"role": "user", "content": "hi"}], "temperature": 3}
        )


def test_request_rejects_non_positive_max_tokens() -> None:
    with pytest.raises(ValidationError):
        ChatRequest.model_validate(
            {"model": "m", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 0}
        )


def test_message_keeps_extra_fields() -> None:
    msg = Message.model_validate({"role": "user", "content": "hi", "name": "ruben"})

    assert msg.model_dump()["name"] == "ruben"


def test_response_round_trips_openai_shape() -> None:
    body = {
        "id": "chatcmpl-1",
        "created": 1700000000,
        "model": "m",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": "hello"},
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 3, "completion_tokens": 2, "total_tokens": 5},
    }

    resp = ChatResponse.model_validate(body)

    assert resp.object == "chat.completion"
    assert resp.choices[0].message.content == "hello"
    assert resp.usage.total_tokens == 5


def test_response_rejects_missing_usage() -> None:
    with pytest.raises(ValidationError):
        ChatResponse.model_validate(
            {"id": "x", "created": 0, "model": "m", "choices": []}
        )
