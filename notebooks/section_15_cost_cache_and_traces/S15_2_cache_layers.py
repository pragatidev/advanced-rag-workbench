# %% [markdown]
# # S15.2 Why a semantic cache has three layers, and one skip
#
# Exact string. Nearby embedding. Provider prompt cache. Personalized skip.

# %%
"""S15.2: exact HIT, nearby threshold, personalized skip, prompt-cache fields."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.cache import SemanticCache

Q = "What does error code TS-999 mean?"
NEAR = "What does TS-999 mean?"
PERSONAL = "What does my invoice TS-999 mean?"
ANSWER = "Duplicate invoice. Do not retry."

cache = SemanticCache(threshold=0.92)
cache.store(Q, ANSWER)

print("=== exact string ===")
exact = cache.lookup(Q)
print("status", exact["status"], "generate", exact["generate"], "sim", exact.get("sim"))
print("answer", exact["answer"])
print("generate_calls on hit", 0 if exact["status"] == "HIT" else 1)

print()
print("=== nearby embedding, threshold 0.92 ===")
near = cache.lookup(NEAR)
print("question", NEAR)
print("sim", round(float(near.get("sim") or 0), 4))
print("status", near["status"], "generate", near["generate"])
print("threshold", cache.threshold)

print()
print("=== same paraphrase if threshold were 0.80 ===")
cache80 = SemanticCache(threshold=0.80)
cache80.store(Q, ANSWER)
near80 = cache80.lookup(NEAR)
print("sim", round(float(near80.get("sim") or 0), 4))
print("status", near80["status"], "generate", near80["generate"])
print("threshold", cache80.threshold)

print()
print("=== personalized skip ===")
skip = cache.lookup(PERSONAL, personalized=True)
print("question", PERSONAL)
print("status", skip["status"], "generate", skip["generate"])
print("answer", skip["answer"])

print()
print("=== provider prompt cache (usage object, 2.1) ===")
# 2.1 capture, 2026-08-16, course_repo venv lane. Not re-invented.
print("cache_creation_input_tokens", 0)
print("cache_read_input_tokens", 0)
print("cached_tokens", 0)
print("note still generate, cheaper prefix when the provider hits")
