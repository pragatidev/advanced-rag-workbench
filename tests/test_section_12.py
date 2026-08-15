from rag.graph.tiny import answer_global, build, community_summaries, refuse_if_local_holds


def test_section_12_graph_and_refuse():
    g = build()
    assert set(community_summaries()) >= {"revenue", "billing", "access", "privacy"}
    assert "sequential revenue" in answer_global("themes")["answer"].lower()
    assert refuse_if_local_holds(True)
    assert refuse_if_local_holds(False) is None
    assert g["index_cost"]["llm_extract_calls"] == 0
