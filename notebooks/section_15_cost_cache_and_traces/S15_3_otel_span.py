# %% [markdown]
# # S15.3 What an OTel-shaped trace must name per ask
#
# One span per ask. The names OpenTelemetry GenAI conventions use.
# Not a Langfuse install.

# %%
"""S15.3: shape one span, a thin JSONL row, and tick required fields."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.observe import REQUIRED_SPAN_FIELDS, missing_span_fields, shape_span

Q = "What does error code TS-999 mean?"
# Usage counts from the lecture 2.1 ask receipt,
# section_2/lecture_2_1 demo/ask_run_token_bill.txt. Not re-invented.
INPUT_TOKENS = 413
OUTPUT_TOKENS = 172
TOKENS = INPUT_TOKENS + OUTPUT_TOKENS

print("=== required names ===")
for name in REQUIRED_SPAN_FIELDS:
    print(name)

span = shape_span(
    question=Q,
    pipeline="hybrid",
    chunk_ids=["error_catalog:rec:1"],
    model="extractive",
    latency_ms=12.4,
    tokens=TOKENS,
    usd=0.0,
)
missing_full = missing_span_fields(span)
print()
print("=== full span ===")
print("missing", missing_full)
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

thin = {"pipeline": "hybrid", "chunk_ids": ["error_catalog:rec:1"]}
missing_thin = missing_span_fields(thin)
print()
print("=== thin JSONL ===")
print("keys", " ".join(sorted(thin)))
print("missing", missing_thin)
print("tick_count", sum(1 for n in REQUIRED_SPAN_FIELDS if n in thin), "of", len(REQUIRED_SPAN_FIELDS))

print()
print("=== live usage belongs on the span ===")
print("input_tokens", INPUT_TOKENS)
print("output_tokens", OUTPUT_TOKENS)
print("tokens", TOKENS)
print("usd", 0.0)
print("note local toy stack. replace with provider usage in live lectures.")
