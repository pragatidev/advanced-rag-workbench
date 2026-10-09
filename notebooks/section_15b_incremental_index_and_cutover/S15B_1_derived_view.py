# %% [markdown]
# # S15B.1 The index is a derived view: upsert and tombstone
#
# Change-driven embed. One file walks to the embedder. Tombstone the old id.

# %%
"""S15B.1: warehouse arithmetic, one-file upsert, tombstone, stale retrieve."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.embed import ToyEmbedder
from rag.incremental import DerivedIndex

print("=== warehouse arithmetic (RisingWave example math) ===")
docs = 50000
changed = 500
print("docs", docs)
print("changed", changed)
print("percent", round(100.0 * changed / docs, 1))
print("embed_calls_nightly", docs)
print("embed_calls_change_driven", changed)
print("factor", str(docs // changed) + "x")
print("note RisingWave example math. Not this corpus.")

idx = DerivedIndex(ToyEmbedder(semantic_mode=False))
for i in range(50):
    idx.upsert(f"doc_{i:02d}", f"warehouse file {i} is unchanged padding about seats and revenue.")
old_text = "Retention is thirty days. That line is the old policy."
new_text = "Retention is seven days. That line is the live policy."
old_id = idx.upsert("policy", old_text)
print()
print("=== derived view ===")
print("source_docs", 51)
print("index_live", sum(1 for r in idx.rows.values() if r.live))
print("embed_calls_full_build", idx.embed_calls)

print()
print("=== one file lights up ===")
print("changed_file", "policy.md")
before = idx.embed_calls
new_id = idx.upsert("policy", new_text)
idx.tombstone(old_id)
print("files_to_embedder", idx.embed_calls - before)
print("embed_calls_this_change", idx.embed_calls - before)
print("old_id", old_id)
print("new_id", new_id)
print("tombstoned", 1)
print("live_after", sum(1 for r in idx.rows.values() if r.live))

print()
print("=== retrieve stale ===")
query = "retention is thirty days"
hits = idx.retrieve(query, k=3)
ids = [h[0] for h in hits]
print("query", query)
print("stale_id_present", old_id in ids)
print("top_id", hits[0][0] if hits else "NONE")
print("top_text", hits[0][1] if hits else "NONE")
