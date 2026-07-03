from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from rag_hole_finder.core import analyze_cases, load_cases, render_json, render_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Find support holes in RAG evaluation JSONL.")
    parser.add_argument("jsonl", type=Path)
    parser.add_argument("--min-overlap", type=float, default=0.25)
    parser.add_argument("--max-age-days", type=int, default=365)
    parser.add_argument("--as-of", default=date.today().isoformat())
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    findings = analyze_cases(
        load_cases(args.jsonl),
        min_overlap=args.min_overlap,
        as_of=date.fromisoformat(args.as_of),
        max_age_days=args.max_age_days,
    )
    print(render_json(findings) if args.json else render_text(findings), end="")
    return 1 if findings else 0
