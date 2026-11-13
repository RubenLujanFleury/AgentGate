"""Scripted fake backend. The only backend unit tests may use.

Per gateway-plan.md section 6B (seams to test with fakes) and agentgate-weekly.md
Week 2. It satisfies the Backend protocol in backends/base.py structurally.
"""

from agentgate.api.schemas import ChatRequest, ChatResponse


class FakeBackend:
    """Returns pre-scripted ChatResponses, one per call, in the order given.

    Contract:
    - Constructed with a non-empty list of ChatResponse objects (the script).
    - Each complete() call returns the next scripted response.
    - The request is not used to choose the response. ASSUMED: request is
      accepted and ignored, because the fake only replays the script.
    - Makes no network calls.

    Failure modes:
    - Empty script at construction: ValueError. ASSUMED: fail at setup, so a
      test with no script never reaches complete().
    - complete() after the script is used up: RuntimeError. ASSUMED: this is a
      test-setup bug, not an upstream failure, so it is not BackendError.

    Learn: typing.Protocol (structural typing); test doubles.
    """

    def __init__(self, script: list[ChatResponse]) -> None:
        if not script:
            raise ValueError("Did not receive a response")
        self.script = script

    async def complete(self, request: ChatRequest) -> ChatResponse:
        if not self.script:
            raise RuntimeError("Unable to complete request")
        return self.script.pop(0)
