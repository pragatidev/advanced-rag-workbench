"""Table rows, figure captions, PDF smash, and Docling restore."""

from __future__ import annotations

from pathlib import Path

from rag.chunkers import Chunk
from rag.corpus import DATA, Document, load_documents

PDF_PATH = DATA / "tables" / "q2_kpis.pdf"
CAPTION_PATH = DATA / "figures" / "caption.txt"


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


def caption_chunks(path: Path | None = None) -> list[Chunk]:
    src = path or CAPTION_PATH
    text = src.read_text(encoding="utf-8").strip()
    return [
        Chunk(
            chunk_id="figure_seats:caption:0",
            doc_id="figure_seats",
            title="ACME Q2 2023 seats figure caption",
            text=text,
            metadata={"doc_type": "figure", "tenant": "shared", "chunker": "caption"},
        )
    ]


def naive_pdf_extract(path: Path | None = None) -> str:
    """Read PDF bytes as latin-1 and keep printable runs. No layout."""
    src = path or PDF_PATH
    raw = src.read_bytes()
    text = raw.decode("latin-1", errors="replace")
    chars = []
    for ch in text:
        if ch.isprintable() or ch in "\n\t":
            chars.append(ch)
        else:
            chars.append(" ")
    blob = "".join(chars)
    blob = " ".join(blob.split())
    return blob


def smash_report(path: Path | None = None) -> dict:
    blob = naive_pdf_extract(path)
    return {
        "chars": len(blob),
        "has_12420": "12420" in blob,
        "has_paid_seats_near_12420": "paid_seats" in blob and "12420" in blob,
        "row_intact": "paid_seats" in blob and "11800" in blob and "12420" in blob and "| paid_seats |" in blob,
        "extract": blob[:400],
    }


def _pdf_string_text(token: str) -> str:
    """Unescape a PDF literal string token that still has its wrapping parentheses."""
    inner = token[1 : token.rfind(")")]
    return inner.replace("\\\\", "\\").replace("\\(", "(").replace("\\)", ")")


def _content_stream(raw: str) -> str:
    start = raw.find("stream")
    end = raw.find("endstream")
    if start < 0 or end <= start:
        return raw
    return raw[start + len("stream") : end]


def dump_print_commands(path: Path | None = None) -> dict:
    """List every Tj print command in a PDF content stream.

    row_intact is True only when 12420 sits inside the same command that
    starts with paid_seats. That is the shear check this lecture teaches.
    """
    src = path or PDF_PATH
    raw = src.read_bytes().decode("latin-1", errors="replace")
    body = _content_stream(raw)
    import re

    tokens = re.findall(r"\((?:\\.|[^\\)])*\)\s*Tj", body)
    commands = [_pdf_string_text(tok[: tok.rfind(")") + 1]) for tok in tokens]
    label = next((c for c in commands if c.startswith("paid_seats")), "")
    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    shear: list[str] = []
    capturing = False
    for ln in lines:
        if "(paid_seats 11800)" in ln and "Tj" in ln:
            capturing = True
        if capturing:
            shear.append(ln)
        if capturing and "(12420)" in ln and "Tj" in ln:
            break
    try:
        rel = src.resolve().relative_to(DATA.parent.parent)
        pdf_label = rel.as_posix()
    except ValueError:
        pdf_label = src.as_posix()
    return {
        "pdf": pdf_label,
        "print_commands": commands,
        "label_command": label,
        "has_12420": any("12420" in c for c in commands),
        "row_intact": "12420" in label,
        "shear_window": shear,
    }


def emit_print_commands(path: Path | None = None) -> None:
    """Print the dump a student can re-run. One line per field. No invented rows."""
    dump = dump_print_commands(path)
    print("pdf", dump["pdf"])
    print("print_commands")
    for text in dump["print_commands"]:
        print("Tj", text)
    print("label_command", dump["label_command"])
    print("has_12420", dump["has_12420"])
    print("row_intact", dump["row_intact"])
    print("shear_window:")
    for ln in dump["shear_window"]:
        print(ln)


def _fallback_rows() -> list[dict]:
    docs = {d.doc_id: d for d in load_documents()}
    rows = table_row_chunks(docs["q2_kpis"])
    return [{"parser": "markdown-fallback", "text": r.text, "chunk_id": r.chunk_id} for r in rows]


def parse_tables(path: Path | None = None) -> dict:
    """Docling when installed. Labeled markdown fallback otherwise."""
    src = path or PDF_PATH
    try:
        from docling.document_converter import DocumentConverter
    except ImportError:
        return {
            "parser": "markdown-fallback",
            "note": "Docling not installed. Using labeled markdown restore of data/acme/tables/q2_kpis.md.",
            "rows": _fallback_rows(),
        }
    try:
        conv = DocumentConverter()
        result = conv.convert(str(src))
        text = result.document.export_to_markdown()
        rows = []
        for i, line in enumerate(text.splitlines()):
            if "12420" in line or "paid_seats" in line:
                rows.append({"parser": "docling", "text": line, "chunk_id": f"docling:{i}"})
        if not rows:
            rows = [{"parser": "docling", "text": text[:500], "chunk_id": "docling:0"}]
        return {"parser": "docling", "note": "Docling layout parse", "rows": rows}
    except Exception as exc:
        return {
            "parser": "markdown-fallback",
            "note": f"Docling failed ({exc}). Using labeled markdown restore.",
            "rows": _fallback_rows(),
        }


def multimodal_chunks() -> list[Chunk]:
    docs = {d.doc_id: d for d in load_documents()}
    chunks = table_row_chunks(docs["q2_kpis"])
    chunks.extend(caption_chunks())
    return chunks
