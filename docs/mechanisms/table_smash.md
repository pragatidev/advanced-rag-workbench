# Why text splitters smash tables

A PDF table is a 2-D layout. A character stream reads left-to-right and shears the row.

`12420` detaches from `paid_seats`. Naive RAG cannot answer the table question.

A layout parser (Docling, local, MIT) restores rows. The fallback in this repo is a labeled markdown restore of the same table. The parser name is printed so the swap is honest.
