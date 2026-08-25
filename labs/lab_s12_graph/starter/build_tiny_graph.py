"""STARTER for step one of a tiny graph. Fill the three TODOs.

TOY. Real GraphRAG extracts entities with a language model. This file uses a
hand written SEED dictionary so the mechanism is readable and the run is free.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import fixed_size
from rag.corpus import load_documents

# The fake extractor. Entity name -> the strings that count as a mention.
SEED = {
    "TS-999": ("ts-999",),
    "billing": ("billing",),
    "national id": ("national id",),
    "revenue": ("revenue",),
    "tenant": ("tenant",),
    "audit": ("audit",),
}


def load_chunks():
    """The same cut the naive pipeline uses: fixed size 80, no overlap."""
    chunks = []
    for doc in load_documents():
        chunks.extend(fixed_size(doc, size=80, overlap=0))
    return chunks


def build_members(chunks):
    """TODO 1. entity -> the chunk ids that mention it. Walk every chunk, lowercase
    its text, and append the chunk id under every entity whose needle is in it.
    Start from {name: [] for name in SEED} so an entity with no hits still prints."""
    raise NotImplementedError("TODO 1: build the nodes and their members")


def build_edges(chunks, members):
    """TODO 2. Two entities sharing a chunk get a link, weight is how many chunks.
    Invert members into chunk_id -> the names in it, then count every sorted pair.
    Return {(left, right): shared chunk count}."""
    raise NotImplementedError("TODO 2: build the edges")


def build_communities(members, edges):
    """TODO 3. Seed communities: entities you can reach through shared chunks.
    A union find is enough. Return a list of sorted member lists."""
    raise NotImplementedError("TODO 3: collect the communities")


def main():
    chunks = load_chunks()
    members = build_members(chunks)
    edges = build_edges(chunks, members)
    communities = build_communities(members, edges)

    print("chunks", len(chunks))
    print("extracted_by seed_dict   llm_extract_calls 0")
    print()
    print("NODES")
    for name in sorted(members):
        chunk_ids = members[name]
        print(f"  {name}  chunks {len(chunk_ids)}")
        for chunk_id in chunk_ids:
            print(f"      {chunk_id}")
    print()
    print("EDGES")
    for (left, right), weight in sorted(edges.items()):
        print(f"  {left} -- {right}   shared_chunks {weight}")
    print()
    print("COMMUNITIES")
    for i, names in enumerate(communities):
        print(f"  community_{i}  members: {', '.join(names)}")


if __name__ == "__main__":
    main()
