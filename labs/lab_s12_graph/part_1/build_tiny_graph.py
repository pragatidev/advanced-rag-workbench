"""Build a tiny entity graph over the ACME corpus. A toy on purpose."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.corpus import load_documents
from rag.chunkers import fixed_size

# Entity name -> the strings that name it in the actual documents.
# Hand written. A real GraphRAG index sends every chunk to a model and asks
# what entities are in here; this dict is a string match and nothing more.
SEED_TERMS = {
    "TS-999": ["TS-999"],
    "billing ledger": ["billing ledger"],
    "duplicate invoice id": ["duplicate invoice id", "Duplicate invoice failures"],
    "billing-ops": ["billing-ops"],
    "national id": ["national id"],
    "PII": ["PII"],
    "redact": ["redact"],
    "AC-2": ["AC-2"],
    "tenant": ["tenant"],
    "shared passwords": ["shared passwords"],
    "revenue": ["revenue"],
    "prior quarter revenue": ["prior quarter revenue"],
    "seats by region": ["seats by region"],
}


def assert_seeds_are_real(docs) -> None:
    """Every surface string must exist in the corpus. A graph built on a typo
    looks fine and is wrong, so stop and name the term that matched nothing."""
    corpus = "\n".join(doc.text for doc in docs).lower()
    missing = sorted(
        f"{entity} -> {surface}"
        for entity, surfaces in SEED_TERMS.items()
        for surface in surfaces
        if surface.lower() not in corpus
    )
    if missing:
        raise SystemExit(
            "SEED TERM NOT IN CORPUS:\n  " + "\n  ".join(missing)
        )


def build_members(chunks) -> dict[str, list[str]]:
    """For every chunk, for every seed term: if the term is in the chunk text,
    record the chunk id under that entity. Those are the nodes and their members."""
    members: dict[str, set[str]] = {}
    for chunk in chunks:
        haystack = chunk.text.lower()
        for entity, surfaces in SEED_TERMS.items():
            if any(surface.lower() in haystack for surface in surfaces):
                members.setdefault(entity, set()).add(chunk.chunk_id)
    return {entity: sorted(ids) for entity, ids in sorted(members.items())}


def build_edges(members: dict[str, list[str]]) -> dict[tuple[str, str], int]:
    """Two entities get an edge when they show up in the same chunk. Not the
    same document. The same eighty word strip. Weight is the shared chunk count."""
    names = sorted(members)
    edges: dict[tuple[str, str], int] = {}
    for i, left in enumerate(names):
        for right in names[i + 1 :]:
            shared = set(members[left]) & set(members[right])
            if shared:
                edges[(left, right)] = len(shared)
    return dict(sorted(edges.items()))


def connected_components(
    names: list[str], edges: dict[tuple[str, str], int]
) -> list[list[str]]:
    """Start at a node, take everything reachable from it, that is one community.
    Repeat until every node has a home. Leiden this is not."""
    adjacency: dict[str, set[str]] = {name: set() for name in names}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    seen: set[str] = set()
    groups: list[list[str]] = []
    for start in sorted(names):
        if start in seen:
            continue
        stack = [start]
        group: set[str] = set()
        while stack:
            node = stack.pop()
            if node in seen:
                continue
            seen.add(node)
            group.add(node)
            stack.extend(sorted(adjacency[node] - seen))
        groups.append(sorted(group))
    return groups


def docs_of(members: dict[str, list[str]], entities: list[str]) -> list[str]:
    """chunk_id is doc_id:fixed:n, so the doc ids fall straight out of the members."""
    return sorted({
        chunk_id.split(":")[0] for entity in entities for chunk_id in members[entity]
    })


def main() -> None:
    docs = load_documents()
    assert_seeds_are_real(docs)

    chunks: list = []
    for doc in docs:
        chunks.extend(fixed_size(doc, size=80, overlap=0))

    members = build_members(chunks)
    edges = build_edges(members)
    communities = connected_components(sorted(members), edges)

    print(f"CORPUS   {len(docs)} documents, {len(chunks)} chunks (fixed, size=80, overlap=0)")
    print(f"SEEDS    {len(SEED_TERMS)} terms, hand written, not model extracted")

    print(f"\nNODES    {len(members)}")
    for entity, ids in members.items():
        print(f"  {entity:<22} {len(ids)} chunks")

    print(f"\nEDGES    {len(edges)} pairs share at least one chunk")

    print(f"\nCOMMUNITIES  {len(communities)}")
    for i, entities in enumerate(communities):
        print(f"  community_{i}")
        print(f"    entities: {', '.join(entities)}")
        print(f"    docs:     {', '.join(docs_of(members, entities))}")

    print("\nCLUSTERING   connected components, not Leiden")


if __name__ == "__main__":
    main()
