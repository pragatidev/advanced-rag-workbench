"""Reference for exercises/ex_rrf.py."""

from __future__ import annotations

from rag.chunkers import Chunk
from rag.retrieve import Hit, rrf_fuse

RRF_K = 60


def rrf(lists: list[list[Hit]], k: int = RRF_K, top_n: int = 5) -> list[Hit]:
    return rrf_fuse(lists, k=k, top_n=top_n)


def _demo_hit(cid: str) -> Hit:
    return Hit(chunk=Chunk(cid, "d", "t", cid), score=0.0, source="ex")


if __name__ == "__main__":
    a = [_demo_hit("x"), _demo_hit("y")]
    b = [_demo_hit("y"), _demo_hit("z")]
    print([h.chunk.chunk_id for h in rrf([a, b])])
