# rag-hole-finder

![rag-hole-finder banner](assets/banner.svg)

A tiny offline diagnostic for RAG evaluation JSONL. It does not grade prose style; it looks for the more
operational failures that make a RAG answer hard to trust.

> Question answered but no citation? Retrieved context present but answer vocabulary barely overlaps?
> Source date outside your freshness window? That is a hole worth reviewing.

## Input

Each line is a case:

```json
{"id":"refund-01","question":"How long do refunds take?","answer":"Usually two days.","citations":[],"contexts":["Refunds settle in 5-7 business days."],"source_date":"2024-01-15"}
```

## Run

```bash
rag-hole-finder examples/rag-cases.jsonl --min-overlap 0.25 --as-of 2026-07-03
rag-hole-finder examples/rag-cases.jsonl --json
```

## Hole labels

| label | meaning |
| --- | --- |
| `missing-citation` | answer has no citation list |
| `low-context-overlap` | answer terms do not show up in retrieved context |
| `stale-source` | source date is older than the allowed window |
| `empty-answer` | model returned no useful answer |

## Development

The test suite covers JSONL parsing, overlap scoring, stale-source handling, JSON rendering, and CLI help.

MIT.
