---
name: ask-acme
description: Answer a question over the ACME policy, filing, error catalog, FAQ, and tables. Use when the user asks about ACME, TS-999, revenue, seats, access control, PII, or the sample corpus.
---

# Ask ACME

This is how a harness invokes RAG. Do not invent file contents. Retrieve first.

```
python -m ragbench ask "<their question>" --pipeline hybrid
```

Read the JSON. Cite `chunk_id` values. If the answer is REFUSE, say the retrieve missed and do not guess.

A real product does not use the CLI. It imports the same function:

```
from ragbench import run_ask
run_ask(question, pipeline="hybrid")
```

Or it POSTs to the desk:

```
POST http://127.0.0.1:8787/ask
{"question": "...", "pipeline": "hybrid"}
```

Ticket-shaped wrapper: `python examples/ticket_desk.py`

To compare pipelines:

```
python -m ragbench eval --a naive --b hybrid
```
