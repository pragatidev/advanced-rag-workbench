"""Route none, single, multi, and source."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.query.router import route

questions = [
    "Good morning, how are you?",
    "What was ACME revenue growth in Q2 2023?",
    "What are the main themes in this ACME corpus?",
    "What does error code TS-999 mean?",
]
for q in questions:
    print(route(q), q)
