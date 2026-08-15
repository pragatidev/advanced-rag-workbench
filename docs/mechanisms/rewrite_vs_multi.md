# Rewrite versus multi-query

Rewrite: one better search string. Leave IDs alone. "TS-999" must stay "TS-999".

Multi-query: several diverse searches, then fuse. Cost is N retrieves, sometimes N generates.

HyDE is neither. It writes a ghost document and retrieves neighbors of that document.

Drop any rewrite whose cost exceeds its recall lift.
