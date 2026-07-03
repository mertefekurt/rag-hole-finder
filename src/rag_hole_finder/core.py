from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

WORDS = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]+")


@dataclass(frozen=True)
class Finding:
    case_id: str
    label: str
    detail: str


def load_cases(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def terms(text: str) -> set[str]:
    return {match.group(0).lower() for match in WORDS.finditer(text) if len(match.group(0)) > 2}


def overlap(answer: str, contexts: list[str]) -> float:
    answer_terms = terms(answer)
    if not answer_terms:
        return 0.0
    context_terms = terms(" ".join(contexts))
    return len(answer_terms & context_terms) / len(answer_terms)


def analyze_case(case: dict, min_overlap: float, as_of: date, max_age_days: int) -> list[Finding]:
    case_id = str(case.get("id", "unknown"))
    answer = str(case.get("answer", ""))
    contexts = [str(item) for item in case.get("contexts", [])]
    findings: list[Finding] = []
    if not answer.strip():
        findings.append(Finding(case_id, "empty-answer", "answer is blank"))
    if not case.get("citations"):
        findings.append(Finding(case_id, "missing-citation", "citation list is empty"))
    if contexts and overlap(answer, contexts) < min_overlap:
        findings.append(
            Finding(case_id, "low-context-overlap", "answer is weakly grounded in retrieved text")
        )
    if case.get("source_date"):
        source_date = date.fromisoformat(str(case["source_date"]))
        if (as_of - source_date).days > max_age_days:
            findings.append(Finding(case_id, "stale-source", "source is outside freshness window"))
    return findings


def analyze_cases(cases: list[dict], min_overlap: float, as_of: date, max_age_days: int) -> list[Finding]:
    return [finding for case in cases for finding in analyze_case(case, min_overlap, as_of, max_age_days)]


def render_text(findings: list[Finding]) -> str:
    if not findings:
        return "No RAG holes found.\n"
    return "\n".join(f"{f.case_id}\t{f.label}\t{f.detail}" for f in findings) + "\n"


def render_json(findings: list[Finding]) -> str:
    return json.dumps([asdict(finding) for finding in findings], indent=2)
