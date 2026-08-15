# Basics labs run report

Date: 2026-08-15
Repo: student-facing course workbench (this git repo)
Lane: Section 2 venv (`.venv\Scripts\python`, CPython 3.11.9)

`.env` was not opened or written. No API key. Scripts use `HashEmbedder` and extractive generate only.

Working directory: repository root.

The venv was created with `uv sync --python 3.11` so the scripts could run in the documented interpreter.

## Commands

### `.venv\Scripts\python basics/embed_two_sentences.py`

```
near_a The company's revenue grew by 3% over the previous quarter.
  first 6 numbers [-0.021, -0.154, -0.019, 0.039, 0.006, 0.056]
near_b Prior quarter revenue was 314 million USD.
  first 6 numbers [0.163, -0.139, 0.018, -0.094, -0.075, -0.018]
far    Shared passwords are forbidden.
  first 6 numbers [-0.185, -0.137, 0.094, -0.036, -0.228, -0.029]
similar pair 0.243
unrelated pair 0.007
story: the two revenue sentences sit nearer than revenue vs the password rule.
```

Exit code: 0

### `.venv\Scripts\python basics/similarity_scores.py`

```
rank  cosine  pair
1     0.243   revenue grew 3% / prior-quarter revenue
2     0.086   prior-quarter revenue / passwords forbidden
3     0.007   revenue grew 3% / passwords forbidden
```

Exit code: 0

### `.venv\Scripts\python basics/cut_one_document.py`

```
document ACME Q2 2023 filing excerpt
path data/acme/filings/q2_2023_excerpt.md
chunk_count 2
one_full_chunk:
# ACME Corp ## Form 10-Q excerpt, fiscal quarter Q2 2023 Filed with the commission for the quarterly period ended 30 June 2023. Safe harbor statement. This excerpt contains forward looking statements that are not historical facts. Readers should not treat any sentence below as investment advice. The filing discusses seasonality, supply chain recovery, and the way management talks about sequential growth. Several paragraphs exist only so a naive fixed-size splitter cuts the heading away from the number. The legal
```

Exit code: 0

### `.venv\Scripts\python basics/store_and_ask.py`

```
question What was ACME revenue growth in Q2 2023?
backend chroma (in memory)
neighbors 2
0.189  filing_q2_2023:fixed:1
preface continues with ordinary language about risks, uncertainties, competitors, currency, and the possibility that actual results will differ. Warehouse throughput improved. Marketing spend was steady. Nothing in this preface names the growth rate. The preface is padding on purpose so the next heading and the next sentence land in a later chunk. ## Results of operations The company's revenue grew by 3% over the previous quarter. Prior quarter revenue was 314 million USD. Gross margin held. Guidance is unchanged.
---
-0.147  filing_q2_2023:fixed:0
# ACME Corp ## Form 10-Q excerpt, fiscal quarter Q2 2023 Filed with the commission for the quarterly period ended 30 June 2023. Safe harbor statement. This excerpt contains forward looking statements that are not historical facts. Readers should not treat any sentence below as investment advice. The filing discusses seasonality, supply chain recovery, and the way management talks about sequential growth. Several paragraphs exist only so a naive fixed-size splitter cuts the heading away from the number. The legal
---
```

Exit code: 0

### `.venv\Scripts\python basics/mini_rag.py`

```
question What was ACME revenue growth in Q2 2023?
answer ## Results of operations The company's revenue grew by 3% over the previous quarter.
from_chunk
preface continues with ordinary language about risks, uncertainties, competitors, currency, and the possibility that actual results will differ. Warehouse throughput improved. Marketing spend was steady. Nothing in this preface names the growth rate. The preface is padding on purpose so the next heading and the next sentence land in a later chunk. ## Results of operations The company's revenue grew by 3% over the previous quarter. Prior quarter revenue was 314 million USD. Gross margin held. Guidance is unchanged.
```

Exit code: 0

### `python -m pytest -q`

Ran as `.venv\Scripts\python -m pytest -q` (same venv).

```
................................................................s.       [100%]
```

Exit code: 0

The single skip is `tests/test_store.py::test_pgvector_optional` (Postgres not running). Docker is optional.

## Notes

- `tests/test_basics.py` smokes that each script is importable and that `mini_rag.answer` is non-empty with no key.
- `_planning/BASICS_LABS_RUN_REPORT.md` is allow-listed in `.gitignore` (same pattern as `REBUILD_RUN_REPORT.md`).
- Chroma in the basics scripts is ephemeral (`persist=False`) so a student run does not rewrite `store/chroma/`.
