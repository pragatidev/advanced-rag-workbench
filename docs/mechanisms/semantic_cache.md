# Three cache layers, and one skip

1. Exact string hit.
2. Near-neighbor hit (cosine above a threshold).
3. Personalized skip: do not reuse an answer that names a user or tenant.

A stale or personalized answer gets amplified if you skip layer 3. The lab prints HIT, a threshold decision, and SKIP_PERSONALIZED.
