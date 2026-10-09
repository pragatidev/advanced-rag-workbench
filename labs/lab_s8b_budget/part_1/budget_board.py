"""Copy the S8.5 millisecond print onto a 2-second board and mark one query SKIP."""
from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.rerank import rerank_cross_encoder, skip_when_confident
from rag.retrieve import bm25_search, dense_search, rrf_fuse

BOARD_MS = {
    "embed": "50-100",
    "retrieve": "50-150",
    "rerank": "100-300",
    "first_token": "300-800",
}
BUDGET_MS = 2000
RERANK_LINE_MAX = 300
SKIP_MIN_TOP = 0.25
SKIP_MIN_GAP = 0.20
Q_FACT = "What does error code TS-999 mean?"
Q_HARD = "How should support handle a billing duplicate?"

docs = load_documents()
chunks = chunk_corpus(docs, "recursive")
emb = HashEmbedder(semantic_mode=True)

t_emb = time.perf_counter()
emb.embed(Q_FACT)
embed_ms = (time.perf_counter() - t_emb) * 1000.0

t_ret = time.perf_counter()
wide = rrf_fuse(
    [
        dense_search(Q_FACT, chunks, embedder=emb, k=20),
        bm25_search(Q_FACT, chunks, k=20),
    ],
    top_n=20,
)
retrieve_ms = (time.perf_counter() - t_ret) * 1000.0

t_rr = time.perf_counter()
ranked, backend = rerank_cross_encoder(Q_FACT, wide, keep=5)
rerank_ms = (time.perf_counter() - t_rr) * 1000.0

print("board embed", BOARD_MS["embed"], "retrieve", BOARD_MS["retrieve"], "rerank", BOARD_MS["rerank"], "first_token", BOARD_MS["first_token"])
print("budget_ms", BUDGET_MS)
print("backend", backend)
print("chunks", len(chunks), "wide", len(wide), "kept", len(ranked))
print(f"embed_ms {embed_ms:.1f}")
print(f"retrieve_ms {retrieve_ms:.1f}")
print(f"rerank_ms {rerank_ms:.1f}")
print("first_token_ms not-measured")
print("rerank_vs_board", "UNDER" if rerank_ms < RERANK_LINE_MAX else "OVER")

for name, q in (("Q_FACT", Q_FACT), ("Q_HARD", Q_HARD)):
    hits = dense_search(q, chunks, embedder=emb, k=5)
    top = hits[0].score
    gap = hits[0].score - hits[1].score
    skip = skip_when_confident(hits, min_top=SKIP_MIN_TOP, min_gap=SKIP_MIN_GAP)
    print(f"query {name} {q}")
    print(f"  first_top {top:.3f} first_gap {gap:.3f} {hits[0].chunk.chunk_id}")
    print(f"  decision {'SKIP' if skip else 'RERANK'}")
