"""Entry point: `python -m agentgate`. Used by `make run` and the Dockerfile.

Not in the planning doc's tree. Added because uvicorn needs a runnable entry,
and create_app takes settings as an argument, so something has to build them.

"""

import os

import uvicorn

from agentgate.api.app import create_app
from agentgate.config import load_settings


def main() -> None:
    """Load settings from os.environ, build the app, and serve it on 0.0.0.0:8000.

    Contract: serves until stopped. Host and port are fixed for Week 1.

    Learn: uvicorn's programmatic API (uvicorn.run).
    """
    settings = load_settings(os.environ)
    app = create_app(settings)
    uvicorn.run(app, port=8000, host="0.0.0.0", log_level="info")

if __name__ == "__main__":
    main()
