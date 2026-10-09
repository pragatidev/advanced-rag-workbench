# Cost per query includes cheaper vectors

Count generate calls. Count tokens. Convert to USD from the provider table.

HyDE is +1 generate. Multi-query is +N. A semantic cache hit is 0.

Vector search is cheap next to generate. Still print it. The board is dollars, not vibes.

Do not add a generate before retrieve unless the board pays. HyDE writes a ghost first. That extra generate sits on a 2-second p95. Refuse it when the budget is already tight.

Quantization is a bytes table, not a required lab. Float32 to int8 is about 4x. Binary is about 32x. Matryoshka lets you truncate dimensions first. Do not install a quantized index to pass this lecture.

This workbench prints usd 0.0 on the local toy stack. Fill the column from the usage object when a key is present.
