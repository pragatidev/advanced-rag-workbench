"""STARTER Watch dense miss TS-999. Fill the TODOs. part_1 is the first working slice."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# TODO: import the package symbols this lab needs

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.retrieve import dense_search

QUESTION = "What does error code TS-999 mean?"

docs = load_documents()
chunks = chunk_corpus(docs, "recursive")
ranked = dense_search(
    QUESTION,
    chunks,
    embedder=HashEmbedder(semantic_mode=True),
    k=len(chunks),
)
print("chunks", len(chunks))
print("dense top:")
for h in ranked[:5]:
    flag = "TS-999" in h.chunk.text
    print(f"  {h.score:.3f} ts999={flag} {h.chunk.chunk_id}")
    print("   ", h.chunk.text[:140].replace("\n", " "))
print("top_is_ts999", "TS-999" in ranked[0].chunk.text)
gen_hit = None
ts_hit = None
gen_rank = None
ts_rank = None
for i, h in enumerate(ranked, 1):
    if gen_rank is None and "error codes in general" in h.chunk.text.lower():
        gen_rank = i
        gen_hit = h
    if ts_rank is None and h.chunk.chunk_id == "error_catalog:rec:2":
        ts_rank = i
        ts_hit = h
print("general_guidance_rank", gen_rank, "score", round(gen_hit.score, 3))
print("  ", gen_hit.chunk.text.replace("\n", " ")[:180])
print("ts999_rank", ts_rank, "score", round(ts_hit.score, 3), "of", len(ranked))
print("  ", ts_hit.chunk.text.replace("\n", " ")[:180])
