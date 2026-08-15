# %% [markdown]
# # Shape log_ask like an OTel span
#
# Lab `lab_s15_prod` / `part_3`.

# %%
"""Shape log_ask like an OTel span."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.observe import REQUIRED_SPAN_FIELDS, log_ask, missing_span_fields, shape_span

span = shape_span(
    question="What does error code TS-999 mean?",
    pipeline="hybrid",
    chunk_ids=["error_catalog:rec:1"],
    model="extractive",
    latency_ms=12.4,
    tokens=80,
    usd=0.0,
)
missing = missing_span_fields(span)
print("missing", missing)
path = ROOT / "runs" / "ask.jsonl"
log_ask(span, path)
print("last_span_keys", sorted(span))
print("required", list(REQUIRED_SPAN_FIELDS))
print("wrote", path)
