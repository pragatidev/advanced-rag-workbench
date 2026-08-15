"""Copy .env.example and read settings.py."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.envload import require_env_file
from rag.settings import Settings, load_env

load_env()
require_env_file()
print("base_url", Settings.llm_base_url)
print("model", Settings.llm_model)
print("key_configured", Settings.has_api_key)
example = (ROOT / ".env.example").read_text(encoding="utf-8")
assert "qwen3.8-max" in example
assert "qwen3.8-max-preview" not in example
print("default generate id is qwen3.8-max")
