"""Clearly separated exploratory metrics for automated annotation suggestions."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

from KnowledgeGraphAI.backend.services.semantic_retrieval.annotation_dashboard import (
    CHUNK_KEY_FIELDS,
    PAPER_KEY_FIELDS,
    load_worksheet,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.assisted_annotation import (
    AUTOMATED_LABELS,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_annotation_workflow import (
    CHUNK_FIELDS,
    PAPER_FIELDS,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.evaluation import (
    ndcg_at_k,
    retrieval_metrics,
)


AUTOMATED_METRICS_PATH = (
    Path(__file__).resolve().parents[4]
    / "KnowledgeGraphAI"
    / "reports"
    / "semantic_retrieval"
    / "automated_annotation_exploratory_report.json"
)


def _load_automated_labels(
    path: Path,
    fields: Sequence[str],
    key_fields: Sequence[str],
    id_field: str,
) -> tuple[Dict[str, Dict[str, str]], Dict[str, Dict[str, int]]]:
    rows, _ = load_worksheet(path, fields, key_fields)
    labels: Dict[str, Dict[str, str]] = {}
    counts: Dict[str, Dict[str, int]] = {}
    for row in rows:
        label = (row.get("automated_label") or "").strip().lower()
        count = counts.setdefault(
            row["query_id"], {"uncertain": 0, "blank": 0}
        )
        if label == "uncertain":
            count["uncertain"] += 1
            continue
        if label not in AUTOMATED_LABELS:
            count["blank"] += 1
            continue
        labels.setdefault(row["query_id"], {})[str(row[id_field])] = label
    return labels, counts


def build_automated_exploratory_report(
    paper_csv: Path,
    chunk_csv: Path,
    benchmark_results: Mapping[str, Any],
    k_values: Iterable[int] = (1, 3, 5, 10),
) -> Dict[str, Any]:
    """Calculate metrics from model suggestions, never from human labels."""
    ks = tuple(k_values)
    if not ks or any(isinstance(k, bool) or not isinstance(k, int) or k < 1 for k in ks):
        raise ValueError("k_values must contain positive integers")
    paper_labels, paper_counts = _load_automated_labels(
        paper_csv, PAPER_FIELDS, PAPER_KEY_FIELDS, "benchmark_paper_id"
    )
    chunk_labels, chunk_counts = _load_automated_labels(
        chunk_csv, CHUNK_FIELDS, CHUNK_KEY_FIELDS, "chunk_id"
    )
    retrieval = benchmark_results.get("retrieval", {})
    per_query: Dict[str, Any] = {}
    aggregates: Dict[str, Dict[str, Dict[str, Any]]] = {
        unit: {} for unit in ("paper", "chunk")
    }

    for query_id, strategies in retrieval.items():
        per_query[query_id] = {}
        for strategy, strategy_result in strategies.items():
            per_query[query_id][strategy] = {}
            for unit, labels, result_id in (
                ("paper", paper_labels, "paper_id"),
                ("chunk", chunk_labels, "chunk_id"),
            ):
                judgments = labels.get(query_id, {})
                ranked_ids = [
                    str(item[result_id])
                    for item in strategy_result.get("results", [])
                    if str(item.get(result_id, "")) in judgments
                ]
                relevant = {
                    item_id for item_id, label in judgments.items()
                    if label == "relevant"
                }
                unit_metrics: Dict[str, Any] = {
                    "label_source": "automated_suggestion_only",
                    "judged_candidate_count": len(judgments),
                    "uncertain_candidate_count": (
                        chunk_counts if unit == "chunk" else paper_counts
                    ).get(query_id, {}).get("uncertain", 0),
                    "blank_candidate_count": (
                        chunk_counts if unit == "chunk" else paper_counts
                    ).get(query_id, {}).get("blank", 0),
                    "uncertain_or_blank_candidates_excluded": True,
                    "by_k": {},
                }
                binary_grades = {
                    item_id: int(label == "relevant")
                    for item_id, label in judgments.items()
                }
                for k in ks:
                    metrics = (
                        retrieval_metrics(ranked_ids, relevant, k)
                        if judgments
                        else None
                    )
                    if metrics is not None:
                        metrics[f"ndcg@{k}"] = ndcg_at_k(
                            ranked_ids, binary_grades, k
                        )
                    unit_metrics["by_k"][str(k)] = metrics
                per_query[query_id][strategy][unit] = unit_metrics

    for unit in ("paper", "chunk"):
        for strategy in sorted({
            strategy
            for query_strategies in per_query.values()
            for strategy in query_strategies
        }):
            aggregates[unit][strategy] = {}
            for k in ks:
                metric_values = [
                    query_data[strategy][unit]["by_k"][str(k)]
                    for query_data in per_query.values()
                    if strategy in query_data
                    and query_data[strategy][unit]["by_k"][str(k)] is not None
                ]
                metric_names = (
                    list(metric_values[0]) if metric_values else
                    [f"precision@{k}", f"recall@{k}", "reciprocal_rank",
                     f"average_precision@{k}", f"ndcg@{k}"]
                )
                aggregates[unit][strategy][str(k)] = {
                    name: {
                        "mean": (
                            sum(value[name] for value in metric_values if value[name] is not None)
                            / sum(value[name] is not None for value in metric_values)
                            if any(value[name] is not None for value in metric_values)
                            else None
                        ),
                        "eligible_query_count": sum(
                            value[name] is not None for value in metric_values
                        ),
                    }
                    for name in metric_names
                }

    return {
        "report_type": "exploratory_automated_pseudo_label_metrics",
        "label_provenance": "LLM suggestions only; not human judgments",
        "human_verified": False,
        "benchmark_acceptance_metrics": False,
        "dataset_version": benchmark_results.get("dataset_version"),
        "benchmark_results_generated_utc": benchmark_results.get("generated_utc"),
        "report_generated_utc": datetime.now(timezone.utc).isoformat(),
        "k_values": list(ks),
        "policy": (
            "Only automated_label values relevant/not_relevant are used. "
            "Uncertain and blank suggestions are excluded. This report is "
            "exploratory and must not be interpreted as human-verified effectiveness."
        ),
        "per_query": per_query,
        "macro_metrics": aggregates,
    }


def write_automated_exploratory_report(
    report: Mapping[str, Any], path: Path = AUTOMATED_METRICS_PATH
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(dict(report), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)
    return path
