# %% [markdown]
# # S16.1 Why pre-filter beats post-filter for access control
#
# Allowed ids are a stencil on the index before search.
# Post-filter checks hits after. A denied neighbor can take a slot.

# %%
"""S16.1: stencil vs retrieve-then-drop, denied never in prompt."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.gov import RLS_SQL, allowed, audit_row, denied_absent, prefilter
from rag.retrieve import bm25_search

docs = load_documents()
chunks = chunk_corpus(docs, "recursive")
query = "How do I reset my password?"
tenant = "helix-west"
k = 3
faq_ids = [c.chunk_id for c in chunks if c.doc_id == "faq"]

print("=== stencil ===")
print("all", len(chunks))
east = prefilter(chunks, "helix-east")
west = prefilter(chunks, "helix-west")
print("east", len(east), "west", len(west))
print("east > west", len(east) > len(west))
print("faq_ids", faq_ids)
print("faq_tenant", [c.metadata.get("tenant") for c in chunks if c.doc_id == "faq"])

print()
print("=== post-filter retrieve then drop ===")
raw = bm25_search(query, chunks, k=k)
print("query", query)
print("tenant", tenant)
print("post_k", k)
print("post_raw_ids", [h.chunk.chunk_id for h in raw])
print("post_raw_tenants", [h.chunk.metadata.get("tenant") for h in raw])
kept = [h for h in raw if allowed(h.chunk, tenant)]
dropped = [h.chunk.chunk_id for h in raw if not allowed(h.chunk, tenant)]
print("post_kept_ids", [h.chunk.chunk_id for h in kept])
print("post_dropped_ids", dropped)
print("post_slots_filled", len(kept), "of", k)
print("denied_took_a_slot", bool(dropped))

print()
print("=== pre-filter stencil then search ===")
allowed_set = prefilter(chunks, tenant)
print("pre_candidate_count", len(allowed_set))
print("faq_in_candidates", any(c.chunk_id in faq_ids for c in allowed_set))
hits = bm25_search(query, allowed_set, k=k)
print("pre_ids", [h.chunk.chunk_id for h in hits])
print("pre_tenants", [h.chunk.metadata.get("tenant") for h in hits])
print("pre_slots_filled", len(hits), "of", k)
prompt_chunks = [h.chunk for h in hits]
row = audit_row(query, prompt_chunks, tenant=tenant)
print("audit_chunk_ids", row["chunk_ids"])
print("denied_absent", denied_absent(row, faq_ids))

print()
print("=== RLS shape ===")
print(RLS_SQL)
