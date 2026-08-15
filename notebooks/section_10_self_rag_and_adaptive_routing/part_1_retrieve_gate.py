# %% [markdown]
# # Retrieve only when the question needs the corpus
#
# Lab `lab_s10_route` / `part_1`.

# %%
"""Retrieve only when the question needs the corpus."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.loops.retrieve_gate import needs_corpus

pairs = [
    "Good morning, how are you?",
    "What does error code TS-999 mean?",
    "Thanks",
]
for q in pairs:
    print(repr(q), "needs_corpus", needs_corpus(q))
