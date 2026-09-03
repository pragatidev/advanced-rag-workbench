"""The two hosted doors this course teaches, as facts the labs can print.

Everything here mirrors .env.example. The code path is the same for both doors; only the four
environment variables change. Model ids are the ones on the vendors' model pages on 2026-09-01;
confirm before relying on any id, vendors retire them.
"""

from __future__ import annotations

ANTHROPIC = {
    "door": "anthropic",
    "backend": "anthropic",
    "base_url": "https://api.anthropic.com",
    "models": ("claude-haiku-4-5", "claude-sonnet-5", "claude-opus-5"),
    "default_model": "claude-haiku-4-5",
    "key_prefix": "sk-ant-",
    "docs": "https://docs.anthropic.com/en/api/messages",
    "note": "Native Anthropic Messages API, so LLM_BACKEND=anthropic. Anthropic serves no embeddings; keep EMBED_MODEL local.",
}

OPENAI = {
    "door": "openai",
    "backend": "openai",
    "base_url": "https://api.openai.com/v1",
    "models": ("gpt-5.6-luna", "gpt-5.6-terra", "gpt-5.6-sol"),
    "default_model": "gpt-5.6-luna",
    "key_prefix": "sk-",
    "docs": "https://platform.openai.com/docs/api-reference",
    "note": "OpenAI chat format, so LLM_BACKEND=openai. Any vendor that speaks this format uses the same four variables.",
}

ENV_NAMES = ("LLM_BACKEND", "LLM_BASE_URL", "LLM_MODEL", "LLM_API_KEY")


def doors() -> tuple[dict, dict]:
    return ANTHROPIC, OPENAI


def door_for(base_url: str, backend: str) -> str:
    """Name the door a configured base URL + backend points at. Never guesses a vendor name from nothing."""
    b = (base_url or "").lower()
    if backend == "anthropic" or "anthropic" in b:
        return "anthropic"
    if "openai.com" in b:
        return "openai"
    if "localhost" in b or "127.0.0.1" in b:
        return "local"
    return "openai-compatible"
