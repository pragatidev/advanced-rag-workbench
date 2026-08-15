from rag.query.hyde import hypothetical_document, run_hyde
from rag.query.rewrite import multi_query, rewrite


def test_section_09_query_enhancement():
    assert "TS-999" in rewrite("What does error code TS-999 mean?")
    assert len(multi_query("What was ACME revenue growth in Q2 2023?")) == 3
    ghost = hypothetical_document("What was ACME revenue growth in Q2 2023?")
    assert ghost
    result = run_hyde("What was ACME revenue growth in Q2 2023?")
    assert result["hypothetical"]
    assert result["hits"]
