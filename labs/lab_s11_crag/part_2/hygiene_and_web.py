"""Hygiene prompt and web search off."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.generate import HYGIENE
from rag.loops.crag import WEB_SEARCH_ENABLED, maybe_web

print("hygiene", HYGIENE)
print("WEB_SEARCH_ENABLED", WEB_SEARCH_ENABLED)
print("maybe_web", maybe_web("What is ACME revenue?"))
assert WEB_SEARCH_ENABLED is False
assert maybe_web("x") is None
