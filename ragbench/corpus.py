"""Load the ACME teaching corpus. No Nike files. Paths stay inside this repo."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "acme"


@dataclass
class Document:
    doc_id: str
    title: str
    path: str
    text: str
    metadata: dict = field(default_factory=dict)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_documents(data_dir: Path | None = None) -> list[Document]:
    base = data_dir or DATA
    specs = [
        (
            "filing_q2_2023",
            "ACME Q2 2023 filing excerpt",
            base / "filings" / "q2_2023_excerpt.md",
            {"doc_type": "filing", "tenant": "shared", "as_of": "2023-06-30"},
        ),
        (
            "error_catalog",
            "Platform error catalog",
            base / "runbooks" / "error_catalog.md",
            {"doc_type": "runbook", "tenant": "shared"},
        ),
        (
            "access_control",
            "ACME access control policy",
            base / "policies" / "access_control.md",
            {"doc_type": "policy", "tenant": "shared"},
        ),
        (
            "privacy",
            "ACME privacy and retention",
            base / "policies" / "privacy.md",
            {"doc_type": "policy", "tenant": "shared"},
        ),
        (
            "faq",
            "ACME support FAQ",
            base / "faq" / "support.md",
            {"doc_type": "faq", "tenant": "helix-east"},
        ),
        (
            "q2_kpis",
            "ACME Q2 2023 KPI table",
            base / "tables" / "q2_kpis.md",
            {"doc_type": "table", "tenant": "shared"},
        ),
        (
            "figure_seats",
            "ACME Q2 2023 seats figure caption",
            base / "figures" / "caption.txt",
            {"doc_type": "figure", "tenant": "shared"},
        ),
    ]
    docs: list[Document] = []
    for doc_id, title, path, meta in specs:
        docs.append(
            Document(
                doc_id=doc_id,
                title=title,
                path=str(path.relative_to(base.parent.parent)).replace("\\", "/"),
                text=_read(path),
                metadata=meta,
            )
        )
    return docs
