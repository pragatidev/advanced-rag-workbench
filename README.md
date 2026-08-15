# Advanced RAG workbench

Companion repo for **Advanced RAG Techniques: Architecture [2026]** (curriculum v1.0).

One corpus (`data/acme/`). One question file (`eval/questions.jsonl`). One package (`rag/`). Keep the winner. Refuse the rest.

[![pytest](https://img.shields.io/badge/pytest-no%20API%20key-2ea44f)](tests/test_smoke.py)
[![python](https://img.shields.io/badge/python-3.11%20%7C%203.12-3776ab)](.python-version)
[![license](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

## Quickstart

```
uv sync
copy .env.example .env
uv run pytest -q
python labs/lab_s3_naive/part_1/load_and_chunk.py
```

pip fallback:

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest -q
```

macOS / Linux: `source .venv/bin/activate` then the same pip and pytest lines.

No cloud key is required for retrieve or for pytest. Generate prints `SKIPPED` until you set a key or start Ollama / LM Studio.

## Course map

| # | Section | Folder | Lab |
|---:|---|---|---|
| 1 | What Advanced RAG is and how you call it | `notebooks/section_01_get_oriented/` | (concept) |
| 2 | Any-provider setup: Qwen, OpenAI-compat, or local | `notebooks/section_02_set_up_any_provider_and_local/` | `labs/lab_s2_env/` |
| 3 | Naive RAG: chunk, embed, retrieve, generate | `notebooks/section_03_run_naive_rag/` | `labs/lab_s3_naive/` |
| 4 | Why naive fails: orphans, goldens, embedders | `notebooks/section_04_watch_naive_fail/` | `labs/lab_s4_diagnose/` |
| 5 | Semantic chunking | `notebooks/section_05_chunk_with_a_measured_reason/` | `labs/lab_s5_chunk/` |
| 6 | Small-to-big: window, parent, auto-merge | `notebooks/section_06_small_to_big_and_late_chunking/` | `labs/lab_s6_s2b/` |
| 7 | Hybrid search and RRF | `notebooks/section_07_hybrid_search_and_rrf/` | `labs/lab_s7_hybrid/` |
| 8 | Contextual chunks, cross-encoder, pack | `notebooks/section_08_contextual_rerank_and_pack/` | `labs/lab_s8_rerank/` |
| 9 | Rewrite, multi-query, HyDE | `notebooks/section_09_query_enhancement/` | `labs/lab_s9_query/` |
| 10 | Self-RAG gate and adaptive routing | `notebooks/section_10_self_rag_and_adaptive_routing/` | `labs/lab_s10_route/` |
| 11 | Corrective RAG (web off) | `notebooks/section_11_corrective_rag_and_retrieve_as_tool/` | `labs/lab_s11_crag/` |
| 12 | Graph RAG and when to refuse it | `notebooks/section_12_graph_rag_and_when_to_refuse/` | `labs/lab_s12_graph/` |
| 13 | Tables, images, captions | `notebooks/section_13_multimodal_tables_and_images/` | `labs/lab_s13_mm/` |
| 14 | Faithfulness and context recall | `notebooks/section_14_evaluation_metrics/` | `labs/lab_s14_eval/` |
| 15 | Cost, semantic cache, OTel-shaped traces | `notebooks/section_15_cost_cache_and_traces/` | `labs/lab_s15_prod/` |
| 16 | Filter, redact, audit | `notebooks/section_16_enterprise_data_governance/` | `labs/lab_s16_gov/` |
| 17 | Ship one pipeline | `notebooks/section_17_ship_one_pipeline_from_evidence/` | `labs/lab_s17_cap/` |

Concept cards: `docs/mechanisms/`. Product door: `python app.py` or `from rag import run_ask`.

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

## Provider matrix

One OpenAI-compatible client. Three variables: base URL, key, model. Names live in `.env` and `rag/settings.py` only.

| Door | Base URL | Key env | Model |
|---|---|---|---|
| Qwen Model Studio (default) | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` | `DASHSCOPE_API_KEY` | `qwen3.8-max` |
| Workspace form | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` | `DASHSCOPE_API_KEY` | `qwen3.8-max` |
| US Virginia | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` | `DASHSCOPE_API_KEY` | `qwen3.8-max` |
| OpenAI | `https://api.openai.com/v1` | `OPENAI_API_KEY` | set at record time |
| Ollama | `http://localhost:11434/v1` | `ollama` (ignored) | `llama3.2:3b` (or `llama3.2:1b`, `gemma3:4b`, `qwen2.5:3b`, `qwen2.5:7b`, `phi4-mini`) |
| LM Studio | `http://localhost:1234/v1` | `lm-studio` (ignored) | whatever GGUF you loaded |

Workbench aliases: `RAGBENCH_API_BASE`, `RAGBENCH_API_KEY`, `RAGBENCH_MODEL`. Same values as `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`.

Local embeds verified in this pass: `nomic-embed-text`, `nomic-embed-text:v1.5`, `mxbai-embed-large`, `all-minilm`. Tests use `HashEmbedder` so clone stays offline.

Anthropic is Messages API, not OpenAI-compat by default. Gemini / xAI / DeepSeek: set the three vars only when you have a documented 2026 id. Do not invent one.

Turn **Free Quota Only** on in Model Studio (Singapore International) if you use the Qwen door.

## Stores

| Store | Runs here | Path |
|---|---|---|
| Chroma | yes | `store/chroma/` |
| FAISS | yes | `store/faiss/<name>/` |
| Qdrant | yes | `store/qdrant/` |
| pgvector | optional | `docker compose up -d` |

## Commands

```
python -m pytest -q
python scripts/smoke_all.py
python app.py
python -m rag ask "What does error code TS-999 mean?" --pipeline hybrid
```

Makefile: `make test`, `make dest`, `make section-N`, `make smoke`.

Optional extras: `uv sync --extra local-rerank` (cross-encoder), `--extra docling`, `--extra pgvector`.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `ModuleNotFoundError: rag` | Run from the repo root. Activate the venv. |
| pytest wants a key | It should not. File an issue if `tests/test_smoke.py` calls a network generate. |
| `SKIPPED: no API key` | Expected. Set `DASHSCOPE_API_KEY` or point at Ollama/LM Studio. |
| pgvector SKIP | Docker is optional. `docker compose up -d` then rerun the store lab. |
| Chroma / Qdrant lock | Delete `store/chroma` or `store/qdrant` (gitignored). Rebuild the index. |
| Wrong model id | Change `.env`. Never edit a notebook to hard-code `gpt-4o` or `qwen-3.8-max`. |
| Web CRAG | Stays off. `WEB_SEARCH_ENABLED=false`. |

## Honesty

- A prompt loop is not Asai Self-RAG. We ship the loop and say so.
- GraphRAG here is a seeded tiny graph, not a Microsoft index.
- Cross-encoder default is a labeled lexical stand-in until `local-rerank` is installed.
- Docling is optional; the lab prints `markdown-fallback` when it is missing.
- HashEmbedder is an offline stand-in so TS-999 and pytest work with no download.

MIT. Built by Pragati Kunwer.
