# Rerank lives on a 2-second board

Interview Coder Q29 (26 May 2026) walks a 2-second RAG response:
embed 50-100 ms, retrieve 50-150, rerank 100-300, first token 300-800.

Skip the reranker when the first-stage score is already confident (KalyanKS Q68).

Do not rerank 150 pairs on CPU at 40 QPS without a measured number.
Anthropic (19 Sep 2024) retrieved 150 and kept 20. That is their width, not a CPU order.

Towards Data Science (11 Apr 2026): at 40 QPS a cross-encoder p99.9 exceeded 21 seconds. ColBERT p50 was 23 ms.
Redis (26 Jul 2026): measure reranker latency against your app's budget, not in isolation.
BigData Boutique (13 May 2026): typical NDCG@10 lift 5-15 points for under 200 ms.

A millisecond print is a clock. A budget has a p95 and a skip rule.
