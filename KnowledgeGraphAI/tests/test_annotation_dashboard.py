import csv

import pytest

from KnowledgeGraphAI.backend.services.semantic_retrieval.annotation_dashboard import (
    load_worksheet,
    save_judgment,
    worksheet_progress,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_annotation_workflow import (
    CHUNK_FIELDS,
    PAPER_FIELDS,
)


def _write_rows(path, fields, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _paper_row():
    return {
        "query_id": "q1",
        "query_text": "A test query",
        "benchmark_paper_id": "101",
        "arxiv_id": "2401.00001",
        "title": "A paper",
        "abstract": "Abstract text.",
        "source_url": "https://arxiv.org/abs/2401.00001",
        "retrieved_by": "faiss_cosine",
        "relevance_judgment": "",
        "grade_0_to_3": "",
        "reviewer": "",
        "reviewed_at": "",
        "independent_review_attested": "",
        "review_notes": "",
    }


def _chunk_row():
    return {
        "query_id": "q1",
        "query_text": "A test query",
        "benchmark_paper_id": "101",
        "arxiv_id": "2401.00001",
        "title": "A paper",
        "abstract": "Abstract text.",
        "page_number": "2",
        "section_title": "Methods",
        "source_document": "paper.pdf",
        "source_identifier": "arxiv:2401.00001",
        "chunk_id": "chunk-1",
        "retrieval_hits": "[]",
        "passage_text": "A retrieved passage.",
        "relevance_judgment": "",
        "grade_0_to_3": "",
        "reviewer": "",
        "reviewed_at": "",
        "independent_review_attested": "",
        "review_notes": "",
    }


@pytest.mark.parametrize(
    ("fields", "key_fields", "row_factory", "identity"),
    [
        (
            PAPER_FIELDS,
            ("query_id", "benchmark_paper_id"),
            _paper_row,
            {"query_id": "q1", "benchmark_paper_id": "101"},
        ),
        (
            CHUNK_FIELDS,
            ("query_id", "chunk_id"),
            _chunk_row,
            {"query_id": "q1", "chunk_id": "chunk-1"},
        ),
    ],
)
def test_saving_paper_and_chunk_judgments_round_trips_with_backup(
    tmp_path, fields, key_fields, row_factory, identity
):
    path = tmp_path / "judgments.csv"
    row = row_factory()
    _write_rows(path, fields, [row])
    original_bytes = path.read_bytes()

    backup = save_judgment(
        path,
        fields,
        key_fields,
        identity,
        "relevant",
        "2",
        "Reviewer One",
        "Supports the query.",
        False,
    )

    rows, saved_fields = load_worksheet(path, fields, key_fields)
    assert saved_fields == list(fields)
    assert rows[0]["relevance_judgment"] == "relevant"
    assert rows[0]["human_label"] == "relevant"
    assert rows[0]["verification_method"] == "manual"
    assert rows[0]["grade_0_to_3"] == "2"
    assert rows[0]["reviewer"] == "Reviewer One"
    assert rows[0]["reviewed_at"]
    assert rows[0]["independent_review_attested"] == ""
    assert rows[0]["review_notes"] == "Supports the query."
    assert backup.read_bytes() == original_bytes
    assert worksheet_progress(rows) == {"total": 1, "reviewed": 1, "remaining": 0}


def test_blank_rows_stay_unjudged_and_extra_columns_are_preserved(tmp_path):
    path = tmp_path / "paper.csv"
    fields = [*PAPER_FIELDS, "future_source_column"]
    row = {**_paper_row(), "future_source_column": "keep me"}
    _write_rows(path, fields, [row])

    rows, loaded_fields = load_worksheet(
        path, PAPER_FIELDS, ("query_id", "benchmark_paper_id")
    )

    assert loaded_fields == fields
    assert rows[0]["relevance_judgment"] == ""
    assert rows[0]["future_source_column"] == "keep me"
    assert worksheet_progress(rows) == {"total": 1, "reviewed": 0, "remaining": 1}


def test_saving_another_record_preserves_existing_judgment(tmp_path):
    path = tmp_path / "paper.csv"
    first = _paper_row()
    first.update(
        relevance_judgment="not_relevant",
        grade_0_to_3="0",
        reviewer="Reviewer One",
        reviewed_at="2026-11-06T00:00:00+00:00",
        review_notes="Previously reviewed.",
    )
    second = {**_paper_row(), "benchmark_paper_id": "102"}
    _write_rows(path, PAPER_FIELDS, [first, second])

    save_judgment(
        path,
        PAPER_FIELDS,
        ("query_id", "benchmark_paper_id"),
        {"query_id": "q1", "benchmark_paper_id": "102"},
        "relevant",
        "1",
        "Reviewer One",
        "",
        True,
    )

    rows, _ = load_worksheet(
        path, PAPER_FIELDS, ("query_id", "benchmark_paper_id")
    )
    assert rows[0]["relevance_judgment"] == "not_relevant"
    assert rows[0]["reviewed_at"] == "2026-11-06T00:00:00+00:00"
    assert rows[0]["review_notes"] == "Previously reviewed."
    assert rows[1]["independent_review_attested"] == "yes"


@pytest.mark.parametrize(
    ("label", "grade"),
    [("maybe", ""), ("relevant", "0"), ("not_relevant", "2"), ("relevant", "4")],
)
def test_invalid_labels_and_grades_are_rejected_without_modifying_file(
    tmp_path, label, grade
):
    path = tmp_path / "paper.csv"
    _write_rows(path, PAPER_FIELDS, [_paper_row()])
    original = path.read_bytes()

    with pytest.raises(ValueError):
        save_judgment(
            path,
            PAPER_FIELDS,
            ("query_id", "benchmark_paper_id"),
            {"query_id": "q1", "benchmark_paper_id": "101"},
            label,
            grade,
            "Reviewer One",
            "",
            False,
        )

    assert path.read_bytes() == original
    assert not list(tmp_path.glob("*.bak"))


def test_duplicate_records_are_rejected(tmp_path):
    path = tmp_path / "chunks.csv"
    row = _chunk_row()
    _write_rows(path, CHUNK_FIELDS, [row, dict(row)])

    with pytest.raises(ValueError, match="duplicates record identity"):
        load_worksheet(path, CHUNK_FIELDS, ("query_id", "chunk_id"))


def test_reviewer_is_required_before_backup_or_write(tmp_path):
    path = tmp_path / "paper.csv"
    _write_rows(path, PAPER_FIELDS, [_paper_row()])
    original = path.read_bytes()

    with pytest.raises(ValueError, match="reviewer name is required"):
        save_judgment(
            path,
            PAPER_FIELDS,
            ("query_id", "benchmark_paper_id"),
            {"query_id": "q1", "benchmark_paper_id": "101"},
            "not_relevant",
            "0",
            " ",
            "",
            False,
        )

    assert path.read_bytes() == original
    assert not list(tmp_path.glob("*.bak"))
