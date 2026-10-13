# Basics

Tiny scripts. One idea each. No API key. Corpus is `data/acme/`.

Run them from the repo root, with the `.venv` you made in Section 1 active.

## Section 1: why RAG

```
.venv\Scripts\python basics/cold_ask.py
.venv\Scripts\python basics/grounded_ask.py
.venv\Scripts\python basics/two_chunks_flags.py
```

1. `cold_ask.py`: TS-999 asked with no documents, of the hosted door in `.env` (Anthropic or OpenAI-compatible; skipped with no key) and of a local model (the local door in `.env`, such as LM Studio, or else Ollama on `localhost:11434`), then the three pieces retrieval finds for the same question.
2. `grounded_ask.py`: the same question through both steps of RAG. Step one finds the same three pieces. Step two sends them to the model in `.env` with the workbench's own instructions (answer only from the pieces, cite them) and prints the message as sent and the answer. Local Ollama needs no key; with no model server running, it prints `SKIPPED` after step one.
3. `two_chunks_flags.py`: the fixed cut on the Q2 filing, both pieces, and which piece holds the name and which the number.

## Section 2: how a language model answers

```
.venv\Scripts\python basics/count_what_you_send.py
```

1. `count_what_you_send.py`: the TS-999 question sent to the local model three times, with the model's own meter printed each time: the three pieces retrieval finds, the whole of `data/acme`, and the whole pile again with the model's window set to 512 tokens on purpose. It reads Ollama's own meter (`/api/chat`, `/api/ps`), so it asks the local door in `.env`, or Ollama on `localhost:11434`; with no Ollama answering it prints `SKIPPED`. No key.

## Sections 3 and 4: the foundations

Run them in this order:

```
.venv\Scripts\python basics/embed_two_sentences.py
.venv\Scripts\python basics/similarity_scores.py
.venv\Scripts\python basics/cut_one_document.py
.venv\Scripts\python basics/store_and_ask.py
.venv\Scripts\python basics/mini_rag.py
```

1. `embed_two_sentences.py`: text becomes a list of numbers. Two ACME revenue sentences sit nearer than a password rule.
2. `similarity_scores.py`: cosine is the angle between those lists, written in plain math. A three-row ranked table.
3. `cut_one_document.py`: load the Q2 filing, cut it fixed-size, print one full chunk so you see what a chunk is.
4. `store_and_ask.py`: put those chunks in Chroma, ask one question, read the neighbors and their scores.
5. `mini_rag.py`: the capstone. Load the corpus, chunk, embed, store, retrieve, extract an answer. Your first working RAG program.

These use `HashEmbedder` so they stay offline. Section 3 does the same loop as lab checkpoints.
