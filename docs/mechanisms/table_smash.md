# Why text splitters smash tables

A PDF table is a 2-D layout. A character stream reads left to right and shears the row.

`12420` detaches from `paid_seats`. Naive RAG cannot answer the table question.

A layout parser (Docling, local, MIT) restores rows. The fallback in this repo is a labeled markdown restore of the same table. The parser name is printed so the swap is honest.

Restore the rows before you split.

Dump the print commands of a PDF from the repo root:

    .venv\Scripts\python notebooks/section_13_multimodal_tables_and_images/S13_1_dump_print_commands.py

Pass your own file as the argument. Ask whether the number you care about still sits in the same print command as its label.

