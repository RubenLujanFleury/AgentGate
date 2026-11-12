"""Anthropic Messages API adapter. Implements the Backend protocol (backends/base.py).

Per gateway-plan.md section 6B, this module may import httpx2 and the Backend
protocol. It must not import gateway or routing. Per agentgate-weekly.md Week 4
and REPO-STRUCTURE.md, the adapter file is anthropic.py; it is built now because
Claude is the first backend the product needs (Week 2 build list says hosted.py,
which this replaces).
"""

import httpx2

from agentgate.api.schemas import ChatRequest, ChatResponse
from agentgate.backends.errors import BackendError  # noqa: F401  # remove noqa once complete() raises it


class AnthropicBackend:
    """Calls the Anthropic Messages API and returns an OpenAI-shaped ChatResponse.

    Contract:
    - `complete` sends one non-streaming POST to `{base_url}/v1/messages`.
    - Request mapping: messages with role "system" move to the top-level
      `system` field. The remaining messages are sent in order. `max_tokens` is
      required upstream, so when the request has none, `default_max_tokens` is
      sent. ASSUMED: default_max_tokens is 1024 unless the caller sets it.
    - Auth: the key goes in the `x-api-key` header, with the `anthropic-version`
      header set. The key is never logged or placed in an exception message.
    - Response mapping: text blocks of the reply are joined into one assistant
      message. `usage` maps input_tokens to prompt_tokens, output_tokens to
      completion_tokens, and their sum to total_tokens. ASSUMED: stop_reason
      maps end_turn to "stop" and max_tokens to "length", the OpenAI names.
    - No retries, no fallback. Those belong to resilience/ (Week 9).

    Failure modes (all raised as BackendError, with fixed message text):
    - Non-2xx HTTP status: BackendError with status_code set. The provider's
      body is not included in the message.
    - Timeout or connection failure (httpx2.TransportError, including timeouts):
      BackendError with status_code None.
    - Reply missing the expected fields, or not JSON: BackendError with
      status_code None.
    - Request contains role "tool": ASSUMED to be out of scope until Week 5, so
      it raises ValueError before any network call.

    Tests: tests/unit/test_anthropic.py mocks the HTTP layer with
    httpx2.MockTransport, which is the only way unit tests reach this adapter.

    Learn: httpx2.AsyncClient and dependency injection of the client; the
    Anthropic Messages API request and response shape.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.anthropic.com",
        client: httpx2.AsyncClient | None = None,
        timeout_seconds: float = 30.0,
        default_max_tokens: int = 1024,
    ) -> None:
        raise NotImplementedError

    async def complete(self, request: ChatRequest) -> ChatResponse:
        raise NotImplementedError


def _to_messages_payload(request: ChatRequest, default_max_tokens: int) -> dict[str, object]:
    """Build the Messages API JSON body from a ChatRequest.

    Contract: returns a dict with `model`, `max_tokens`, `messages`, and,
    when there are system messages, `system`. Temperature is passed through
    when set. Raises ValueError on role "tool" (see AnthropicBackend).

    Learn: the Messages API top-level `system` field versus OpenAI's system role.
    """
    raise NotImplementedError


def _from_messages_reply(reply: dict[str, object], model: str) -> ChatResponse:
    """Map a Messages API reply to a ChatResponse.

    Contract: joins text blocks, maps usage and stop_reason as in
    AnthropicBackend. Raises BackendError(status_code=None) when `content` or
    `usage` is missing or has the wrong type.

    Learn: content blocks as a list of typed dicts.
    """
    raise NotImplementedError
