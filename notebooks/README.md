# Notebooks

VS Code `# %%` files. Open one in VS Code and use Run Cell, or run it as a script from the repo root.

Two kinds of file live here. `part_N_*.py` is the twin of a lab part under `labs/`, built by `scripts/make_twins.py` (edit the lab part, never the twin). `S*_*.py` is a concept walk that has no lab part.

Section numbers are the course map in the main README.md. Folder names are older and keep their old numbers.

| # | Section | Folder |
|---:|---|---|
| 1 | Why RAG, Where It Fits, and What It Costs You | `section_01_get_oriented/` |
| 2 | The Workbench: Any Model, Any Provider, and a Private Option | `section_02_set_up_any_provider_and_local/` |
| 5 | Naive RAG: Chunk, Embed, Retrieve, Then Generate | `section_03_run_naive_rag/` |
| 6 | Why Naive RAG Fails: Orphans, Goldens, Embedders | `section_04_watch_naive_fail/` |
| 7 | Semantic Chunking: Cut by Meaning, Measure the Difference | `section_05_chunk_with_a_measured_reason/` |
| 8 | Small-to-Big Retrieval: Window, Parent, Auto-Merge | `section_06_small_to_big_and_late_chunking/` |
| 9 | Hybrid Search: Vector Plus Keyword, Fuse the Ranks | `section_07_hybrid_search_and_rrf/` |
| 10 | Re-ranking: Contextual Chunks, Cross-Encoder, Pack | `section_08_contextual_rerank_and_pack/` |
| 11 | Rerank Budget and When to Escalate Documents | `section_08b_rerank_budget_and_self_route/` |
| 12 | Query Enhancement: Rewrite, Multi-Query, and HyDE | `section_09_query_enhancement/` |
| 13 | Self-RAG and Adaptive Routing: Retrieve or Not | `section_10_self_rag_and_adaptive_routing/` |
| 14 | Corrective RAG: Grade the Set, Then Rewrite or Answer | `section_11_corrective_rag_and_retrieve_as_tool/` |
| 16 | Graph RAG: Answer Global Questions, Refuse the Rest | `section_12_graph_rag_and_when_to_refuse/` |
| 17 | Multimodal Retrieval: Tables, Images, and Captions | `section_13_multimodal_tables_and_images/` |
| 18 | RAG Evaluation: Meters, Ranking Metrics, and Judges | `section_14_evaluation_metrics/` |
| 19 | Cost per Query: Semantic Cache and Observability | `section_15_cost_cache_and_traces/` |
| 20 | Incremental Index and Embedder Cutover | `section_15b_incremental_index_and_cutover/` |
| 21 | Enterprise Data Governance: Filter, Redact, Audit | `section_16_enterprise_data_governance/` |
| 22 | Ship One Pipeline: Design Walk, Metrics File, Decision Note | `section_17_ship_one_pipeline_from_evidence/` |
| 23 | Optional. 2026 Frontier Cards You Can Skip | `section_18_optional_2026_frontier_cards/` |

Sections 3, 4 and 15 have no folder here: their scripts are `basics/` (sections 3 and 4) and `labs/lab_s11b_hop/` with `hop_budget.py` (section 15).

The runnable source of truth is `labs/`. Concept cards are `docs/mechanisms/`.
