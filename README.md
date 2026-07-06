# RAG Hole Finder

Find unsupported answers and citation gaps in RAG evaluation files.

![RAG Hole Finder cover](assets/readme-cover.svg)

## What it looks for

- weak overlap between answer and cited material
- stale evidence based on `--as-of` and `--max-age-days`
- cases where the answer reads stronger than its support

```bash
git clone https://github.com/mertefekurt/rag-hole-finder.git
cd rag-hole-finder
python -m pip install -e ".[dev]"
rag-hole-finder examples/rag-cases.jsonl --min-overlap 0.25
```
