# A new embedder cannot query an old index

A v3 query against a v1 column returns a cosine number and no error. Mixed spaces fail silently. The store will not warn you.

Same words, different coordinates. The salt is the version. Do not query the new model against the old column even if the names match. The space is the name that matters.

Production pattern: side by side columns, shadow traffic, feature flag cutover. Fill the new column beside the live one. Flip when the new space is ready. Notion re-embedded on a provider move. Full re-index, not in place.

This clone uses two hash salts so the geometry is visible offline. A hosted model swap is the same geometry with a bigger bill. Drift-Adapter ninety five to ninety nine percent is their tested setting, not a number we measured here.
