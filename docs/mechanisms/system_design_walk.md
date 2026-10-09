# Design a RAG system station by station

The walk is six stations in interview order, not teaching order.

1. Requirements. Five scoping questions: corpus size and formats, query mix, p95, cost per query, who is allowed and is abstention allowed.
2. Ingestion. Parse, chunk, embed, version the embedder, upsert, tombstone deletes, index lag as an SLO.
3. Retrieval. Query rewrite, hybrid (dense plus BM25), fuse with RRF, ACL pre-filter, rerank, pack.
4. Generation. Grounded prompt, citations, refuse when weak, retrieved text as data. Fallback: abstain, show sources, clarify, ticket.
5. Evals. Per-stage metrics, golden file, CI regression gate.
6. Ops. Traces, cache, freshness, cost, drift, three-bin debug: missing, mis-ranked, ignored.

Refuse to start at a vendor name. Speak a 2-second budget and a cost column in one breath.

Interview Coder Q29 board: embed 50-100 ms, retrieve 50-150, rerank 100-300, first token 300-800.

Do not add HyDE under a 2-second p95. HyDE is plus one generate.

Ten thousand tenants is a spoken tradeoff: separate index, shared plus filter, or hybrid. Not a cluster lab.
