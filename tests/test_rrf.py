from rag.chunkers import Chunk
from rag.retrieve import Hit, rrf_fuse


def _hit(cid: str, rank_score: float) -> Hit:
    return Hit(
        chunk=Chunk(chunk_id=cid, doc_id="d", title="t", text=cid),
        score=rank_score,
        source="x",
    )


def test_rrf_k60_formula():
    a = [_hit("x", 1.0), _hit("y", 0.5)]
    b = [_hit("y", 1.0), _hit("z", 0.5)]
    fused = rrf_fuse([a, b], k=60, top_n=3)
    scores = {h.chunk.chunk_id: h.score for h in fused}
    # y is rank 2 in A and rank 1 in B: 1/62 + 1/61
    assert abs(scores["y"] - (1 / 62 + 1 / 61)) < 1e-9
    # x is rank 1 in A only
    assert abs(scores["x"] - (1 / 61)) < 1e-9
