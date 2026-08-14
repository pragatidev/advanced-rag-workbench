from ragbench.chunkers import chunk_corpus, token_count
from ragbench.corpus import load_documents


def test_fixed_chunk_loses_company_on_growth_sentence():
    docs = load_documents()
    chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
    growth = [c for c in chunks if "revenue grew by 3%" in c.text.lower()]
    assert growth, "expected a chunk that still has the 3 percent sentence"
    assert all("acme" not in c.text.lower() for c in growth)


def test_chunkers_swap():
    docs = load_documents()
    fixed = chunk_corpus(docs, "fixed", size=80, overlap=0)
    rec = chunk_corpus(docs, "recursive")
    sem = chunk_corpus(docs, "semantic")
    assert fixed and rec and sem
    assert {c.metadata["chunker"] for c in rec} == {"recursive"}
    assert sum(token_count(c) for c in fixed) > 0
