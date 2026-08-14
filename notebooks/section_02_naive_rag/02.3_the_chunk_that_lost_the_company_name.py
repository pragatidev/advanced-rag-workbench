# %% [markdown]
# # S2.3 The chunk that lost the company name
#
# Anthropic (19 Sep 2024) described this failure: the retrieved sentence is true,
# and the company name is gone. Our filing was written so a fixed 80-word split
# does the same thing. This is a chunking failure, not a model failure.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.chunking import chunk_corpus
from rag.corpus import load_documents

docs = load_documents()
chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
hit = [c for c in chunks if "revenue grew by 3%" in c.text.lower()]
assert hit, "the 3 percent sentence should still exist in some chunk"
for c in hit:
    print(c.chunk_id)
    print("  contains ACME:", "acme" in c.text.lower())
    print("  contains Q2:", "q2" in c.text.lower())
    print(c.text)
    print("---")
print("A true sentence without ACME or Q2 cannot answer 'What was ACME revenue growth in Q2 2023?'")
