"""Reproducible information-retrieval metrics for labeled search queries."""

import math
from typing import Any, Callable, Dict, Iterable, List, Optional, Set


def retrieval_metrics(
    retrieved_ids: Iterable[str],
    relevant_ids: Iterable[str],
    k: int,
) -> Dict[str, Optional[float]]:
    """Calculate Precision@K, Recall@K, reciprocal rank, and AP@K.

    Duplicate retrieved IDs count only once. Precision uses ``k`` as its
    denominator, including when fewer than ``k`` results were returned.
    """
    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer")
    relevant: Set[str] = set(relevant_ids)

    unique_retrieved: List[str] = []
    seen = set()
    for item in retrieved_ids:
        if item not in seen:
            unique_retrieved.append(item)
            seen.add(item)

    top_ids = unique_retrieved[:k]
    relevant_ranks = [
        rank
        for rank, item in enumerate(top_ids, start=1)
        if item in relevant
    ]
    precision = len(relevant_ranks) / k
    recall = len(relevant_ranks) / len(relevant) if relevant else None
    reciprocal_rank = (
        1.0 / relevant_ranks[0] if relevant_ranks and relevant else None
    )
    average_precision = (
        sum(index / rank for index, rank in enumerate(relevant_ranks, start=1))
        / len(relevant)
        if relevant else None
    )
    return {
        f"precision@{k}": precision,
        f"recall@{k}": recall,
        "reciprocal_rank": reciprocal_rank,
        f"average_precision@{k}": average_precision,
    }


def ndcg_at_k(
    retrieved_ids: Iterable[str],
    relevance_grades: Dict[str, int],
    k: int,
) -> float:
    """Compute graded nDCG@K over explicitly judged IDs only."""
    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer")
    if any(
        isinstance(grade, bool) or not isinstance(grade, int) or grade < 0
        for grade in relevance_grades.values()
    ):
        raise ValueError("relevance grades must be non-negative integers")
    ranked = []
    seen = set()
    for item in retrieved_ids:
        if item in relevance_grades and item not in seen:
            ranked.append(item)
            seen.add(item)
            if len(ranked) == k:
                break
    dcg = sum(
        (2 ** relevance_grades[item] - 1) / math.log2(rank + 1)
        for rank, item in enumerate(ranked, start=1)
    )
    ideal = sorted(relevance_grades.values(), reverse=True)[:k]
    idcg = sum(
        (2 ** grade - 1) / math.log2(rank + 1)
        for rank, grade in enumerate(ideal, start=1)
    )
    return dcg / idcg if idcg else 0.0


def evaluate_dataset(
    dataset: Dict[str, Any],
    search: Callable[[str, int], Iterable[Dict[str, Any]]],
    k: int,
) -> Dict[str, Any]:
    """Evaluate labeled queries and preserve the dataset's label provenance."""
    label_type = dataset.get("label_type")
    if label_type not in {"synthetic", "human_annotated"}:
        raise ValueError("label_type must be synthetic or human_annotated")
    queries = dataset.get("queries")
    if not isinstance(queries, list) or not queries:
        raise ValueError("dataset must contain a non-empty queries list")

    per_query = []
    for query_data in queries:
        results = list(search(query_data["query"], k))
        metrics = retrieval_metrics(
            (result["chunk_id"] for result in results),
            query_data["relevant_chunk_ids"],
            k,
        )
        per_query.append({
            "query": query_data["query"],
            "retrieved_chunk_ids": [result["chunk_id"] for result in results],
            "metrics": metrics,
        })

    metric_names = per_query[0]["metrics"]
    aggregate = {}
    for name in metric_names:
        values = [
            item["metrics"][name]
            for item in per_query
            if item["metrics"][name] is not None
        ]
        aggregate[name] = sum(values) / len(values) if values else None
        aggregate[f"{name}_eligible_query_count"] = len(values)
    aggregate[f"mean_average_precision@{k}"] = aggregate.pop(
        f"average_precision@{k}"
    )
    return {
        "label_type": label_type,
        "dataset_description": dataset.get("description", ""),
        "query_count": len(per_query),
        "k": k,
        "aggregate": aggregate,
        "per_query": per_query,
    }
