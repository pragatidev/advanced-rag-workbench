"""Load a local .env if present. Never print values. .env is gitignored."""

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


def api_base() -> str:
    return (
        os.environ.get("RAGBENCH_API_BASE")
        or os.environ.get("ANTHROPIC_BASE_URL")
        or "https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1"
    ).rstrip("/")


def api_key() -> str:
    for name in (
        "RAGBENCH_API_KEY",
        "ANTHROPIC_API_KEY",
        "ANTHROPIC_AUTH_TOKEN",
        "BAILIAN_TOKEN_PLAN_API_KEY",
        "DASHSCOPE_API_KEY",
        "OPENAI_API_KEY",
    ):
        val = os.environ.get(name, "").strip()
        if val:
            return val
    return ""


def api_model() -> str:
    return (
        os.environ.get("RAGBENCH_MODEL")
        or os.environ.get("ANTHROPIC_MODEL")
        or "qwen3.8-max-preview"
    ).strip()


def api_backend() -> str:
    explicit = (os.environ.get("RAGBENCH_API_BACKEND") or "").strip().lower()
    if explicit in {"anthropic", "openai"}:
        return explicit
    base = api_base().lower()
    if "apps/anthropic" in base or "anthropic" in base:
        return "anthropic"
    return "openai"


def generate_mode(cli_value: str | None = None) -> str:
    if cli_value:
        mode = cli_value.strip().lower()
    elif os.environ.get("RAGBENCH_GENERATE"):
        mode = os.environ["RAGBENCH_GENERATE"].strip().lower()
    elif api_key():
        mode = "api"
    else:
        mode = "extractive"
    if mode not in {"extractive", "api"}:
        return "extractive"
    return mode
