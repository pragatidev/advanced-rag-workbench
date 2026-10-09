# Faithfulness is not context recall

Context recall: did the retrieved set contain the gold span?

Faithfulness: did the answer stick to the retrieved set?

A fluent answer that used the wrong chunks can score high on faithfulness and low on context recall. That is the failure the lab labels.

The RAG triad names both plus answer relevance.

Es et al. 2023 published three reference-free judges: faithfulness, answer relevance, context relevance. The later library adds Context Precision and Context Recall, which need a reference. Do not say Es et al. published four RAGAS scores.

This workbench does not install RAGAS. Faithfulness here is extractive token support. Context recall here is whether the gold span sits in the retrieved text.
