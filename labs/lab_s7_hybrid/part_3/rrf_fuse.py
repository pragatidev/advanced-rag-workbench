"""Fuse with Reciprocal Rank Fusion."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.retrieve import RRF_K, bm25_search, dense_search, rrf_fuse

QUESTION = "What does error code TS-999 mean?"
HEADING = "error_catalog:rec:0"
TS999 = "error_catalog:rec:2"

docs = load_documents()
chunks = chunk_corpus(docs, "recursive")
dense = dense_search(QUESTION, chunks, embedder=HashEmbedder(semantic_mode=True), k=8)
sparse = bm25_search(QUESTION, chunks, k=8)
fused = rrf_fuse([dense, sparse], k=RRF_K, top_n=16)

print(f"formula RRFscore(d) = sum 1/(k + rank)  k={RRF_K}")
print("rank-1 contribution", round(1.0 / (RRF_K + 1), 6))
print("dense", [h.chunk.chunk_id for h in dense[:3]])
print("bm25 ", [h.chunk.chunk_id for h in sparse[:3]])
print("rrf  ", [h.chunk.chunk_id for h in fused[:5]])

dense_top = [h.chunk.chunk_id for h in dense[:3]]
bm25_top = [h.chunk.chunk_id for h in sparse[:3]]
rrf_top = [h.chunk.chunk_id for h in fused[:3]]
print("fused order is neither input list", rrf_top != dense_top and rrf_top != bm25_top)

for i, h in enumerate(fused[:8], 1):
    flag = "TS-999" in h.chunk.text
    print(f"  r{i} rrf={h.score:.6f} ts999={flag} {h.chunk.chunk_id}")


def rank_of(hits, cid):
    for i, h in enumerate(hits, 1):
        if h.chunk.chunk_id == cid:
            return i
    return None


hd_d = rank_of(dense, HEADING)
hd_s = rank_of(sparse, HEADING)
hd = next(h for h in fused if h.chunk.chunk_id == HEADING)
print("heading dense_rank", hd_d, "bm25_rank", hd_s, "two votes rrf", round(hd.score, 6))
print(
    "ts999 dense_rank",
    rank_of(dense, TS999),
    "bm25_rank",
    rank_of(sparse, TS999),
    "rrf_rank",
    rank_of(fused, TS999),
    "rrf_score",
    round(next(h.score for h in fused if h.chunk.chunk_id == TS999), 6),
)
print("fused set holds TS-999", any("TS-999" in h.chunk.text for h in fused))
print("missing lists contribute 0")
