from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "notebooks/section_01_setup/01.3_set_up_the_workbench.py",
    "notebooks/section_02_naive_rag/02.2_build_the_naive_pipeline.py",
    "notebooks/section_02_naive_rag/02.2b_vector_stores.py",
    "notebooks/section_02_naive_rag/02.3_the_chunk_that_lost_the_company_name.py",
    "notebooks/section_03_chunking/03.2_compare_chunkers.py",
    "notebooks/section_03_chunking/03.4_late_chunking.py",
    "notebooks/section_04_hybrid/04.2_hybrid_search_with_rrf.py",
    "notebooks/section_04_hybrid/04.3_contextual_chunks.py",
    "notebooks/section_04_hybrid/04.4_rerank_the_shortlist.py",
    "notebooks/section_05_query/05.2_rewrite_and_multi_query.py",
    "notebooks/section_05_query/05.4_run_hyde.py",
    "notebooks/section_06_retrieve_or_not/06.2_retrieve_gate.py",
    "notebooks/section_06_retrieve_or_not/06.3_support_or_refuse.py",
    "notebooks/section_07_crag/07.2_score_the_retrieved_set.py",
    "notebooks/section_07_crag/07.3_web_search_is_a_policy.py",
    "notebooks/section_08_graph/08.2_tiny_graph.py",
    "notebooks/section_09_tables/09.2_parse_tables_and_captions.py",
    "notebooks/section_09_tables/09.3_multimodal_retrieve.py",
    "notebooks/section_10_eval/10.2_run_the_suite.py",
    "notebooks/section_10_eval/10.3_cost_per_query.py",
    "notebooks/section_10_eval/10.4_traces.py",
    "notebooks/section_11_govern/11.2_metadata_filters.py",
    "notebooks/section_11_govern/11.3_audit.py",
    "notebooks/section_12_capstone/12.2_final_comparison.py",
]


def test_every_screen_walk_notebook_exists():
    missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
    assert missing == []


def test_naive_notebook_teaches_chroma_and_named_embedder():
    text = (ROOT / "notebooks/section_02_naive_rag/02.2_build_the_naive_pipeline.py").read_text(
        encoding="utf-8"
    )
    assert "Chroma" in text
    assert "HashEmbedder" in text
    assert "# %% [markdown]" in text


def test_store_notebook_names_all_four_local_backends():
    text = (ROOT / "notebooks/section_02_naive_rag/02.2b_vector_stores.py").read_text(
        encoding="utf-8"
    )
    for name in ("Chroma", "FAISS", "Qdrant", "pgvector", "Pinecone"):
        assert name in text
