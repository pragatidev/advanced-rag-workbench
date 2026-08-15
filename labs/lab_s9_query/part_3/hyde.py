"""Run HyDE, throw the ghost away."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.query.hyde import hypothetical_document, run_hyde

q = "What was ACME revenue growth in Q2 2023?"
ghost = hypothetical_document(q)
print("ghost", ghost)
result = run_hyde(q)
print("hypothetical kept in result for teaching:", bool(result["hypothetical"]))
print("answer uses retrieved hits, not the ghost text as the answer source")
print("hits", [h["chunk_id"] for h in result["hits"]])
print("answer", result["answer"][:200])
