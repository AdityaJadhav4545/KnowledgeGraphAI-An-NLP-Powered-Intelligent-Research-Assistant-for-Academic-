import csv
import json
from pathlib import Path

from KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_annotation_workflow import (
    CHUNK_FIELDS,
    PAPER_FIELDS,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.phase43_reporting import (
    build_phase43_report,
    write_versioned_report,
)


def _write(path, fields, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _row(fields, values):
    return {field: values.get(field, "") for field in fields}


def test_report_separates_human_metrics_agreement_and_pseudo_labels(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    queries_path = tmp_path / "queries.json"
    annotations_path = tmp_path / "annotations.json"
    results_path = tmp_path / "results.json"
    paper_path = tmp_path / "papers.csv"
    chunk_path = tmp_path / "chunks.csv"
    error_path = tmp_path / "error.md"
    manifest_path.write_text(
        json.dumps(
            {
                "dataset_version": "test-v1",
                "papers": [
                    {
                        "benchmark_paper_id": 1,
                        "topics": ["nlp"],
                        "index_status": "indexed",
                        "chunk_count": 2,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    queries_path.write_text(
        json.dumps({"queries": [{"query_id": "q1", "query_text": "query"}]}),
        encoding="utf-8",
    )
    annotations_path.write_text(
        json.dumps({"queries": [{"query_id": "q1", "judgment_status": "pending_human_review"}]}),
        encoding="utf-8",
    )
    strategy_results = {}
    for strategy in (
        "faiss_cosine",
        "metadata_filtered_cosine",
        "paper_aggregation",
        "mmr_diversity",
    ):
        strategy_results[strategy] = {
            "human_relevance_metrics_available": False,
            "mean_end_to_end_latency_seconds": 0.1,
            "mean_distinct_papers_at_10": 1.0,
            "macro_human_metrics": {},
        }
    results_path.write_text(
        json.dumps(
            {
                "dataset_version": "test-v1",
                "generated_utc": "2026-11-06T00:00:00+00:00",
                "benchmark_status": "provisional_pending_human_review",
                "model": {"embedding_dimension": 768},
                "strategy_comparison": strategy_results,
                "retrieval": {
                    "q1": {
                        strategy: {
                            "results": [
                                {"paper_id": 1, "chunk_id": "c1"}
                            ]
                        }
                        for strategy in strategy_results
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    _write(
        paper_path,
        PAPER_FIELDS,
        [
            _row(PAPER_FIELDS, {
                "query_id": "q1",
                "benchmark_paper_id": "1",
                "human_label": "relevant",
                "relevance_judgment": "relevant",
                "automated_label": "not_relevant",
                "automated_confidence": "0.91",
                "automated_explanation": "A test suggestion",
                "automated_model": "llama3.1",
                "reviewer": "reviewer-1",
                "reviewed_at": "2026-11-06T00:00:00+00:00",
            }),
        ],
    )
    _write(
        chunk_path,
        CHUNK_FIELDS,
        [
            _row(CHUNK_FIELDS, {
                "query_id": "q1",
                "benchmark_paper_id": "1",
                "chunk_id": "c1",
                "human_label": "relevant",
                "relevance_judgment": "relevant",
                "automated_label": "uncertain",
                "automated_confidence": "0.4",
                "automated_explanation": "Insufficient evidence",
            }),
        ],
    )
    error_path.write_text("No classified misses.", encoding="utf-8")

    report = build_phase43_report(
        manifest_path=manifest_path,
        query_path=queries_path,
        annotations_path=annotations_path,
        paper_csv=paper_path,
        chunk_csv=chunk_path,
        results_path=results_path,
        error_analysis_path=error_path,
    )

    assert report["dataset"]["indexed_chunk_count"] == 2
    assert report["human_benchmark_evaluation"]["status"] == "pending_human_validation"
    assert report["llm_human_agreement"]["paper"]["confusion_matrix"][
        "relevant"
    ]["not_relevant"] == 1
    assert report["llm_human_agreement"]["paper"]["metrics"]["accuracy"] == 0.0
    assert report["llm_human_agreement"]["chunk"]["uncertain_suggestions_excluded"] == 1
    assert report["llm_human_agreement"]["chunk"]["paired_decisive_count"] == 0
    assert report["llm_human_agreement"]["paper"]["cohen_kappa"]["status"] == (
        "not_calculated"
    )
    assert report["human_benchmark_evaluation"]["strategy_comparison"][
        "faiss_cosine"
    ]["paper_metrics_at_5"] is None

    outputs = write_versioned_report(report, tmp_path / "reports")
    assert all(tmp_path.joinpath("reports").glob("phase43_assisted_report_*"))
    assert "pseudo-labeled exploration" in Path(outputs["markdown"]).read_text(
        encoding="utf-8"
    )
    assert Path(outputs["visualization"]).is_file()
