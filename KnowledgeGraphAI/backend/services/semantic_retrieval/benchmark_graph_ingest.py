"""Ingest the isolated arXiv benchmark into Neo4j through project NLP services."""

import argparse
import json
import logging
from pathlib import Path
from time import perf_counter
from typing import Any, Dict, List

from sqlalchemy import or_

from KnowledgeGraphAI.backend.database import SessionLocal, engine, init_db
from KnowledgeGraphAI.backend.nlp.ner.entity_schema import ExtractedSentence
from KnowledgeGraphAI.backend.nlp.ner.ner_pipeline import NERPipeline
from KnowledgeGraphAI.backend.nlp.preprocessing.pipeline import NLPProcessingPipeline
from KnowledgeGraphAI.backend.nlp.relation_extraction.relation_extraction_service import (
    ScientificRelationExtractionService,
)
from KnowledgeGraphAI.backend.services.knowledge_graph.graph_construction import (
    GraphConstructionService,
)
from KnowledgeGraphAI.backend.services.knowledge_graph.graph_query import GraphQueryService
from KnowledgeGraphAI.backend.services.knowledge_graph.neo4j_connection import (
    get_neo4j_manager,
)
from KnowledgeGraphAI.backend.services.pdf_ingestion import PDFIngestionService
from KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_corpus import (
    BENCHMARK_ROOT,
    MANIFEST_PATH,
    load_manifest,
    write_json_atomic,
)
from KnowledgeGraphAI.models.paper import Paper


logger = logging.getLogger(__name__)
INGEST_REPORT = BENCHMARK_ROOT / "benchmark_graph_ingest.json"


def _register_canonical_paper(paper: Dict[str, Any], pdf_path: Path) -> int:
    file_hash = PDFIngestionService.compute_sha256(str(pdf_path))
    content_hash = PDFIngestionService.compute_content_hash(str(pdf_path))
    extracted = PDFIngestionService.extract_pdf_data(str(pdf_path))
    with SessionLocal() as db:
        rows = db.query(Paper).filter(
            or_(Paper.file_hash == file_hash, Paper.content_hash == content_hash)
        ).all()
        unique_rows = {row.id: row for row in rows}
        if len(unique_rows) > 1:
            raise RuntimeError(
                f"Multiple canonical SQL papers match hashes for arXiv:{paper['arxiv_id']}"
            )
        if unique_rows:
            existing = next(iter(unique_rows.values()))
            return int(existing.id)

        authors = paper.get("authors") or []
        record = Paper(
            title=paper["title"],
            author=", ".join(authors) if authors else extracted.get("author", ""),
            file_path=str(pdf_path.resolve()),
            file_hash=file_hash,
            content_hash=content_hash,
            page_count=extracted["page_count"],
            metadata_json={
                "source": "arXiv",
                "arxiv_id": paper["arxiv_id"],
                "source_url": paper["source_url"],
                "benchmark_dataset": "phase4.3-arxiv-pilot-v1",
                "benchmark_pdf_path": str(pdf_path.resolve()),
            },
            status="uploaded",
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return int(record.id)


def _graph_paper_records(manager: Any, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    return manager.execute_query(
        """
        MATCH (p:Paper)
        WHERE p.paper_id = $paper_id
           OR p.arxiv_id = $arxiv_id
           OR p.file_hash = $file_hash
           OR p.content_hash = $content_hash
           OR toLower(p.title) = toLower($title)
        RETURN p.paper_id AS paper_id, p.title AS title, p.arxiv_id AS arxiv_id,
               p.file_hash AS file_hash, p.content_hash AS content_hash
        LIMIT 5
        """,
        metadata,
    )


def _snapshot(manager: Any, paper_id: int) -> Dict[str, Any]:
    paper = manager.execute_query(
        "MATCH (p:Paper {paper_id: $paper_id}) "
        "RETURN p.paper_id AS paper_id, p.title AS title, p.arxiv_id AS arxiv_id, "
        "p.file_hash AS file_hash",
        {"paper_id": paper_id},
    )
    entities = manager.execute_query(
        """
        MATCH (p:Paper {paper_id: $paper_id})-[r:CONTAINS_ENTITY]->(e)
        RETURN e.entity_id AS entity_id, e.canonical_name AS canonical_name,
               e.occurrence_count AS occurrence_count,
               r.paper_id AS paper_id, r.page_number AS page_number,
               r.sentence_id AS sentence_id, r.start_char AS start_char,
               r.end_char AS end_char, r.original_text AS original_text,
               r.cleaned_text AS cleaned_text, r.evidence AS evidence
        ORDER BY entity_id
        """,
        {"paper_id": paper_id},
    )
    relations = manager.execute_query(
        """
        MATCH (s)-[r]->(o)
        WHERE r.paper_id = $paper_id AND type(r) <> 'CONTAINS_ENTITY'
        RETURN s.entity_id AS subject_id, s.canonical_name AS subject,
               type(r) AS relationship_type, o.entity_id AS object_id,
               o.canonical_name AS object, r.confidence AS confidence,
               r.paper_id AS paper_id, r.page_number AS page_number,
               r.sentence_id AS sentence_id, r.start_char AS start_char,
               r.end_char AS end_char, r.original_text AS original_text,
               r.cleaned_text AS cleaned_text, r.evidence AS evidence
        ORDER BY relationship_type, subject_id, object_id
        """,
        {"paper_id": paper_id},
    )
    authors = manager.execute_query(
        """
        MATCH (a:Author)-[r:AUTHORED]->(p:Paper {paper_id: $paper_id})
        RETURN a.author_id AS author_id, a.name AS name, r.order AS order
        ORDER BY order
        """,
        {"paper_id": paper_id},
    )
    return {
        "paper": paper,
        "entities": entities,
        "relationships": relations,
        "authors": authors,
    }


def _counts(manager: Any) -> Dict[str, int]:
    records = manager.execute_query(
        """
        CALL () {
            MATCH (n)
            RETURN count(n) AS nodes
        }
        CALL () {
            MATCH ()-[r]->()
            RETURN count(r) AS relationships
        }
        RETURN nodes, relationships
        """
    )
    if len(records) != 1:
        raise RuntimeError("Neo4j graph count query returned an invalid result")
    return records[0]


def _process_pdf(
    paper: Dict[str, Any],
    canonical_id: int,
    pdf_path: Path,
) -> Dict[str, Any]:
    extraction = PDFIngestionService.extract_pdf_data(str(pdf_path), paper_id=canonical_id)
    if not extraction.get("has_extractable_text"):
        raise ValueError(f"PDF has no extractable text: {pdf_path}")

    preprocessing = NLPProcessingPipeline(canonical_id, str(pdf_path)).process()
    sentences = [
        ExtractedSentence(**sentence)
        for paragraph in preprocessing["paragraphs"]
        for sentence in paragraph["sentences"]
    ]
    if not sentences:
        raise ValueError("preprocessing produced no sentences")

    ner_pipeline = NERPipeline()
    entity_batch = ner_pipeline.extract_paper(sentences)
    entities = entity_batch.entities
    for entity in entities:
        if (
            entity.paper_id != canonical_id
            or not entity.original_text
            or not entity.cleaned_text
            or entity.page_number < 1
            or entity.start_char < 0
            or entity.end_char <= entity.start_char
            or entity.end_char > len(entity.cleaned_text)
            or entity.cleaned_text[entity.start_char:entity.end_char] != entity.text
        ):
            raise ValueError(
                f"NER entity provenance is incomplete for {entity.entity_type}:{entity.text}"
            )

    cleaned_text = " ".join(sentence.cleaned_text for sentence in sentences)
    relation_service = ScientificRelationExtractionService(
        use_relabel=False,
        use_classifier=False,
    )
    extracted_relations = relation_service.extract_relations(
        cleaned_text, entities, sentences, canonical_id
    )
    relations = [relation.to_dict() for relation in extracted_relations]
    for relation in relations:
        original = relation["original_text"]
        cleaned = relation["cleaned_text"]
        subject = relation["subject"]
        object_ = relation["object"]
        if (
            relation["paper_id"] != canonical_id
            or not original
            or not cleaned
            or not relation.get("evidence")
            or relation["evidence"] != cleaned
            or not original.strip()
            or not cleaned.strip()
            or not (
                cleaned[subject["start"]:subject["end"]] == subject["text"]
                or subject["text"] in cleaned
            )
            or not (
                cleaned[object_["start"]:object_["end"]] == object_["text"]
                or object_["text"] in cleaned
            )
        ):
            raise ValueError(
                f"relation provenance is incomplete for {relation.get('relation')}"
            )

    author = ", ".join(paper.get("authors") or [])
    construction = GraphConstructionService()
    metadata = {
        "paper_id": canonical_id,
        "arxiv_id": paper["arxiv_id"],
        "title": paper["title"],
        "author": author,
        "file_path": str(pdf_path.resolve()),
        "file_hash": PDFIngestionService.compute_sha256(str(pdf_path)),
        "content_hash": PDFIngestionService.compute_content_hash(str(pdf_path)),
        "page_count": extraction["page_count"],
        "status": "processed",
    }
    return {
        "metadata": metadata,
        "entities": entities,
        "relations": relations,
        "construction": construction,
        "extraction": extraction,
        "sentence_count": len(sentences),
        "ner_entity_count": len(entities),
        "relation_count": len(relations),
        "ner_distribution": ner_pipeline.stats["entity_distribution"],
    }


def ingest_benchmark_graph(
    manifest_path: Path = MANIFEST_PATH,
    *,
    report_path: Path = INGEST_REPORT,
) -> Dict[str, Any]:
    if engine.dialect.name != "sqlite":
        raise RuntimeError(
            "Benchmark graph ingestion is restricted to the configured SQLite "
            "application store; PostgreSQL and other SQL stores will not be modified."
        )
    manifest = load_manifest(manifest_path)
    manager = get_neo4j_manager()
    if not manager.connect():
        health = manager.health_check()
        raise RuntimeError(f"Neo4j is unavailable: {health.get('error', health)}")

    init_db()
    counts_before = _counts(manager)
    query_service = GraphQueryService()
    paper_reports: List[Dict[str, Any]] = []
    for paper in manifest["papers"]:
        pdf_path = BENCHMARK_ROOT / paper["local_pdf_path"]
        if not pdf_path.is_file():
            paper_reports.append({
                "arxiv_id": paper["arxiv_id"],
                "status": "failed",
                "error": f"PDF is missing: {pdf_path}",
            })
            continue

        started = perf_counter()
        try:
            canonical_id = _register_canonical_paper(paper, pdf_path)
            if canonical_id == int(paper["benchmark_paper_id"]):
                raise RuntimeError(
                    "canonical SQL paper ID collides with benchmark-local ID"
                )
            processed = _process_pdf(paper, canonical_id, pdf_path)
            graph_metadata = processed["metadata"]
            existing = _graph_paper_records(manager, graph_metadata)
            if existing:
                if (
                    len(existing) != 1
                    or existing[0]["paper_id"] != canonical_id
                    or existing[0]["file_hash"] != graph_metadata["file_hash"]
                    or existing[0]["title"] != graph_metadata["title"]
                ):
                    raise RuntimeError(
                        "A conflicting Neo4j Paper record already exists; refusing "
                        f"to modify it: {existing}"
                    )

            first = processed["construction"].build_graph_for_paper(
                graph_metadata, processed["entities"], processed["relations"]
            )
            if first["errors"]:
                raise RuntimeError(f"Graph construction failed: {first['errors']}")
            before_retry = _snapshot(manager, canonical_id)
            if len(before_retry["paper"]) != 1:
                raise RuntimeError("Paper node was not persisted exactly once")
            expected_entities: Dict[str, List[Any]] = {}
            for entity in processed["entities"]:
                entity_id = processed["construction"]._generate_entity_id(
                    entity.text, entity.entity_type
                )
                expected_entities.setdefault(entity_id, []).append(entity)
            for persisted in before_retry["entities"]:
                candidates = expected_entities.get(persisted["entity_id"], [])
                if not any(
                    candidate.paper_id == persisted["paper_id"] == canonical_id
                    and candidate.page_number == persisted["page_number"]
                    and candidate.sentence_index == persisted["sentence_id"]
                    and candidate.start_char == persisted["start_char"]
                    and candidate.end_char == persisted["end_char"]
                    and candidate.original_text == persisted["original_text"]
                    and candidate.cleaned_text == persisted["cleaned_text"]
                    and candidate.source_text == persisted["evidence"]
                    for candidate in candidates
                ):
                    raise RuntimeError(
                        f"Stored CONTAINS_ENTITY provenance mismatch: {persisted}"
                    )

            expected_relations: Dict[tuple, List[Dict[str, Any]]] = {}
            for relation in processed["relations"]:
                key = (
                    processed["construction"]._generate_entity_id(
                        relation["subject"]["text"],
                        relation["subject"]["label"],
                    ),
                    relation["relation"],
                    processed["construction"]._generate_entity_id(
                        relation["object"]["text"],
                        relation["object"]["label"],
                    ),
                )
                expected_relations.setdefault(key, []).append(relation)
            for persisted in before_retry["relationships"]:
                key = (
                    persisted["subject_id"],
                    persisted["relationship_type"],
                    persisted["object_id"],
                )
                candidates = expected_relations.get(key, [])
                if not any(
                    candidate["paper_id"] == persisted["paper_id"] == canonical_id
                    and candidate["page_number"] == persisted["page_number"]
                    and candidate["sentence_id"] == persisted["sentence_id"]
                    and min(
                        candidate["subject"]["start"],
                        candidate["object"]["start"],
                    ) == persisted["start_char"]
                    and max(
                        candidate["subject"]["end"],
                        candidate["object"]["end"],
                    ) == persisted["end_char"]
                    and candidate["original_text"] == persisted["original_text"]
                    and candidate["cleaned_text"] == persisted["cleaned_text"]
                    and candidate["evidence"] == persisted["evidence"]
                    for candidate in candidates
                ):
                    raise RuntimeError(
                        f"Stored relation provenance mismatch: {persisted}"
                    )

            second = processed["construction"].build_graph_for_paper(
                graph_metadata, processed["entities"], processed["relations"]
            )
            if second["errors"]:
                raise RuntimeError(f"Repeated graph construction failed: {second['errors']}")
            after_retry = _snapshot(manager, canonical_id)
            if before_retry != after_retry:
                raise RuntimeError(
                    "Repeated ingestion changed persisted node, relationship, "
                    "occurrence, or provenance data"
                )

            paper_entities = query_service.get_paper_entities(canonical_id)
            paper_relationships = query_service.get_paper_relationships(canonical_id)
            if len(paper_entities) != len(after_retry["entities"]):
                raise RuntimeError("GraphQueryService entity retrieval count mismatch")
            if len(paper_relationships) != len(after_retry["relationships"]):
                raise RuntimeError("GraphQueryService relationship retrieval count mismatch")
            if any(
                not entity.get("original_text")
                or not entity.get("cleaned_text")
                or entity.get("paper_id") != canonical_id
                for entity in paper_entities
            ):
                raise RuntimeError("Paper entity query did not retain provenance")
            if any(
                not relation.get("original_text")
                or not relation.get("cleaned_text")
                or relation.get("paper_id") != canonical_id
                for relation in paper_relationships
            ):
                raise RuntimeError("Paper relationship query did not retain provenance")

            paper["canonical_neo4j_paper_id"] = canonical_id
            paper["graph_ingest_status"] = (
                "indexed_with_entities"
                if processed["entities"]
                else "paper_only_no_entities"
            )
            paper["graph_entity_count"] = len(after_retry["entities"])
            paper["graph_relationship_count"] = len(after_retry["relationships"])
            paper["graph_ingest_error"] = None
            paper_reports.append({
                "arxiv_id": paper["arxiv_id"],
                "canonical_paper_id": canonical_id,
                "title": graph_metadata["title"],
                "status": paper["graph_ingest_status"],
                "page_count": processed["extraction"]["page_count"],
                "sentence_count": processed["sentence_count"],
                "ner_entity_count": processed["ner_entity_count"],
                "persisted_entity_count": len(after_retry["entities"]),
                "extracted_relation_count": processed["relation_count"],
                "persisted_relationship_count": len(after_retry["relationships"]),
                "graph_query_entity_count": len(paper_entities),
                "graph_query_relationship_count": len(paper_relationships),
                "idempotency_verified": True,
                "provenance_verified": True,
                "entity_types": sorted({
                    entity.entity_type for entity in processed["entities"]
                }),
                "relationship_types": sorted({
                    relation["relation"] for relation in processed["relations"]
                }),
                "warnings": first.get("warnings", []),
                "elapsed_seconds": perf_counter() - started,
            })
        except Exception as exc:
            paper["graph_ingest_status"] = "failed"
            paper["graph_ingest_error"] = f"{type(exc).__name__}: {exc}"
            paper_reports.append({
                "arxiv_id": paper["arxiv_id"],
                "canonical_paper_id": paper.get("canonical_neo4j_paper_id"),
                "status": "failed",
                "error": paper["graph_ingest_error"],
                "elapsed_seconds": perf_counter() - started,
            })
        write_json_atomic(manifest_path, manifest)

    counts_after = _counts(manager)
    report = {
        "generated_utc": datetime_now_utc(),
        "neo4j_database": manager.database,
        "sql_dialect": engine.dialect.name,
        "counts_before": counts_before,
        "counts_after": counts_after,
        "papers": paper_reports,
        "papers_succeeded": sum(item["status"] != "failed" for item in paper_reports),
        "papers_failed": sum(item["status"] == "failed" for item in paper_reports),
        "graph_mutations_are_scoped_to_benchmark_papers": True,
        "postgresql_modified": False,
    }
    write_json_atomic(report_path, report)
    return report


def datetime_now_utc() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=INGEST_REPORT)
    args = parser.parse_args()
    report = ingest_benchmark_graph(report_path=args.report)
    print(json.dumps({
        "counts_before": report["counts_before"],
        "counts_after": report["counts_after"],
        "papers_succeeded": report["papers_succeeded"],
        "papers_failed": report["papers_failed"],
        "report": str(args.report),
    }, indent=2))


if __name__ == "__main__":
    main()
