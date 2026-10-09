# %% [markdown]
# # Step one of a tiny graph: entities, the chunks they live in, and seed communities
#
# Lab `lab_s12_graph` / `part_1`.

# %%
"""Step one of a tiny graph: entities, the chunks they live in, and seed communities.

TOY. Real GraphRAG extracts entities with a language model. This file uses a
hand written SEED dictionary so the mechanism is readable and the run is free.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
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
    """entity -> the chunk ids that mention it. This is the whole index."""
    members = {name: [] for name in SEED}
    for chunk in chunks:
        text = chunk.text.lower()
        for name, needles in SEED.items():
            if any(needle in text for needle in needles):
                members[name].append(chunk.chunk_id)
    return members


def build_edges(chunks, members):
    """Two entities sharing a chunk get a link. Weight is how many chunks."""
    in_chunk = {chunk.chunk_id: [] for chunk in chunks}
    for name, chunk_ids in members.items():
        for chunk_id in chunk_ids:
            in_chunk[chunk_id].append(name)
    edges = {}
    for chunk_id, names in in_chunk.items():
        names = sorted(names)
        for i, left in enumerate(names):
            for right in names[i + 1:]:
                edges[(left, right)] = edges.get((left, right), 0) + 1
    return edges


def build_communities(members, edges):
    """Seed communities: entities you can reach through shared chunks."""
    parent = {name: name for name in members}

    def find(name):
        while parent[name] != name:
            parent[name] = parent[parent[name]]
            name = parent[name]
        return name

    for left, right in edges:
        parent[find(left)] = find(right)
    groups = {}
    for name in members:
        groups.setdefault(find(name), []).append(name)
    return [sorted(names) for _, names in sorted(groups.items())]


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
