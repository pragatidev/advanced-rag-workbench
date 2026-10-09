"""STARTER Copy the S8.5 millisecond print onto a 2-second board. Fill the TODOs."""
from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# TODO: import skip_when_confident and the retrieve helpers this board needs

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.rerank import rerank_cross_encoder, skip_when_confident
from rag.retrieve import bm25_search, dense_search, rrf_fuse

# TODO: print the four-stage board, copy S8.5 rerank_ms onto it, mark one query SKIP

docs = load_documents()
chunks = chunk_corpus(docs, "recursive")
emb = HashEmbedder(semantic_mode=True)
q = "What does error code TS-999 mean?"
wide = rrf_fuse(
    [
        dense_search(q, chunks, embedder=emb, k=20),
        bm25_search(q, chunks, k=20),
    ],
    top_n=20,
)
t0 = time.perf_counter()
ranked, backend = rerank_cross_encoder(q, wide, keep=5)
rerank_ms = (time.perf_counter() - t0) * 1000.0
print("backend", backend)
print(f"rerank_ms {rerank_ms:.1f}")
hits = dense_search(q, chunks, embedder=emb, k=5)
print("decision", "SKIP" if skip_when_confident(hits) else "RERANK")
