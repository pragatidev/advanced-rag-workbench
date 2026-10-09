# The index is a derived view

The files are the source. The vectors are computed. When one file changes, only that file walks to the embedder.

Upsert by a stable chunk key (document id plus a hash of the span). Tombstone the old id so a stale vector cannot retrieve. Freshness is an SLO, seconds not a nightly rebuild.

Nightly re-embed of an unchanged warehouse is a design failure for docs that change daily. The 50,000 versus 500 arithmetic is RisingWave example math, not this clone.

HNSW does not vacuum on delete. A tombstone is a flag the retriever honors. Soft delete flags can bloat until you compact.
