"""Retrieve only when the question needs the corpus."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
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
