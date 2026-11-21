"""Liveness and readiness endpoints that do not disclose configuration."""

from __future__ import annotations

import logging
from typing import Any, Dict

from fastapi import APIRouter, Response, status
from sqlalchemy import text

from KnowledgeGraphAI.backend.config import get_settings
from KnowledgeGraphAI.backend.database import SessionLocal
from KnowledgeGraphAI.backend.services.knowledge_graph.neo4j_connection import (
    neo4j_manager,
)


logger = logging.getLogger(__name__)
router = APIRouter(tags=["health"])


def _database_available() -> bool:
    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
        return True
    except Exception:
        logger.exception("Database health check failed")
        return False


def service_status() -> Dict[str, Any]:
    settings = get_settings()
    database_ok = _database_available()
    try:
        neo4j_ok = neo4j_manager.is_available()
    except Exception:
        neo4j_ok = False
    # The production FAISS metadata count is intentionally not used as a claim
    # that embeddings/models are available; it only signals indexed content.
    semantic_indexed = False
    try:
        from KnowledgeGraphAI.models.semantic_chunk import SemanticChunkRecord

        with SessionLocal() as session:
            semantic_indexed = session.query(SemanticChunkRecord).count() > 0
    except Exception:
        semantic_indexed = False
    ready = database_ok and (
        not settings.neo4j_required or neo4j_ok
    ) and (
        not settings.semantic_required or semantic_indexed
    )
    return {
        "status": "ok" if database_ok else "unhealthy",
        "ready": ready,
        "service": "KnowledgeGraph AI Backend",
        "database_available": database_ok,
        "neo4j_available": neo4j_ok,
        "semantic_indexed": semantic_indexed,
        "required_services": {
            "neo4j": settings.neo4j_required,
            "semantic_retrieval": settings.semantic_required,
        },
    }


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Liveness endpoint; inspect ``ready`` before routing write traffic."""

    return service_status()


@router.get("/ready")
async def readiness_check(response: Response) -> Dict[str, Any]:
    """Return HTTP 503 whenever a configured required dependency is absent."""

    payload = service_status()
    if not payload["ready"]:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return payload
