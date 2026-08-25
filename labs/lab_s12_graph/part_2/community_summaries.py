"""Step two of a tiny graph: write one summary per community, at index time.

Global mode never searches your chunks at question time. It reads summaries that
were written once, here. This file builds the same graph part_1 built (by
importing part_1 directly), collects each community's own chunks, and writes one
summary per community to disk.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
# labs/ is not a package, so part_1 goes on the path by folder.
PART_1 = HERE.parent / "part_1"
if str(PART_1) not in sys.path:
    sys.path.insert(0, str(PART_1))

from build_tiny_graph import (  # noqa: E402
    build_communities,
    build_edges,
    build_members,
    load_chunks,
)

from rag.chunkers import Chunk  # noqa: E402
from rag.settings import Settings, load_env  # noqa: E402
from rag.text import split_sentences, tokenize  # noqa: E402

OUT_PATH = HERE / "community_summaries.json"

# The index time prompt. There is no question yet, so the theme is the question.
PROMPT = (
    "Summarize what this group of sources is about, as one theme. "
    "Answer only from the supplied text. Two sentences maximum."
)

STOPWORDS = frozenset(
    "a an and are as at be by can do does for from has have if in into is it its "
    "may must no not of on or over s that the their them then there these this to "
    "was what when where which who will with you your".split()
)


def community_chunks(community: list[str], members: dict[str, list[str]]) -> list[str]:
    """The community's evidence: every chunk id where any of its entities appears."""
    chunk_ids: set[str] = set()
    for entity in community:
        chunk_ids.update(members.get(entity, []))
    return sorted(chunk_ids)


def _content(text: str) -> list[str]:
    return [word for word in tokenize(text) if word not in STOPWORDS]


def _extractive(entity_names: list[str], texts: list[str]) -> str:
    """No key, no server: the two sentences of this community's own text that are
    most made of its own entity words. Derived from the corpus, never hand written."""
    wanted = set(_content(" ".join(entity_names)))
    scored: list[tuple[float, str]] = []
    for text in texts:
        for sentence in split_sentences(text):
            if sentence.lstrip().startswith("#") or sentence.endswith("?"):
                continue
            words = _content(sentence)
            if not words:
                continue
            scored.append((len(wanted.intersection(words)) / len(words), sentence))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    picked = [sentence for _, sentence in scored[:2]]
    return " ".join(picked) if picked else "(no text)"


def summarize(name: str, entity_names: list[str], texts: list[str]) -> tuple[str, str]:
    """One community in, one summary out. Returns (summary, mode)."""
    load_env()
    # The same switch S2.1 taught: RAGBENCH_GENERATE. Ships extractive.
    if Settings.generate_mode != "api":
        return _extractive(entity_names, texts), "extractive"
    from rag.llm import chat

    chunks = [
        Chunk(chunk_id=f"{name}:{i}", doc_id=name, title=name, text=text)
        for i, text in enumerate(texts)
    ]
    try:
        result = chat(PROMPT, chunks)
    except Exception:  # a dead endpoint must not fake a summary
        print(f"  {name}: model call did not return, falling back to extractive")
        return _extractive(entity_names, texts), "extractive"
    return result["text"], "api"


def main() -> None:
    chunks = load_chunks()
    members = build_members(chunks)
    edges = build_edges(chunks, members)
    communities = build_communities(members, edges)
    by_id = {chunk.chunk_id: chunk.text for chunk in chunks}

    written: dict[str, dict] = {}
    calls = 0
    mode = "extractive"
    for i, entity_names in enumerate(communities):
        name = f"community_{i}"
        chunk_ids = community_chunks(entity_names, members)
        texts = [by_id[chunk_id] for chunk_id in chunk_ids]
        summary, mode = summarize(name, entity_names, texts)
        if mode == "api":
            calls += 1
        written[name] = {
            "entities": entity_names,
            "chunks": chunk_ids,
            "summary": summary,
        }
        print(f"{name}  entities: {', '.join(entity_names)}")
        print(f"  chunks: {', '.join(chunk_ids)}")
        print(f"  summary: {summary}")
        print()

    print(
        f"summaries_written {len(written)}   "
        f"model_calls {calls}   mode {mode}"
    )
    OUT_PATH.write_text(
        json.dumps(written, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("wrote", OUT_PATH.as_posix())


if __name__ == "__main__":
    main()
