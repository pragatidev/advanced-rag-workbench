# Advanced RAG workbench

Companion Python repo for **Advanced RAG Techniques: Hybrid Search to Graph [2026]**.

One corpus. One question file. Every pipeline prints a delta. Keep the winner. Refuse the rest.

This is not a LangChain tour. This is not Nike. The ACME files were written for this course so gold spans are ours.

Lectures use this repo in three ways: **conceptual walkthrough** (animated picture of the idea), **hands-on working demo** (this folder on screen), **advanced walkthrough** (the same folder, later pipeline). The capture is of a real run, not a mock UI.

## How we walk the pipeline on screen

`run_ask` is the product. It is the wrong file to *teach* chunking.

Screen walks are a **normal VS Code Python file**. Open `labs/02_naive_pipeline.py`. Press Run, or Run Cell on each `# %%` block (Python Interactive). That is the same loop as a notebook, without a Jupyter install. Twin notebook if you want `.ipynb`: `notebooks/02_naive_pipeline.ipynb`.

```
# in VS Code: open the file, Run
python labs/02_naive_pipeline.py
```

You will see, in order:

1. **Documents** from `data/acme/` (paths printed)
2. **Chunker** (`fixed`, size 80, overlap 0) and the chunk that kept `3%` but lost ACME
3. **Embedder card**: `ToyEmbedder`, dim 64, semantic mode on. Why it exists. What you swap on Monday (`text-embedding-3-small`, Voyage, MiniLM)
4. **Store** written to `store/naive/` (`manifest.json`, `chunks.jsonl`, `vectors.npy`)
5. **Retrieve** from that store
6. **Generate** from those hits

Open `store/naive/manifest.json` on camera. That is "which semantic model" and "where is it stored."

```
python -m ragbench index naive
python -m ragbench inspect naive
```

| Lab | Lecture | Opens |
|---|---|---|
| `labs/02_naive_pipeline.py` | 2.2 | load, chunk, named model, store, retrieve, generate |
| `labs/03_compare_chunkers.py` | 3.2 | four chunkers, 3% sentence |
| `labs/04_hybrid_vs_dense.py` | 4.2 | same TS-999 question, two stores |

## How a real program invokes this

The CLI is a lab. Production never types `python -m ragbench ask`. A support desk, Slack bot, or chat widget calls **one function**:

```
from ragbench import run_ask

result = run_ask(user_question, pipeline="hybrid")
# result["answer"], result["hits"]
```

That is the whole invoke. Practical shapes are just wrappers:

| Use case | What calls `run_ask` |
|---|---|
| Website help widget | browser → `POST /ask` → `run_ask` |
| Slack / Teams / Zendesk | webhook handler imports `run_ask` |
| Ticket auto-draft | `examples/ticket_desk.py` (`handle_ticket`) |
| Editor harness | `ask-acme` skill runs retrieve, then writes from the hits |

Start the product door (tiny ACME desk in the browser):

```
python -m ragbench serve
```

Open http://127.0.0.1:8787/ and ask TS-999. Same path as curl:

```
curl -s http://127.0.0.1:8787/ask -H "Content-Type: application/json" -d "{\"question\":\"What does error code TS-999 mean?\",\"pipeline\":\"hybrid\"}"
```

Or skip HTTP and import it, the way a ticket bot would:

```
python examples/ticket_desk.py
```

## Two ways to run the lab (both are first-class)

Chunking, storage, BM25, vectors, and eval are always **local**. No key for that.

### 1. Harness (how developers work day to day)

Open this folder in VS Code. Start Claude Code, Grok, or Cursor. Ask in English. The harness already has a model on the plan.

- `run pytest`
- `run hybrid on error code TS-999`
- `compare naive vs hybrid on the eval file`

No `.env`. No API key. This is the everyday door.

### 2. CLI (same repo, what the screen-walkthrough films)

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest -q
python -m ragbench ask "What does error code TS-999 mean?" --pipeline hybrid
python -m ragbench eval --a naive --b hybrid
```

No key: retrieve is real, the answer is extractive (read from the chunks).

### Production-shaped generate (API key)

A shipped service retrieves, then calls a model with a secret. Copy `.env.example` to `.env`. Never commit `.env`.

Token Plan / Qwen (Anthropic-compatible, same shape as Claude Code `env_INFO`):

```
RAGBENCH_API_BASE=https://token-plan.ap-southeast-1.maas.aliyuncs.com/apps/anthropic
RAGBENCH_MODEL=qwen3.8-max-preview
RAGBENCH_API_KEY=your-key
RAGBENCH_API_BACKEND=anthropic
```

Or OpenAI-compatible:

```
RAGBENCH_API_BASE=https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
RAGBENCH_MODEL=qwen3.8-max
RAGBENCH_API_KEY=your-key
RAGBENCH_API_BACKEND=openai
```

```
python -m ragbench ask "What does error code TS-999 mean?" --pipeline hybrid --generate api
```

If a key is already in `.env`, `ask` uses the API unless you pass `--generate extractive`. `pytest` stays extractive.

## Ladder

| Pipeline | Section | What it is |
|---|---|---|
| `naive` | S2 | Fixed chunks, semantic-only vectors, top-k cosine |
| chunkers | S3 | `fixed`, `recursive`, `semantic`, `parent_child` |
| `hybrid` | S4 | BM25 + dense + RRF (k=60) + rerank + optional contextual prefix |
| `hyde` | S5 | Fake document, then retrieve neighbors |
| retrieve gate | S6 | Skip chitchat. Refuse unsupported answers |
| CRAG grade | S7 | Correct / Incorrect / Ambiguous. Web flag default off |
| `graph` | S8 | Tiny community summary. Not a full GraphRAG index |
| table rows | S9 | Row-level chunks + figure caption |
| `eval` | S10 | Faithfulness, context recall, needles, latency, cost column |
| `gov` | S11 | Tenant filter, PII redact, audit hashes |

## Failures the corpus is built to show

1. The 3 percent sentence does not name ACME or Q2 after a naive split.
2. `error code TS-999` can retrieve "error codes in general" if you only use the semantic embedder.
3. Global themes need the graph summary, not one vector hit.
4. A table cell and a figure caption are easy to smash or skip.

## Layout

```
data/acme/     teaching corpus
eval/          questions.jsonl
labs/          screen-walk programs (# %% cells, like a notebook)
notebooks/     optional .ipynb twin of lab 02
store/         the index you just built (manifest names the model)
ragbench/      the library (run_ask is the product)
examples/      ticket desk: how an app calls run_ask
runs/          metrics and ask logs
tests/         the suite you just ran
```

## Honesty

- A prompt loop is not Asai Self-RAG. We ship the loop and say so.
- Anthropic's 49 percent / 67 percent figures are theirs, September 2024.
- HyDE invents details on purpose.
- GraphRAG is not the default index.
- Web CRAG stays off unless policy turns it on.

## What is tested (no API key)

```
pytest -q
```

Covers: lost-company chunk split, TS-999 dense miss vs BM25 hit vs hybrid recover, RRF k=60 formula, retrieve-or-not chitchat, CRAG web flag off, tiny graph themes, PII redact + audit, naive vs hybrid eval file, HyDE / graph pipelines, table-row chunks, CLI ask + refuse, HTTP POST /ask, ticket handler, on-disk store + named embedder, naive lab run.

Not tested in CI (needs a paid key, later lectures): live OpenAI or Anthropic generation, hosted rerankers, a full Microsoft GraphRAG index.

MIT. Built by Pragati Kunwer.
