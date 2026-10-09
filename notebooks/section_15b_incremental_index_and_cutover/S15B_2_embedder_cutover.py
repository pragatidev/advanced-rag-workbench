# %% [markdown]
# # S15B.2 Why a new embedder cannot query an old index
#
# A v3 query against a v1 column returns a cosine number and no error.
# Dual columns, then a feature-flag flip.

# %%
"""S15B.2: mixed-space retrieve, dual-column fill, feature-flag cutover."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.embed import cosine
from rag.cutover import DualColumnIndex, VersionedEmbedder

chunks = [
    ("policy", "Retention is seven days. That line is the live policy."),
    ("warehouse_00", "Warehouse throughput improved. Marketing spend was steady."),
    ("warehouse_01", "Seats by region east west north south. Padding about capacity."),
    ("error_catalog", "TS-999 means the billing ledger rejected a duplicate invoice ID."),
    ("privacy", "Customer email, phone, and national id are PII. Redact national id."),
    ("access", "Least privilege. Support may read email. National id stays redacted."),
    ("faq", "Reset the token, then retry the invoice. Do not invent a new id."),
    ("kpis", "Q2 seats east 4100 west 3900 north 2420 south 2000."),
]

query = "retention is seven days"
idx = DualColumnIndex()
v1 = VersionedEmbedder("v1")
v3 = VersionedEmbedder("v3")

print("=== same sentence, two versions ===")
same = "Retention is seven days. That line is the live policy."
print("text", same)
print("v1_vs_v3_cosine", round(float(cosine(v1.embed(same), v3.embed(same))), 4))
print("note same words. different coordinates. no error.")

idx.fill_column("v1", chunks, v1)
idx.fill_column("v3", chunks, v3)
idx.shadow = True

print()
print("=== same space (v1 query, v1 column) ===")
hits_same, meta_same = idx.retrieve(query, "v1", column="v1", k=3)
print("query", query)
print("query_version", meta_same["query_version"])
print("column", meta_same["column"])
print("mixed", meta_same["mixed"])
print("error_raised", meta_same["error_raised"])
print("top_id", hits_same[0][0])
print("top_score", round(hits_same[0][2], 4))
print("top_text", hits_same[0][1])

print()
print("=== mixed space (v3 query, v1 column) ===")
hits_mix, meta_mix = idx.retrieve(query, "v3", column="v1", k=3)
print("query", query)
print("query_version", meta_mix["query_version"])
print("column", meta_mix["column"])
print("mixed", meta_mix["mixed"])
print("error_raised", meta_mix["error_raised"])
print("top_id", hits_mix[0][0])
print("top_score", round(hits_mix[0][2], 4))
print("top_text", hits_mix[0][1])
print("same_space_top_id", hits_same[0][0])
print("mixed_matches_same_space", hits_mix[0][0] == hits_same[0][0])
print("note cosine still returns a number. no exception.")

print()
print("=== dual column fill ===")
print("v1_rows", len(idx.columns["v1"]))
print("v3_rows", len(idx.columns["v3"]))
print("live", idx.live)
print("shadow", idx.shadow)

print()
print("=== shadow traffic ===")
shadow_hits, shadow_meta = idx.retrieve(query, "v3", column="v3", k=1)
print("query_version", "v3")
print("live_column", idx.live)
print("shadow_column", "v3")
print("live_top", hits_mix[0][0])
print("shadow_top", shadow_hits[0][0])
print("agree", hits_mix[0][0] == shadow_hits[0][0])
print("shadow_error_raised", shadow_meta["error_raised"])

print()
print("=== feature flag cutover ===")
print("live_before", idx.live)
flipped = idx.flip("v3")
print("flip", flipped)
print("live_after", idx.live)
hits_live, meta_live = idx.retrieve(query, "v3", k=1)
print("query_version", meta_live["query_version"])
print("column", meta_live["column"])
print("mixed", meta_live["mixed"])
print("error_raised", meta_live["error_raised"])
print("top_id", hits_live[0][0])
print("top_score", round(hits_live[0][2], 4))
print("top_text", hits_live[0][1])
