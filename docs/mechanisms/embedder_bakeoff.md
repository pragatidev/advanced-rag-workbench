# The embedder is a bake-off, not a brand

Two embedders on the same chunks and the same question file. That is the experiment.

This repo's offline stand-in is `HashEmbedder`. It is named so you do not pretend it is Voyage.

Monday swaps that do not need a rewrite:

- `nomic-embed-text` (Ollama)
- `text-embedding-3-large` (OpenAI, default 3072 dims, optional MRL `dimensions=`)
- `all-MiniLM-L6-v2` (local ONNX)

The bake-off reports recall@k and embed_ms. Keep the winner for this corpus, not the brand.
