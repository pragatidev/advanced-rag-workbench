# Choose a graph family, or refuse it

Refuse the graph when local still holds.

A graph is not a better index. It is a different index, and it costs a pass over the whole
corpus with a language model before anybody asks a question. Earn that bill by failing first,
on a question the vector pipeline genuinely cannot answer. See `local_vs_global.md`.

## The refuse test

Take the questions that actually failed.

- Local failures (one span in one document holds the answer): not a graph problem. Chunking or
  ranking. Cheaper cures, already in this repo.
- A global failure (the answer is a property of the whole corpus: name the themes, count the
  incidents, tell me what changed across the quarter): now shop for a family.

Write the refusal down next to the failing question, so nobody relitigates it in six months.

## The four questions that pick the family

1. What can you afford at index time? Some families summarize every community up front with a
   model. Some do almost nothing up front and pay at query time instead.
2. Does the answer come from a theme, or from a chain? A theme wants a summary over a group of
   documents. A chain wants to walk from one fact to the next.
3. Does the domain have real types and real rules (a table, a policy clause, a defined unit of
   knowledge), or is plain prose enough?
4. Do you need a graph at all, or do you need structure over your documents?

## The six names

| Family | Answers | Cost shape |
|---|---|---|
| GraphRAG (Microsoft) | entities + relationships, Leiden communities, a summary on every community | dense at index time |
| LazyGraphRAG | same idea, summarization deferred to query time | cheap index, pays per question |
| LightRAG | dual level keywords: narrow entity terms and broad theme terms, merged | mid |
| HippoRAG | personalized PageRank seeded from the question entities, relevance spreads along edges | mid |
| KAG | typed indexes walked by a logic form instead of an unnamed community blob | schema work up front |
| RAPTOR | not a graph: cluster chunks, summarize, cluster the summaries, read the upper levels | tree build |

## KAG is a card, not an install

KAG 0.8.0 (OpenSPG, 27 Jun 2025) defines six built-in index types over your documents:

    Outline · Summary · KnowledgeUnit · AtomicQuery · Chunk · Table

A question arrives as a logic form and walks that schema, choosing which typed index answers it.
You can copy those six index types onto your own corpus in an afternoon and get most of the value
with OpenSPG nowhere near your machine. Source: https://github.com/OpenSPG/KAG

## What the Section 12 lab actually ships

A seeded tiny graph on ACME. Not a Microsoft index. If local questions still hold, it prints
REFUSE and skips the graph cost. See `refuse_shelf.md`.
