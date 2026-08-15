"""The only module that reads provider names, model ids, and base URLs.

Notebooks and labs import Settings. They never hard-code a model string.
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORE_ROOT = ROOT / "store"

# Official Model Studio International (Singapore). Not the unofficial token-plan host.
DEFAULT_LLM_BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
DEFAULT_LLM_MODEL = "qwen3.8-max"
DEFAULT_EMBED_MODEL = "nomic-embed-text"
DEFAULT_EMBED_MODEL_B = "text-embedding-3-large"
DEFAULT_RERANK_MODEL = "BAAI/bge-reranker-base"
WORKSPACE_BASE_URL = "https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1"
US_BASE_URL = "https://dashscope-us.aliyuncs.com/compatible-mode/v1"
OLLAMA_BASE_URL = "http://localhost:11434/v1"
LMSTUDIO_BASE_URL = "http://localhost:1234/v1"

# Verified laptop-capable Ollama tags (curriculum_gap_list.json, access 2026-08-15).
OLLAMA_GENERATE_MODELS = (
    "llama3.2:3b",
    "llama3.2:1b",
    "gemma3:4b",
    "qwen2.5:3b",
    "qwen2.5:7b",
    "phi4-mini",
)
OLLAMA_EMBED_MODELS = (
    "nomic-embed-text",
    "nomic-embed-text:v1.5",
    "mxbai-embed-large",
    "all-minilm",
)

# Lab embedder. Not a hosted semantic model. Named on purpose so the screen walk
# can say what is running and what you would swap on Monday.
LAB_EMBEDDER = {
    "name": "HashEmbedder",
    "dim": 64,
    "semantic_mode": True,
    "role": "lab stand-in",
    "why": (
        "Reproduces the TS-999 miss (rare IDs fade, 'error codes in general' ranks first) "
        "without downloading a 400MB model."
    ),
    "production_swap": [
        "nomic-embed-text",
        "OpenAI text-embedding-3-large",
        "sentence-transformers/all-MiniLM-L6-v2",
    ],
}

PROFILES = {
    "naive": {
        "chunker": "fixed",
        "chunk_kwargs": {"size": 80, "overlap": 0},
        "contextual": False,
        "search": "dense",
        "k": 3,
    },
    "hybrid": {
        "chunker": "recursive",
        "chunk_kwargs": {},
        "contextual": True,
        "search": "hybrid",
        "k": 4,
    },
}

_KEY_ENV_NAMES = (
    "RAGBENCH_API_KEY",
    "LLM_API_KEY",
    "DASHSCOPE_API_KEY",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "BAILIAN_TOKEN_PLAN_API_KEY",
    "GEMINI_API_KEY",
    "XAI_API_KEY",
    "DEEPSEEK_API_KEY",
)


def load_env(path: Path | None = None) -> None:
    """Read .env once. Never print values. Missing file is fine."""
    from rag.envload import load_dotenv

    load_dotenv(path)


def _first_env(*names: str, default: str = "") -> str:
    for name in names:
        val = os.environ.get(name)
        if val is not None and str(val).strip() != "":
            return str(val).strip()
    return default


class _Settings:
    """Live view of process env. Read attributes; do not cache a stale key."""

    @property
    def root(self) -> Path:
        return ROOT

    @property
    def llm_provider(self) -> str:
        return _first_env("RAGBENCH_PROVIDER", "LLM_PROVIDER", default="qwen").lower()

    @property
    def llm_base_url(self) -> str:
        return _first_env(
            "RAGBENCH_API_BASE",
            "RAGBENCH_BASE_URL",
            "LLM_BASE_URL",
            "ANTHROPIC_BASE_URL",
            default=DEFAULT_LLM_BASE_URL,
        ).rstrip("/")

    @property
    def llm_model(self) -> str:
        return _first_env(
            "RAGBENCH_MODEL",
            "LLM_MODEL",
            "ANTHROPIC_MODEL",
            default=DEFAULT_LLM_MODEL,
        )

    @property
    def api_key(self) -> str:
        return _first_env(*_KEY_ENV_NAMES, default="")

    @property
    def has_api_key(self) -> bool:
        key = self.api_key
        if not key:
            return False
        # Dummy keys used by local OpenAI-compat servers are not cloud secrets.
        if key.lower() in {"ollama", "lm-studio", "lmstudio", "not-needed", "none"}:
            return False
        return True

    @property
    def embed_model(self) -> str:
        return _first_env(
            "RAGBENCH_EMBED_MODEL",
            "EMBED_MODEL",
            default=DEFAULT_EMBED_MODEL,
        )

    @property
    def embed_model_b(self) -> str:
        return _first_env(
            "RAGBENCH_EMBED_MODEL_B",
            "EMBED_MODEL_B",
            default=DEFAULT_EMBED_MODEL_B,
        )

    @property
    def rerank_model(self) -> str:
        return _first_env("RERANK_MODEL", default=DEFAULT_RERANK_MODEL)

    @property
    def web_search_enabled(self) -> bool:
        raw = _first_env("WEB_SEARCH_ENABLED", "RAGBENCH_WEB_SEARCH", default="false")
        return raw.lower() in {"1", "true", "yes", "on"}

    @property
    def generate_mode(self) -> str:
        raw = _first_env("RAGBENCH_GENERATE", default="")
        if raw in {"extractive", "api"}:
            return raw
        return "api" if self.has_api_key else "extractive"

    @property
    def api_backend(self) -> str:
        explicit = _first_env("RAGBENCH_API_BACKEND", default="").lower()
        if explicit in {"anthropic", "openai"}:
            return explicit
        if self.llm_provider == "anthropic":
            return "anthropic"
        base = self.llm_base_url.lower()
        if "anthropic" in base:
            return "anthropic"
        return "openai"

    @property
    def is_local(self) -> bool:
        base = self.llm_base_url.lower()
        return "localhost" in base or "127.0.0.1" in base


Settings = _Settings()

__all__ = [
    "DEFAULT_EMBED_MODEL",
    "DEFAULT_EMBED_MODEL_B",
    "DEFAULT_LLM_BASE_URL",
    "DEFAULT_LLM_MODEL",
    "DEFAULT_RERANK_MODEL",
    "LAB_EMBEDDER",
    "LMSTUDIO_BASE_URL",
    "OLLAMA_BASE_URL",
    "OLLAMA_EMBED_MODELS",
    "OLLAMA_GENERATE_MODELS",
    "PROFILES",
    "ROOT",
    "STORE_ROOT",
    "Settings",
    "US_BASE_URL",
    "WORKSPACE_BASE_URL",
    "load_env",
]
