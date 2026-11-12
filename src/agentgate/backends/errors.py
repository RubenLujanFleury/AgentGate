"""Normalized error raised by every backend adapter.

Per agentgate-weekly.md Week 2: "Map upstream errors to a normalized error type."
The gateway handles this type. It never sees a raw provider exception.
"""


class BackendError(Exception):
    """An upstream model call failed. Carries no provider detail.

    Contract:
    - `message` is fixed, human-readable text written by the adapter. It never
      contains the provider's response body, headers, or the API key.
    - `status_code` is the upstream HTTP status when there was one, else None.
      ASSUMED: the gateway needs the status to choose retry behavior in Week 9.

    Learn: exception subclassing; why error detail is redacted at the boundary.
    """

    status_code: int | None

    def __init__(self, message: str, status_code: int | None = None) -> None:
        raise NotImplementedError
