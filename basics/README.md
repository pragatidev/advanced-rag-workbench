# Basics

Tiny scripts. One idea each. No API key. Corpus is `data/acme/`.

Run them in this order from the repo root, same interpreter as Section 2:

```
.venv\Scripts\python basics/embed_two_sentences.py
.venv\Scripts\python basics/similarity_scores.py
.venv\Scripts\python basics/cut_one_document.py
.venv\Scripts\python basics/store_and_ask.py
.venv\Scripts\python basics/mini_rag.py
```

1. `embed_two_sentences.py` — text becomes a list of numbers. Two ACME revenue sentences sit nearer than a password rule.
2. `similarity_scores.py` — cosine is the angle between those lists, written in plain math. A three-row ranked table.
3. `cut_one_document.py` — load the Q2 filing, cut it fixed-size, print one full chunk so you see what a chunk is.
4. `store_and_ask.py` — put those chunks in Chroma, ask one question, read the neighbors and their scores.
5. `mini_rag.py` — the capstone. Load the corpus, chunk, embed, store, retrieve, extract an answer. Your first working RAG program.

These use `HashEmbedder` so they stay offline. Section 3 does the same loop as lab checkpoints.
