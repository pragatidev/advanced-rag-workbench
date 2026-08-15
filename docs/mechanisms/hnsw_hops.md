# HNSW hops, not a full scan

Dense search is cosine in a vector space. The store does not scan every vector.

HNSW (Hierarchical Navigable Small World) is a layered graph:

- The upper layer is sparse. The query hops long distances.
- Lower layers are denser. The query walks to nearer neighbors.
- Search stops at a neighborhood. It is not a full scan.

Two knobs you will see on Qdrant and pgvector:

- `M`: how many neighbors each node keeps.
- `ef` / `efSearch`: how wide the search is at query time.

The picture in this lecture is the hop already running under `store/qdrant/`.
