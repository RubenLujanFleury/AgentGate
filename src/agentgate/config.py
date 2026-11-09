"""Settings. Passed into constructors; never read from module-level globals."""

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Runtime settings for the app.

    commit_hash: the git commit the image was built from. GET /version returns it.
    database_url: Postgres connection string.

    Learn: frozen dataclasses (dataclasses module docs).
    """

    commit_hash: str
    database_url: str


def load_settings(env: Mapping[str, str]) -> Settings:
    """Build Settings from an environment mapping (pass os.environ from the caller).

    Reads AGENTGATE_COMMIT_HASH and DATABASE_URL.

    Failure modes: raises ValueError naming the variable if either one is missing.
    Tested for DATABASE_URL only; see tests/unit/test_config.py.

    Learn: the 12-factor config section on environment variables.
    """

    if "DATABASE_URL" not in env:
      raise ValueError("DATABASE_URL is required")

    if "AGENTGATE_COMMIT_HASH" not in env:
      raise ValueError("AGENTGATE_COMMIT_HASH is required")

    commit_hash = env["AGENTGATE_COMMIT_HASH"]
    database_url = env["DATABASE_URL"]

    return Settings(commit_hash, database_url)
    
    
