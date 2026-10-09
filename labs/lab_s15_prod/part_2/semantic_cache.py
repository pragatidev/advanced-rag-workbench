"""Cache hit, paraphrase, personalized skip."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.cache import SemanticCache

Q = "What does error code TS-999 mean?"
NEAR = "What does TS-999 mean?"
PERSONAL = "What does my invoice TS-999 mean?"
ANSWER = "Duplicate invoice. Do not retry."

cache = SemanticCache(threshold=0.92)
cache.store(Q, ANSWER)
exact = cache.lookup(Q)
near = cache.lookup(NEAR)
cache80 = SemanticCache(threshold=0.80)
cache80.store(Q, ANSWER)
near80 = cache80.lookup(NEAR)
skip = cache.lookup(PERSONAL, personalized=True)
print(exact["status"], "generate", exact["generate"], "sim", exact.get("sim"))
print("threshold_decision", near["status"], "sim", round(float(near.get("sim") or 0), 4), "threshold", cache.threshold)
print("maybe HIT status", near80["status"], "sim", round(float(near80.get("sim") or 0), 4), "threshold", cache80.threshold)
print(skip["status"], "generate", skip["generate"])
print("generate_calls on hit", 0 if exact["status"] == "HIT" else 1)
