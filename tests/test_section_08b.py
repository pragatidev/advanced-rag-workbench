from rag.chunkers import Chunk
from rag.rerank import skip_when_confident
from rag.retrieve import Hit


def _hit(score: float, cid: str = "x") -> Hit:
    ch = Chunk(chunk_id=cid, doc_id="d", title="t", text="body")
    return Hit(chunk=ch, score=score, source="dense")


def test_skip_when_confident_needs_peak_and_gap():
    assert skip_when_confident([_hit(0.31, "a"), _hit(0.06, "b")]) is True
    assert skip_when_confident([_hit(0.309, "a"), _hit(0.299, "b")]) is False
    assert skip_when_confident([_hit(0.20, "a"), _hit(0.00, "b")]) is False
    assert skip_when_confident([_hit(0.40, "a")]) is False
