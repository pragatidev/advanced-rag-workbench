"""Coding exercise: find the fixed chunk that holds 3 percent but not ACME."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import Chunk, chunk_corpus
from rag.corpus import load_documents


def find_orphan() -> Chunk:
    # TODO: fixed size=80 overlap=0, return the chunk with "revenue grew by 3%"
    raise NotImplementedError("find the orphan 3 percent chunk")


if __name__ == "__main__":
    chunk = find_orphan()
    print(chunk.chunk_id)
    print("acme" in chunk.text.lower())
