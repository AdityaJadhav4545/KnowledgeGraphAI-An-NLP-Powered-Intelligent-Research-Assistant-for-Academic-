"""Isolated real-paper semantic retrieval benchmark orchestration."""

import argparse
import hashlib
import json
import platform
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import faiss  # noqa: F401 – may raise ImportError on some Windows environments
import numpy as np
import torch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from KnowledgeGraphAI.backend.services.knowledge_graph.graph_query import GraphQueryService
from KnowledgeGraphAI.backend.services.knowledge_graph.neo4j_connection import (
    get_neo4j_manager,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_corpus import (
    BENCHMARK_ROOT,
    FAILURES_PATH,
    MANIFEST_PATH,
    create_manifest,
    download_papers,
    load_manifest,
    validate_annotations,
    validate_query_dataset,
    write_annotation_template,
    write_json_atomic,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.config import (
    SemanticRetrievalConfig,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.embedding_service import (
    Specter2EmbeddingService,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.evaluation import (
    ndcg_at_k,
    retrieval_metrics,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.metadata_store import (
    ChunkMetadataStore,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.retrieval_service import (
    SemanticRetrievalService,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.validation import (
    _process_memory_bytes,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.vector_store import (
    FaissVectorStore,
)


PROJECT_ROOT = Path(__file__).resolve().parents[4]
QUERY_PATH = Path(__file__).with_name("benchmark_queries.json")
DATA_ROOT = PROJECT_ROOT / "KnowledgeGraphAI" / "data" / "benchmark"
REPORT_ROOT = PROJECT_ROOT / "KnowledgeGraphAI" / "reports" / "semantic_retrieval"
ANNOTATION_PATH = DATA_ROOT / "benchmark_annotations.json"
RESULTS_PATH = REPORT_ROOT / "benchmark_results.json"
REPORT_PATH = REPORT_ROOT / "benchmark_report.md"
ERROR_ANALYSIS_PATH = REPORT_ROOT / "error_analysis.md"
DATABASE_PATH = DATA_ROOT / "benchmark_metadata.sqlite"
INDEX_PATH = DATA_ROOT / "benchmark.faiss"
K_VALUES = (1, 3, 5, 10)
CONFIGURATIONS = (
    "faiss_cosine",
    "metadata_filtered_cosine",
    "paper_aggregation",
    "mmr_diversity",
)


class _TimedEmbeddingService:
    def __init__(self, service: Specter2EmbeddingService, timings: Dict[str, List[float]]):
        self._service = service
        self._timings = timings

    def __getattr__(self, name: str) -> Any:
        return getattr(self._service, name)

    def embed_documents(self, *args: Any, **kwargs: Any) -> np.ndarray:
        started = time.perf_counter()
        try:
            return self._service.embed_documents(*args, **kwargs)
        finally:
            self._timings["document_embedding_seconds"].append(
                time.perf_counter() - started
            )

    def embed_queries(self, *args: Any, **kwargs: Any) -> np.ndarray:
        started = time.perf_counter()
        try:
            return self._service.embed_queries(*args, **kwargs)
        finally:
            self._timings["query_embedding_seconds"].append(
                time.perf_counter() - started
            )


class _TimedVectorStore:
    def __init__(self, store: FaissVectorStore, timings: Dict[str, List[float]]):
        self._store = store
        self._timings = timings

    def __getattr__(self, name: str) -> Any:
        return getattr(self._store, name)

    def search(self, *args: Any, **kwargs: Any):
        started = time.perf_counter()
        try:
            return self._store.search(*args, **kwargs)
        finally:
            self._timings["faiss_search_seconds"].append(time.perf_counter() - started)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _summary(values: Sequence[float]) -> Dict[str, Optional[float]]:
    if not values:
        return {"mean": None, "median": None, "count": 0}
    return {
        "mean": statistics.fmean(values),
        "median": statistics.median(values),
        "count": len(values),
    }


def _recorded_indexing_seconds(manifest: Dict[str, Any]) -> float:
    return sum(
        float(paper.get("index_seconds", 0.0))
        for paper in manifest["papers"]
        if paper.get("index_status") == "indexed"
    )


def _open_benchmark_store():
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    engine = create_engine(
        f"sqlite:///{DATABASE_PATH.as_posix()}",
        connect_args={"check_same_thread": False},
    )
    metadata = ChunkMetadataStore(
        sessionmaker(bind=engine, expire_on_commit=False)
    )
    store = FaissVectorStore(
        SemanticRetrievalConfig.from_env().embedding_dimension,
        INDEX_PATH,
        metadata_store=metadata,
    )
    return engine, metadata, store


def prepare_corpus(*, download: bool = True) -> Dict[str, Any]:
    manifest = create_manifest(DATA_ROOT)
    query_dataset = json.loads(QUERY_PATH.read_text(encoding="utf-8"))
    validate_query_dataset(query_dataset)
    write_json_atomic(DATA_ROOT / "benchmark_queries.json", query_dataset)
    write_annotation_template(query_dataset, manifest, ANNOTATION_PATH)
    if download:
        outcome = download_papers(manifest, DATA_ROOT)
        manifest = outcome["manifest"]
    else:
        write_json_atomic(MANIFEST_PATH, manifest)
    return manifest


def _index_manifest(
    manifest: Dict[str, Any],
    retrieval: SemanticRetrievalService,
    metadata: ChunkMetadataStore,
) -> Dict[str, Any]:
    failures: List[Dict[str, str]] = []
    initial_count = metadata.count()
    started_all = time.perf_counter()
    for paper in manifest["papers"]:
        pdf_path = DATA_ROOT / paper["local_pdf_path"]
        if not pdf_path.is_file():
            paper["index_status"] = "failed"
            paper["index_error"] = f"PDF is missing: {paper['local_pdf_path']}"
            failures.append({
                "arxiv_id": paper["arxiv_id"],
                "error": paper["index_error"],
            })
            write_json_atomic(MANIFEST_PATH, manifest)
            continue

        content_hash = _sha256(pdf_path)
        if (
            paper.get("index_status") == "indexed"
            and paper.get("index_pdf_sha256") == content_hash
        ):
            continue

        # A partial previous attempt is safely discarded only in the isolated
        # benchmark SQLite/FAISS store before reprocessing this paper.
        retrieval.delete_paper(int(paper["benchmark_paper_id"]))
        paper["index_status"] = "indexing"
        paper["index_error"] = None
        write_json_atomic(MANIFEST_PATH, manifest)
        paper_started = time.perf_counter()
        try:
            chunks = retrieval.index_pdf(
                str(pdf_path),
                int(paper["benchmark_paper_id"]),
                validate_graph=False,
                paper_title=paper["title"],
                source_identifier=f"arxiv:{paper['arxiv_id']}",
            )
            paper["index_status"] = "indexed"
            paper["index_pdf_sha256"] = content_hash
            paper["chunk_count"] = len(chunks)
            paper["index_seconds"] = time.perf_counter() - paper_started
            paper["index_error"] = None
        except Exception as exc:
            paper["index_status"] = "failed"
            paper["index_error"] = f"{type(exc).__name__}: {exc}"
            paper["chunk_count"] = 0
            failures.append({
                "arxiv_id": paper["arxiv_id"],
                "error": paper["index_error"],
            })
        write_json_atomic(MANIFEST_PATH, manifest)

    elapsed = time.perf_counter() - started_all
    write_json_atomic(FAILURES_PATH, {"failures": failures})
    return {
        "initial_chunk_count": initial_count,
        "total_chunk_count": metadata.count(),
        "indexing_seconds": _recorded_indexing_seconds(manifest),
        "indexing_invocation_seconds": elapsed,
        "failures": failures,
    }


def _traceability(
    manifest: Dict[str, Any],
    retrieved: Dict[str, Any],
    manager: Any,
) -> Dict[str, Any]:
    traceability: Dict[str, Any] = {}
    graph_queries = GraphQueryService()
    titles = {
        item["title"]
        for query_result in retrieved.values()
        for strategy_result in query_result.values()
        for item in strategy_result["results"]
    }
    paper_by_title = {
        paper["title"]: paper for paper in manifest["papers"]
    }
    for title in sorted(titles):
        paper = paper_by_title.get(title)
        if paper is None:
            continue
        matches = manager.execute_query(
            "MATCH (p:Paper) WHERE p.arxiv_id = $arxiv_id "
            "OR toLower(p.title) = toLower($title) "
            "RETURN p.paper_id AS paper_id, p.title AS title, "
            "p.arxiv_id AS arxiv_id LIMIT 3",
            {"arxiv_id": paper["arxiv_id"], "title": title},
        )
        key = paper["arxiv_id"]
        if len(matches) == 1:
            graph_paper_id = matches[0].get("paper_id")
            paper["canonical_neo4j_paper_id"] = graph_paper_id
            graph_entities = graph_queries.get_paper_entities(graph_paper_id)
            graph_relationships = graph_queries.get_paper_relationships(graph_paper_id)
            traceability[key] = {
                "status": "matched",
                "canonical_paper_id": graph_paper_id,
                "neo4j_title": matches[0].get("title"),
                "sampled_retrieved_chunk_ids": [
                    item["chunk_id"]
                    for query_result in retrieved.values()
                    for strategy_result in query_result.values()
                    for item in strategy_result["results"]
                    if item["title"] == title
                ],
                "entity_count": len(graph_entities),
                "relationship_count": len(graph_relationships),
                "entities": graph_entities,
                "relationships": graph_relationships,
            }
        elif matches:
            paper["canonical_neo4j_paper_id"] = None
            traceability[key] = {
                "status": "ambiguous_title_match",
                "matches": matches,
            }
        else:
            paper["canonical_neo4j_paper_id"] = None
            traceability[key] = {
                "status": "not_in_neo4j",
                "note": "No exact-title Paper node was found; graph context was not invented.",
            }
    write_json_atomic(MANIFEST_PATH, manifest)
    return traceability


def _load_annotations(
    manifest: Dict[str, Any],
    queries: Dict[str, Any],
    metadata: Optional[ChunkMetadataStore] = None,
) -> Dict[str, Any]:
    if not ANNOTATION_PATH.exists():
        return {"schema_version": 1, "label_type": "human_annotated", "queries": []}
    annotations = json.loads(ANNOTATION_PATH.read_text(encoding="utf-8"))
    validate_annotations(
        annotations,
        (query["query_id"] for query in queries["queries"]),
        (paper["benchmark_paper_id"] for paper in manifest["papers"]),
        (
            metadata.chunk_ids()
            if metadata is not None else None
        ),
    )
    return annotations


def _evaluate_configuration(
    query: Dict[str, Any],
    results: Sequence[Dict[str, Any]],
    annotation: Dict[str, Any],
) -> Dict[str, Any]:
    if annotation.get("judgment_status") != "human_verified":
        return {
            "judgment_status": "pending_human_review",
            "metrics": None,
            "note": "Metrics withheld because relevance labels are not human-verified.",
        }

    report: Dict[str, Any] = {
        "judgment_status": "human_verified",
        "evaluation_policy": (
            "Metrics use only explicitly judged IDs. Unjudged results are removed "
            "before ranking (condensed judged-set evaluation), never treated as "
            "irrelevant."
        ),
        "metrics": {},
    }
    for unit, judged_key, relevant_key, result_key in (
        ("chunk", "judged_chunk_ids", "relevant_chunk_ids", "chunk_id"),
        ("paper", "judged_paper_ids", "relevant_paper_ids", "paper_id"),
    ):
        judged_ids = {str(value) for value in annotation.get(judged_key, [])}
        relevant = {str(value) for value in annotation.get(relevant_key, [])}
        retrieved_ids = [
            str(item[result_key])
            for item in results
            if str(item[result_key]) in judged_ids
        ]
        if unit == "paper":
            retrieved_ids = list(dict.fromkeys(retrieved_ids))

        if not judged_ids:
            report["metrics"][unit] = {
                "status": "no_judgments",
                "judged_result_count": 0,
                "unjudged_result_count": len(results),
                "by_k": None,
            }
            continue

        raw_grades = annotation.get(
            "paper_relevance_grades" if unit == "paper"
            else "chunk_relevance_grades",
            {},
        )
        grades = {
            str(document_id): int(grade)
            for document_id, grade in raw_grades.items()
        }
        by_k = {}
        for k in K_VALUES:
            metrics = retrieval_metrics(retrieved_ids, relevant, k)
            metrics[f"ndcg@{k}"] = (
                ndcg_at_k(retrieved_ids, grades, k) if grades else None
            )
            by_k[str(k)] = metrics
        report["metrics"][unit] = {
            "status": "judged_set",
            "judged_result_count": len(retrieved_ids),
            "unjudged_result_count": len(results) - len(retrieved_ids),
            "judged_document_count": len(judged_ids),
            "no_judged_relevant_documents": not relevant,
            "by_k": by_k,
            "note": (
                "Recall and MAP use the annotated relevant-ID set; chunk-level "
                "values are conditional on the judged candidate pool."
            ),
        }
    return report


def _macro_evaluation(per_query: Dict[str, Any], strategy: str) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for unit in ("chunk", "paper"):
        by_k: Dict[str, Any] = {}
        for k in K_VALUES:
            metric_names = (
                f"precision@{k}",
                f"recall@{k}",
                "reciprocal_rank",
                f"average_precision@{k}",
                f"ndcg@{k}",
            )
            metrics_for_k: Dict[str, Any] = {}
            for metric_name in metric_names:
                values = []
                for query_results in per_query.values():
                    unit_eval = (
                        query_results[strategy]["evaluation"]["metrics"] or {}
                    ).get(unit, {})
                    metrics = unit_eval.get("by_k") or {}
                    value = metrics.get(str(k), {}).get(metric_name)
                    if value is not None:
                        values.append(float(value))
                metrics_for_k[metric_name] = {
                    "macro_mean": statistics.fmean(values) if values else None,
                    "eligible_query_count": len(values),
                }
            by_k[str(k)] = metrics_for_k
        result[unit] = by_k
    return result


def _evaluation_summary(
    strategy_comparison: Dict[str, Any],
    all_human_verified: bool,
) -> Dict[str, Any]:
    return {
        "status": "human_judged" if all_human_verified else "pending_human_annotations",
        "metric_names": [
            "precision@k", "recall@k", "mrr", "map@k", "ndcg@k"
        ],
        "k_values": list(K_VALUES),
        "macro_averaging": True,
        "chunk_level": {
            strategy: metrics["macro_human_metrics"]["chunk"]
            for strategy, metrics in strategy_comparison.items()
        },
        "paper_level": {
            strategy: metrics["macro_human_metrics"]["paper"]
            for strategy, metrics in strategy_comparison.items()
        },
        "unjudged_documents_are_excluded_not_counted_as_irrelevant": True,
        "chunk_metric_scope": "explicitly judged candidate pool",
    }


def _compare_and_evaluate(
    retrieval: SemanticRetrievalService,
    manifest: Dict[str, Any],
    queries: Dict[str, Any],
    annotations: Dict[str, Any],
    timings: Dict[str, List[float]],
) -> Dict[str, Any]:
    papers_by_area: Dict[str, List[int]] = {}
    for paper in manifest["papers"]:
        for area in paper["topics"]:
            papers_by_area.setdefault(area, []).append(paper["benchmark_paper_id"])

    annotations_by_query = {
        entry["query_id"]: entry for entry in annotations.get("queries", [])
    }
    output: Dict[str, Any] = {}
    for query in queries["queries"]:
        query_results = {}
        annotation = annotations_by_query.get(query["query_id"], {})
        topic_ids = sorted({
            int(paper_id)
            for area in query["target_areas"]
            for paper_id in papers_by_area.get(area, [])
        })
        strategies = {
            "faiss_cosine": {},
            "metadata_filtered_cosine": {
                "paper_ids": topic_ids,
            },
            "paper_aggregation": {
                "aggregate_by_paper": True,
            },
            "mmr_diversity": {
                "diversity": True,
                "diversity_lambda": 0.7,
            },
        }
        for strategy, options in strategies.items():
            started = time.perf_counter()
            results = retrieval.search(
                query["query_text"],
                top_k=10,
                **options,
            )
            elapsed = time.perf_counter() - started
            query_results[strategy] = {
                "results": results,
                "result_count": len(results),
                "distinct_paper_count": len({
                    item["paper_id"] for item in results
                }),
                "duplicate_chunk_count": len(results) - len({
                    item["chunk_id"] for item in results
                }),
                "end_to_end_latency_seconds": elapsed,
                "evaluation": _evaluate_configuration(
                    query, results, annotation
                ),
            }
        output[query["query_id"]] = query_results

    comparisons: Dict[str, Any] = {}
    for strategy in CONFIGURATIONS:
        per_query = [
            results[strategy]
            for results in output.values()
        ]
        comparisons[strategy] = {
            "mean_end_to_end_latency_seconds": statistics.fmean(
                item["end_to_end_latency_seconds"] for item in per_query
            ),
            "median_end_to_end_latency_seconds": statistics.median(
                item["end_to_end_latency_seconds"] for item in per_query
            ),
            "mean_result_count": statistics.fmean(
                item["result_count"] for item in per_query
            ),
            "mean_distinct_papers_at_10": statistics.fmean(
                item["distinct_paper_count"] for item in per_query
            ),
            "mean_duplicate_chunks_at_10": statistics.fmean(
                item["duplicate_chunk_count"] for item in per_query
            ),
            "human_relevance_metrics_available": all(
                item["evaluation"]["judgment_status"] == "human_verified"
                for item in per_query
            ),
            "macro_human_metrics": _macro_evaluation(output, strategy),
        }
    return {
        "per_query": output,
        "strategy_comparison": comparisons,
        "timings": {name: _summary(values) for name, values in timings.items()},
    }


def _error_analysis(
    comparison: Dict[str, Any],
    annotations: Dict[str, Any],
    queries: Dict[str, Any],
) -> str:
    annotations_by_id = {
        item["query_id"]: item for item in annotations.get("queries", [])
    }
    query_by_id = {item["query_id"]: item for item in queries["queries"]}
    pending = []
    failures = []
    for query_id, strategies in comparison["per_query"].items():
        annotation = annotations_by_id.get(query_id, {})
        query_text = query_by_id[query_id]["query_text"]
        if annotation.get("judgment_status") != "human_verified":
            pending.append(query_id)
            continue
        expected = set(annotation.get("relevant_chunk_ids", []))
        retrieved = {
            item["chunk_id"]
            for item in strategies["faiss_cosine"]["results"]
        }
        missing = sorted(expected - retrieved)
        if missing:
            failures.append(
                f"- `{query_id}` ({query_text}): judged relevant chunks not in "
                f"baseline top 10: {', '.join(missing)}. Error type requires "
                "human classification."
            )
    lines = [
        "# Semantic Retrieval Error Analysis",
        "",
        (
            "Status: complete for the available human labels."
            if not pending
            else "Status: provisional; unjudged results are not classified as irrelevant."
        ),
        "",
    ]
    if pending:
        lines += [
            f"{len(pending)} queries still need independent human annotation:",
            "",
            *[f"- `{query_id}`" for query_id in pending],
            "",
        ]
    if failures:
        lines += ["## Judged baseline misses", "", *failures, ""]
    if not failures:
        if pending:
            lines += [
                "No relevance misses are reported while human judgments are pending.",
                "",
            ]
        else:
            lines += [
                "No judged relevant chunk misses were observed in the baseline top 10.",
                "",
            ]
    lines += [
        "Similar terminology, passage relevance, chunk boundaries, and ambiguous "
        "queries must be reviewed by annotators before assigning error classes.",
        "",
    ]
    return "\n".join(lines)


def _report_markdown(results: Dict[str, Any]) -> str:
    performance = results["performance"]
    comparisons = results["strategy_comparison"]
    metric_lines = [
        "| Strategy | Mean / median end-to-end query latency (s) | Mean distinct papers / 10 | Mean duplicate chunks / 10 | Relevance metrics available |",
        "|---|---:|---:|---:|---|",
    ]
    for strategy, values in comparisons.items():
        metric_lines.append(
            f"| {strategy} | {values['mean_end_to_end_latency_seconds']:.4f} / "
            f"{values['median_end_to_end_latency_seconds']:.4f} "
            f"| {values['mean_distinct_papers_at_10']:.2f} "
            f"| {values['mean_duplicate_chunks_at_10']:.2f} "
            f"| {values['human_relevance_metrics_available']} |"
        )
    relevance_lines = [
        "| Strategy | Unit | K | P@K | Recall@K | MRR | MAP@K | nDCG@K | P@K eligible queries |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for strategy, values in comparisons.items():
        for unit, k_values in values["macro_human_metrics"].items():
            for k, metrics in k_values.items():
                names = (
                    f"precision@{k}",
                    f"recall@{k}",
                    "reciprocal_rank",
                    f"average_precision@{k}",
                    f"ndcg@{k}",
                )
                rendered = [
                    "n/a" if metrics[name]["macro_mean"] is None
                    else f"{metrics[name]['macro_mean']:.4f}"
                    for name in names
                ]
                eligible = metrics[f"precision@{k}"]["eligible_query_count"]
                relevance_lines.append(
                    f"| {strategy} | {unit} | {k} | "
                    + " | ".join(rendered)
                    + f" | {eligible} |"
                )
    return "\n".join([
        "# Phase 4.3 Scientific Semantic Retrieval Benchmark",
        "",
        f"Status: **{results['benchmark_status']}**",
        "",
        results["status_explanation"],
        "",
        "## Corpus and model",
        "",
        f"- Publications in manifest: {performance['papers_in_manifest']}",
        f"- Successfully indexed: {performance['papers_indexed']}",
        f"- Failed: {performance['papers_failed']}",
        f"- Chunks/embeddings: {performance['chunks']}",
        f"- Embedding dimension: {performance['embedding_dimension']}",
        f"- Model/adapters: `{results['model']['model']}` / "
        f"`{results['model']['document_adapter']}` / "
        f"`{results['model']['query_adapter']}`",
        f"- Device: {results['model']['device']}",
        f"- Benchmark index bytes: {performance['index_size_bytes']}",
        "",
        "## Retrieval strategy comparison",
        "",
        *metric_lines,
        "",
        "Unjudged documents are excluded from metric rankings, not treated as "
        "irrelevant. Chunk-level metrics are conditional on the judged candidate "
        "pool; recall/MAP denominators include only explicitly labeled relevant IDs.",
        "",
        "### Human-judged macro metrics",
        "",
        *relevance_lines,
        "",
        "",
        "## Runtime",
        "",
        f"- Recorded PDF processing + embedding time: "
        f"{performance['indexing_seconds']:.2f} seconds across indexed papers",
        f"- Index command time in this run: "
        f"{performance['indexing_invocation_seconds']:.2f} seconds",
        f"- Mean document embedding seconds/batch: "
        f"{results['timings']['document_embedding_seconds']['mean']}",
        f"- Document embedding timing note: "
        f"{performance['document_embedding_timing_note']}",
        f"- Query embedding seconds/call (mean / median): "
        f"{results['timings']['query_embedding_seconds']['mean']} / "
        f"{results['timings']['query_embedding_seconds']['median']}",
        f"- FAISS search seconds/call (mean / median): "
        f"{results['timings']['faiss_search_seconds']['mean']} / "
        f"{results['timings']['faiss_search_seconds']['median']}",
        f"- Process memory before/after: {performance['memory_before']} / "
        f"{performance['memory_after']}",
        "",
        "## Relevance evaluation",
        "",
        f"- Annotation status: {results['annotation_status']}",
        f"- Human-verified queries: {results['human_verified_query_count']}",
        f"- Queries without judged relevant documents: "
        f"{results['queries_with_no_judged_relevant_documents']}",
        "- Macro metrics report eligible-query denominators per measure; undefined "
        "recall/MRR/MAP values for queries with no judged relevant items are omitted.",
        "",
        "## Neo4j traceability",
        "",
        f"- Sampled retrieved papers found in Neo4j: "
        f"{results['neo4j_traceability_summary']['matched']}",
        f"- Not found: {results['neo4j_traceability_summary']['not_in_neo4j']}",
        f"- Ambiguous title matches: "
        f"{results['neo4j_traceability_summary']['ambiguous_title_match']}",
        "- Benchmark indexing uses benchmark-local numeric IDs; canonical Neo4j "
        "IDs are recorded only when an exact title match exists.",
        "",
        "## Limitations",
        "",
        "- The arXiv corpus is a curated pilot, not a representative scientific IR benchmark.",
        "- Relevance labels require independent human inspection; pending papers "
        "are unjudged, not irrelevant.",
        "- The ranking comparison's metadata filter uses each query's predeclared "
        "target-area tags; this is a controlled filter condition, not an automatic "
        "intent classifier.",
        "- Full-text PDFs remain local and are excluded from Git.",
        "",
        "## Reproduction",
        "",
        "See the PowerShell commands in README.md; model download and benchmark "
        "indexing are explicit commands and do not run during ordinary pytest.",
        "",
    ])


def run_benchmark(
    *,
    download: bool = True,
    index: bool = True,
    trace_neo4j: bool = True,
) -> Dict[str, Any]:
    manifest = create_manifest(DATA_ROOT)
    if download:
        download_papers(manifest, DATA_ROOT)
    manifest = load_manifest(MANIFEST_PATH)
    query_dataset = json.loads(QUERY_PATH.read_text(encoding="utf-8"))
    validate_query_dataset(query_dataset)
    write_json_atomic(DATA_ROOT / "benchmark_queries.json", query_dataset)
    query_ids = [query["query_id"] for query in query_dataset["queries"]]
    if not ANNOTATION_PATH.exists():
        write_annotation_template(
            query_dataset, manifest, ANNOTATION_PATH
        )

    timings: Dict[str, List[float]] = {
        "document_embedding_seconds": [],
        "query_embedding_seconds": [],
        "faiss_search_seconds": [],
    }
    embedding_service = Specter2EmbeddingService()
    timed_embedding = _TimedEmbeddingService(embedding_service, timings)
    engine, metadata, raw_store = _open_benchmark_store()
    vector_store = _TimedVectorStore(raw_store, timings)
    retrieval = SemanticRetrievalService(
        config=SemanticRetrievalConfig.from_env(),
        embedding_service=timed_embedding,
        vector_store=vector_store,
        neo4j_manager=object(),
    )
    memory_before = _process_memory_bytes()
    dimension = embedding_service.dimension
    if index:
        indexing = _index_manifest(manifest, retrieval, metadata)
    else:
        indexing = {
            "initial_chunk_count": metadata.count(),
            "total_chunk_count": metadata.count(),
            "indexing_seconds": _recorded_indexing_seconds(manifest),
            "indexing_invocation_seconds": 0.0,
            "failures": [],
        }
    if retrieval.vector_store.count != metadata.count():
        retrieval.vector_store.reload()
        if retrieval.vector_store.count != metadata.count():
            raise RuntimeError(
                "FAISS/SQLite vector count mismatch in the isolated benchmark index"
            )
    manifest = load_manifest(MANIFEST_PATH)
    annotations = _load_annotations(manifest, query_dataset, metadata)
    comparison = _compare_and_evaluate(
        retrieval,
        manifest,
        query_dataset,
        annotations,
        timings,
    )
    traceability: Dict[str, Any] = {}
    if trace_neo4j:
        try:
            manager = get_neo4j_manager()
            traceability = _traceability(manifest, comparison["per_query"], manager)
        except Exception as exc:
            traceability = {
                "status": "unavailable",
                "error": f"{type(exc).__name__}: {exc}",
            }
    else:
        traceability = {"status": "not_run"}

    papers_indexed = sum(
        paper.get("index_status") == "indexed" for paper in manifest["papers"]
    )
    papers_failed = sum(
        paper.get("download_status") == "failed"
        or paper.get("index_status") == "failed"
        for paper in manifest["papers"]
    )
    annotation_entries = annotations.get("queries", [])
    human_verified = sum(
        entry.get("judgment_status") == "human_verified"
        for entry in annotation_entries
    )
    no_judged_relevant = sum(
        entry.get("judgment_status") == "human_verified"
        and not entry.get("relevant_paper_ids")
        for entry in annotation_entries
    )
    all_human_verified = human_verified == len(query_ids)
    all_papers_indexed = papers_indexed == len(manifest["papers"])
    benchmark_complete = (
        all_human_verified and all_papers_indexed and not papers_failed
    )
    incomplete_reasons = [
        reason
        for condition, reason in (
            (not all_human_verified, "human annotations are incomplete"),
            (not all_papers_indexed, "not all papers were indexed"),
            (bool(papers_failed), "download or indexing failures remain"),
        )
        if condition
    ]
    result = {
        "schema_version": 1,
        "dataset_version": manifest["dataset_version"],
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "benchmark_status": (
            "complete_human_judgments"
            if benchmark_complete
            else "provisional_pending_human_review"
        ),
        "status_explanation": (
            "All papers were indexed and all query/paper relevance judgments were "
            "human-verified."
            if benchmark_complete
            else "The benchmark remains provisional because "
            + ", ".join(incomplete_reasons)
            + "."
        ),
        "model": {
            "model": embedding_service.config.model_name,
            "document_adapter": embedding_service.config.document_adapter,
            "query_adapter": embedding_service.config.query_adapter,
            "device": str(embedding_service._device),
            "embedding_dimension": dimension,
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "torch": torch.__version__,
            "numpy": np.__version__,
            "faiss": getattr(faiss, "__version__", "unknown"),
            "seed": 0,
        },
        "annotation_status": "human_verified" if all_human_verified else "pending_human_review",
        "human_verified_query_count": human_verified,
        "queries_with_no_judged_relevant_documents": no_judged_relevant,
        "indexing": indexing,
        "timings": {name: _summary(values) for name, values in timings.items()},
        "performance": {
            "papers_in_manifest": len(manifest["papers"]),
            "papers_indexed": papers_indexed,
            "papers_failed": papers_failed,
            "chunks": metadata.count(),
            "embedding_dimension": dimension,
            "indexing_seconds": indexing["indexing_seconds"],
            "indexing_invocation_seconds": indexing["indexing_invocation_seconds"],
            "document_embedding_timing_note": (
                "Measured directly during indexing."
                if timings["document_embedding_seconds"]
                else (
                    "Not separately recorded because this run reused indexed "
                    "vectors; recorded per-paper times include PDF extraction "
                    "and embedding."
                )
            ),
            "index_size_bytes": INDEX_PATH.stat().st_size if INDEX_PATH.exists() else 0,
            "memory_before": memory_before,
            "memory_after": _process_memory_bytes(),
        },
        "strategy_comparison": comparison["strategy_comparison"],
        "retrieval": comparison["per_query"],
        "neo4j_traceability": traceability,
        "neo4j_traceability_summary": {
            status: sum(
                1 for value in traceability.values()
                if isinstance(value, dict) and value.get("status") == status
            )
            for status in ("matched", "not_in_neo4j", "ambiguous_title_match")
        },
        "evaluation": _evaluation_summary(
            comparison["strategy_comparison"], all_human_verified
        ),
    }
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    write_json_atomic(RESULTS_PATH, result)
    write_json_atomic(
        DATA_ROOT / "benchmark_annotations.json",
        annotations,
    )
    REPORT_PATH.write_text(_report_markdown(result), encoding="utf-8")
    ERROR_ANALYSIS_PATH.write_text(
        _error_analysis(comparison, annotations, query_dataset),
        encoding="utf-8",
    )
    engine.dispose()
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=("prepare", "index", "benchmark"),
        help="prepare papers/manifest, index the local corpus, or run retrieval comparison",
    )
    parser.add_argument(
        "--no-download",
        action="store_true",
        help="do not download PDFs (prepare command only)",
    )
    parser.add_argument(
        "--no-trace-neo4j",
        action="store_true",
        help="do not make read-only Neo4j title lookups",
    )
    args = parser.parse_args()
    if args.command == "prepare":
        manifest = prepare_corpus(download=not args.no_download)
        print(json.dumps({
            "manifest": str(MANIFEST_PATH),
            "papers": len(manifest["papers"]),
            "downloaded": sum(
                item.get("download_status") == "downloaded"
                for item in manifest["papers"]
            ),
        }, indent=2))
        return
    if args.command == "index":
        result = run_benchmark(
            download=not args.no_download,
            index=True,
            trace_neo4j=not args.no_trace_neo4j,
        )
    else:
        result = run_benchmark(
            download=not args.no_download,
            index=False,
            trace_neo4j=not args.no_trace_neo4j,
        )
    print(json.dumps({
        "benchmark_status": result["benchmark_status"],
        "results_path": str(RESULTS_PATH),
        "report_path": str(REPORT_PATH),
        "papers_indexed": result["performance"]["papers_indexed"],
        "chunks": result["performance"]["chunks"],
        "human_verified_query_count": result["human_verified_query_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
