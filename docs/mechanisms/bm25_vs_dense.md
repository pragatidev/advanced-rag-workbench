# Why embeddings miss error codes

`HashEmbedder(semantic_mode=True)` downweights rare IDs. "error codes in general" ranks above TS-999. That is the same miss a real semantic model makes on a rare token.

BM25 sees the raw token. It locks TS-999.

The fix is not "better embeddings." The fix is to run both and fuse ranks.
