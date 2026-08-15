# Retrieve, then generate

Advanced RAG is retrieve-then-generate plus the controls you add when the wrong span answers.

1. Split documents into chunks.
2. Embed and index the chunks.
3. For a question, hop an HNSW graph to a shortlist.
4. Stuff only those chunks into the prompt.
5. The model cannot see the rest of the corpus.

Lewis 2020 trained BART plus DPR. Production "naive RAG" is prompt stuffing. This course measures the production loop.

The question file is `eval/questions.jsonl`. The product door is `rag.ask.run_ask` and `POST /ask`.
