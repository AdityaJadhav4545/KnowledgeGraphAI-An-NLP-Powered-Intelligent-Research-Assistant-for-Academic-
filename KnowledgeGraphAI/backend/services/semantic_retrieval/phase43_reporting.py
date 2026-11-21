"""Reproducible Phase 4.3 human, exploratory, and agreement reporting."""

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from KnowledgeGraphAI.backend.services.semantic_retrieval.annotation_dashboard import (
    CHUNK_KEY_FIELDS,
    CHUNK_WORKSHEET,
    PAPER_KEY_FIELDS,
    PAPER_WORKSHEET,
    load_worksheet,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.annotation_evaluation import (
    build_automated_exploratory_report,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_annotation_workflow import (
    ANNOTATION_PATH,
    CHUNK_FIELDS,
    PAPER_FIELDS,
    QUERY_PATH,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_corpus import MANIFEST_PATH


PROJECT_ROOT = Path(__file__).resolve().parents[4]
REPORT_ROOT = PROJECT_ROOT / "KnowledgeGraphAI" / "reports" / "semantic_retrieval"
RESULTS_PATH = REPORT_ROOT / "benchmark_results.json"
ERROR_ANALYSIS_PATH = REPORT_ROOT / "error_analysis.md"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _record_counts(
    path: Path,
    fields: Sequence[str],
    key_fields: Sequence[str],
    total_corpus_papers: int,
) -> Dict[str, Any]:
    rows, _ = load_worksheet(path, fields, key_fields)
    human_by_query: Dict[str, int] = {}
    automated_by_query: Dict[str, int] = {}
    human_labels = {"relevant": 0, "not_relevant": 0}
    automated_labels = {
        "relevant": 0,
        "not_relevant": 0,
        "uncertain": 0,
    }
    human_reviewers = set()
    independent_attestations = 0
    for row in rows:
        human_label = (
            row.get("human_label") or row.get("relevance_judgment") or ""
        ).strip().lower()
        automated_label = (row.get("automated_label") or "").strip().lower()
        if human_label in human_labels:
            human_labels[human_label] += 1
            human_by_query[row["query_id"]] = (
                human_by_query.get(row["query_id"], 0) + 1
            )
            if row.get("reviewer", "").strip():
                human_reviewers.add(row["reviewer"].strip())
            if row.get("independent_review_attested", "").strip().lower() == "yes":
                independent_attestations += 1
        if automated_label in automated_labels:
            automated_labels[automated_label] += 1
            automated_by_query[row["query_id"]] = (
                automated_by_query.get(row["query_id"], 0) + 1
            )
    complete_paper_queries = (
        sum(count == total_corpus_papers for count in human_by_query.values())
        if key_fields[-1] == "benchmark_paper_id"
        else None
    )
    return {
        "candidate_rows": len(rows),
        "human_judged_rows": sum(human_labels.values()),
        "unjudged_rows": len(rows) - sum(human_labels.values()),
        "human_label_counts": human_labels,
        "automated_suggestion_count": sum(automated_labels.values()),
        "automated_label_counts": automated_labels,
        "human_judgments_by_query": human_by_query,
        "automated_suggestions_by_query": automated_by_query,
        "complete_paper_judgment_queries": complete_paper_queries,
        "distinct_human_reviewers": len(human_reviewers),
        "independent_attestation_count": independent_attestations,
        "independent_attestation_complete": (
            sum(human_labels.values()) > 0
            and independent_attestations == sum(human_labels.values())
        ),
    }


def _agreement_for_rows(rows: Sequence[Mapping[str, str]]) -> Dict[str, Any]:
    classes = ("relevant", "not_relevant")
    confusion = {actual: {predicted: 0 for predicted in classes} for actual in classes}
    uncertain_suggestion_count = 0
    missing_human_count = 0
    missing_suggestion_count = 0
    paired_decisive_count = 0
    disagreements = []
    for row in rows:
        actual = (
            row.get("human_label") or row.get("relevance_judgment") or ""
        ).strip().lower()
        predicted = (row.get("automated_label") or "").strip().lower()
        if actual not in classes:
            missing_human_count += 1
            continue
        if predicted == "uncertain":
            uncertain_suggestion_count += 1
            continue
        if predicted not in classes:
            missing_suggestion_count += 1
            continue
        paired_decisive_count += 1
        confusion[actual][predicted] += 1
        if actual != predicted:
            disagreements.append({
                "query_id": row["query_id"],
                "candidate_id": row.get("benchmark_paper_id") or row.get("chunk_id"),
                "human_label": actual,
                "automated_label": predicted,
                "title": row.get("title", ""),
            })

    true_positive = confusion["relevant"]["relevant"]
    false_positive = confusion["not_relevant"]["relevant"]
    false_negative = confusion["relevant"]["not_relevant"]
    true_negative = confusion["not_relevant"]["not_relevant"]
    accuracy = (
        (true_positive + true_negative) / paired_decisive_count
        if paired_decisive_count else None
    )
    precision = (
        true_positive / (true_positive + false_positive)
        if true_positive + false_positive else None
    )
    recall = (
        true_positive / (true_positive + false_negative)
        if true_positive + false_negative else None
    )
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision is not None and recall is not None and precision + recall
        else 0.0 if precision == 0 or recall == 0 else None
    )
    return {
        "paired_decisive_count": paired_decisive_count,
        "uncertain_suggestions_excluded": uncertain_suggestion_count,
        "missing_human_judgment_count": missing_human_count,
        "missing_automated_suggestion_count": missing_suggestion_count,
        "disagreement_count": len(disagreements),
        "confusion_matrix": confusion,
        "metrics": {
            "accuracy": accuracy,
            "precision_relevant": precision,
            "recall_relevant": recall,
            "f1_relevant": f1,
        },
        "disagreements": disagreements,
        "cohen_kappa": {
            "value": None,
            "status": "not_calculated",
            "reason": (
                "The worksheets contain one human judgment per candidate; "
                "there are no overlapping independent human raters."
            ),
        },
    }


def _human_strategy_comparison(results: Mapping[str, Any]) -> Dict[str, Any]:
    comparison = {}
    for strategy, values in results.get("strategy_comparison", {}).items():
        available = bool(values.get("human_relevance_metrics_available"))
        macro = values.get("macro_human_metrics", {})
        comparison[strategy] = {
            "human_metrics_available": available,
            "mean_end_to_end_latency_seconds": values.get(
                "mean_end_to_end_latency_seconds"
            ),
            "mean_distinct_papers_at_10": values.get(
                "mean_distinct_papers_at_10"
            ),
            "paper_metrics_at_5": (
                macro.get("paper", {}).get("5", {}) if available else None
            ),
            "chunk_metrics_at_5": (
                macro.get("chunk", {}).get("5", {}) if available else None
            ),
            "metrics_by_k": (
                {
                    unit: macro.get(unit, {})
                    for unit in ("paper", "chunk")
                }
                if available
                else None
            ),
        }
    return comparison


def build_phase43_report(
    *,
    manifest_path: Path = MANIFEST_PATH,
    query_path: Path = QUERY_PATH,
    annotations_path: Path = ANNOTATION_PATH,
    paper_csv: Path = PAPER_WORKSHEET,
    chunk_csv: Path = CHUNK_WORKSHEET,
    results_path: Path = RESULTS_PATH,
    error_analysis_path: Path = ERROR_ANALYSIS_PATH,
) -> Dict[str, Any]:
    manifest = _load_json(manifest_path)
    query_dataset = _load_json(query_path)
    annotations = _load_json(annotations_path)
    results = _load_json(results_path)
    paper_counts = _record_counts(
        paper_csv, PAPER_FIELDS, PAPER_KEY_FIELDS, len(manifest["papers"])
    )
    chunk_counts = _record_counts(
        chunk_csv, CHUNK_FIELDS, CHUNK_KEY_FIELDS, len(manifest["papers"])
    )
    query_count = len(query_dataset["queries"])
    topic_counts: Dict[str, int] = {}
    for paper_record in manifest["papers"]:
        for topic in paper_record.get("topics", []):
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
    chunks = sum(
        int(paper.get("chunk_count", 0))
        for paper in manifest["papers"]
        if paper.get("index_status") == "indexed"
    )
    verified_queries = sum(
        entry.get("judgment_status") == "human_verified"
        for entry in annotations.get("queries", [])
    )
    paper_rows, _ = load_worksheet(paper_csv, PAPER_FIELDS, PAPER_KEY_FIELDS)
    chunk_rows, _ = load_worksheet(chunk_csv, CHUNK_FIELDS, CHUNK_KEY_FIELDS)
    automated_metrics = build_automated_exploratory_report(
        paper_csv, chunk_csv, results
    )
    report = {
        "report_type": "phase43_reproducible_assisted_annotation_report",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "dataset": {
            "dataset_version": manifest.get("dataset_version"),
            "paper_count": len(manifest["papers"]),
            "query_count": query_count,
            "indexed_chunk_count": chunks,
            "topic_distribution": dict(sorted(topic_counts.items())),
            "benchmark_generated_utc": results.get("generated_utc"),
            "benchmark_status": results.get("benchmark_status"),
        },
        "annotation_methodology": {
            "paper_and_chunk_suggestions_are_separate": True,
            "automated_suggestions_are_not_human_ground_truth": True,
            "human_metrics_require_human_verified_benchmark_annotations": True,
            "uncertain_suggestions_excluded_from_binary_agreement": True,
            "suggestion_model_names": sorted({
                row.get("automated_model", "").strip()
                for row in paper_rows + chunk_rows
                if row.get("automated_model", "").strip()
            }),
        },
        "annotations": {
            "paper_level": paper_counts,
            "chunk_level": chunk_counts,
            "verified_query_count_in_annotation_manifest": verified_queries,
            "independent_human_review_complete": bool(
                paper_counts["independent_attestation_complete"]
                and chunk_counts["independent_attestation_complete"]
            ),
        },
        "human_benchmark_evaluation": {
            "source": str(results_path),
            "status": (
                "available_from_human_verified_results"
                if verified_queries == query_count
                and results.get("benchmark_status") == "complete_human_judgments"
                else "pending_human_validation"
            ),
            "human_verified_query_count": verified_queries,
            "query_count": query_count,
            "strategy_comparison": _human_strategy_comparison(results),
        },
        "automated_exploratory_evaluation": automated_metrics,
        "llm_human_agreement": {
            "paper": _agreement_for_rows(paper_rows),
            "chunk": _agreement_for_rows(chunk_rows),
        },
        "error_analysis": {
            "source_report": (
                str(error_analysis_path) if error_analysis_path.exists() else None
            ),
            "text": (
                error_analysis_path.read_text(encoding="utf-8")
                if error_analysis_path.exists()
                else "No benchmark error-analysis report was available."
            ),
            "pending_human_queries": max(0, query_count - verified_queries),
        },
        "limitations": [
            "Automated suggestions are exploratory and do not satisfy human judgment requirements.",
            "No Cohen's kappa is reported because the present worksheet design has one human judgment per candidate.",
            "Retrieval effectiveness metrics remain unavailable unless the benchmark annotation manifest and results both indicate complete human-verified judgments.",
        ],
        "reproducibility": {
            "input_sha256": {
                str(path): _sha256(path)
                for path in (
                    manifest_path,
                    query_path,
                    annotations_path,
                    paper_csv,
                    chunk_csv,
                    results_path,
                )
            },
            "model_configuration": results.get("model", {}),
            "reproduction_commands": [
                "py -3.10 -m KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_batch_annotation --type both --batch-size 8 --rate-limit-seconds 0.25",
                "py -3.10 -m KnowledgeGraphAI.backend.services.semantic_retrieval.phase43_reporting",
            ],
        },
    }
    return report


def _strategy_metrics_for_plot(report: Mapping[str, Any]):
    strategies = report["human_benchmark_evaluation"]["strategy_comparison"]
    labels = list(strategies)
    latency = [
        strategies[name]["mean_end_to_end_latency_seconds"] for name in labels
    ]
    diversity = [strategies[name]["mean_distinct_papers_at_10"] for name in labels]
    precision = []
    for name in labels:
        values = strategies[name]["paper_metrics_at_5"]
        precision.append(values.get("precision@5", {}).get("macro_mean") if values else None)
    return labels, latency, diversity, precision


def _write_visualization(report: Mapping[str, Any], path: Path) -> None:
    labels, latency, diversity, precision = _strategy_metrics_for_plot(report)
    figure = make_subplots(
        rows=1,
        cols=3,
        subplot_titles=(
            "Mean latency",
            "Distinct papers in top 10",
            "Human-judged paper Precision@5",
        ),
    )
    figure.add_trace(
        go.Bar(x=labels, y=latency, name="Latency (seconds)"),
        row=1,
        col=1,
    )
    figure.add_trace(
        go.Bar(x=labels, y=diversity, name="Distinct papers"),
        row=1,
        col=2,
    )
    if any(value is not None for value in precision):
        figure.add_trace(
            go.Bar(x=labels, y=precision, name="Human P@5"),
            row=1,
            col=3,
        )
    else:
        figure.add_annotation(
            text="Pending complete human validation",
            x=0.5,
            y=0.5,
            xref="x3 domain",
            yref="y3 domain",
            showarrow=False,
        )
    figure.update_layout(
        title="Phase 4.3 Retrieval Strategy Comparison",
        showlegend=False,
        height=520,
    )
    path.write_text(
        figure.to_html(full_html=True, include_plotlyjs=True),
        encoding="utf-8",
    )


def _markdown_report(report: Mapping[str, Any], chart_name: str) -> str:
    dataset = report["dataset"]
    annotations = report["annotations"]
    paper = annotations["paper_level"]
    chunk = annotations["chunk_level"]
    strategies = report["human_benchmark_evaluation"]["strategy_comparison"]
    lines = [
        "# Phase 4.3 Assisted Annotation and Retrieval Report",
        "",
        f"Generated: `{report['generated_utc']}`",
        f"Dataset: `{dataset['dataset_version']}`",
        "",
        "## Corpus",
        "",
        f"- Papers: {dataset['paper_count']}",
        f"- Queries: {dataset['query_count']}",
        f"- Indexed chunks: {dataset['indexed_chunk_count']}",
        f"- Benchmark status: `{dataset['benchmark_status']}`",
        "",
        "## Annotation counts",
        "",
        "| Unit | Candidates | Human judgments | Unjudged | Automated suggestions | Independent attestations |",
        "|---|---:|---:|---:|---:|---:|",
        f"| Papers | {paper['candidate_rows']} | {paper['human_judged_rows']} | {paper['unjudged_rows']} | {paper['automated_suggestion_count']} | {paper['independent_attestation_count']} |",
        f"| Chunks | {chunk['candidate_rows']} | {chunk['human_judged_rows']} | {chunk['unjudged_rows']} | {chunk['automated_suggestion_count']} | {chunk['independent_attestation_count']} |",
        "",
        "Automated suggestions are separate from human judgments. They are never used as ground truth for the human benchmark.",
        "",
        "## Human-validated strategy comparison",
        "",
        "| Strategy | Mean latency (s) | Distinct papers @10 | Paper P@5 | Chunk P@5 | Human metric status |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for name, values in strategies.items():
        paper_metrics = values["paper_metrics_at_5"]
        chunk_metrics = values["chunk_metrics_at_5"]
        paper_p5 = (
            paper_metrics.get("precision@5", {}).get("macro_mean")
            if paper_metrics else None
        )
        chunk_p5 = (
            chunk_metrics.get("precision@5", {}).get("macro_mean")
            if chunk_metrics else None
        )
        lines.append(
            f"| {name} | {values['mean_end_to_end_latency_seconds']} | "
            f"{values['mean_distinct_papers_at_10']} | {paper_p5} | {chunk_p5} | "
            f"{'available' if values['human_metrics_available'] else 'pending human validation'} |"
        )
    lines += [
        "",
        "Human retrieval metrics by strategy and cutoff (available only after complete validated human annotations):",
        "",
        "| Unit | Strategy | K | Precision@K | Recall@K | MRR | MAP@K | nDCG@K |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for strategy, values in strategies.items():
        if not values["human_metrics_available"]:
            continue
        for unit in ("paper", "chunk"):
            for k, metrics in values["metrics_by_k"][unit].items():
                lines.append(
                    f"| {unit} | {strategy} | {k} | "
                    f"{metrics.get(f'precision@{k}', {}).get('macro_mean')} | "
                    f"{metrics.get(f'recall@{k}', {}).get('macro_mean')} | "
                    f"{metrics.get('reciprocal_rank', {}).get('macro_mean')} | "
                    f"{metrics.get(f'average_precision@{k}', {}).get('macro_mean')} | "
                    f"{metrics.get(f'ndcg@{k}', {}).get('macro_mean')} |"
                )
    if not any(item["human_metrics_available"] for item in strategies.values()):
        lines += [
            "| — | — | — | Pending | Pending | Pending | Pending | Pending |",
        ]
    lines += [
        "",
        f"![Strategy comparison](./{chart_name})",
        "",
        "## LLM / human agreement",
        "",
    ]
    for unit in ("paper", "chunk"):
        agreement = report["llm_human_agreement"][unit]
        lines += [
            f"### {unit.title()} candidates",
            "",
            f"- Decisive paired labels: {agreement['paired_decisive_count']}",
            f"- Uncertain model suggestions excluded: {agreement['uncertain_suggestions_excluded']}",
            f"- Disagreements: {agreement['disagreement_count']}",
            f"- Confusion matrix (rows human, columns automated): `{json.dumps(agreement['confusion_matrix'], sort_keys=True)}`",
            f"- Accuracy / precision / recall / F1: `{json.dumps(agreement['metrics'], sort_keys=True)}`",
            f"- Cohen's kappa: not calculated — {agreement['cohen_kappa']['reason']}",
            "",
        ]
    lines += [
        "## Exploratory automated-label evaluation",
        "",
        "Automated metrics use only decisive model suggestions (`relevant` or `not_relevant`); uncertain/blank candidates are excluded. This section is pseudo-labeled exploration, not validated benchmark effectiveness.",
        "",
    ]
    automated = report["automated_exploratory_evaluation"]["macro_metrics"]
    lines += [
        "| Unit | Strategy | K | Precision | Recall | MRR | MAP | nDCG |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for unit in ("paper", "chunk"):
        for strategy, k_metrics in automated.get(unit, {}).items():
            for k, metrics in k_metrics.items():
                values = {
                    name: metrics.get(name, {}).get("mean")
                    for name in (
                        f"precision@{k}",
                        f"recall@{k}",
                        "reciprocal_rank",
                        f"average_precision@{k}",
                        f"ndcg@{k}",
                    )
                }
                lines.append(
                    f"| {unit} | {strategy} | {k} | "
                    f"{values[f'precision@{k}']} | {values[f'recall@{k}']} | "
                    f"{values['reciprocal_rank']} | "
                    f"{values[f'average_precision@{k}']} | "
                    f"{values[f'ndcg@{k}']} |"
                )
    lines += [
        "",
        "## Error analysis and limitations",
        "",
        report["error_analysis"]["text"].strip(),
        "",
        *[f"- {item}" for item in report["limitations"]],
        "",
        "## Reproducibility",
        "",
        "```powershell",
        *report["reproducibility"]["reproduction_commands"],
        "```",
        "",
        "Input SHA-256 digests and complete machine-readable results are in the sibling JSON report.",
        "",
    ]
    return "\n".join(lines)


def write_versioned_report(
    report: Mapping[str, Any], output_dir: Path = REPORT_ROOT
) -> Dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    version = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    stem = f"phase43_assisted_report_{version}"
    json_path = output_dir / f"{stem}.json"
    markdown_path = output_dir / f"{stem}.md"
    chart_path = output_dir / f"{stem}_strategies.html"
    _write_visualization(report, chart_path)
    json_path.write_text(
        json.dumps(dict(report), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        _markdown_report(report, chart_path.name),
        encoding="utf-8",
    )
    return {
        "json": str(json_path),
        "markdown": str(markdown_path),
        "visualization": str(chart_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=REPORT_ROOT)
    args = parser.parse_args()
    report = build_phase43_report()
    print(json.dumps(write_versioned_report(report, args.output_dir), indent=2))


if __name__ == "__main__":
    main()
