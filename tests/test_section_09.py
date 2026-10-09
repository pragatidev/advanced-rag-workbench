from rag.query.hyde import hypothetical_document, run_hyde
from rag.query.rewrite import multi_query, ngram_overlap, rewrite


def test_section_09_query_enhancement():
    assert "TS-999" in rewrite("What does error code TS-999 mean?")
    q = "What was ACME revenue growth in Q2 2023?"
    qs = multi_query(q)
    assert len(qs) == 3
    pairs = ngram_overlap(qs)
    assert len(pairs) == 3
    assert all(0.0 <= score <= 1.0 for _, _, score in pairs)
    clones = [q, q, q]
    clone_pairs = ngram_overlap(clones)
    assert all(score == 1.0 for _, _, score in clone_pairs)
    ghost = hypothetical_document("What was ACME revenue growth in Q2 2023?")
    assert ghost
    result = run_hyde("What was ACME revenue growth in Q2 2023?")
    assert result["hypothetical"]
    assert result["hits"]
