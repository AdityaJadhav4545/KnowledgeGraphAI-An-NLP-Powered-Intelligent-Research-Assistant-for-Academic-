"""Safe, parameterized API for the existing Neo4j knowledge graph."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from KnowledgeGraphAI.backend.api.security import require_write_access
from KnowledgeGraphAI.backend.database import get_db
from KnowledgeGraphAI.backend.nlp.ner.entity_schema import ExtractedEntity
from KnowledgeGraphAI.backend.nlp.relation_extraction.relation_schema import ExtractedRelation
from KnowledgeGraphAI.backend.services.knowledge_graph.graph_construction import (
    GraphConstructionService,
)
from KnowledgeGraphAI.backend.services.knowledge_graph.graph_query import GraphQueryService
from KnowledgeGraphAI.backend.services.knowledge_graph.neo4j_connection import (
    get_neo4j_manager,
)
from KnowledgeGraphAI.models.paper import Paper


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/graph", tags=["graph"])


def _load_metadata_list(value: Any) -> List[Dict[str, Any]]:
    if value is None:
        return []
    decoded = json.loads(value) if isinstance(value, str) else value
    if not isinstance(decoded, list):
        raise ValueError("Expected graph metadata to contain a list")
    return [item for item in decoded if isinstance(item, dict)]


def _get_paper_or_404(paper_id: int, db: Session) -> Paper:
    paper = db.query(Paper).filter(Paper.id == paper_id, Paper.status != "archived").first()
    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found.")
    return paper


def _rehydrate(paper: Paper) -> tuple[List[ExtractedEntity], List[ExtractedRelation]]:
    metadata = paper.metadata_json or {}
    entities: List[ExtractedEntity] = []
    relations: List[ExtractedRelation] = []
    try:
        entity_data = _load_metadata_list(metadata.get("entities"))
        relation_data = _load_metadata_list(metadata.get("relations"))
    except (ValueError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=422, detail="Stored extraction metadata is invalid.") from exc
    for item in entity_data:
        try:
            entities.append(
                ExtractedEntity(
                    text=str(item.get("text", "")),
                    entity_type=str(item.get("entity_type", "")),
                    start_char=int(item.get("start_char", item.get("start", 0))),
                    end_char=int(item.get("end_char", item.get("end", 0))),
                    confidence=float(item.get("confidence", 0.5)),
                    paper_id=paper.id,
                    page_number=int(item.get("page_number", 0)),
                    sentence_index=int(item.get("sentence_index", 0)),
                    source_text=str(item.get("source_text", "")),
                    extraction_method=str(item.get("extraction_method", "rule_based")),
                    original_text=item.get("original_text"),
                    cleaned_text=item.get("cleaned_text"),
                )
            )
        except (TypeError, ValueError):
            logger.warning("Skipping malformed entity metadata for paper id=%s", paper.id)
    for item in relation_data:
        subject = item.get("subject") or {}
        object_ = item.get("object") or {}
        try:
            relations.append(
                ExtractedRelation(
                    relation=str(item.get("relation", "")),
                    subject_entity_id=str(item.get("subject_entity_id", "")),
                    subject_text=str(item.get("subject_text", subject.get("text", ""))),
                    subject_start=int(item.get("subject_start", subject.get("start", 0))),
                    subject_end=int(item.get("subject_end", subject.get("end", 0))),
                    subject_entity_type=str(item.get("subject_entity_type", subject.get("label", ""))),
                    object_entity_id=str(item.get("object_entity_id", "")),
                    object_text=str(item.get("object_text", object_.get("text", ""))),
                    object_start=int(item.get("object_start", object_.get("start", 0))),
                    object_end=int(item.get("object_end", object_.get("end", 0))),
                    object_entity_type=str(item.get("object_entity_type", object_.get("label", ""))),
                    confidence=float(item.get("confidence", 0.5)),
                    paper_id=paper.id,
                    sentence_id=int(item.get("sentence_id", 0)),
                    page_number=int(item.get("page_number", 0)),
                    evidence=str(item.get("evidence", "")),
                    extraction_method=str(item.get("extraction_method", "rule_based")),
                    original_text=item.get("original_text"),
                    cleaned_text=item.get("cleaned_text"),
                )
            )
        except (TypeError, ValueError):
            logger.warning("Skipping malformed relation metadata for paper id=%s", paper.id)
    return entities, relations


def _require_graph() -> Any:
    manager = get_neo4j_manager()
    if not manager.is_available():
        raise HTTPException(status_code=503, detail="Neo4j is unavailable.")
    return manager


def _build(paper: Paper) -> Dict[str, Any]:
    _require_graph()
    entities, relations = _rehydrate(paper)
    result = GraphConstructionService().build_graph_for_paper(
        {
            "paper_id": paper.id,
            "title": paper.title or "Untitled",
            "author": paper.author or "Unknown",
            # Graph provenance keeps a filename, never a local filesystem path.
            "file_path": Path(paper.file_path).name if paper.file_path else "",
            "file_hash": paper.file_hash,
            "content_hash": paper.content_hash,
            "page_count": paper.page_count or 0,
            "status": paper.status,
        },
        entities,
        relations,
    )
    if result.get("errors"):
        raise HTTPException(status_code=500, detail="Graph construction failed.")
    return result


@router.get("/health")
async def graph_health() -> Dict[str, Any]:
    manager = get_neo4j_manager()
    available = manager.is_available()
    return {
        "status": "ok" if available else "degraded",
        "neo4j_available": available,
        "neo4j_message": "Connected" if available else "Neo4j unavailable",
    }


@router.get("/stats")
@router.get("/analytics")
async def graph_stats() -> Dict[str, Any]:
    _require_graph()
    from KnowledgeGraphAI.backend.services.knowledge_graph.graph_analytics import GraphAnalytics

    return {"statistics": GraphAnalytics().get_stats()}


@router.get("/paper/{paper_id}")
async def paper_graph(paper_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    paper = _get_paper_or_404(paper_id, db)
    graph = GraphQueryService()
    try:
        return {
            "paper_id": paper.id,
            "paper_title": paper.title,
            "entities": graph.get_paper_entities(paper.id),
            "relationships": graph.get_paper_relationships(paper.id),
        }
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Neo4j is unavailable.") from exc


@router.get("/entity/{entity_id}")
async def entity_detail(
    entity_id: str,
    entity_type: str = Query(default="Model", min_length=1, max_length=50),
) -> Dict[str, Any]:
    try:
        detail = GraphQueryService().get_entity_details(entity_id, entity_type)
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=400, detail="Invalid graph entity query.") from exc
    if not detail:
        raise HTTPException(status_code=404, detail="Entity not found.")
    return detail


@router.get("/entity/{entity_id}/neighbors")
async def entity_neighbors(
    entity_id: str,
    entity_type: str = Query(default="Model", min_length=1, max_length=50),
    limit: int = Query(default=50, ge=1, le=200),
) -> Dict[str, Any]:
    try:
        neighbors = GraphQueryService().get_entity_neighbors(
            entity_id, entity_type, limit=limit
        )
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=400, detail="Invalid graph neighbor query.") from exc
    return {"entity_id": entity_id, "neighbors": neighbors}


@router.get("/search")
async def graph_search(
    query: str = Query(default="", max_length=500),
    entity_types: Optional[List[str]] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
) -> Dict[str, Any]:
    graph = GraphQueryService()
    try:
        return {
            "entities": graph.search_entities(query, entity_types, limit),
            "papers": graph.search_papers(query, limit),
        }
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=400, detail="Invalid graph search.") from exc


@router.get("/relationships/{paper_id}")
async def paper_relationships(paper_id: int) -> Dict[str, Any]:
    try:
        relations = GraphQueryService().get_paper_relationships(paper_id)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail="Neo4j is unavailable.") from exc
    return {"paper_id": paper_id, "relationships": relations}


@router.get("/path")
async def graph_path(
    source_id: str = Query(min_length=1, max_length=100),
    target_id: str = Query(min_length=1, max_length=100),
    max_depth: int = Query(default=4, ge=1, le=10),
) -> Dict[str, Any]:
    try:
        path = GraphQueryService().find_path_between_entities(source_id, target_id, max_depth=max_depth)
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=400, detail="Invalid graph path query.") from exc
    return {"source_id": source_id, "target_id": target_id, "path": path}


@router.post("/build/{paper_id}")
@router.post("/rebuild/{paper_id}")
async def build_graph(
    paper_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_write_access),
) -> Dict[str, Any]:
    paper = _get_paper_or_404(paper_id, db)
    result = _build(paper)
    return {"status": "graph_built", "paper_id": paper.id, "stats": result}


@router.get("/papers/using-entity")
async def papers_using_entity(
    entity_name: str = Query(min_length=1, max_length=300),
    limit: int = Query(default=50, ge=1, le=200),
) -> Dict[str, Any]:
    """Find papers using/mentioning a named method, model, or entity."""

    manager = _require_graph()
    rows = manager.execute_query(
        """
        MATCH (p:Paper)-[:CONTAINS_ENTITY]->(e)
        WHERE toLower(coalesce(e.canonical_name, e.name, '')) CONTAINS toLower($entity_name)
        RETURN DISTINCT p.paper_id AS paper_id, p.title AS title, p.author AS author,
               labels(e) AS entity_types, e.canonical_name AS matched_entity
        ORDER BY p.title
        LIMIT $limit
        """,
        {"entity_name": entity_name, "limit": limit},
    )
    return {"papers": rows}


@router.get("/papers/evaluating-dataset")
async def papers_evaluating_dataset(
    dataset_name: str = Query(min_length=1, max_length=300),
    limit: int = Query(default=50, ge=1, le=200),
) -> Dict[str, Any]:
    manager = _require_graph()
    rows = manager.execute_query(
        """
        MATCH (p:Paper)-[:CONTAINS_ENTITY]->(m:Model)-[r:EVALUATED_ON]->(d:Dataset)
        WHERE toLower(d.canonical_name) CONTAINS toLower($dataset_name)
        RETURN DISTINCT p.paper_id AS paper_id, p.title AS title, m.canonical_name AS model,
               d.canonical_name AS dataset, r.confidence AS confidence, r.evidence AS evidence
        ORDER BY r.confidence DESC
        LIMIT $limit
        """,
        {"dataset_name": dataset_name, "limit": limit},
    )
    return {"papers": rows}


@router.get("/methods/by-task")
async def methods_by_task(
    task_name: str = Query(min_length=1, max_length=300),
    limit: int = Query(default=50, ge=1, le=200),
) -> Dict[str, Any]:
    manager = _require_graph()
    rows = manager.execute_query(
        """
        MATCH (m)-[r:PROPOSES|APPLIES_TO]->(t:Task)
        WHERE toLower(t.canonical_name) CONTAINS toLower($task_name)
        RETURN DISTINCT m.canonical_name AS method, labels(m) AS method_types,
               t.canonical_name AS task, r.confidence AS confidence, r.paper_id AS paper_id
        ORDER BY r.confidence DESC
        LIMIT $limit
        """,
        {"task_name": task_name, "limit": limit},
    )
    return {"methods": rows}


@router.get("/papers/by-metric")
async def papers_by_metric(
    metric_name: str = Query(min_length=1, max_length=300),
    limit: int = Query(default=50, ge=1, le=200),
) -> Dict[str, Any]:
    manager = _require_graph()
    rows = manager.execute_query(
        """
        MATCH (p:Paper)-[:CONTAINS_ENTITY]->(m:Model)-[r:ACHIEVES]->(metric:Metric)
        WHERE toLower(metric.canonical_name) CONTAINS toLower($metric_name)
        RETURN DISTINCT p.paper_id AS paper_id, p.title AS title, m.canonical_name AS model,
               metric.canonical_name AS metric, r.confidence AS confidence, r.evidence AS evidence
        ORDER BY r.confidence DESC
        LIMIT $limit
        """,
        {"metric_name": metric_name, "limit": limit},
    )
    return {"papers": rows}


@router.get("/connections")
async def paper_connections(
    source_paper_id: int = Query(ge=1),
    target_paper_id: int = Query(ge=1),
    limit: int = Query(default=100, ge=1, le=500),
) -> Dict[str, Any]:
    manager = _require_graph()
    rows = manager.execute_query(
        """
        MATCH (a:Paper {paper_id: $source_paper_id})-[:CONTAINS_ENTITY]->(e)<-[:CONTAINS_ENTITY]-(b:Paper {paper_id: $target_paper_id})
        RETURN e.entity_id AS entity_id, e.canonical_name AS shared_entity, labels(e) AS entity_types
        LIMIT $limit
        """,
        {"source_paper_id": source_paper_id, "target_paper_id": target_paper_id, "limit": limit},
    )
    return {"source_paper_id": source_paper_id, "target_paper_id": target_paper_id, "connections": rows}


@router.post("/schema/initialize")
async def initialize_graph_schema(_: None = Depends(require_write_access)) -> Dict[str, Any]:
    """Add missing Neo4j constraints/indexes without reset or recreation."""

    manager = _require_graph()
    from KnowledgeGraphAI.backend.services.knowledge_graph.graph_schema import (
        CONSTRAINT_STATEMENTS,
        INDEX_STATEMENTS,
    )

    applied = 0
    failures: List[str] = []
    for statement in [*CONSTRAINT_STATEMENTS, *INDEX_STATEMENTS]:
        try:
            manager.execute_write(statement)
            applied += 1
        except Exception as exc:
            # Continue to identify existing-data conflicts without changing or
            # deleting data.  Details remain in server logs.
            logger.warning("Graph schema statement failed: %s", exc)
            failures.append("A schema statement could not be applied; inspect server logs.")
    return {"applied_statement_count": applied, "failure_count": len(failures), "failures": failures}
