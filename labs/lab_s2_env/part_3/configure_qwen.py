"""Point generate at Qwen Model Studio."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.providers import qwen
from rag.settings import Settings, load_env

load_env()
print("official_model", qwen.MODEL_ID)
print("legacy_intl", qwen.LEGACY_INTL)
print("workspace", qwen.WORKSPACE)
print("configured_base", Settings.llm_base_url)
print("configured_model", Settings.llm_model)
print("Free Quota Only: on")
print(qwen.FREE_QUOTA)
if not Settings.has_api_key:
    print("SKIPPED: no DASHSCOPE_API_KEY; live call not sent")
else:
    print("key present (not printed). Ready for part_4 ping.")
