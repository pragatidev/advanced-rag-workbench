# AST chunking for code, named only

Not the Monday loop. Monday is retrieve then generate: stuff a shortlist from the corpus.

## The wrong belief

The same fixed window that cuts filings should cut a repo. A function is the unit.

## The split

A function split through its return invents the type.
An AST cut keeps the whole function in one chunk.

## cAST

Zhang et al. arXiv 2506.15655, 18 Jun 2025, CMU and Augment Code.
Recursive AST split-then-merge via tree-sitter.
Recall@5 plus 4.3 on RepoEval retrieval is their comparison.
Pass@1 plus 2.67 on SWE-bench generation is their comparison.
StarCoder2-7B plus 5.5 average on RepoEval versus fixed-size is their comparison.

## Cousin

Heading-aware cuts on documents. AST cuts on code.
Sourcegraph Cody: search-first RAG plus a code graph.
Course identity stays enterprise documents. No SWE-bench lab.

## Refuse as Monday

This clone's loop is retrieve then generate on ACME markdown. AST chunking is a later tax.
