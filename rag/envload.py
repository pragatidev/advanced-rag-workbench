"""Load a local .env if present. Never print values. .env is gitignored.

Name resolution lives in rag.settings. This module is the file loader plus
thin wrappers so older imports keep working.
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_dotenv(path: Path | None = None) -> None:
    env_path = path or (ROOT / ".env")
    if not env_path.is_file():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def require_env_file() -> Path:
    """Teach copy-to-.env without printing secrets."""
    env_path = ROOT / ".env"
    example = ROOT / ".env.example"
    if env_path.is_file():
        print(".env present. Values are not printed.")
    else:
        print("No .env file. Copy .env.example to .env, then set a key or a local base URL.")
        print("example:", example.as_posix())
    return env_path


def api_base() -> str:
    from rag.settings import Settings

    return Settings.llm_base_url


def api_key() -> str:
    from rag.settings import Settings

    return Settings.api_key


def api_model() -> str:
    from rag.settings import Settings

    return Settings.llm_model


def api_backend() -> str:
    from rag.settings import Settings

    return Settings.api_backend


def generate_mode(cli_value: str | None = None) -> str:
    from rag.settings import Settings

    if cli_value:
        mode = cli_value.strip().lower()
        if mode in {"extractive", "api"}:
            return mode
        return "extractive"
    return Settings.generate_mode
