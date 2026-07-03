from __future__ import annotations

import json
from datetime import date

from rag_hole_finder.cli import main
from rag_hole_finder.core import analyze_case, overlap, render_json, render_text, terms


def test_terms_normalize_words() -> None:
    assert "refunds" in terms("Refunds take days.")


def test_overlap_scores_context_support() -> None:
    assert overlap("export invoices", ["You can export invoices"]) == 1


def test_missing_citation_is_flagged() -> None:
    findings = analyze_case(
        {"id": "x", "answer": "ok", "citations": [], "contexts": []},
        0.2,
        date(2026, 1, 1),
        365,
    )
    assert findings[0].label == "missing-citation"


def test_stale_source_is_flagged() -> None:
    findings = analyze_case(
        {"id": "x", "answer": "ok", "citations": ["a"], "source_date": "2020-01-01"},
        0.2,
        date(2026, 1, 1),
        365,
    )
    assert any(item.label == "stale-source" for item in findings)


def test_json_render_is_valid() -> None:
    findings = analyze_case(
        {"id": "x", "answer": "", "citations": []},
        0.2,
        date(2026, 1, 1),
        365,
    )
    assert json.loads(render_json(findings))[0]["case_id"] == "x"


def test_text_render_empty() -> None:
    assert "No RAG holes" in render_text([])


def test_cli_help(capsys) -> None:
    try:
        main(["--help"])
    except SystemExit as exc:
        assert exc.code == 0
    assert "RAG" in capsys.readouterr().out
