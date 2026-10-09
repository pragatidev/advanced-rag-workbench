# An OTel-shaped trace

This is not a Langfuse install. It is a JSONL span with names shaped to match the OpenTelemetry GenAI conventions, and one of them, `gen_ai.request.model`, is theirs:

- `trace_id`, `span_id`
- `latency_ms`
- `gen_ai.request.model`
- `tokens`, `usd`
- retrieval `chunk_ids`

Every ask writes one. The prod board greps two.
