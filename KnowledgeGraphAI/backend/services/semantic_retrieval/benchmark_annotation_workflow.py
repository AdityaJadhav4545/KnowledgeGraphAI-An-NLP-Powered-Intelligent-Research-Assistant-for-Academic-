"""Generate reviewer worksheets and import completed human judgments."""

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_corpus import (
    BENCHMARK_ROOT,
    validate_annotations,
    validate_manifest,
    validate_query_dataset,
)


PROJECT_ROOT = Path(__file__).resolve().parents[4]
QUERY_PATH = Path(__file__).with_name("benchmark_queries.json")
RESULTS_PATH = PROJECT_ROOT / "KnowledgeGraphAI" / "reports" / "semantic_retrieval" / "benchmark_results.json"
PAPER_WORKSHEET = BENCHMARK_ROOT / "paper_judgments.csv"
CHUNK_WORKSHEET = BENCHMARK_ROOT / "chunk_judgments.csv"
REVIEW_REPORT = PROJECT_ROOT / "KnowledgeGraphAI" / "reports" / "semantic_retrieval" / "annotation_review.md"
ANNOTATION_PATH = BENCHMARK_ROOT / "benchmark_annotations.json"

PAPER_FIELDS = (
    "query_id",
    "query_text",
    "benchmark_paper_id",
    "arxiv_id",
    "title",
    "abstract",
    "source_url",
    "retrieved_by",
    "relevance_judgment",
    "grade_0_to_3",
    "reviewer",
    "reviewed_at",
    "independent_review_attested",
    "review_notes",
    "automated_label",
    "automated_confidence",
    "automated_explanation",
    "automated_model",
    "automated_generated_at",
    "automated_suggestion_history",
    "human_label",
    "verification_method",
)
CHUNK_FIELDS = (
    "query_id",
    "query_text",
    "benchmark_paper_id",
    "arxiv_id",
    "title",
    "abstract",
    "page_number",
    "section_title",
    "source_document",
    "source_identifier",
    "chunk_id",
    "retrieval_hits",
    "passage_text",
    "relevance_judgment",
    "grade_0_to_3",
    "reviewer",
    "reviewed_at",
    "independent_review_attested",
    "review_notes",
    "automated_label",
    "automated_confidence",
    "automated_explanation",
    "automated_model",
    "automated_generated_at",
    "automated_suggestion_history",
    "human_label",
    "verification_method",
)
ASSISTED_ANNOTATION_FIELDS = (
    "automated_label",
    "automated_confidence",
    "automated_explanation",
    "automated_model",
    "automated_generated_at",
    "automated_suggestion_history",
    "human_label",
    "verification_method",
)
STRATEGIES = (
    "faiss_cosine",
    "metadata_filtered_cosine",
    "paper_aggregation",
    "mmr_diversity",
)


def _write_csv_if_missing(path: Path, fields: Iterable[str], rows: List[Dict[str, Any]]) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(fields), extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)
    return True


def build_review_package(
    manifest: Dict[str, Any],
    queries: Dict[str, Any],
    results: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], str]:
    validate_manifest(manifest)
    validate_query_dataset(queries)
    if results.get("dataset_version") != manifest.get("dataset_version"):
        raise ValueError("benchmark results and manifest dataset versions differ")

    paper_by_id = {
        str(paper["benchmark_paper_id"]): paper for paper in manifest["papers"]
    }
    paper_rows: List[Dict[str, Any]] = []
    chunk_rows: List[Dict[str, Any]] = []
    report_lines = [
        "# Independent Relevance Annotation Review",
        "",
        f"Dataset: `{manifest['dataset_version']}`",
        f"Results generated: `{results.get('generated_utc', 'unknown')}`",
        "",
        "## Reviewer instructions",
        "",
        "- Review every paper row for every query using the query, paper title, abstract, and cited source.",
        "- Review every retrieved passage in the chunk worksheet; use the PDF/source link if more context is needed.",
        "- Enter `relevant` or `not_relevant`; leave no judgment blank if marking a query complete.",
        "- Optional grade is an integer from 0 (not relevant) through 3 (highly relevant).",
        "- Fill reviewer, ISO-8601 review time, and set independent-review attestation to `yes` only if applicable.",
        "- Retrieval rank and similarity are descriptive system outputs, not relevance labels.",
        "- Do not mark a candidate relevant solely because it ranked highly.",
        "",
        "## Query worksheets",
        "",
    ]

    query_results = results.get("retrieval", {})
    for query in queries["queries"]:
        query_id = query["query_id"]
        report_lines += [
            f"### {query_id}",
            "",
            query["query_text"],
            "",
            "#### Paper-level judgments (all corpus papers)",
            "",
            "| Benchmark paper ID | arXiv ID | Title | Source | Judgment (relevant/not_relevant) | Optional grade 0-3 | Reviewer notes |",
            "|---:|---|---|---|---|---:|---|",
        ]
        strategies = query_results.get(query_id, {})
        hits_by_chunk: Dict[str, Dict[str, Any]] = {}
        for strategy in STRATEGIES:
            for rank, result in enumerate(strategies.get(strategy, {}).get("results", []), 1):
                chunk_id = str(result.get("chunk_id", ""))
                paper_id = str(result.get("paper_id", ""))
                if not chunk_id or paper_id not in paper_by_id:
                    raise ValueError(
                        f"result in {query_id}/{strategy} has unknown chunk or paper ID"
                    )
                item = hits_by_chunk.setdefault(chunk_id, {
                    "paper_id": paper_id,
                    "result": result,
                    "hits": [],
                })
                if item["paper_id"] != paper_id:
                    raise ValueError(f"chunk {chunk_id} maps to multiple papers")
                item["hits"].append({
                    "strategy": strategy,
                    "rank": rank,
                    "similarity_score": result.get("similarity_score"),
                    "reranking_score": result.get("reranking_score"),
                })

        for paper in manifest["papers"]:
            paper_id = str(paper["benchmark_paper_id"])
            markdown_title = paper["title"].replace("|", "\\|")
            paper_rows.append({
                "query_id": query_id,
                "query_text": query["query_text"],
                "benchmark_paper_id": paper["benchmark_paper_id"],
                "arxiv_id": paper["arxiv_id"],
                "title": paper["title"],
                "abstract": paper["abstract"],
                "source_url": paper["source_url"],
                "retrieved_by": ";".join(
                    strategy
                    for strategy in STRATEGIES
                    if any(
                        hit["strategy"] == strategy
                        for item in hits_by_chunk.values()
                        if item["paper_id"] == paper_id
                        for hit in item["hits"]
                    )
                ),
                "relevance_judgment": "",
                "grade_0_to_3": "",
                "reviewer": "",
                "reviewed_at": "",
                "independent_review_attested": "",
                "review_notes": "",
                **{field: "" for field in ASSISTED_ANNOTATION_FIELDS},
            })
            report_lines += [
                f"| {paper['benchmark_paper_id']} | {paper['arxiv_id']} | "
                f"{markdown_title} | [arXiv]({paper['source_url']}) |  |  |  |",
                "",
                f"**Abstract — {paper['title']}**",
                "",
                paper["abstract"],
                "",
            ]

        report_lines += [
            "#### Retrieved passages",
            "",
            "Scores/ranks below are for review context only. Each unique passage is shown once; its occurrences across strategies are listed.",
            "",
        ]
        for chunk_id, grouped in hits_by_chunk.items():
            item = grouped["result"]
            paper = paper_by_id[grouped["paper_id"]]
            row = {
                "query_id": query_id,
                "query_text": query["query_text"],
                "benchmark_paper_id": paper["benchmark_paper_id"],
                "arxiv_id": paper["arxiv_id"],
                "title": paper["title"],
                "abstract": paper["abstract"],
                "page_number": item.get("page_number", ""),
                "section_title": item.get("section_title", ""),
                "source_document": item.get("source_document", ""),
                "source_identifier": item.get("source_identifier", ""),
                "chunk_id": chunk_id,
                "retrieval_hits": json.dumps(grouped["hits"], ensure_ascii=False),
                "passage_text": item.get("text", ""),
                "relevance_judgment": "",
                "grade_0_to_3": "",
                "reviewer": "",
                "reviewed_at": "",
                "independent_review_attested": "",
                "review_notes": "",
                **{field: "" for field in ASSISTED_ANNOTATION_FIELDS},
            }
            chunk_rows.append(row)
            hit_text = "; ".join(
                f"{hit['strategy']} rank {hit['rank']} similarity "
                f"{hit['similarity_score']} rerank {hit['reranking_score']}"
                for hit in grouped["hits"]
            )
            report_lines += [
                f"**[{paper['title']}]({paper['source_url']})** — arXiv:{paper['arxiv_id']}, "
                f"page {row['page_number']}, section {row['section_title']}",
                "",
                f"Chunk `{chunk_id}`; source `{row['source_identifier']}`; {hit_text}",
                "",
                "> " + row["passage_text"].replace("\n", "\n> "),
                "",
                "Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________",
                "",
            ]
        report_lines += ["---", ""]

    return paper_rows, chunk_rows, "\n".join(report_lines)


def prepare_review_package(
    manifest_path: Path = BENCHMARK_ROOT / "benchmark_manifest.json",
    query_path: Path = QUERY_PATH,
    results_path: Path = RESULTS_PATH,
    *,
    refresh_report: bool = False,
) -> Dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    queries = json.loads(query_path.read_text(encoding="utf-8"))
    results = json.loads(results_path.read_text(encoding="utf-8"))
    paper_rows, chunk_rows, report = build_review_package(manifest, queries, results)
    created = {
        "paper_worksheet": _write_csv_if_missing(PAPER_WORKSHEET, PAPER_FIELDS, paper_rows),
        "chunk_worksheet": _write_csv_if_missing(CHUNK_WORKSHEET, CHUNK_FIELDS, chunk_rows),
        "review_report": False,
    }
    if refresh_report or not REVIEW_REPORT.exists():
        REVIEW_REPORT.parent.mkdir(parents=True, exist_ok=True)
        REVIEW_REPORT.write_text(report, encoding="utf-8")
        created["review_report"] = True
    return {
        "query_count": len(queries["queries"]),
        "paper_judgment_rows": len(paper_rows),
        "retrieved_chunk_judgment_rows": len(chunk_rows),
        "created": created,
        "paths": {
            "paper_worksheet": str(PAPER_WORKSHEET),
            "chunk_worksheet": str(CHUNK_WORKSHEET),
            "review_report": str(REVIEW_REPORT),
        },
    }


def _read_rows(path: Path, expected_fields: Iterable[str]) -> List[Dict[str, str]]:
    expected = tuple(expected_fields)
    optional_assisted_fields = set(ASSISTED_ANNOTATION_FIELDS)
    with path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        missing = set(expected) - optional_assisted_fields - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path.name} is missing columns: {sorted(missing)}")
        rows = list(reader)
    for row in rows:
        for field in optional_assisted_fields:
            row.setdefault(field, "")
        if not row.get("human_label"):
            row["human_label"] = row.get("relevance_judgment", "")
        if row.get("human_label") and not row.get("verification_method"):
            row["verification_method"] = "manual_legacy"
    return rows


def _parse_label(row: Dict[str, str], context: str) -> Tuple[str, Optional[int]]:
    label = (row.get("human_label") or "").strip().lower()
    compatibility_label = (row.get("relevance_judgment") or "").strip().lower()
    if label and compatibility_label and label != compatibility_label:
        raise ValueError(f"{context}: human_label conflicts with relevance_judgment")
    label = label or compatibility_label
    if label not in {"relevant", "not_relevant"}:
        raise ValueError(f"{context}: relevance_judgment must be relevant or not_relevant")
    raw_grade = (row.get("grade_0_to_3") or "").strip()
    grade = None
    if raw_grade:
        try:
            grade = int(raw_grade)
        except ValueError as exc:
            raise ValueError(f"{context}: grade_0_to_3 must be an integer from 0 to 3") from exc
        if not 0 <= grade <= 3:
            raise ValueError(f"{context}: grade_0_to_3 must be an integer from 0 to 3")
        if (grade > 0) != (label == "relevant"):
            raise ValueError(f"{context}: grade conflicts with relevance_judgment")
    return label, grade


def import_human_annotations(
    paper_csv: Path,
    chunk_csv: Path,
    annotation_path: Path,
    manifest: Dict[str, Any],
    queries: Dict[str, Any],
    results: Dict[str, Any],
) -> Dict[str, Any]:
    paper_rows = _read_rows(paper_csv, PAPER_FIELDS)
    chunk_rows = _read_rows(chunk_csv, CHUNK_FIELDS)
    papers_by_id = {str(item["benchmark_paper_id"]): item for item in manifest["papers"]}
    query_by_id = {item["query_id"]: item for item in queries["queries"]}
    expected_paper_pairs = {
        (query_id, paper_id)
        for query_id in query_by_id
        for paper_id in papers_by_id
    }
    seen_paper_pairs = set()
    paper_judgments: Dict[str, Dict[str, Any]] = {query_id: {} for query_id in query_by_id}
    expected_paper_rows, expected_chunk_rows, _ = build_review_package(
        manifest, queries, results
    )
    expected_paper_data = {
        (row["query_id"], str(row["benchmark_paper_id"])): row
        for row in expected_paper_rows
    }
    for row in paper_rows:
        query_id = row.get("query_id", "")
        paper_id = row.get("benchmark_paper_id", "")
        key = (query_id, paper_id)
        if key not in expected_paper_pairs or key in seen_paper_pairs:
            raise ValueError(f"unexpected or duplicate paper judgment row: {key}")
        source = expected_paper_data[key]
        for field in ("query_text", "arxiv_id", "title", "abstract", "source_url"):
            if row.get(field) != source[field]:
                raise ValueError(f"{query_id}/{paper_id}: source field {field} was changed")
        seen_paper_pairs.add(key)
        label, grade = _parse_label(row, f"{query_id}/{paper_id}")
        paper_judgments[query_id][paper_id] = (label, grade, row)
    if seen_paper_pairs != expected_paper_pairs:
        raise ValueError("paper worksheet must contain exactly one judgment per query and corpus paper")

    expected_chunks = {
        (row["query_id"], row["chunk_id"]) for row in expected_chunk_rows
    }
    observed_chunks = {
        (row.get("query_id", ""), row.get("chunk_id", "")) for row in chunk_rows
    }
    if len(observed_chunks) != len(chunk_rows):
        raise ValueError("chunk worksheet contains duplicate query/chunk rows")
    if observed_chunks != expected_chunks:
        raise ValueError(
            "chunk worksheet must contain exactly the retrieved candidate chunks "
            "from the current benchmark results"
        )
    expected_chunk_data = {
        (row["query_id"], row["chunk_id"]): row for row in expected_chunk_rows
    }
    chunk_judgments: Dict[str, Dict[str, Any]] = {query_id: {} for query_id in query_by_id}
    for row in chunk_rows:
        query_id = row.get("query_id", "")
        chunk_id = row.get("chunk_id", "")
        if query_id not in query_by_id or not chunk_id:
            raise ValueError(f"unexpected chunk judgment row: {query_id}/{chunk_id}")
        source = expected_chunk_data[(query_id, chunk_id)]
        for field in (
            "query_text",
            "benchmark_paper_id",
            "arxiv_id",
            "title",
            "abstract",
            "page_number",
            "section_title",
            "source_document",
            "source_identifier",
            "retrieval_hits",
            "passage_text",
        ):
            if row.get(field) != str(source[field]) and row.get(field) != source[field]:
                raise ValueError(f"{query_id}/{chunk_id}: source field {field} was changed")
        label, grade = _parse_label(row, f"{query_id}/{chunk_id}")
        chunk_judgments[query_id][chunk_id] = (label, grade, row)

    template = json.loads(annotation_path.read_text(encoding="utf-8"))
    entries = []
    for query_id, query in query_by_id.items():
        paper_records = paper_judgments[query_id]
        chunk_records = chunk_judgments[query_id]
        all_records = list(paper_records.values()) + list(chunk_records.values())
        reviewers = {
            row.get("reviewer", "").strip()
            for _label, _grade, row in all_records
        }
        if "" in reviewers:
            raise ValueError(f"{query_id}: reviewer is required on every row")
        if not reviewers:
            raise ValueError(f"{query_id}: at least one reviewer is required")
        review_times = []
        verification_methods = set()
        for _label, _grade, row in all_records:
            raw_reviewed_at = row.get("reviewed_at", "").strip()
            if not raw_reviewed_at:
                raise ValueError(f"{query_id}: reviewed_at is required on every row")
            try:
                parsed_time = datetime.fromisoformat(
                    raw_reviewed_at.replace("Z", "+00:00")
                )
                if parsed_time.tzinfo is None:
                    raise ValueError("timezone is required")
            except ValueError as exc:
                raise ValueError(f"{query_id}: reviewed_at must be ISO-8601") from exc
            review_times.append(parsed_time.astimezone(timezone.utc))
            verification_method = (
                row.get("verification_method", "").strip() or "manual_legacy"
            )
            if verification_method not in {
                "manual",
                "bulk_confirmed",
                "manual_legacy",
            }:
                raise ValueError(
                    f"{query_id}: invalid human verification_method "
                    f"{verification_method!r}"
                )
            verification_methods.add(verification_method)
        reviewed_at = max(review_times).isoformat()
        independent_attested = all(
            (row.get("independent_review_attested") or "").strip().lower() == "yes"
            for _label, _grade, row in all_records
        )

        relevant_papers = [
            int(paper_id)
            for paper_id, (label, _grade, _row) in paper_records.items()
            if label == "relevant"
        ]
        paper_grades = {
            paper_id: grade
            for paper_id, (_label, grade, _row) in paper_records.items()
            if grade is not None
        }
        relevant_chunks = [
            chunk_id
            for chunk_id, (label, _grade, _row) in chunk_records.items()
            if label == "relevant"
        ]
        chunk_grades = {
            chunk_id: grade
            for chunk_id, (_label, grade, _row) in chunk_records.items()
            if grade is not None
        }
        notes = [
            row["review_notes"].strip()
            for _label, _grade, row in list(paper_records.values()) + list(chunk_records.values())
            if row.get("review_notes", "").strip()
        ]
        old_entry = next(
            entry for entry in template["queries"] if entry["query_id"] == query_id
        )
        entries.append({
            **old_entry,
            "query_text": query["query_text"],
            "judgment_status": "human_verified",
            "judged_paper_ids": sorted(int(value) for value in paper_records),
            "unjudged_paper_ids": [],
            "relevant_paper_ids": sorted(relevant_papers),
            "paper_relevance_grades": paper_grades,
            "judged_chunk_ids": sorted(chunk_records),
            "relevant_chunk_ids": sorted(relevant_chunks),
            "chunk_relevance_grades": chunk_grades,
            "annotation_source": (
                "independent_human_review"
                if independent_attested
                else "human_review_with_model_assistance"
                if "bulk_confirmed" in verification_methods
                else "human_review"
            ),
            "annotator": "; ".join(sorted(reviewers)),
            "annotators": sorted(reviewers),
            "reviewed_at": reviewed_at,
            "independent_review_attested": independent_attested,
            "verification_method": (
                "bulk_confirmed"
                if "bulk_confirmed" in verification_methods
                else "manual"
            ),
            "annotation_notes": " | ".join(notes) or "No additional reviewer notes.",
        })

    updated = {**template, "queries": entries, "updated_utc": datetime.now(timezone.utc).isoformat()}
    validate_annotations(
        updated,
        query_by_id,
        (paper["benchmark_paper_id"] for paper in manifest["papers"]),
        (row["chunk_id"] for row in chunk_rows),
    )
    temporary = annotation_path.with_suffix(annotation_path.suffix + ".tmp")
    temporary.write_text(json.dumps(updated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(annotation_path)
    return {
        "query_count": len(entries),
        "human_verified_query_count": sum(
            entry["judgment_status"] == "human_verified" for entry in entries
        ),
        "paper_judgment_rows": len(paper_rows),
        "chunk_judgment_rows": len(chunk_rows),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "import"))
    parser.add_argument("--paper-csv", type=Path, default=PAPER_WORKSHEET)
    parser.add_argument("--chunk-csv", type=Path, default=CHUNK_WORKSHEET)
    parser.add_argument(
        "--refresh-report",
        action="store_true",
        help="regenerate only the Markdown report; never overwrite judgment CSVs",
    )
    args = parser.parse_args()
    if args.command == "prepare":
        outcome = prepare_review_package(refresh_report=args.refresh_report)
    else:
        manifest = json.loads((BENCHMARK_ROOT / "benchmark_manifest.json").read_text(encoding="utf-8"))
        queries = json.loads(QUERY_PATH.read_text(encoding="utf-8"))
        outcome = import_human_annotations(
            args.paper_csv,
            args.chunk_csv,
            ANNOTATION_PATH,
            manifest,
            queries,
            json.loads(RESULTS_PATH.read_text(encoding="utf-8")),
        )
    print(json.dumps(outcome, indent=2))


if __name__ == "__main__":
    main()
