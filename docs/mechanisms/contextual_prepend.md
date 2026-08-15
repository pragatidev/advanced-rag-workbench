# Contextual chunks restore the missing header

Anthropic-style contextual retrieval prepends a short sticker before embed and before BM25:

    This chunk is from ACME Q2 2023 filing excerpt (doc filing_q2_2023).

The orphan 3% sentence now names its source. This repo does it from the title we already have. No LLM rewrite of every chunk.

That is cheaper than the paper's LLM prepend and enough to teach the mechanism.
