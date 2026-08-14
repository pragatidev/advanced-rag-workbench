"""Table rows and figure captions as first-class chunks."""

from __future__ import annotations

from ragbench.chunkers import Chunk
from ragbench.corpus import Document


def table_row_chunks(doc: Document) -> list[Chunk]:
    chunks: list[Chunk] = []
    n = 0
    for line in doc.text.splitlines():
        if "|" not in line or set(line.strip()) <= set("|-: "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or cells[0].lower() == "kpi":
            continue
        text = " | ".join(cells)
        chunks.append(
            Chunk(
                chunk_id=f"{doc.doc_id}:row:{n}",
                doc_id=doc.doc_id,
                title=doc.title,
                text=text,
                metadata={**doc.metadata, "chunker": "table_row"},
            )
        )
        n += 1
    return chunks
