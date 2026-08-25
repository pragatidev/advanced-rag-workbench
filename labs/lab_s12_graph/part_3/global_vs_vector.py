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
FOUR_THEMES = ("sequential", "billing", "least-privilege", "pii")
HAND_WRITTEN = "Themes across this corpus:"


def search(docs, question, collection, k=3):
    """The same retrieval the naive pipeline runs, on the docs we hand it."""
    chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
    embedder = HashEmbedder(semantic_mode=True)
    store = ChromaStore(collection, persist=False)
    store.reset()
    store.add(chunks, embedder.encode([c.text for c in chunks]).tolist())
    hits = store.query(embedder.embed(question).tolist(), k=k)
    return [(h.chunk.chunk_id, h.score, h.chunk.text) for h in hits]


def names_four_themes(text):
    low = text.lower()
    return all(word in low for word in FOUR_THEMES)


def report(hits, mark_hand_written=False):
    for chunk_id, score, text in hits:
        line = f"  {chunk_id:24s} {score:.4f}"
        if mark_hand_written and HAND_WRITTEN.lower() in text.lower():
            line += "   <- carries the hand written themes sentence"
        print(line)
    joined = " ".join(text for _, _, text in hits)
    print("  four themes in the retrieved strips:", names_four_themes(joined))


def cut_hand_written(docs):
    """Delete the one sentence nobody writes for a real corpus."""
    removed = 0
    for doc in docs:
        if HAND_WRITTEN in doc.text:
            before = len(doc.text.split())
            doc.text = doc.text.split(HAND_WRITTEN)[0].rstrip() + "\n"
            removed = before - len(doc.text.split())
            print(f"  removed {removed} words from {doc.path}")
    return docs


def summarize_communities(docs):
    """Part one's graph and part two's summarizer, run on the corpus we hand them."""
    chunks = []
    for doc in docs:
        chunks.extend(fixed_size(doc, size=80, overlap=0))
    members = build_members(chunks)
    communities = build_communities(members, build_edges(chunks, members))
    by_id = {chunk.chunk_id: chunk.text for chunk in chunks}
    for i, entities in enumerate(communities):
        chunk_ids = community_chunks(entities, members)
        texts = [by_id[chunk_id] for chunk_id in chunk_ids]
        print(f"  community_{i}  entities: {', '.join(entities)}")
        print(f"    summary: {_extractive(entities, texts)}")
    return communities


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
    communities = summarize_communities(docs)
    print(f"  communities read {len(communities)}   chunks searched at question time 0")
    print("  llm_extract_calls 0   seed dictionary, not a model extract")


if __name__ == "__main__":
    main()
