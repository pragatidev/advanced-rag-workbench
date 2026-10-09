# %% [markdown]
# # S15.1 Why cost per query includes cheaper vectors
#
# Generate calls, tokens, USD. Cheaper vectors are a bytes table.
# Do not add HyDE under a 2-second p95.

# %%
"""S15.1: USD board, live usage convert, cheaper-vector bytes."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.eval.cost import USD_PER_1K_IN, USD_PER_1K_OUT, estimate, usd_from_tokens

print("=== generate calls ===")
for name, extra in (("naive", 0), ("hybrid", 0), ("hyde", 1)):
    row = estimate(name, extra_generates=extra)
    print(name, "generate_calls", row["generate_calls"], "usd", row["usd"])
print("note", estimate("naive")["note"])

print()
print("=== live usage object ===")
# Usage counts from the lecture 2.1 ask receipt,
# section_2/lecture_2_1 demo/ask_run_token_bill.txt. Not re-invented.
input_tokens = 413
output_tokens = 172
print("input_tokens", input_tokens)
print("output_tokens", output_tokens)
print("usd_from_table", round(usd_from_tokens(input_tokens, output_tokens), 6))
print("table_in_per_1k", USD_PER_1K_IN)
print("table_out_per_1k", USD_PER_1K_OUT)

print()
print("=== cheaper vectors, 1M x 1536-dim ===")
DIM = 1536
N = 1_000_000
print("dtype", "bytes_per_vec", "gb_per_1M", "shrink")
specs = (("float32", 4.0), ("int8", 1.0), ("binary", 0.125))
base_bytes = DIM * 4.0
for dtype, nbytes in specs:
    b = DIM * nbytes
    gb = (b * N) / 1_000_000_000.0
    shrink = int(round(base_bytes / b))
    print(dtype, int(b) if b == int(b) else b, gb, str(shrink) + "x")

print()
print("=== Hyde under a 2s p95 ===")
print("hyde extra generate", 1)
print("rule refuse Hyde when p95 budget is 2 seconds")
