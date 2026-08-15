# Index small, generate from neighbors

Three mechanisms, not one nickname:

- Parent-child: retrieve a small child; generate from a stored parent.
- Sentence-window: retrieve one sentence; reconstruct prev/next from metadata.
- Auto-merge: if several leaves of one parent hit, replace them with that parent.

They are not interchangeable. Measure each. Keep only the one the board pays for.
