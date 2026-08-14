from ragbench.corpus import load_documents
from ragbench.multimodal import table_row_chunks
from ragbench.pipelines import PIPELINES
from ragbench.query.hyde import hypothetical_document
from ragbench.query.rewrite import multi_query


def test_all_named_pipelines_run():
    q = "What does error code TS-999 mean?"
    for name, fn in PIPELINES.items():
        result = fn(q)
        assert result["pipeline"]
        assert "answer" in result
        assert "hits" in result, name


def test_hyde_builds_a_fake_document():
    fake = hypothetical_document("What was ACME revenue growth in Q2 2023?")
    assert "ACME" in fake or "question" in fake.lower()
    result = PIPELINES["hyde"]("What was ACME revenue growth in Q2 2023?")
    assert result["hypothetical"]
    assert result["hits"]


def test_multi_query_returns_three():
    assert len(multi_query("What does error code TS-999 mean?")) == 3


def test_table_rows_keep_the_seat_number():
    docs = {d.doc_id: d for d in load_documents()}
    rows = table_row_chunks(docs["q2_kpis"])
    blob = " ".join(r.text for r in rows)
    assert "12420" in blob
