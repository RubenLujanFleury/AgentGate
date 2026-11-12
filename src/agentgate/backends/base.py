"""The Backend protocol: the one interface every model provider adapter implements.

Per gateway-plan.md section 6B, backends may import httpx, provider SDKs, and this
protocol. They must not import gateway or routing.
"""

from typing import Protocol

from agentgate.api.schemas import ChatRequest, ChatResponse


class Backend(Protocol):
    """A model provider that can complete a non-streaming chat request.

    Contract:
    - `complete` takes a validated ChatRequest and returns a ChatResponse in the
      OpenAI shape, whatever format the upstream provider uses.
    - `complete` does not retry, time out, or fall back. Those belong to
      resilience/ and routing/ (Weeks 4 and 9).
    - ASSUMED: `complete` is a coroutine, because the gateway runs on asyncio
      and Week 3 cancels upstream work by cancelling the task.

    Failure modes: upstream failures are raised as BackendError
    (backends/errors.py, next component). No raw provider exception or response
    body escapes the adapter.

    Tests: none. A protocol has no behavior to fail red. Its contract is tested
    through backends/fake.py (next component).

    Learn: typing.Protocol (structural typing); async def and asyncio tasks.
    """

    async def complete(self, request: ChatRequest) -> ChatResponse:
        raise NotImplementedError


        
