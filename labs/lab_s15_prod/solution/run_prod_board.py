"""SOLUTION Two pipelines, USD, and traces."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import json
import time

from rag.cache import SemanticCache
from rag.eval.cost import estimate
from rag.observe import log_ask, missing_span_fields, shape_span
from rag.pipelines.hybrid import run_hybrid
from rag.pipelines.naive import run_naive

cache = SemanticCache()
q = "What does error code TS-999 mean?"
board = {"generate_calls": 0, "cache_hits": 0, "traces": []}
for name, fn in (("naive", run_naive), ("hybrid", run_hybrid)):
    look = cache.lookup(q)
    t0 = time.perf_counter()
    if look["status"] == "HIT":
        board["cache_hits"] += 1
        answer = look["answer"]
        hits = []
        gens = 0
    else:
        result = fn(q)
        answer = result["answer"]
        hits = result["hits"]
        gens = estimate(name)["generate_calls"]
        cache.store(q, answer)
    elapsed = (time.perf_counter() - t0) * 1000
    board["generate_calls"] += gens
    span = shape_span(
        question=q,
        pipeline=name,
        chunk_ids=[h["chunk_id"] for h in hits],
        model="extractive",
        latency_ms=elapsed,
        tokens=0,
        usd=0.0,
        cache_status=look["status"],
        generate_calls=gens,
    )
    assert not missing_span_fields(span)
    board["traces"].append(span)
    log_ask(span, ROOT / "runs" / "ask.jsonl")
# repeat hybrid: should HIT
look = cache.lookup(q)
if look["status"] == "HIT":
    board["cache_hits"] += 1
dest = ROOT / "runs" / "smoke" / "prod_board.json"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps(board, indent=2), encoding="utf-8")
print("generate_calls", board["generate_calls"], "cache_hits", board["cache_hits"])
print("traces", len(board["traces"]))
print("wrote", dest)
