# Long prompts lose the middle

Liu et al. 2023: models use the start and the end of a long context more than the middle. A U-shaped accuracy curve.

After you rerank, pack winners at the ends of the prompt. Best chunk first. Second-best last. The middle can hold the rest.

Do this after rerank, not instead of it.
