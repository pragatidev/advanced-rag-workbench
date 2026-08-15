from rag.chunkers import chunk_corpus, contextualize
from rag.corpus import load_documents
from rag.rerank import pack_ends, rerank_cross_encoder
from rag.retrieve import Hit


def test_section_08_context_and_pack():
    docs = load_documents()
    chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
    orphan = next(c for c in chunks if "revenue grew by 3%" in c.text.lower())
    assert "acme" not in orphan.text.lower()
    assert "acme" in contextualize(orphan).text.lower()
    hits = [
        Hit(chunk=chunks[0], score=0.2, source="x"),
        Hit(chunk=chunks[1], score=0.9, source="x"),
        Hit(chunk=chunks[2], score=0.6, source="x"),
    ]
    packed = pack_ends(hits)
    assert packed[0].score == 0.9
    assert packed[-1].score == 0.6
    ranked, backend = rerank_cross_encoder("q", hits, keep=2)
    assert ranked and backend
