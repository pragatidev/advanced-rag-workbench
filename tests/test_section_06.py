from rag.chunkers import parent_child
from rag.chunking.auto_merge import merge_hits
from rag.chunking.late import late_vectors
from rag.chunking.sentence_window import build
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.retrieve import dense_search


def test_section_06_small_to_big():
    docs = load_documents()
    pc = []
    sent = []
    for d in docs:
        pc.extend(parent_child(d))
        sent.extend(build(d))
    hit = next(c for c in pc if "revenue grew by 3%" in c.text.lower())
    assert hit.metadata.get("parent_id")
    assert hit.metadata["child_chars"] < hit.metadata["parent_chars"]
    assert sent
    late_chunks, vecs = late_vectors(docs, embedder=HashEmbedder(semantic_mode=False))
    assert len(late_chunks) == len(vecs)
    hits = dense_search("What was ACME revenue growth in Q2 2023?", pc, embedder=HashEmbedder(semantic_mode=False), k=6)
    merged = merge_hits(hits)
    assert merged
