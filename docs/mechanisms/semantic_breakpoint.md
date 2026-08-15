# Cosine-breakpoint semantic chunking

Embed consecutive sentences. Plot cosine(sentence_i, sentence_i+1). Cut where the line crosses a low-similarity percentile.

That is the LlamaIndex SemanticSplitter idea. This repo implements it in `rag/chunking/semantic.py` with `HashEmbedder` so the lab stays offline.

It is not "one chunk per heading." Heading split is `semantic_heading` and is labeled as such.
