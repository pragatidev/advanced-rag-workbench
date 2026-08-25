"""Step three of a tiny graph: watch a global question fail vector RAG.

The corpus ships with one hand written sentence in privacy.md that lists the
themes. That sentence is why vector search looks like it can answer a global
question. Remove it, which is the state every real corpus is in, and vector
search misses. The community summaries still answer, because they were written
from the corpus at index time.

TOY. Real GraphRAG extracts entities with a language model. Part one used a seed
dictionary, and so does this.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
# labs/ is not a package, so part_1 and part_2 go on the path by folder.
for folder in ("part_1", "part_2"):
    path = HERE.parent / folder
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from build_tiny_graph import (  # noqa: E402
    build_communities,
    build_edges,
    build_members,
)
from community_summaries import _extractive, community_chunks  # noqa: E402

from rag.chunkers import chunk_corpus, fixed_size  # noqa: E402
from rag.corpus import load_documents  # noqa: E402
from rag.embedders import HashEmbedder  # noqa: E402
from rag.stores.chroma_store import ChromaStore  # noqa: E402

QUESTION = "What are the main themes in this ACME corpus?"
HAND_WRITTEN = "Themes across this corpus:"

# The grading rule, on screen. A theme counts as covered when the text names it
# in any of these words. Same rule for retrieved strips and for summaries.
THEME_TERMS = {
    "sequential revenue reporting": ("sequential", "revenue", "quarter"),
    "billing integrity": ("billing", "invoice", "ts-999"),
    "least-privilege access": ("least privilege", "least-privilege", "privileged", "tenant", "audit"),
    "PII minimization": ("pii", "national id", "redact", "retention"),
}


def grade(text):
    """The one instrument. Which of the four themes does this text name?"""
    low = text.lower()
    covered = []
    for theme, terms in THEME_TERMS.items():
        hit = next((t for t in terms if t in low), None)
        print(f"    {theme:30s} {'COVERED  ' + hit if hit else 'MISSING'}")
        if hit:
            covered.append(theme)
    print(f"  themes covered {len(covered)} of {len(THEME_TERMS)}")
    return covered


def search(docs, question, collection, k=3):
    """The same retrieval the naive pipeline runs, on the docs we hand it."""
    chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
    embedder = HashEmbedder(semantic_mode=True)
    store = ChromaStore(collection, persist=False)
    store.reset()
    store.add(chunks, embedder.encode([c.text for c in chunks]).tolist())
    hits = store.query(embedder.embed(question).tolist(), k=k)
    print(f"  collection {collection}   chunks indexed {len(chunks)}")
    return [(h.chunk.chunk_id, h.score, h.chunk.text) for h in hits]


def report(hits, mark_hand_written=False):
    for chunk_id, score, text in hits:
        line = f"  {chunk_id:24s} {score:.4f}"
        if mark_hand_written and HAND_WRITTEN.lower() in text.lower():
            line += "   <- carries the hand written themes sentence"
        print(line)
    return grade(" ".join(text for _, _, text in hits))


def cut_hand_written(docs):
    """Delete the one sentence nobody writes for a real corpus. In memory only."""
    for doc in docs:
        if HAND_WRITTEN in doc.text:
            before = len(doc.text.split())
            doc.text = doc.text.split(HAND_WRITTEN)[0].rstrip() + "\n"
            print(f"  removed {before - len(doc.text.split())} words from {doc.path} in memory")
            on_disk = next(d for d in load_documents() if d.doc_id == doc.doc_id)
            print(f"  {doc.path} on disk still {len(on_disk.text.split())} words, not edited")
    return docs


def read_summaries(docs):
    """Part one's graph and part two's summarizer, run on the corpus we hand them."""
    chunks = []
    for doc in docs:
        chunks.extend(fixed_size(doc, size=80, overlap=0))
    members = build_members(chunks)
    communities = build_communities(members, build_edges(chunks, members))
    by_id = {chunk.chunk_id: chunk.text for chunk in chunks}
    summaries = []
    for i, entities in enumerate(communities):
        chunk_ids = community_chunks(entities, members)
        summary = _extractive(entities, [by_id[cid] for cid in chunk_ids])
        summaries.append(summary)
        print(f"  community_{i}  entities: {', '.join(entities)}")
        print(f"    summary: {summary}")
    print(f"  communities read {len(communities)}   chunks searched at question time 0")
    print("  llm_extract_calls 0   seed dictionary, not a model extract")
    return grade(" ".join(summaries))


def main():
    print("QUESTION", QUESTION)
    print()

    print("BLOCK 1  vector search, corpus exactly as it ships")
    report(search(load_documents(), QUESTION, "s12_5_shipped"), mark_hand_written=True)
    print()

    print("BLOCK 2  the same search, with that one sentence deleted")
    docs = cut_hand_written(load_documents())
    report(search(docs, QUESTION, "s12_5_cut"))
    print()

    print("BLOCK 3  global mode on the same cut corpus, reading summaries")
    read_summaries(docs)


if __name__ == "__main__":
    main()
