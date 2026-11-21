import csv
import json

from KnowledgeGraphAI.backend.services.semantic_retrieval import (
    benchmark_batch_annotation as batch_service,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.annotation_dashboard import (
    CHUNK_KEY_FIELDS,
    load_worksheet,
    save_suggestions,
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
        "automated_suggestion_history": "",
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
        "passage_text": f"Evidence in {chunk_id}.",
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
        "automated_suggestion_history": "",
        "human_label": "",
        "verification_method": "",
    }


def _write_rows(path, fields, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _query_path(tmp_path):
    path = tmp_path / "queries.json"
    path.write_text(
        json.dumps(
            {
                "queries": [
                    {
                        "query_id": "q1",
                        "query_text": "Does method X improve retrieval?",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    return path


def _fake_suggestion(label="relevant"):
    def suggest(query, title, abstract, passage=None, **kwargs):
        assert query == "Does method X improve retrieval?"
        assert title and abstract
        if passage is not None:
            assert passage.startswith("Evidence")
        return {
            "label": label,
            "confidence": 0.91,
            "explanation": "The supplied abstract/passage addresses the query.",
            "model": kwargs["model"],
        }

    return suggest


def test_batch_generates_paper_and_chunk_suggestions_separately(tmp_path):
    papers = tmp_path / "papers.csv"
    chunks = tmp_path / "chunks.csv"
    _write_rows(papers, PAPER_FIELDS, [_paper_row()])
    _write_rows(chunks, CHUNK_FIELDS, [_chunk_row()])
    checkpoint = tmp_path / "checkpoint.json"

    result = batch_service.run_batch_annotation(
        annotation_type="both",
        query_path=_query_path(tmp_path),
        paper_csv=papers,
        chunk_csv=chunks,
        checkpoint_path=checkpoint,
        model="llama3.1",
        batch_size=1,
        suggest=_fake_suggestion(),
    )

    paper_rows, _ = load_worksheet(
        papers, PAPER_FIELDS, ("query_id", "benchmark_paper_id")
    )
    chunk_rows, _ = load_worksheet(chunks, CHUNK_FIELDS, CHUNK_KEY_FIELDS)
    checkpoint_data = json.loads(checkpoint.read_text(encoding="utf-8"))
    assert result["results"]["paper"]["generated"] == 1
    assert result["results"]["chunk"]["generated"] == 1
    assert paper_rows[0]["automated_label"] == "relevant"
    assert chunk_rows[0]["automated_label"] == "relevant"
    assert paper_rows[0]["human_label"] == chunk_rows[0]["human_label"] == ""
    assert len(checkpoint_data["records"]) == 2
    assert {item["annotation_type"] for item in checkpoint_data["records"].values()} == {
        "paper", "chunk"
    }


def test_batch_skips_existing_suggestions_and_never_touches_human_labels(tmp_path):
    papers = tmp_path / "papers.csv"
    row = _paper_row()
    row.update(
        automated_label="not_relevant",
        automated_confidence="0.8",
        automated_explanation="Existing suggestion.",
        human_label="relevant",
        relevance_judgment="relevant",
        reviewer="Human reviewer",
        reviewed_at="2026-11-06T00:00:00+00:00",
    )
    _write_rows(papers, PAPER_FIELDS, [row])
    chunks = tmp_path / "chunks.csv"
    _write_rows(chunks, CHUNK_FIELDS, [])
    checkpoint = tmp_path / "checkpoint.json"
    calls = []

    result = batch_service.run_batch_annotation(
        annotation_type="paper",
        query_path=_query_path(tmp_path),
        paper_csv=papers,
        chunk_csv=chunks,
        checkpoint_path=checkpoint,
        suggest=lambda *_a, **_kw: calls.append(True),
    )

    saved, _ = load_worksheet(
        papers, PAPER_FIELDS, ("query_id", "benchmark_paper_id")
    )
    assert result["results"]["paper"]["skipped_existing"] == 1
    assert calls == []
    assert saved[0]["automated_label"] == "not_relevant"
    assert saved[0]["human_label"] == "relevant"
    assert saved[0]["reviewer"] == "Human reviewer"


def test_checkpoint_recovers_suggestion_after_interrupted_csv_persist(tmp_path, monkeypatch):
    papers = tmp_path / "papers.csv"
    chunks = tmp_path / "chunks.csv"
    checkpoint = tmp_path / "checkpoint.json"
    _write_rows(papers, PAPER_FIELDS, [_paper_row()])
    _write_rows(chunks, CHUNK_FIELDS, [])
    query_path = _query_path(tmp_path)
    original_save = batch_service.save_suggestions
    call_count = []

    def fail_first_write(*args, **kwargs):
        call_count.append(1)
        if len(call_count) == 1:
            raise OSError("simulated interruption during CSV write")
        return original_save(*args, **kwargs)

    monkeypatch.setattr(batch_service, "save_suggestions", fail_first_write)
    first_calls = []
    try:
        batch_service.run_batch_annotation(
            annotation_type="paper",
            query_path=query_path,
            paper_csv=papers,
            chunk_csv=chunks,
            checkpoint_path=checkpoint,
            suggest=lambda *args, **kwargs: (
                first_calls.append(True) or _fake_suggestion()(*args, **kwargs)
            ),
            batch_size=1,
        )
    except OSError as error:
        assert "simulated interruption" in str(error)
    else:
        raise AssertionError("simulated CSV persistence failure did not propagate")

    monkeypatch.setattr(batch_service, "save_suggestions", original_save)
    second_calls = []
    resumed = batch_service.run_batch_annotation(
        annotation_type="paper",
        query_path=query_path,
        paper_csv=papers,
        chunk_csv=chunks,
        checkpoint_path=checkpoint,
        suggest=lambda *args, **kwargs: (
            second_calls.append(True) or _fake_suggestion()(*args, **kwargs)
        ),
        batch_size=1,
    )

    saved, _ = load_worksheet(
        papers, PAPER_FIELDS, ("query_id", "benchmark_paper_id")
    )
    assert len(first_calls) == 1
    assert second_calls == []
    assert resumed["results"]["paper"]["recovered_from_checkpoint"] == 1
    assert saved[0]["automated_label"] == "relevant"


def test_force_regeneration_preserves_prior_suggestion_history(tmp_path):
    papers = tmp_path / "papers.csv"
    chunks = tmp_path / "chunks.csv"
    _write_rows(papers, PAPER_FIELDS, [_paper_row()])
    _write_rows(chunks, CHUNK_FIELDS, [])
    args = {
        "annotation_type": "paper",
        "query_path": _query_path(tmp_path),
        "paper_csv": papers,
        "chunk_csv": chunks,
        "checkpoint_path": tmp_path / "checkpoint.json",
        "suggest": _fake_suggestion("relevant"),
    }

    batch_service.run_batch_annotation(**args)
    batch_service.run_batch_annotation(**{**args, "force": True, "suggest": _fake_suggestion("uncertain")})

    rows, _ = load_worksheet(papers, PAPER_FIELDS, ("query_id", "benchmark_paper_id"))
    history = json.loads(rows[0]["automated_suggestion_history"])
    assert rows[0]["automated_label"] == "uncertain"
    assert len(history) == 2
    assert history[0]["label"] == "relevant"
    assert history[1]["label"] == "uncertain"


def test_candidate_filter_keeps_disagreement_out_of_automated_only_metrics():
    from KnowledgeGraphAI.backend.services.semantic_retrieval.annotation_dashboard import (
        _filter_candidates,
    )

    rows = [
        {
            "human_label": "relevant",
            "relevance_judgment": "relevant",
            "automated_label": "not_relevant",
        },
        {
            "human_label": "",
            "relevance_judgment": "",
            "automated_label": "uncertain",
        },
    ]

    assert len(_filter_candidates(rows, "Disagreement")) == 1
