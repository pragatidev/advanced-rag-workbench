# Precision, recall, MRR, MAP, nDCG

Accuracy is the wrong word for a ranked list.

Precision at k: how many of the top k are labeled relevant.

Recall at k: how many of the labeled relevant items landed in the top k.

Perfect recall at 10 with low precision at 10 still stuffs junk into generate.

MRR: one over the rank of the first relevant item. It celebrates the first hit. It is the wrong metric when several chunks are relevant.

MAP: average precision across every relevant rank. It counts both golds.

nDCG: the same hits, discounted by rank, then divided by the ideal ranking.

This workbench does not install a ranking library. The functions take a binary relevance list.
