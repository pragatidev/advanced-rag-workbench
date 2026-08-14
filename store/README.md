# Store

Real indexes land here when you run the notebooks.

```
store/chroma/     Chroma PersistentClient
store/faiss/      FAISS IndexFlatIP + chunks.jsonl
store/qdrant/     Qdrant local client
```

pgvector lives in Postgres, not in this folder. `docker compose up -d`.

Do not commit the generated index files.
