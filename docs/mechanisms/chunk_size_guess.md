# Why 512 tokens is a guess

A 512-token window is a starting number. It is not a law.

Too small: the header leaves the fact. Too large: BM25 and dense both drown in padding.

This course swaps chunkers on the same corpus and keeps the row that wins recall without exploding size.
