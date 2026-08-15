"""Ollama, LM Studio, live generate ping."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.llm import ping
from rag.settings import OLLAMA_BASE_URL, LMSTUDIO_BASE_URL, OLLAMA_GENERATE_MODELS, Settings, load_env

load_env()
print("provider", Settings.llm_provider)
print("model", Settings.llm_model)
print("base", Settings.llm_base_url)
print("ollama", OLLAMA_BASE_URL, "models", ", ".join(OLLAMA_GENERATE_MODELS))
print("lmstudio", LMSTUDIO_BASE_URL, "model id is whatever GGUF you loaded")
result = ping("Reply with the single word pong.")
if result.get("skipped"):
    print(result.get("note") or "SKIPPED")
else:
    print("ping", result.get("text"))
    print("endpoint", result.get("endpoint"))
