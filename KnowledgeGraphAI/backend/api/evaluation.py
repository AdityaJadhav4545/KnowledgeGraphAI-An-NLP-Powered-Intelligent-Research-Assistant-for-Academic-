"""Read-only access to verified benchmark summaries.

This endpoint intentionally reports missing human labels as missing rather than
turning automated suggestions into evaluation results.
"""

from __future__ import annotations

import json
import csv
from pathlib import Path
from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from KnowledgeGraphAI.backend.config import PROJECT_ROOT


router = APIRouter(prefix="/api/evaluation", tags=["evaluation"])
_RESULTS = PROJECT_ROOT / "reports" / "semantic_retrieval" / "benchmark_results.json"
_BENCHMARK = PROJECT_ROOT / "data" / "benchmark"


def _annotation_summary() -> Dict[str, Any]:
    """Count only explicit human worksheet fields, never automated suggestions."""

    summary: Dict[str, Any] = {}
    for kind in ("paper", "chunk"):
        path = _BENCHMARK / f"{kind}_judgments.csv"
        try:
            with path.open(encoding="utf-8-sig", newline="") as stream:
                rows = list(csv.DictReader(stream))
        except FileNotFoundError:
            rows = []
        human_judgments = sum(
            bool(
                (row.get("human_label") or "").strip()
                or (row.get("relevance_judgment") or "").strip()
            )
            for row in rows
        )
        independent_reviews = sum(
            (row.get("independent_review_attested") or "").strip().casefold()
            in {"1", "true", "yes"}
            for row in rows
        )
        summary[kind] = {
            "candidate_count": len(rows),
            "human_judgment_count": human_judgments,
            "unjudged_count": len(rows) - human_judgments,
            "independent_review_count": independent_reviews,
        }
    return summary


def _load_results() -> Dict[str, Any]:
    try:
        return json.loads(_RESULTS.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="No benchmark report has been generated.") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=500, detail="Benchmark report could not be read.") from exc


@router.get("/benchmark")
async def benchmark_summary() -> Dict[str, Any]:
    report = _load_results()
    comparison = report.get("strategy_comparison") or {}
    strategies: Dict[str, Any] = {}
    for name, values in comparison.items():
        if not isinstance(values, dict):
            continue
        strategies[name] = {
            "mean_end_to_end_latency_seconds": values.get("mean_end_to_end_latency_seconds"),
            "median_end_to_end_latency_seconds": values.get("median_end_to_end_latency_seconds"),
            "mean_result_count": values.get("mean_result_count"),
            "mean_distinct_papers_at_10": values.get("mean_distinct_papers_at_10"),
            "mean_duplicate_chunks_at_10": values.get("mean_duplicate_chunks_at_10"),
            "human_relevance_metrics_available": values.get("human_relevance_metrics_available", False),
            "macro_human_metrics": values.get("macro_human_metrics", {}),
        }
    return {
        "benchmark_status": report.get("benchmark_status", "unknown"),
        "status_explanation": report.get("status_explanation", ""),
        "generated_utc": report.get("generated_utc"),
        "dataset_version": report.get("dataset_version"),
        "annotation_status": report.get("annotation_status"),
        "human_verified_query_count": report.get("human_verified_query_count", 0),
        "indexing": report.get("indexing", {}),
        "performance": report.get("performance", {}),
        "strategies": strategies,
        "limitations": report.get("limitations", []),
        "annotations": _annotation_summary(),
    }
