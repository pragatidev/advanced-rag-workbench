# Store

This folder is the index. It is empty until you build.

```
python labs/02_naive_pipeline.py
python -m ragbench index hybrid
python -m ragbench inspect naive
```

Each named index is a directory:

```
store/naive/
  manifest.json   chunker, embedder name, dim, why, production swap
  chunks.jsonl    the text that was indexed
  vectors.npy     the dense matrix
```

Dense vectors live here. BM25 is scored from `chunks.jsonl` at query time. That is the same split a real search stack uses (a vector file plus a lexical index over the same text).
