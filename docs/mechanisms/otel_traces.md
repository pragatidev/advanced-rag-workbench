# An OTel-shaped trace

This is not a Langfuse install. It is a JSONL span with the names OpenTelemetry GenAI conventions use:

- `trace_id`, `span_id`
- `latency_ms`
- `gen_ai.request.model`
- `tokens`, `usd`
- retrieval `chunk_ids`

Every ask writes one. The prod board greps two.
