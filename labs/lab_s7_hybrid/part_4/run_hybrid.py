"""Alpha swamp, then RRF, TS-999 board."""
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
from rag.retrieve import Hit, RRF_K, alpha_hybrid, bm25_search, dense_search, rrf_fuse

QUESTION = "What does error code TS-999 mean?"
HEADING = "error_catalog:rec:0"
TS999 = "error_catalog:rec:2"

docs = load_documents()
chunks = chunk_corpus(docs, "recursive")
dense = dense_search(QUESTION, chunks, embedder=HashEmbedder(semantic_mode=True), k=8)
sparse = bm25_search(QUESTION, chunks, k=8)

print("cosine range is about minus one to one. BM25 has no ceiling.")
print(f"dense rank-1 {dense[0].score:+.3f} {dense[0].chunk.chunk_id}")
print(f"bm25  rank-1 {sparse[0].score:.3f} {sparse[0].chunk.chunk_id}")
print(
    "sparse larger by",
    f"{sparse[0].score / max(abs(dense[0].score), 1e-9):.1f}x",
)


def unscaled_alpha(dense_hits, sparse_hits, alpha, top_n=8):
    """alpha * dense + (1-alpha) * sparse with NO min-max. The swamp."""
    dmap = {h.chunk.chunk_id: h.score for h in dense_hits}
    smap = {h.chunk.chunk_id: h.score for h in sparse_hits}
    by_id = {h.chunk.chunk_id: h.chunk for h in dense_hits + sparse_hits}
    fused = []
    for cid, chunk in by_id.items():
        score = alpha * dmap.get(cid, 0.0) + (1.0 - alpha) * smap.get(cid, 0.0)
        fused.append(Hit(chunk=chunk, score=score, source=f"unscaled:{alpha}"))
    fused.sort(key=lambda h: h.score, reverse=True)
    return fused[:top_n]


print("unscaled alpha=0.5  mix = 0.5*cosine + 0.5*bm25  (no min-max)")
swamp = unscaled_alpha(dense, sparse, alpha=0.5, top_n=5)
for i, h in enumerate(swamp, 1):
    d = next((x.score for x in dense if x.chunk.chunk_id == h.chunk.chunk_id), 0.0)
    s = next((x.score for x in sparse if x.chunk.chunk_id == h.chunk.chunk_id), 0.0)
    print(
        f"  r{i} mix={h.score:.3f} cosine={d:+.3f} bm25={s:.3f}"
        f" ts999={'TS-999' in h.chunk.text} {h.chunk.chunk_id}"
    )
print("unscaled top has TS-999", "TS-999" in swamp[0].chunk.text)
print("story: alpha 0.5 on raw scores still lets BM25 crush cosine")

print("scaled alpha table (min-max, then mix):")
for alpha in (0.1, 0.5, 0.9):
    fused = alpha_hybrid(dense, sparse, alpha=alpha, top_n=3)
    top = fused[0]
    print(
        f"  alpha={alpha} top={top.chunk.chunk_id}"
        f" score={top.score:.3f} ts999={'TS-999' in top.chunk.text}"
    )

rrf = rrf_fuse([dense, sparse], k=RRF_K, top_n=16)
print(f"formula RRFscore(d) = sum 1/(k + rank)  k={RRF_K}")
print("rrf ", [h.chunk.chunk_id for h in rrf[:5]])
print("RRF TS-999", any("TS-999" in h.chunk.text for h in rrf))
print(
    "ts999 rrf_rank",
    next(i for i, h in enumerate(rrf, 1) if h.chunk.chunk_id == TS999),
)
print(
    "heading rrf_rank",
    next(i for i, h in enumerate(rrf, 1) if h.chunk.chunk_id == HEADING),
)

result = run_hybrid(QUESTION)
blob = " ".join(h["text"] for h in result["hits"])
board = {
    "ts999_in_hybrid": "TS-999" in blob,
    "chunk_ids": [h["chunk_id"] for h in result["hits"]],
}
dest = ROOT / "runs" / "smoke" / "hybrid_board.json"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps(board, indent=2), encoding="utf-8")
print("board", board)
print("RRF board TS-999 true", board["ts999_in_hybrid"])
print("wrote", dest)
