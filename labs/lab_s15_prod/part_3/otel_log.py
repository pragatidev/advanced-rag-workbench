"""Shape log_ask like an OTel span."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.observe import REQUIRED_SPAN_FIELDS, log_ask, missing_span_fields, shape_span

Q = "What does error code TS-999 mean?"
INPUT_TOKENS = 413
OUTPUT_TOKENS = 172
TOKENS = INPUT_TOKENS + OUTPUT_TOKENS
SCORE = 0.333

span = shape_span(
    question=Q,
    pipeline="hybrid",
    chunk_ids=["error_catalog:rec:1"],
    model="extractive",
    latency_ms=12.4,
    tokens=TOKENS,
    usd=0.0,
    extra={"scores": [SCORE]},
)
row = {name: span[name] for name in REQUIRED_SPAN_FIELDS}
row["scores"] = span["scores"]
missing = missing_span_fields(span)
print("=== one JSON row ===")
print(json.dumps(row, ensure_ascii=False))
print("missing", missing)
print("=== ticks ===")
for name in REQUIRED_SPAN_FIELDS:
    print("tick", name, "yes" if name in span else "no")
print("tick_count", sum(1 for n in REQUIRED_SPAN_FIELDS if n in span), "of", len(REQUIRED_SPAN_FIELDS))
print("trace_id_len", len(str(span["trace_id"])))
print("span_id_len", len(str(span["span_id"])))
print("name", span["name"])
print("latency_ms", span["latency_ms"])
print("gen_ai.request.model", span["gen_ai.request.model"])
print("tokens", span["tokens"])
print("usd", span["usd"])
print("chunk_ids", span["chunk_ids"])
print("scores", span["scores"])

thin = {"pipeline": "hybrid", "chunk_ids": ["error_catalog:rec:1"]}
print("=== thin JSONL ===")
print("keys", " ".join(sorted(thin)))
print("missing", missing_span_fields(thin))
print("tick_count", sum(1 for n in REQUIRED_SPAN_FIELDS if n in thin), "of", len(REQUIRED_SPAN_FIELDS))

path = ROOT / "runs" / "ask.jsonl"
log_ask(span, path)
print("wrote", path.relative_to(ROOT).as_posix())
