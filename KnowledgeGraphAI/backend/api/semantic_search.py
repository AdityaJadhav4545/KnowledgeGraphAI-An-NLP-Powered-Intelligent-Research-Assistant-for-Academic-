"""Production semantic-search API over the separate FAISS index."""

from __future__ import annotations

from functools import lru_cache
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from KnowledgeGraphAI.backend.config import get_settings


router = APIRouter(prefix="/api/semantic-search", tags=["semantic search"])


class SemanticSearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=20_000)
    top_k: int = Field(default=5, ge=1, le=100)
    paper_id: Optional[int] = Field(default=None, ge=0)
    page_number: Optional[int] = Field(default=None, ge=1)
    section_title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    min_similarity: Optional[float] = Field(default=None, ge=-1.0, le=1.0)
    aggregate_by_paper: bool = False
    diversity: bool = False
    diversity_lambda: float = Field(default=0.7, ge=0.0, le=1.0)


@lru_cache(maxsize=1)
def _service() -> Any:
    # Deliberately lazy: importing/starting the API must not load the 768-dim
    # SPECTER2 model or download weights.
    from KnowledgeGraphAI.backend.services.semantic_retrieval.retrieval_service import (
        SemanticRetrievalService,
    )

    return SemanticRetrievalService()


def _search(payload: SemanticSearchRequest) -> Dict[str, Any]:
    try:
        results = _service().search(
            payload.query,
            top_k=payload.top_k,
            paper_id=payload.paper_id,
            page_number=payload.page_number,
            section_title=payload.section_title,
            min_similarity=payload.min_similarity,
            aggregate_by_paper=payload.aggregate_by_paper,
            diversity=payload.diversity,
            diversity_lambda=payload.diversity_lambda,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        # Model/index dependency failures are availability failures, not a
        # misleading empty result set.
        raise HTTPException(
            status_code=503,
            detail="Semantic retrieval is unavailable. Check model and index service health.",
        ) from exc
    return {
        "query": payload.query,
        "result_count": len(results),
        "results": results,
        "strategy": {
            "aggregate_by_paper": payload.aggregate_by_paper,
            "diversity": payload.diversity,
            "min_similarity": payload.min_similarity,
        },
    }


@router.post("")
def semantic_search(payload: SemanticSearchRequest) -> Dict[str, Any]:
    return _search(payload)


@router.get("")
def semantic_search_get(
    query: str = Query(min_length=1, max_length=20_000),
    top_k: int = Query(default=5, ge=1, le=100),
    paper_id: Optional[int] = Query(default=None, ge=0),
    page_number: Optional[int] = Query(default=None, ge=1),
    section_title: Optional[str] = Query(default=None, min_length=1, max_length=200),
    min_similarity: Optional[float] = Query(default=None, ge=-1.0, le=1.0),
    aggregate_by_paper: bool = False,
    diversity: bool = False,
    diversity_lambda: float = Query(default=0.7, ge=0.0, le=1.0),
) -> Dict[str, Any]:
    return _search(
        SemanticSearchRequest(
            query=query,
            top_k=top_k,
            paper_id=paper_id,
            page_number=page_number,
            section_title=section_title,
            min_similarity=min_similarity,
            aggregate_by_paper=aggregate_by_paper,
            diversity=diversity,
            diversity_lambda=diversity_lambda,
        )
    )


@router.get("/status")
async def semantic_search_status() -> Dict[str, Any]:
    """Expose only non-sensitive production-index metadata."""

    try:
        service = _service()
        return {
            "available": True,
            "indexed_chunk_count": service.vector_store.count,
            "embedding_dimension": service.config.embedding_dimension,
            "index_name": service.config.index_name,
        }
    except Exception:
        # Do not leak local paths, model cache paths, or stack details.
        return {
            "available": False,
            "indexed_chunk_count": 0,
            "embedding_dimension": get_settings() and 768,
        }
