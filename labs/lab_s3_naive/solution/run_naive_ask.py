"""SOLUTION Retrieve, generate, read the naive answer."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.ask import run_ask
from rag.pipelines.naive import NaivePipeline

pipe = NaivePipeline()
result = pipe("What did ACME revenue do last quarter?")
print("answer", result["answer"])
print("chunk_ids", [h["chunk_id"] for h in result["hits"]])
print("answer_source", result["answer_source"])
assert result["answer_source"] == "retrieved_text"

via_door = run_ask("What did ACME revenue do last quarter?", pipeline="naive", generate="extractive")
print("run_ask", via_door["answer"][:120])
