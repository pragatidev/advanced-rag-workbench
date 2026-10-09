# Advanced RAG workbench

Companion repo for **Advanced RAG Techniques: Architecture [2026]**: 23 sections, 20 labs.

One corpus (`data/acme/`). One question file (`eval/questions.jsonl`). One package (`rag/`). Keep the winner. Refuse the rest.

[![pytest](https://img.shields.io/badge/pytest-no%20API%20key-2ea44f)](tests/test_smoke.py)
[![python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-3776ab)](.python-version)
[![license](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

## Quickstart

Python 3.13 is the one the course uses (3.11 and 3.12 also work). With uv:

```
uv sync
copy .env.example .env
uv run pytest
uv run python labs/lab_s3_naive/part_1/load_and_chunk.py
```

With pip, step by step for Windows, macOS and Linux: [INSTALL.md](INSTALL.md).

No key is needed for retrieval, the labs or pytest. pytest ends with one count line, `N passed, 1 skipped`; the skip is pgvector, which needs Docker.

## Course map

| # | Section | Notebook folder | Lab |
|---:|---|---|---|
| 1 | Why RAG, Where It Fits, and What It Costs You | `notebooks/section_01_get_oriented/` | `basics/cold_ask.py`, `basics/two_chunks_flags.py` |
| 2 | The Workbench: Any Model, Any Provider, and a Private Option | `notebooks/section_02_set_up_any_provider_and_local/` | `labs/lab_s2_env/` |
| 3 | Foundations: Embeddings, Cosine, and Your First Cut (skip if you already ship RAG) | none | `basics/embed_two_sentences.py`, `basics/similarity_scores.py`, `basics/cut_one_document.py` |
| 4 | Foundations: Store, Ask, and Your First RAG Program (skip if you already ship RAG) | none | `basics/store_and_ask.py`, `basics/mini_rag.py` |
| 5 | Naive RAG: Chunk, Embed, Retrieve, Then Generate | `notebooks/section_03_run_naive_rag/` | `labs/lab_s3_naive/` |
| 6 | Why Naive RAG Fails: Orphans, Goldens, Embedders | `notebooks/section_04_watch_naive_fail/` | `labs/lab_s4_diagnose/` |
| 7 | Semantic Chunking: Cut by Meaning, Measure the Difference | `notebooks/section_05_chunk_with_a_measured_reason/` | `labs/lab_s5_chunk/` |
| 8 | Small-to-Big Retrieval: Window, Parent, Auto-Merge | `notebooks/section_06_small_to_big_and_late_chunking/` | `labs/lab_s6_s2b/` |
| 9 | Hybrid Search: Vector Plus Keyword, Fuse the Ranks | `notebooks/section_07_hybrid_search_and_rrf/` | `labs/lab_s7_hybrid/` |
| 10 | Re-ranking: Contextual Chunks, Cross-Encoder, Pack | `notebooks/section_08_contextual_rerank_and_pack/` | `labs/lab_s8_rerank/` |
| 11 | Rerank Budget and When to Escalate Documents | `notebooks/section_08b_rerank_budget_and_self_route/` | `labs/lab_s8b_budget/` |
| 12 | Query Enhancement: Rewrite, Multi-Query, and HyDE | `notebooks/section_09_query_enhancement/` | `labs/lab_s9_query/` |
| 13 | Self-RAG and Adaptive Routing: Retrieve or Not | `notebooks/section_10_self_rag_and_adaptive_routing/` | `labs/lab_s10_route/` |
| 14 | Corrective RAG: Grade the Set, Then Rewrite or Answer | `notebooks/section_11_corrective_rag_and_retrieve_as_tool/` | `labs/lab_s11_crag/` |
| 15 | Two-Hop Retrieve and Lost-in-Retrieval | none | `labs/lab_s11b_hop/`, `hop_budget.py` |
| 16 | Graph RAG: Answer Global Questions, Refuse the Rest | `notebooks/section_12_graph_rag_and_when_to_refuse/` | `labs/lab_s12_graph/` |
| 17 | Multimodal Retrieval: Tables, Images, and Captions | `notebooks/section_13_multimodal_tables_and_images/` | `labs/lab_s13_mm/` |
| 18 | RAG Evaluation: Meters, Ranking Metrics, and Judges | `notebooks/section_14_evaluation_metrics/` | `labs/lab_s14_eval/` |
| 19 | Cost per Query: Semantic Cache and Observability | `notebooks/section_15_cost_cache_and_traces/` | `labs/lab_s15_prod/` |
| 20 | Incremental Index and Embedder Cutover | `notebooks/section_15b_incremental_index_and_cutover/` | `labs/lab_s15b_fresh/` |
| 21 | Enterprise Data Governance: Filter, Redact, Audit | `notebooks/section_16_enterprise_data_governance/` | `labs/lab_s16_gov/` |
| 22 | Ship One Pipeline: Design Walk, Metrics File, Decision Note | `notebooks/section_17_ship_one_pipeline_from_evidence/` | `labs/lab_s17_walk/`, `labs/lab_s17_cap/` |
| 23 | Optional. 2026 Frontier Cards You Can Skip | `notebooks/section_18_optional_2026_frontier_cards/` | none (cards only) |

Folder names are older than the numbering and stay as they are: the folder for section 5 is `section_03_run_naive_rag`, and so on.

Concept cards: `docs/mechanisms/`. Product door: `python app.py` or `from rag import run_ask`.

## Layout

| Folder | What it holds |
|---|---|
| `basics/` | Seven one-idea scripts for sections 1, 3 and 4: a cold ask, the two pieces of a fixed cut, embeddings, cosine, one document cut, store and ask, and a mini RAG. Offline. |
| `data/` | The one corpus, `data/acme/`: an FAQ, a figure caption, a Q2 filing excerpt, two policies, an error catalog, and a KPI table as Markdown and PDF. |
| `demo/` | `cold_ask.txt`, a saved run of the section 1 cold ask: two models asked about TS-999 with no documents. |
| `docs/` | `corpus_map.md` (what is in the corpus) and `mechanisms/`, one concept card per idea, plus the section 23 code sample `classify_invoice.py`. |
| `eval/` | `questions.jsonl`, the question file every evaluation reads. |
| `examples/` | Two small programs on top of `rag/`: four asks through the router, and a support ticket answered by `run_ask`. |
| `exercises/` | The coding exercises, with TODOs to fill. |
| `solutions/` | Reference answers for `exercises/`. |
| `labs/` | 20 labs, 67 parts. Each part is one script you run from the repo root; most labs also have `starter/` and `solution/`. |
| `notebooks/` | 20 section folders (sections 3, 4 and 15 have none): VS Code `# %%` twins of 65 lab parts (every lab except section 15's), plus concept walks. Twins are built from the lab parts by `scripts/make_twins.py`. |
| `rag/` | The package: chunkers, embedders, stores, retrieval, rerank, query, routing, loops, graph, multimodal, eval, governance, cost and cache, settings. |
| `runs/` | Where evaluations write `metrics.json` and ask logs. Contents are ignored by git. |
| `scripts/` | `smoke_all.py` (every test file, one at a time, as a PASS/FAIL table) and `make_twins.py` (rebuilds the notebook twins). |
| `store/` | Local indexes for Chroma, FAISS and Qdrant, built when you run the labs. Contents are ignored by git. |
| `tests/` | The pytest suite: one file per section plus the package tests. No key needed. |
| `.claude/`, `.grok/` | The same `ask-acme` agent skill, for Claude Code and for Grok. |
| `_planning/` | Two build reports from the August 2026 rebuild. History, not course material. |

At the root: `INSTALL.md` (setup step by step), `TROUBLESHOOTING.md` (every error we have seen, with its fix), `app.py` (the product door, an HTTP endpoint on port 8787), `hop_budget.py` (section 15), `pyproject.toml`, `uv.lock` and `requirements.txt` (the same pinned versions), `.env.example`, `docker-compose.yml` (optional pgvector), `Makefile`, `pytest.ini`.

## Checkpoint folders

Each lab is a folder you can reopen a week later.

```
labs/lab_s7_hybrid/
  starter/     TODOs
  part_1/      first working slice
  part_2/
  part_3/
  part_4/      full run (writes the board)
  solution/    reference
```

Run a part from the repo root:

```
python labs/lab_s7_hybrid/part_1/dense_miss.py
```

The `# %%` twin is under `notebooks/section_07_hybrid_search_and_rrf/`.

## The three model doors

Retrieval never needs a model. Generate does, and the workbench reaches every model through four variables in `.env`. Names live in `.env` and `rag/settings.py` only, never in a notebook.

| Door | `LLM_BACKEND` | `LLM_BASE_URL` | `LLM_API_KEY` | `LLM_MODEL` |
|---|---|---|---|---|
| Local, Ollama (the default) | `openai` | `http://localhost:11434/v1` | none needed | `qwen3:8b` |
| Anthropic | `anthropic` | `https://api.anthropic.com` | your key | `claude-haiku-4-5` |
| OpenAI-compatible | `openai` | `https://api.openai.com/v1` | your key | `gpt-5.6-luna` |

With no `.env`, the workbench uses the local door: `qwen3:8b` on Ollama (`ollama pull qwen3:8b`). Laptop-sized alternatives: `llama3.2:3b`, `llama3.2:1b`, `gemma3:4b`, `qwen2.5:3b`, `phi4-mini`. LM Studio is the same door on `http://localhost:1234/v1`. Your prompts never leave your machine.

Anthropic speaks its own Messages API, which is why it sets `LLM_BACKEND=anthropic`. Every other vendor that speaks the OpenAI chat format is the OpenAI-compatible door with its own base URL and model id, for example Qwen on Alibaba Model Studio at `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`. Take the model id from that vendor's docs. `.env.example` has each block ready to uncomment.

Answers are extractive (copied from the retrieved text) by default, and `.env.example` keeps them that way with `RAGBENCH_GENERATE=extractive`. To have the model write them, fill in one door in `.env` and set `RAGBENCH_GENERATE=api`, or pass `--generate api` for one question. The local door needs no key. A hosted door with no key prints `SKIPPED`, and so does the local door when Ollama is not running; either way the answer stays extractive.

Embeddings are a separate choice: `EMBED_MODEL=all-MiniLM-L6-v2`, a real local model that runs through Chroma and downloads once on first use. pytest uses the offline `HashEmbedder`, so it never downloads anything.

Workbench aliases: `RAGBENCH_API_BASE`, `RAGBENCH_API_KEY`, `RAGBENCH_MODEL` take the same values as `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`.

## Stores

| Store | Runs here | Path |
|---|---|---|
| Chroma | yes | `store/chroma/` |
| FAISS | yes | `store/faiss/<name>/` |
| Qdrant | yes | `store/qdrant/` |
| pgvector | optional | `docker compose up -d` |

## Commands

```
python -m pytest
python scripts/smoke_all.py
python app.py
python -m rag ask "What does error code TS-999 mean?" --pipeline hybrid
```

Makefile: `make test`, `make dest`, `make smoke`, and `make section-N`, which runs `tests/test_section_N.py` (`make section-8b` runs `tests/test_section_08b.py`). Like the folder names, those numbers are older than the course map. Windows has no `make` unless you install one; `python -m pytest tests/test_section_08b.py` is the same run.

Optional extras: `uv sync --extra local-rerank` (cross-encoder), `--extra docling`, `--extra pgvector`.

## Troubleshooting

[TROUBLESHOOTING.md](TROUBLESHOOTING.md) has every error we have seen while setting this repo up and running it, each
with the exact text it prints, what it means and the fix: Git or Python not found, PowerShell blocking the venv, a
command typed in the wrong folder, no model running, a wrong key, an account with no credit, and more.

## Honesty

- A prompt loop is not Asai Self-RAG. We ship the loop and say so.
- GraphRAG here is a seeded tiny graph, not a Microsoft index.
- Cross-encoder default is a labeled lexical stand-in until `local-rerank` is installed.
- Docling is optional; the lab prints `markdown-fallback` when it is missing.
- HashEmbedder is an offline stand-in so TS-999 and pytest work with no download.

MIT. Built by Pragati Kunwer.
