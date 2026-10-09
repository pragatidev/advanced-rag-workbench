# Three cache layers, and one skip

1. Exact string hit. Same bytes. Skip generate.
2. Near-neighbor hit. Cosine at or above a threshold. Skip generate.
3. Provider prompt cache. Still generate. The stuffed prefix can be billed cheaper.

Skip: do not reuse an answer that names a user or tenant. Do not store a personalized question.

A stale or personalized answer gets amplified if you skip that check. Nearby is a threshold, not a vibe. The lab prints HIT, a threshold decision, and SKIP_PERSONALIZED.

Keep this page next to the print.
