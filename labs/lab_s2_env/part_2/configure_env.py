"""Copy .env.example and read settings.py (lab S2, part 2).

Proves two things on your machine: the .env file exists, and settings.py resolved it to a backend,
a base URL and a model id. The key is never printed, only whether one is set.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.envload import require_env_file
from rag.providers.hosted import door_for
from rag.settings import Settings, load_env

load_env()
require_env_file()
print("backend", Settings.api_backend)
print("base_url", Settings.llm_base_url)
print("model", Settings.llm_model)
print("door", door_for(Settings.llm_base_url, Settings.api_backend))
print("key_configured", Settings.has_api_key)

example = (ROOT / ".env.example").read_text(encoding="utf-8")
# .env.example documents all three doors; the repo itself has no vendor default
for door in ("LLM_BACKEND=anthropic", "LLM_BACKEND=openai", "http://localhost:11434/v1"):
    assert door in example, door
print("three doors documented in .env.example: anthropic, openai-compatible, local")
