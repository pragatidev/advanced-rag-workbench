"""STARTER Build a tiny entity graph over the ACME corpus. Fill the three TODOs."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.corpus import load_documents
from rag.chunkers import fixed_size

# Entity name -> the strings that name it in the actual documents.
# Add your own. Every surface string must exist in the corpus verbatim.
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
        raise SystemExit("SEED TERM NOT IN CORPUS:\n  " + "\n  ".join(missing))


def build_members(chunks) -> dict[str, list[str]]:
    """TODO 1. For every chunk, for every seed term: if the term is in the chunk
    text, record the chunk id under that entity. Return entity -> sorted chunk ids,
    with the entities themselves in sorted order. Skip entities that matched nothing."""
    raise NotImplementedError("TODO 1: build the nodes and their members")


def build_edges(members: dict[str, list[str]]) -> dict[tuple[str, str], int]:
    """TODO 2. Two entities get an edge when they share at least one chunk.
    Return {(left, right): shared chunk count} with left < right, sorted."""
    raise NotImplementedError("TODO 2: build the edges")


def connected_components(
    names: list[str], edges: dict[tuple[str, str], int]
) -> list[list[str]]:
    """TODO 3. Start at a node, take everything reachable from it, that is one
    community. Repeat until every node has a home. Sort everything you return."""
    raise NotImplementedError("TODO 3: collect the connected components")


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
