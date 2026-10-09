# LLM as judge is not ground truth

Judges have three named failure modes.

Position bias: the first slot wins when you swap the same pair.

Verbosity bias: the longer answer wins even when it missed the gold span.

Self-preference: the judge prefers the family it was trained as.

Calibrate against humans. A judge score is not a label.

Offline golden is not online thumbs. The tagged file is one object. Live thumbs are another.

Changing the chunker moves the IDs, so retrieval metrics on a frozen candidate set lie. You also need end to end.

This workbench does not install an LLM as judge library. The functions take labeled pairs.
