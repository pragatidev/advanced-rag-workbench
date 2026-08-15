"""Coding exercise: fuse two ranked lists with Reciprocal Rank Fusion.

Fill in rrf(). Tests import the solution or this file.
"""

from __future__ import annotations

from rag.chunkers import Chunk
from rag.retrieve import Hit

RRF_K = 60


def rrf(lists: list[list[Hit]], k: int = RRF_K, top_n: int = 5) -> list[Hit]:
    # TODO: score each chunk as sum 1/(k + rank) with 1-based ranks
    # TODO: sort descending and return top_n
    raise NotImplementedError("implement Reciprocal Rank Fusion")


def _demo_hit(cid: str) -> Hit:
    return Hit(chunk=Chunk(cid, "d", "t", cid), score=0.0, source="ex")


if __name__ == "__main__":
    a = [_demo_hit("x"), _demo_hit("y")]
    b = [_demo_hit("y"), _demo_hit("z")]
    print(rrf([a, b]))
