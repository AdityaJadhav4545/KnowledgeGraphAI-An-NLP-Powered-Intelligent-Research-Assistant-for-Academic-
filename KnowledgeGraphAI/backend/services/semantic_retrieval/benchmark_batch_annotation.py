"""Resumable, opt-in Ollama suggestions for Phase 4.3 benchmark candidates."""

import argparse
import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

from KnowledgeGraphAI.backend.services.semantic_retrieval.annotation_dashboard import (
    CHUNK_KEY_FIELDS,
    CHUNK_WORKSHEET,
    PAPER_KEY_FIELDS,
    PAPER_WORKSHEET,
    load_worksheet,
    save_suggestions,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.assisted_annotation import (
    suggest_relevance,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_annotation_workflow import (
    CHUNK_FIELDS,
    PAPER_FIELDS,
    QUERY_PATH,
)


PROJECT_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_CHECKPOINT_PATH = (
    PROJECT_ROOT
    / "KnowledgeGraphAI"
    / "data"
    / "benchmark"
    / "automated_annotation_checkpoint.json"
)


def _atomic_json_write(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(dict(payload), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def _input_digest(
    query: str, title: str, abstract: str, passage: Optional[str]
) -> str:
    value = json.dumps(
        {
            "query": query,
            "title": title,
            "abstract": abstract,
            "passage": passage or "",
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _load_checkpoint(path: Path, model: str) -> Dict[str, Any]:
    if not path.exists():
        return {
            "schema_version": 1,
            "model": model,
            "updated_utc": datetime.now(timezone.utc).isoformat(),
            "records": {},
        }
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("records"), dict):
        raise ValueError(f"invalid annotation checkpoint: {path}")
    data.setdefault("model", model)
    return data


def _checkpoint_key(
    annotation_type: str, query_id: str, candidate_id: str, model: str
) -> str:
    return "|".join((model, annotation_type, query_id, candidate_id))


def _specification(annotation_type: str, worksheet_path: Optional[Path] = None):
    if annotation_type == "paper":
        return (
            worksheet_path or PAPER_WORKSHEET,
            PAPER_FIELDS,
            PAPER_KEY_FIELDS,
            "benchmark_paper_id",
        )
    if annotation_type == "chunk":
        return worksheet_path or CHUNK_WORKSHEET, CHUNK_FIELDS, CHUNK_KEY_FIELDS, "chunk_id"
    raise ValueError(f"unsupported annotation_type: {annotation_type}")


def _suggestion_update(
    query_id: str,
    candidate_id: str,
    annotation_type: str,
    suggestion: Mapping[str, Any],
) -> Dict[str, Any]:
    update = {
        "query_id": query_id,
        "candidate_id": candidate_id,
        "annotation_type": annotation_type,
        "label": suggestion["label"],
        "confidence": suggestion["confidence"],
        "explanation": suggestion["explanation"],
        "model": suggestion["model"],
        "generated_at": suggestion.get(
            "generated_at", datetime.now(timezone.utc).isoformat()
        ),
    }
    update[
        "benchmark_paper_id" if annotation_type == "paper" else "chunk_id"
    ] = candidate_id
    return update


def _run_worksheet(
    annotation_type: str,
    *,
    worksheet_path: Path,
    query_by_id: Mapping[str, str],
    checkpoint: Dict[str, Any],
    checkpoint_path: Path,
    model: str,
    base_url: Optional[str],
    timeout_seconds: float,
    max_retries: int,
    rate_limit_seconds: float,
    batch_size: int,
    query_id_filter: Optional[str],
    candidate_ids: Optional[set[str]],
    limit: Optional[int],
    force: bool,
    suggest: Callable[..., Dict[str, Any]],
    progress: Optional[Callable[[Mapping[str, Any]], None]],
) -> Dict[str, Any]:
    path, fields, key_fields, id_field = _specification(
        annotation_type, worksheet_path
    )
    rows, _existing_fields = load_worksheet(path, fields, key_fields)
    target_rows = [
        row for row in rows
        if (query_id_filter is None or row["query_id"] == query_id_filter)
        and (candidate_ids is None or str(row[id_field]) in candidate_ids)
    ]
    unknown_queries = sorted({
        row["query_id"] for row in target_rows if row["query_id"] not in query_by_id
    })
    if unknown_queries:
        raise ValueError(f"worksheet contains unknown query IDs: {unknown_queries}")
    for row in target_rows:
        if row["query_text"] != query_by_id[row["query_id"]]:
            raise ValueError(
                f"{annotation_type} worksheet query text differs for {row['query_id']}"
            )

    counts = {
        "candidate_count": len(target_rows),
        "generated": 0,
        "recovered_from_checkpoint": 0,
        "skipped_existing": 0,
        "skipped_limit": 0,
        "failed": 0,
        "errors": [],
    }
    pending: List[Dict[str, Any]] = []
    requests_started = 0
    max_new_requests = limit

    def persist_pending() -> None:
        if not pending:
            return
        save_suggestions(path, fields, key_fields, pending)
        for item in pending:
            record_key = _checkpoint_key(
                annotation_type,
                str(item["query_id"]),
                str(item["candidate_id"]),
                model,
            )
            checkpoint["records"][record_key]["persisted"] = True
        pending.clear()
        checkpoint["updated_utc"] = datetime.now(timezone.utc).isoformat()
        _atomic_json_write(checkpoint_path, checkpoint)

    for row_index, row in enumerate(target_rows, start=1):
        query_id = row["query_id"]
        candidate_id = str(row[id_field])
        record_key = _checkpoint_key(
            annotation_type, query_id, candidate_id, model
        )
        passage = row.get("passage_text") if annotation_type == "chunk" else None
        digest = _input_digest(
            query_by_id[query_id],
            row["title"],
            row["abstract"],
            passage,
        )
        existing_label = row.get("automated_label", "").strip()
        if existing_label and not force:
            counts["skipped_existing"] += 1
            continue

        prior = checkpoint["records"].get(record_key)
        if (
            not force
            and prior
            and prior.get("status") == "suggested"
            and prior.get("input_sha256") == digest
        ):
            suggestion = prior["suggestion"]
            pending.append(_suggestion_update(
                query_id, candidate_id, annotation_type, suggestion
            ))
            counts["recovered_from_checkpoint"] += 1
        else:
            if max_new_requests is not None and requests_started >= max_new_requests:
                counts["skipped_limit"] += len(target_rows) - row_index + 1
                break
            if requests_started and rate_limit_seconds:
                time.sleep(rate_limit_seconds)
            requests_started += 1
            try:
                suggestion = suggest(
                    query_by_id[query_id],
                    row["title"],
                    row["abstract"],
                    passage,
                    base_url=base_url,
                    model=model,
                    timeout_seconds=timeout_seconds,
                    max_retries=max_retries,
                )
                enriched = _suggestion_update(
                    query_id, candidate_id, annotation_type, suggestion
                )
                checkpoint["records"][record_key] = {
                    "status": "suggested",
                    "annotation_type": annotation_type,
                    "query_id": query_id,
                    "candidate_id": candidate_id,
                    "input_sha256": digest,
                    "suggestion": enriched,
                    "attempted_utc": datetime.now(timezone.utc).isoformat(),
                    "persisted": False,
                }
                pending.append(enriched)
                counts["generated"] += 1
            except Exception as exc:
                checkpoint["records"][record_key] = {
                    "status": "failed",
                    "annotation_type": annotation_type,
                    "query_id": query_id,
                    "candidate_id": candidate_id,
                    "input_sha256": digest,
                    "error": f"{type(exc).__name__}: {exc}",
                    "attempted_utc": datetime.now(timezone.utc).isoformat(),
                }
                counts["failed"] += 1
                counts["errors"].append({
                    "query_id": query_id,
                    "candidate_id": candidate_id,
                    "error": f"{type(exc).__name__}: {exc}",
                })

        checkpoint["updated_utc"] = datetime.now(timezone.utc).isoformat()
        _atomic_json_write(checkpoint_path, checkpoint)
        if len(pending) >= batch_size:
            persist_pending()
        if progress:
            progress({
                "annotation_type": annotation_type,
                "completed": row_index,
                "total": len(target_rows),
                **counts,
            })

    persist_pending()
    counts["requests_attempted"] = requests_started
    return counts


def run_batch_annotation(
    *,
    annotation_type: str = "both",
    query_path: Path = QUERY_PATH,
    paper_csv: Path = PAPER_WORKSHEET,
    chunk_csv: Path = CHUNK_WORKSHEET,
    checkpoint_path: Path = DEFAULT_CHECKPOINT_PATH,
    model: Optional[str] = None,
    base_url: Optional[str] = None,
    timeout_seconds: float = 120.0,
    max_retries: int = 2,
    rate_limit_seconds: float = 0.0,
    batch_size: int = 8,
    query_id: Optional[str] = None,
    candidate_ids: Optional[Sequence[str]] = None,
    limit: Optional[int] = None,
    force: bool = False,
    suggest: Callable[..., Dict[str, Any]] = suggest_relevance,
    progress: Optional[Callable[[Mapping[str, Any]], None]] = None,
) -> Dict[str, Any]:
    """Generate suggestions and checkpoint each response for safe resume."""
    if annotation_type not in {"paper", "chunk", "both"}:
        raise ValueError("annotation_type must be paper, chunk, or both")
    if batch_size < 1:
        raise ValueError("batch_size must be positive")
    if rate_limit_seconds < 0:
        raise ValueError("rate_limit_seconds must be non-negative")
    if limit is not None and limit < 1:
        raise ValueError("limit must be positive when supplied")
    model_name = (model or os.getenv("ANNOTATION_LLM_MODEL", "llama3.1")).strip()
    if not model_name:
        raise ValueError("model name cannot be empty")
    queries_data = json.loads(query_path.read_text(encoding="utf-8"))
    queries = queries_data.get("queries")
    if not isinstance(queries, list):
        raise ValueError("benchmark query dataset must contain a queries list")
    query_by_id = {
        str(item["query_id"]): str(item["query_text"])
        for item in queries
    }
    if query_id is not None and query_id not in query_by_id:
        raise ValueError(f"unknown benchmark query ID: {query_id}")

    checkpoint = _load_checkpoint(checkpoint_path, model_name)
    checkpoint["model"] = model_name
    selected_types = (
        ("paper", "chunk") if annotation_type == "both" else (annotation_type,)
    )
    outcome: Dict[str, Any] = {
        "model": model_name,
        "base_url": (
            base_url or os.getenv(
                "ANNOTATION_LLM_BASE_URL", "http://localhost:11434"
            )
        ),
        "checkpoint_path": str(checkpoint_path),
        "resumed": checkpoint_path.exists(),
        "results": {},
    }
    worksheet_by_type = {"paper": paper_csv, "chunk": chunk_csv}
    for current_type in selected_types:
        outcome["results"][current_type] = _run_worksheet(
            current_type,
            worksheet_path=worksheet_by_type[current_type],
            query_by_id=query_by_id,
            checkpoint=checkpoint,
            checkpoint_path=checkpoint_path,
            model=model_name,
            base_url=base_url,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
            rate_limit_seconds=rate_limit_seconds,
            batch_size=batch_size,
            query_id_filter=query_id,
            candidate_ids=set(candidate_ids) if candidate_ids else None,
            limit=limit,
            force=force,
            suggest=suggest,
            progress=progress,
        )
    return outcome


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--type", choices=("paper", "chunk", "both"), default="both")
    parser.add_argument("--query-id")
    parser.add_argument("--candidate-id", action="append")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--rate-limit-seconds", type=float, default=0.0)
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument("--model", default=os.getenv("ANNOTATION_LLM_MODEL", "llama3.1"))
    parser.add_argument("--base-url", default=os.getenv(
        "ANNOTATION_LLM_BASE_URL", "http://localhost:11434"
    ))
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT_PATH)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    last_failed_count = 0

    def report_progress(state: Mapping[str, Any]) -> None:
        nonlocal last_failed_count
        failed_count = int(state["failed"])
        if (
            int(state["completed"]) % args.batch_size == 0
            or state["completed"] == state["total"]
            or failed_count != last_failed_count
        ):
            print(json.dumps(dict(state), ensure_ascii=False), flush=True)
        last_failed_count = failed_count

    outcome = run_batch_annotation(
        annotation_type=args.type,
        query_id=args.query_id,
        candidate_ids=args.candidate_id,
        limit=args.limit,
        batch_size=args.batch_size,
        rate_limit_seconds=args.rate_limit_seconds,
        timeout_seconds=args.timeout_seconds,
        max_retries=args.max_retries,
        model=args.model,
        base_url=args.base_url,
        checkpoint_path=args.checkpoint,
        force=args.force,
        progress=report_progress,
    )
    print(json.dumps(outcome, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
