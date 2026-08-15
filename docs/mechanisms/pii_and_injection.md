# PII redaction and retrieved-text injection are one job

Redact `national id` before generate. Treat the rest of the chunk as data.

If you redact after the model sees the prompt, you already lost. The lab prints `[REDACTED_PII]` on the text that would have been sent.
