# Hot RAM versus object-store vectors

Not the Monday loop. Monday is retrieve then generate: stuff a shortlist from the corpus.

## The wrong belief

Cost is only generate tokens. Storage tier and no-op re-embeds are the other bill.

## The picture

Where the vectors live is a cost lever.
Hot HNSW RAM versus object-store cold.
Namespace equals tenant.
Hash before you re-embed.

## Their comparison

turbopuffer architecture table: RAM plus 3x SSD versus S3 plus SSD cache.
Notion, 19 Feb 2026: 10x scale, 90 percent cost cut over two years, 60 percent search-engine spend cut on the turbopuffer migration. Page-state hashes cut write and embed volume 70 percent. That is their comparison.

## Refuse as Monday

This clone's loop is retrieve then generate on ACME markdown. Ten chunks. No turbopuffer account.
