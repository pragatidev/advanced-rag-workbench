# %% [markdown]
# # S18.4 AST chunking for code, named only
#
# Named frontier card. Not the Monday loop.
# This file prints the card and the split. It does not install cAST or tree-sitter.

# %%
"""S18.4: print the AST-chunking card. Does not install cAST or tree-sitter."""
from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

HERE = Path(__file__).resolve().parent
src_path = HERE / "classify_invoice.py"
src = src_path.read_text(encoding="utf-8")
page = (ROOT / "docs" / "mechanisms" / "ast_chunking.md").read_text(encoding="utf-8")

cut = src.index("->") + 2
left = src[:cut].rstrip()
right = src[cut:].lstrip()
right_head = right.splitlines()[0]

tree = ast.parse(src)
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef))
ret = ast.unparse(fn.returns) if fn.returns is not None else ""

print("=== not a filing window ===")
print("file docs/mechanisms/ast_chunking.md")
print("split through the return")
print("left", " ".join(left.split()))
print("right", right_head)
print("invented the model fills the type")
print("ast keeps the whole function")
print("name", fn.name)
print("return", ret)
print("rule A function is the unit.")
print()
print("=== classify_invoice.py ===")
print(src.strip())
print()
print("=== ast_chunking.md ===")
print(page.strip())
