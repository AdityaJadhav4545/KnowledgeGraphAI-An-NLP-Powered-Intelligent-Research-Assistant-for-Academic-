import csv

import pytest
import requests

from KnowledgeGraphAI.backend.services.semantic_retrieval import (
    annotation_dashboard,
    assisted_annotation,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.annotation_dashboard import (
    CHUNK_KEY_FIELDS,
    PAPER_KEY_FIELDS,
    bulk_accept_suggestions,
    load_worksheet,
    save_judgment,
    save_suggestion,
    worksheet_progress,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.annotation_evaluation import (
    build_automated_exploratory_report,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_annotation_workflow import (
    CHUNK_FIELDS,
    PAPER_FIELDS,
)


def _paper_row(paper_id="101"):
    return {
        "query_id": "q1",
        "query_text": "Does method X improve retrieval?",
        "benchmark_paper_id": paper_id,
        "arxiv_id": f"2401.000{paper_id[-1]}",
        "title": f"Paper {paper_id}",
        "abstract": f"Abstract {paper_id}",
        "source_url": f"https://arxiv.org/abs/2401.000{paper_id[-1]}",
        "retrieved_by": "faiss_cosine",
        "relevance_judgment": "",
        "grade_0_to_3": "",
        "reviewer": "",
        "reviewed_at": "",
        "independent_review_attested": "",
        "review_notes": "",
        "automated_label": "",
        "automated_confidence": "",
        "automated_explanation": "",
        "automated_model": "",
        "automated_generated_at": "",
        "human_label": "",
        "verification_method": "",
    }


def _chunk_row(chunk_id="chunk-1"):
    return {
        "query_id": "q1",
        "query_text": "Does method X improve retrieval?",
        "benchmark_paper_id": "101",
        "arxiv_id": "2401.0001",
        "title": "Paper 101",
        "abstract": "Abstract 101",
        "page_number": "1",
        "section_title": "Results",
        "source_document": "paper.pdf",
        "source_identifier": "arxiv:2401.0001",
        "chunk_id": chunk_id,
        "retrieval_hits": '[{"strategy":"faiss_cosine","rank":1}]',
        "passage_text": "The method improves retrieval.",
        "relevance_judgment": "",
        "grade_0_to_3": "",
        "reviewer": "",
        "reviewed_at": "",
        "independent_review_attested": "",
        "review_notes": "",
        "automated_label": "",
        "automated_confidence": "",
        "automated_explanation": "",
        "automated_model": "",
        "automated_generated_at": "",
        "human_label": "",
        "verification_method": "",
    }


def _write_rows(path, fields, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def test_llm_suggestion_generation_validates_label_and_evidence(monkeypatch):
    class _Response:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "message": {
                    "content": (
                        '{"label":"relevant","confidence":0.92,'
                        '"explanation":"The passage directly reports the queried result."}'
                    )
                }
            }

    calls = []

    def fake_post(url, **kwargs):
        calls.append((url, kwargs))
        return _Response()

    monkeypatch.setattr(assisted_annotation.requests, "post", fake_post)
    result = assisted_annotation.suggest_relevance(
        "Does method X improve retrieval?",
        "A retrieval paper",
        "We test method X.",
        "Method X improves retrieval.",
        model="local-model",
    )

    assert result == {
        "label": "relevant",
        "confidence": 0.92,
        "explanation": "The passage directly reports the queried result.",
        "model": "local-model",
    }
    assert calls[0][0] == "http://localhost:11434/api/chat"
    assert "Method X improves retrieval." in calls[0][1]["json"]["messages"][0]["content"]
    assert calls[0][1]["json"]["format"] == "json"


@pytest.mark.parametrize(
    "content",
    [
        '{"label":"maybe","confidence":0.7,"explanation":"Unsure"}',
        '{"label":"relevant","confidence":1.1,"explanation":"Evidence"}',
        '{"label":"uncertain","confidence":0.4,"explanation":""}',
    ],
)
def test_llm_rejects_malformed_or_out_of_range_suggestions(monkeypatch, content):
    class _Response:
        def raise_for_status(self):
            pass

        def json(self):
            return {"message": {"content": content}}

    monkeypatch.setattr(assisted_annotation.requests, "post", lambda *_a, **_k: _Response())

    with pytest.raises(ValueError):
        assisted_annotation.suggest_relevance("query", "title", "abstract")


def test_llm_retries_transient_failures_and_parses_wrapped_json(monkeypatch):
    class _Response:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "message": {
                    "content": (
                        'Suggestion follows: {"label":"uncertain",'
                        '"confidence":0.55,"explanation":"Evidence is mixed."}'
                    )
                }
            }

    calls = []

    def fake_post(*_args, **_kwargs):
        calls.append(True)
        if len(calls) == 1:
            raise requests.Timeout("temporary timeout")
        return _Response()

    monkeypatch.setattr(assisted_annotation.requests, "post", fake_post)
    monkeypatch.setattr(assisted_annotation.time, "sleep", lambda _seconds: None)
    result = assisted_annotation.suggest_relevance(
        "query", "title", "abstract", max_retries=1
    )

    assert len(calls) == 2
    assert result["label"] == "uncertain"
    assert result["confidence"] == 0.55


def test_saving_suggestion_does_not_replace_human_judgment(tmp_path):
    path = tmp_path / "paper.csv"
    row = _paper_row()
    row.update(
        human_label="not_relevant",
        relevance_judgment="not_relevant",
        reviewer="Human reviewer",
        reviewed_at="2026-11-06T00:00:00+00:00",
        verification_method="manual",
    )
    _write_rows(path, PAPER_FIELDS, [row])

    save_suggestion(
        path,
        PAPER_FIELDS,
        PAPER_KEY_FIELDS,
        {"query_id": "q1", "benchmark_paper_id": "101"},
        {
            "label": "relevant",
            "confidence": 0.98,
            "explanation": "Automated suggestion only.",
            "model": "test-model",
        },
    )

    rows, _ = load_worksheet(path, PAPER_FIELDS, PAPER_KEY_FIELDS)
    assert rows[0]["automated_label"] == "relevant"
    assert rows[0]["automated_confidence"] == "0.98"
    assert rows[0]["automated_explanation"] == "Automated suggestion only."
    assert rows[0]["automated_model"] == "test-model"
    assert rows[0]["automated_generated_at"]
    assert rows[0]["human_label"] == "not_relevant"
    assert rows[0]["relevance_judgment"] == "not_relevant"
    assert rows[0]["reviewer"] == "Human reviewer"
    assert rows[0]["verification_method"] == "manual"


def test_saving_suggestion_migrates_legacy_csv_without_losing_columns(tmp_path):
    path = tmp_path / "legacy-paper.csv"
    legacy_fields = [field for field in PAPER_FIELDS if field not in {
        "automated_label",
        "automated_confidence",
        "automated_explanation",
        "automated_model",
        "automated_generated_at",
        "human_label",
        "verification_method",
    }]
    row = _paper_row()
    row.update(
        relevance_judgment="not_relevant",
        reviewer="Legacy reviewer",
        reviewed_at="2026-11-06T00:00:00+00:00",
    )
    _write_rows(
        path,
        legacy_fields,
        [{field: row.get(field, "") for field in legacy_fields}],
    )
    original_bytes = path.read_bytes()

    backup = save_suggestion(
        path,
        PAPER_FIELDS,
        PAPER_KEY_FIELDS,
        {"query_id": "q1", "benchmark_paper_id": "101"},
        {
            "label": "uncertain",
            "confidence": 0.4,
            "explanation": "Insufficient evidence.",
            "model": "test-model",
        },
    )

    rows, fields = load_worksheet(path, PAPER_FIELDS, PAPER_KEY_FIELDS)
    assert set(legacy_fields) <= set(fields)
    assert set(PAPER_FIELDS) <= set(fields)
    assert backup.read_bytes() == original_bytes
    assert rows[0]["human_label"] == "not_relevant"
    assert rows[0]["verification_method"] == "manual_legacy"
    assert rows[0]["reviewer"] == "Legacy reviewer"
    assert rows[0]["reviewed_at"] == "2026-11-06T00:00:00+00:00"
    assert rows[0]["automated_label"] == "uncertain"


def test_bulk_acceptance_requires_confirmation_and_preserves_existing_labels(tmp_path):
    path = tmp_path / "papers.csv"
    rows = [_paper_row("101"), _paper_row("102"), _paper_row("103")]
    rows[0].update(
        automated_label="relevant",
        automated_confidence="0.96",
        automated_explanation="High confidence suggestion.",
    )
    rows[1].update(
        automated_label="uncertain",
        automated_confidence="0.99",
        automated_explanation="Insufficient evidence.",
    )
    rows[2].update(
        automated_label="relevant",
        automated_confidence="0.99",
        automated_explanation="Suggestion.",
        human_label="not_relevant",
        relevance_judgment="not_relevant",
        reviewer="Existing reviewer",
    )
    _write_rows(path, PAPER_FIELDS, rows)
    identities = [
        {"query_id": "q1", "benchmark_paper_id": value}
        for value in ("101", "102", "103")
    ]

    with pytest.raises(ValueError, match="explicit reviewer confirmation"):
        bulk_accept_suggestions(
            path, PAPER_FIELDS, PAPER_KEY_FIELDS, identities, "Reviewer", 0.85,
            confirmed=False,
        )

    outcome = bulk_accept_suggestions(
        path, PAPER_FIELDS, PAPER_KEY_FIELDS, identities, "Reviewer", 0.85,
        confirmed=True,
    )
    saved, _ = load_worksheet(path, PAPER_FIELDS, PAPER_KEY_FIELDS)
    assert outcome["accepted_count"] == 1
    assert outcome["skipped_existing_human_count"] == 1
    assert saved[0]["human_label"] == "relevant"
    assert saved[0]["grade_0_to_3"] == ""
    assert saved[0]["verification_method"] == "bulk_confirmed"
    assert saved[0]["independent_review_attested"] == ""
    assert saved[1]["human_label"] == ""
    assert saved[2]["human_label"] == "not_relevant"
    assert outcome["backup_path"]


def test_candidate_filtering_and_progress_use_human_labels():
    rows = [
        {**_paper_row("101"), "automated_label": "uncertain"},
        {**_paper_row("102"), "automated_label": "relevant"},
        {**_paper_row("103"), "human_label": "not_relevant"},
    ]

    assert len(annotation_dashboard._filter_candidates(rows, "Uncertain suggestions")) == 1
    assert len(annotation_dashboard._filter_candidates(rows, "Unreviewed")) == 2
    assert worksheet_progress(rows) == {"total": 3, "reviewed": 1, "remaining": 2}


def test_chunk_top_k_order_uses_retrieval_rank():
    rows = [
        {**_chunk_row("late"), "retrieval_hits": '[{"rank":4}]'},
        {**_chunk_row("first"), "retrieval_hits": '[{"rank":1}]'},
        {**_chunk_row("second"), "retrieval_hits": '[{"rank":2}]'},
    ]

    top_two = sorted(rows, key=annotation_dashboard._best_retrieval_rank)[:2]

    assert [row["chunk_id"] for row in top_two] == ["first", "second"]


def test_exploratory_metrics_use_automated_labels_not_human_labels(tmp_path):
    paper_path = tmp_path / "papers.csv"
    chunk_path = tmp_path / "chunks.csv"
    paper_rows = [_paper_row("101"), _paper_row("102")]
    paper_rows[0].update(
        automated_label="relevant",
        automated_confidence="0.9",
        automated_explanation="Model suggestion.",
        human_label="not_relevant",
        relevance_judgment="not_relevant",
    )
    paper_rows[1].update(
        automated_label="not_relevant",
        automated_confidence="0.8",
        automated_explanation="Model suggestion.",
        human_label="relevant",
        relevance_judgment="relevant",
    )
    chunk = _chunk_row()
    chunk.update(
        automated_label="uncertain",
        automated_confidence="0.5",
        automated_explanation="Insufficient evidence.",
    )
    _write_rows(paper_path, PAPER_FIELDS, paper_rows)
    _write_rows(chunk_path, CHUNK_FIELDS, [chunk])
    results = {
        "dataset_version": "test",
        "generated_utc": "2026-11-06T00:00:00+00:00",
        "retrieval": {
            "q1": {
                "baseline": {
                    "results": [
                        {"paper_id": 101, "chunk_id": "chunk-1"},
                        {"paper_id": 102, "chunk_id": "chunk-2"},
                    ]
                }
            }
        },
    }

    report = build_automated_exploratory_report(
        paper_path, chunk_path, results, k_values=(1,)
    )

    assert report["human_verified"] is False
    assert report["benchmark_acceptance_metrics"] is False
    assert report["per_query"]["q1"]["baseline"]["paper"]["by_k"]["1"][
        "precision@1"
    ] == 1.0
    assert report["per_query"]["q1"]["baseline"]["paper"]["by_k"]["1"][
        "ndcg@1"
    ] == 1.0
    assert report["per_query"]["q1"]["baseline"]["paper"]["label_source"] == (
        "automated_suggestion_only"
    )
    assert report["per_query"]["q1"]["baseline"]["chunk"]["judged_candidate_count"] == 0
    assert report["per_query"]["q1"]["baseline"]["chunk"]["uncertain_candidate_count"] == 1
