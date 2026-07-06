# RAG Hole Finder

<p align="center">
  <img src="assets/readme-cover.svg" alt="RAG Hole Finder cover" width="100%" />
</p>

Find unsupported answers and citation gaps in RAG evaluation files.

## Working notes

- quick local checks around retrieval quality
- small CI jobs where a readable report is enough
- review workflows that need deterministic output
- examples based on `examples/rag-cases.jsonl`

## Install

```bash
git clone https://github.com/mertefekurt/rag-hole-finder.git
cd rag-hole-finder
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Use

```bash
rag-hole-finder examples/rag-cases.jsonl
```

## Files

```text
.github/        CI workflow
examples/       sample inputs
src/            package source
tests/          test coverage
.gitignore      project file
pyproject.toml  package metadata
```
