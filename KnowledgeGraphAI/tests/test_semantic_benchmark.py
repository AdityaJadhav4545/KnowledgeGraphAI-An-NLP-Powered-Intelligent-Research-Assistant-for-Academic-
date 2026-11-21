import json
import csv
from pathlib import Path

import pytest

# faiss-cpu DLL may fail to initialise under certain Windows pytest collection
# orderings.  Skip the entire module rather than crashing the suite.
faiss = pytest.importorskip("faiss", reason="faiss-cpu DLL unavailable in this environment")

from KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_corpus import (
    validate_annotations,
    validate_manifest,
    validate_query_dataset,
    write_annotation_template,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_annotation_workflow import (
    CHUNK_FIELDS,
    PAPER_FIELDS,
    build_review_package,
    import_human_annotations,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_runner import (
    _evaluation_summary,
    _evaluate_configuration,
    _macro_evaluation,
    _recorded_indexing_seconds,
    _traceability,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.evaluation import (
    ndcg_at_k,
    retrieval_metrics,
)


def _manifest():
    return {
        "schema_version": 1,
        "dataset_version": "phase4.3-arxiv-pilot-v1",
        "papers": [
            {
                "arxiv_id": "2401.00001",
                "benchmark_paper_id": 101,
                "title": "First scientific paper",
                "abstract": "An abstract.",
                "source_url": "https://arxiv.org/abs/2401.00001",
                "local_pdf_path": "pdfs/2401.00001.pdf",
                "topics": ["nlp"],
            },
            {
                "arxiv_id": "2401.00002",
                "benchmark_paper_id": 102,
                "title": "Second scientific paper",
                "abstract": "Another abstract.",
                "source_url": "https://arxiv.org/abs/2401.00002",
                "local_pdf_path": "pdfs/2401.00002.pdf",
                "topics": ["nlp"],
            },
        ],
    }


def _queries():
    return {
        "queries": [
            {
                "query_id": "q1",
                "query_text": "How does scientific retrieval work?",
                "target_areas": ["nlp"],
            }
        ]
    }


def test_manifest_rejects_duplicate_papers():
    manifest = _manifest()
    manifest["papers"][1]["arxiv_id"] = manifest["papers"][0]["arxiv_id"]
    with pytest.raises(ValueError, match="duplicate arXiv ID"):
        validate_manifest(manifest)


def test_query_dataset_rejects_duplicate_ids():
    dataset = _queries()
    dataset["queries"].append(dict(dataset["queries"][0]))
    with pytest.raises(ValueError, match="duplicate benchmark query IDs"):
        validate_query_dataset(dataset)


def test_annotation_template_does_not_overwrite_human_work(tmp_path):
    path = tmp_path / "annotations.json"
    first = write_annotation_template(_queries(), _manifest(), path)
    first["queries"][0]["annotation_notes"] = "Review in progress."
    path.write_text(json.dumps(first), encoding="utf-8")

    returned = write_annotation_template(_queries(), _manifest(), path)

    assert returned["queries"][0]["annotation_notes"] == "Review in progress."
    assert json.loads(path.read_text(encoding="utf-8")) == returned


def test_human_annotations_must_explicitly_judge_papers_and_chunks(tmp_path):
    annotations = write_annotation_template(
        _queries(), _manifest(), tmp_path / "annotations.json"
    )
    entry = annotations["queries"][0]
    entry.update({
        "judgment_status": "human_verified",
        "annotator": "reviewer-1",
        "reviewed_at": "2026-11-06T00:00:00+00:00",
        "independent_review_attested": True,
        "judged_paper_ids": [101, 102],
        "unjudged_paper_ids": [],
        "relevant_paper_ids": [101],
        "paper_relevance_grades": {"101": 2, "102": 0},
        "judged_chunk_ids": ["chunk-1"],
        "relevant_chunk_ids": ["chunk-1"],
        "annotation_source": "Independent reviewer",
        "annotation_notes": "Reviewed both titles, abstracts, and candidate passage.",
    })
    validate_annotations(annotations, ["q1"], [101, 102], ["chunk-1"])
    with pytest.raises(ValueError, match="unknown judged chunk ID"):
        validate_annotations(annotations, ["q1"], [101, 102], ["other-chunk"])


def test_unjudged_results_are_excluded_from_benchmark_metrics():
    annotation = {
        "judgment_status": "human_verified",
        "judged_chunk_ids": ["c1", "c2"],
        "relevant_chunk_ids": ["c2"],
        "judged_paper_ids": [101, 102],
        "relevant_paper_ids": [102],
        "paper_relevance_grades": {"101": 0, "102": 2},
    }
    results = [
        {"chunk_id": "unjudged", "paper_id": 999},
        {"chunk_id": "c1", "paper_id": 101},
        {"chunk_id": "c2", "paper_id": 102},
    ]

    evaluation = _evaluate_configuration({}, results, annotation)

    assert evaluation["metrics"]["chunk"]["unjudged_result_count"] == 1
    assert evaluation["metrics"]["chunk"]["by_k"]["3"]["precision@3"] == pytest.approx(1 / 3)
    assert evaluation["metrics"]["chunk"]["by_k"]["3"]["reciprocal_rank"] == 0.5
    assert evaluation["metrics"]["paper"]["by_k"]["3"]["reciprocal_rank"] == 0.5


def test_ir_metrics_handle_empty_relevance_and_graded_ranking():
    metrics = retrieval_metrics(["a", "b"], [], 2)

    assert metrics["precision@2"] == 0
    assert metrics["recall@2"] is None
    assert metrics["reciprocal_rank"] is None
    assert metrics["average_precision@2"] is None
    assert ndcg_at_k(["low", "high"], {"low": 1, "high": 2}, 2) < 1
    assert ndcg_at_k(["high", "low"], {"low": 1, "high": 2}, 2) == pytest.approx(1)


def test_macro_evaluation_reports_query_denominators():
    evaluation = {
        "judgment_status": "human_verified",
        "metrics": {
            "paper": {
                "by_k": {
                    "1": {
                        "precision@1": 1.0,
                        "recall@1": None,
                        "reciprocal_rank": None,
                        "average_precision@1": None,
                        "ndcg@1": 0.0,
                    }
                }
            },
            "chunk": {"by_k": {}},
        },
    }
    data = {"q1": {"baseline": {"evaluation": evaluation}}}

    macro = _macro_evaluation(data, "baseline")

    assert macro["paper"]["1"]["precision@1"]["macro_mean"] == 1.0
    assert macro["paper"]["1"]["precision@1"]["eligible_query_count"] == 1
    assert macro["paper"]["1"]["recall@1"]["eligible_query_count"] == 0


def test_evaluation_summary_uses_macro_chunk_and_paper_results():
    comparison = {
        "baseline": {
            "macro_human_metrics": {
                "chunk": {"1": {"precision@1": {"macro_mean": None}}},
                "paper": {"1": {"precision@1": {"macro_mean": None}}},
            }
        }
    }

    summary = _evaluation_summary(comparison, all_human_verified=False)

    assert summary["status"] == "pending_human_annotations"
    assert summary["chunk_level"]["baseline"] == comparison["baseline"]["macro_human_metrics"]["chunk"]
    assert summary["paper_level"]["baseline"] == comparison["baseline"]["macro_human_metrics"]["paper"]


def test_traceability_reads_nested_strategy_results(monkeypatch, tmp_path):
    class _GraphQueries:
        def get_paper_entities(self, _paper_id):
            return [{"entity_id": "e1"}]

        def get_paper_relationships(self, _paper_id):
            return [{"relationship_id": "r1"}]

    class _Neo4jManager:
        def execute_query(self, _query, parameters):
            return [{"paper_id": "canonical-1", "title": parameters["title"]}]

    from KnowledgeGraphAI.backend.services.semantic_retrieval import benchmark_runner

    monkeypatch.setattr(benchmark_runner, "GraphQueryService", _GraphQueries)
    monkeypatch.setattr(
        benchmark_runner, "MANIFEST_PATH", tmp_path / "manifest.json"
    )
    title = "A research paper"
    result = _traceability(
        {
            "papers": [
                {"arxiv_id": "2401.00001", "title": title}
            ]
        },
        {
            "q1": {
                "faiss_cosine": {
                    "results": [{"title": title, "chunk_id": "chunk-1"}]
                }
            }
        },
        _Neo4jManager(),
    )

    assert result["2401.00001"]["status"] == "matched"
    assert result["2401.00001"]["sampled_retrieved_chunk_ids"] == ["chunk-1"]
    assert result["2401.00001"]["entity_count"] == 1


def test_recorded_index_duration_uses_only_successfully_indexed_papers():
    manifest = {
        "papers": [
            {"index_status": "indexed", "index_seconds": 1.25},
            {"index_status": "failed", "index_seconds": 10.0},
            {"index_status": "indexed", "index_seconds": 2.5},
        ]
    }

    assert _recorded_indexing_seconds(manifest) == pytest.approx(3.75)


def _review_results():
    manifest = _manifest()
    query = _queries()
    first = {
        "paper_id": 101,
        "chunk_id": "chunk-1",
        "title": "First scientific paper",
        "text": "BERT retrieval evidence.",
        "page_number": 2,
        "section_title": "Methods",
        "source_document": "2401.00001.pdf",
        "source_identifier": "arxiv:2401.00001",
        "similarity_score": 0.81,
        "reranking_score": None,
    }
    second = {
        **first,
        "paper_id": 102,
        "chunk_id": "chunk-2",
        "title": "Second scientific paper",
        "text": "A distinct retrieval passage.",
        "source_document": "2401.00002.pdf",
        "source_identifier": "arxiv:2401.00002",
        "page_number": 3,
        "similarity_score": 0.72,
    }
    retrieval = {
        "q1": {
            strategy: {
                "results": [first, second] if strategy == "faiss_cosine" else [second]
            }
            for strategy in (
                "faiss_cosine",
                "metadata_filtered_cosine",
                "paper_aggregation",
                "mmr_diversity",
            )
        }
    }
    return manifest, query, {
        "dataset_version": "phase4.3-arxiv-pilot-v1",
        "generated_utc": "2026-11-06T00:00:00+00:00",
        "retrieval": retrieval,
    }


def _write_rows(path, fields, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def test_review_package_has_candidates_but_no_automatic_judgments():
    manifest, queries, results = _review_results()

    paper_rows, chunk_rows, report = build_review_package(
        manifest, queries, results
    )

    assert len(paper_rows) == 2
    assert len(chunk_rows) == 2
    assert all(row["relevance_judgment"] == "" for row in paper_rows + chunk_rows)
    assert "BERT retrieval evidence." in report
    assert "0.81" in report
    assert "not_relevant" in report


def test_import_requires_full_human_judgments_and_provenance(tmp_path):
    manifest, queries, results = _review_results()
    paper_rows, chunk_rows, _ = build_review_package(manifest, queries, results)
    for index, row in enumerate(paper_rows):
        row.update({
            "relevance_judgment": "relevant" if index == 0 else "not_relevant",
            "grade_0_to_3": "2" if index == 0 else "0",
            "reviewer": "reviewer-a",
            "reviewed_at": f"2026-11-06T00:00:0{index}+00:00",
            "independent_review_attested": "yes",
        })
    for index, row in enumerate(chunk_rows):
        row.update({
            "relevance_judgment": "relevant" if index == 0 else "not_relevant",
            "grade_0_to_3": "3" if index == 0 else "0",
            "reviewer": "reviewer-a",
            "reviewed_at": f"2026-11-06T00:00:0{index + 2}+00:00",
            "independent_review_attested": "yes",
        })

    paper_path = tmp_path / "paper.csv"
    chunk_path = tmp_path / "chunk.csv"
    annotation_path = tmp_path / "benchmark_annotations.json"
    _write_rows(paper_path, PAPER_FIELDS, paper_rows)
    _write_rows(chunk_path, CHUNK_FIELDS, chunk_rows)
    write_annotation_template(queries, manifest, annotation_path)

    outcome = import_human_annotations(
        paper_path, chunk_path, annotation_path, manifest, queries, results
    )

    annotations = json.loads(annotation_path.read_text(encoding="utf-8"))
    entry = annotations["queries"][0]
    assert outcome["human_verified_query_count"] == 1
    assert entry["judgment_status"] == "human_verified"
    assert entry["relevant_paper_ids"] == [101]
    assert entry["relevant_chunk_ids"] == ["chunk-1"]
    assert entry["independent_review_attested"] is True
    assert entry["reviewed_at"] == "2026-11-06T00:00:03+00:00"
    assert entry["paper_relevance_grades"] == {"101": 2, "102": 0}
    assert entry["chunk_relevance_grades"] == {"chunk-1": 3, "chunk-2": 0}


def test_import_and_benchmark_metrics_use_human_labels_not_model_suggestions(tmp_path):
    manifest, queries, results = _review_results()
    paper_rows, chunk_rows, _ = build_review_package(manifest, queries, results)
    for index, row in enumerate(paper_rows):
        label = "not_relevant" if index == 0 else "relevant"
        row.update({
            "relevance_judgment": label,
            "human_label": label,
            "automated_label": "relevant",
            "automated_confidence": "0.99",
            "automated_explanation": "Automated suggestions are separate.",
            "reviewer": "reviewer-a",
            "reviewed_at": f"2026-11-06T00:00:0{index}+00:00",
            "verification_method": "manual",
            "independent_review_attested": "",
        })
    for index, row in enumerate(chunk_rows):
        label = "not_relevant" if index == 0 else "relevant"
        row.update({
            "relevance_judgment": label,
            "human_label": label,
            "automated_label": "relevant",
            "automated_confidence": "0.99",
            "automated_explanation": "Automated suggestions are separate.",
            "reviewer": "reviewer-a",
            "reviewed_at": f"2026-11-06T00:00:0{index + 2}+00:00",
            "verification_method": "bulk_confirmed",
            "independent_review_attested": "",
        })

    paper_path = tmp_path / "paper.csv"
    chunk_path = tmp_path / "chunk.csv"
    annotation_path = tmp_path / "benchmark_annotations.json"
    _write_rows(paper_path, PAPER_FIELDS, paper_rows)
    _write_rows(chunk_path, CHUNK_FIELDS, chunk_rows)
    write_annotation_template(queries, manifest, annotation_path)
    import_human_annotations(
        paper_path, chunk_path, annotation_path, manifest, queries, results
    )

    annotations = json.loads(annotation_path.read_text(encoding="utf-8"))
    entry = annotations["queries"][0]
    assert entry["judgment_status"] == "human_verified"
    assert entry["relevant_paper_ids"] == [102]
    assert entry["independent_review_attested"] is False
    assert entry["verification_method"] == "bulk_confirmed"
    first_result = {
        "paper_id": 101,
        "chunk_id": "chunk-1",
        "title": "First scientific paper",
    }
    second_result = {
        "paper_id": 102,
        "chunk_id": "chunk-2",
        "title": "Second scientific paper",
    }
    metrics = _evaluate_configuration(
        {"query_id": "q1"},
        [first_result, second_result],
        entry,
    )
    assert metrics["metrics"]["paper"]["by_k"]["1"]["precision@1"] == 0.0
    assert metrics["metrics"]["paper"]["by_k"]["1"]["recall@1"] == 0.0


def test_import_rejects_missing_judgment_or_modified_passage(tmp_path):
    manifest, queries, results = _review_results()
    paper_rows, chunk_rows, _ = build_review_package(manifest, queries, results)
    paper_path = tmp_path / "paper.csv"
    chunk_path = tmp_path / "chunk.csv"
    annotation_path = tmp_path / "annotations.json"
    write_annotation_template(queries, manifest, annotation_path)
    _write_rows(paper_path, PAPER_FIELDS, paper_rows)
    _write_rows(chunk_path, CHUNK_FIELDS, chunk_rows)

    with pytest.raises(ValueError, match="relevance_judgment"):
        import_human_annotations(
            paper_path, chunk_path, annotation_path, manifest, queries, results
        )

    for row in chunk_rows:
        row.update({
            "relevance_judgment": "not_relevant",
            "reviewer": "reviewer-a",
            "reviewed_at": "2026-11-06T00:00:00+00:00",
            "independent_review_attested": "yes",
        })
    for row in paper_rows:
        row.update({
            "relevance_judgment": "not_relevant",
            "reviewer": "reviewer-a",
            "reviewed_at": "2026-11-06T00:00:00+00:00",
            "independent_review_attested": "yes",
        })
    chunk_rows[0]["passage_text"] = "Edited source text."
    _write_rows(paper_path, PAPER_FIELDS, paper_rows)
    _write_rows(chunk_path, CHUNK_FIELDS, chunk_rows)
    with pytest.raises(ValueError, match="passage_text was changed"):
        import_human_annotations(
            paper_path, chunk_path, annotation_path, manifest, queries, results
        )
