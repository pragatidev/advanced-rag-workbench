# A cross-encoder re-ranks what cosine cannot

Bi-encoder cosine embeds query and doc separately. A cross-encoder reads (query, doc) as one pair and scores the pair.

Haystack's 2026 hybrid tutorial uses `BAAI/bge-reranker-base`. Anthropic retrieved 150 and kept 20.

This repo defaults to a labeled lexical stand-in so clone stays offline. Extra `local-rerank` loads the real cross-encoder. The API is the same function.
