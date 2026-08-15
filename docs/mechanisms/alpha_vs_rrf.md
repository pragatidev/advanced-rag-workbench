# Why ranks beat scores

Alpha hybrid: `alpha * dense + (1-alpha) * sparse` after you scale both to the same range.

If you skip the scale, unbounded BM25 scores swamp cosine in [-1, 1]. The table in the lab shows that swamp.

Reciprocal Rank Fusion ignores the raw numbers:

    RRFscore(d) = sum 1 / (k + rank)     with k = 60 (Cormack 2009)

Missing lists contribute 0. The fused order is neither input list.
