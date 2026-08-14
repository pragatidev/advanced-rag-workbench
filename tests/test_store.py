import pytest

from rag.chunking import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.stores.chroma_store import ChromaStore
from rag.stores.faiss_store import FaissStore
from rag.stores.qdrant_store import QdrantStore


def _payload():
    docs = load_documents()
    chunks = chunk_corpus(docs, "recursive")
    emb = HashEmbedder(semantic_mode=True)
    vectors = emb.encode([c.text for c in chunks]).tolist()
    q = emb.embed("What does error code TS-999 mean?").tolist()
    return chunks, vectors, q


def test_chroma_roundtrip(tmp_path):
    chunks, vectors, q = _payload()
    store = ChromaStore("test", path=tmp_path / "chroma", persist=True)
    store.reset()
    store.add(chunks, vectors)
    hits = store.query(q, k=3)
    assert hits
    assert store.info().backend == "chroma"
    assert (tmp_path / "chroma").is_dir()


def test_faiss_roundtrip(tmp_path):
    chunks, vectors, q = _payload()
    store = FaissStore("test", path=tmp_path / "faiss")
    store.reset()
    store.add(chunks, vectors)
    hits = store.query(q, k=3)
    assert hits
    assert (tmp_path / "faiss" / "index.faiss").is_file()


def test_qdrant_roundtrip(tmp_path):
    chunks, vectors, q = _payload()
    store = QdrantStore("test", path=tmp_path / "qdrant")
    store.reset()
    store.add(chunks, vectors)
    hits = store.query(q, k=3)
    assert hits


def test_pgvector_optional():
    from rag.stores import pgvector_store as pgs

    if not pgs.available():
        pytest.skip("Postgres/pgvector not running")
    chunks, vectors, q = _payload()
    store = pgs.PgVectorStore("pytest")
    store.reset()
    store.add(chunks, vectors)
    hits = store.query(q, k=3)
    assert hits
