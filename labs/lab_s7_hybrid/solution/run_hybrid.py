"""SOLUTION Alpha swamp, then RRF, TS-999 board."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import json

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.pipelines.hybrid import run_hybrid
from rag.retrieve import alpha_hybrid, bm25_search, dense_search, rrf_fuse

docs = load_documents()
chunks = chunk_corpus(docs, "recursive")
q = "What does error code TS-999 mean?"
dense = dense_search(q, chunks, embedder=HashEmbedder(semantic_mode=True), k=8)
sparse = bm25_search(q, chunks, k=8)
print("alpha table (raw sparse can swamp cosine):")
for alpha in (0.1, 0.5, 0.9):
    fused = alpha_hybrid(dense, sparse, alpha=alpha, top_n=3)
    print(f"  alpha={alpha} top={fused[0].chunk.chunk_id} ts999={'TS-999' in fused[0].chunk.text}")
rrf = rrf_fuse([dense, sparse], top_n=16)
print("RRF TS-999", any("TS-999" in h.chunk.text for h in rrf))
result = run_hybrid(q)
blob = " ".join(h["text"] for h in result["hits"])
board = {"ts999_in_hybrid": "TS-999" in blob, "chunk_ids": [h["chunk_id"] for h in result["hits"]]}
dest = ROOT / "runs" / "smoke" / "hybrid_board.json"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps(board, indent=2), encoding="utf-8")
print("board", board)
print("wrote", dest)
