"""Cache hit, paraphrase, personalized skip."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.cache import SemanticCache

cache = SemanticCache(threshold=0.92)
cache.store("What does error code TS-999 mean?", "Duplicate invoice. Do not retry.")
exact = cache.lookup("What does error code TS-999 mean?")
near = cache.lookup("What does error code TS-999 mean?")
skip = cache.lookup("What does my invoice TS-999 mean?", personalized=True)
print(exact["status"], "generate", exact["generate"])
print("threshold_decision", near["status"], near.get("sim"))
print(skip["status"])
print("generate_calls on hit", 0 if exact["status"] == "HIT" else 1)
