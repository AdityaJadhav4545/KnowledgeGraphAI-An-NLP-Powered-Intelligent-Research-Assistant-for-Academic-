"""Coordinated, stateful paper-processing workflow.

This module is the single integration point for PDF extraction, preprocessing,
scientific NER and relations, Neo4j construction, and production semantic
indexing.  It deliberately records each transition before work begins and
never marks a paper complete after an essential stage has failed.
"""

from __future__ import annotations

import json
import logging
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from sqlalchemy.orm import Session

from KnowledgeGraphAI.backend.config import Settings, get_settings
from KnowledgeGraphAI.backend.nlp.ner.entity_schema import ExtractedSentence
from KnowledgeGraphAI.backend.nlp.ner.ner_pipeline import NERPipeline
from KnowledgeGraphAI.backend.nlp.preprocessing.pipeline import NLPProcessingPipeline
from KnowledgeGraphAI.backend.nlp.relation_extraction.relation_extraction_service import (
    extract_relations_from_paper,
)
from KnowledgeGraphAI.backend.services.pdf_ingestion import PDFIngestionService
from KnowledgeGraphAI.models.paper import Paper


logger = logging.getLogger(__name__)


PROCESSING_STATES = frozenset(
    {
        "uploaded",
        "extracting",
        "preprocessing",
        "extracting_entities",
        "extracting_relations",
        "graph_indexing",
        "completed",
        "failed",
        "archived",
    }
)
ACTIVE_PROCESSING_STATES = frozenset(PROCESSING_STATES - {"uploaded", "completed", "failed", "archived"})


class PaperProcessingError(RuntimeError):
    """A failed stage with a safe, user-facing summary."""

    def __init__(self, stage: str, message: str) -> None:
        self.stage = stage
        self.safe_message = message
        super().__init__(f"{stage}: {message}")


def _utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _json_safe_error(exc: Exception) -> str:
    """Keep status errors useful without leaking absolute local paths."""

    message = str(exc).replace("\\", "/")
    root = str(get_settings().upload_dir.parent.parent).replace("\\", "/")
    if root and root in message:
        message = message.replace(root, "[project]")
    return message[:1000] or exc.__class__.__name__


class PaperProcessingService:
    """Execute the real ingestion pipeline for one persisted ``Paper``."""

    def __init__(
        self,
        db: Session,
        *,
        settings: Optional[Settings] = None,
        graph_service_factory: Any = None,
        semantic_service_factory: Any = None,
    ) -> None:
        self.db = db
        self.settings = settings or get_settings()
        self._graph_service_factory = graph_service_factory
        self._semantic_service_factory = semantic_service_factory

    @staticmethod
    def _metadata(paper: Paper) -> Dict[str, Any]:
        return dict(paper.metadata_json or {})

    def _transition(
        self,
        paper: Paper,
        state: str,
        *,
        stage: Optional[str] = None,
        error: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        if state not in PROCESSING_STATES:
            raise ValueError(f"Unsupported processing state: {state}")
        metadata = self._metadata(paper)
        events = list(metadata.get("processing_events") or [])
        events.append(
            {
                "state": state,
                "stage": stage or state,
                "at": _utc_now().isoformat() + "Z",
                "error": error,
            }
        )
        # Keep status metadata bounded while retaining recent audit context.
        metadata["processing_events"] = events[-50:]
        if extra:
            metadata.update(extra)
        paper.metadata_json = metadata
        paper.status = state
        paper.updated_at = _utc_now()
        if state == "extracting":
            paper.processing_started_at = _utc_now()
            paper.processing_completed_at = None
            paper.processing_error = None
        if state == "completed":
            paper.processing_completed_at = _utc_now()
            paper.processing_error = None
        if state == "failed":
            paper.processing_error = error or "Processing failed"
        self.db.add(paper)
        self.db.commit()
        self.db.refresh(paper)

    def _write_artifact(self, paper: Paper, payload: Dict[str, Any]) -> Path:
        """Persist an atomically-written processing artifact outside the DB."""

        self.settings.processed_dir.mkdir(parents=True, exist_ok=True)
        identifier = paper.content_hash or f"paper-{paper.id}"
        target = self.settings.processed_dir / f"{identifier}.pipeline.json"
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f"{identifier}.", suffix=".tmp", dir=self.settings.processed_dir
        )
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                json.dump(payload, stream, ensure_ascii=False, indent=2)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary_name, target)
        except Exception:
            try:
                os.unlink(temporary_name)
            except FileNotFoundError:
                pass
            raise
        return target

    @staticmethod
    def _sentences(preprocessing: Dict[str, Any]) -> List[ExtractedSentence]:
        sentences: List[ExtractedSentence] = []
        for paragraph in preprocessing.get("paragraphs", []):
            for sentence in paragraph.get("sentences", []):
                sentences.append(
                    ExtractedSentence(
                        paper_id=int(sentence.get("paper_id", preprocessing["paper_id"])),
                        page_number=int(sentence.get("page_number", 0)),
                        section_name=str(sentence.get("section_name", "UNKNOWN")),
                        paragraph_index=int(sentence.get("paragraph_index", 0)),
                        sentence_index=int(sentence.get("sentence_index", 0)),
                        original_text=str(sentence.get("original_text", "")),
                        cleaned_text=str(sentence.get("cleaned_text", "")),
                    )
                )
        return sentences

    def _graph_service(self) -> Any:
        if self._graph_service_factory is not None:
            return self._graph_service_factory()
        from KnowledgeGraphAI.backend.services.knowledge_graph.graph_construction import (
            GraphConstructionService,
        )

        return GraphConstructionService()

    def _semantic_service(self) -> Any:
        if self._semantic_service_factory is not None:
            return self._semantic_service_factory()
        from KnowledgeGraphAI.backend.services.semantic_retrieval.retrieval_service import (
            SemanticRetrievalService,
        )

        return SemanticRetrievalService()

    def _fail(self, paper: Paper, stage: str, exc: Exception) -> None:
        message = _json_safe_error(exc)
        logger.exception("Paper %s failed at %s", paper.id, stage)
        self._transition(paper, "failed", stage=stage, error=message)

    def process(self, paper: Paper, *, force: bool = False) -> Dict[str, Any]:
        """Run all essential stages and return verified stage counts.

        ``force`` permits a deliberate retry of a completed/failed record.  The
        graph and vector stores are idempotent on canonical identifiers, so a
        retry updates rather than appends duplicate records.
        """

        if paper.status == "archived":
            raise PaperProcessingError("validation", "Archived papers cannot be processed")
        if paper.status in ACTIVE_PROCESSING_STATES:
            raise PaperProcessingError("validation", "Paper is already being processed")
        if paper.status == "completed" and not force:
            metadata = self._metadata(paper)
            return {
                "paper_id": paper.id,
                "status": "completed",
                "already_completed": True,
                "entity_count": metadata.get("entity_count", 0),
                "relation_count": metadata.get("relation_count", 0),
                "semantic_chunk_count": metadata.get("semantic_chunk_count", 0),
            }
        if not paper.file_path or not Path(paper.file_path).is_file():
            self._fail(paper, "validation", FileNotFoundError("Source PDF is unavailable"))
            raise PaperProcessingError("validation", "Source PDF is unavailable")

        try:
            self._transition(paper, "extracting")
            original_name = (paper.metadata_json or {}).get("original_filename")
            extracted = PDFIngestionService.extract_pdf_data(
                paper.file_path,
                paper_id=paper.id,
                fallback_title=original_name or paper.title,
            )
            if not extracted.get("has_extractable_text"):
                raise PaperProcessingError(
                    "extracting", "The PDF has no extractable text; OCR is required"
                )
            paper.title = extracted.get("title") or paper.title
            paper.author = extracted.get("author") or paper.author
            paper.page_count = extracted.get("page_count")
            self.db.commit()

            self._transition(paper, "preprocessing")
            preprocessing = NLPProcessingPipeline(paper.id, paper.file_path).process()
            sentences = self._sentences(preprocessing)
            if not sentences:
                raise PaperProcessingError("preprocessing", "No sentences were extracted")

            self._transition(paper, "extracting_entities")
            ner = NERPipeline(use_transformer=False)
            entity_batch = ner.extract_paper(sentences)
            entities = entity_batch.entities
            entity_dicts = [entity.to_dict() for entity in entities]

            self._transition(paper, "extracting_relations")
            full_text = "\n".join(
                str(page.get("text") or "") for page in extracted.get("pages", [])
            )
            relations = extract_relations_from_paper(
                full_text,
                entities,
                sentences,
                paper.id,
                # Explicitly choose the implemented baseline.  This is not
                # represented as transformer/REBEL inference in metadata.
                use_relabel=False,
                use_rebel=False,
                use_classifier=False,
            )
            relation_dicts = [relation.to_dict() for relation in relations]

            artifact = self._write_artifact(
                paper,
                {
                    "paper_id": paper.id,
                    "extracted": extracted,
                    "preprocessing": preprocessing,
                    "entities": entity_dicts,
                    "relations": relation_dicts,
                },
            )
            metadata = self._metadata(paper)
            metadata.update(
                {
                    "pipeline_version": "3.0",
                    "pipeline_artifact": artifact.name,
                    "is_scanned": bool(extracted.get("is_scanned")),
                    "entity_count": len(entity_dicts),
                    "entity_distribution": ner.get_stats().get("entity_distribution", {}),
                    "entities": entity_dicts,
                    "relation_count": len(relation_dicts),
                    "relations": relation_dicts,
                    "relation_extraction_method": "rule_based",
                }
            )
            paper.metadata_json = metadata
            self.db.commit()

            self._transition(paper, "graph_indexing")
            graph = self._graph_service()
            graph_result = graph.build_graph_for_paper(
                {
                    "paper_id": paper.id,
                    "title": paper.title or "Untitled",
                    "author": paper.author or "Unknown",
                    # Graph provenance uses a non-sensitive filename; the
                    # absolute upload location is never exposed in Neo4j/API.
                    "file_path": Path(paper.file_path).name,
                    "file_hash": paper.file_hash,
                    "content_hash": paper.content_hash,
                    "page_count": paper.page_count or 0,
                    "status": "graph_indexing",
                },
                entities,
                relation_dicts,
            )
            if graph_result.get("errors"):
                if self.settings.neo4j_required:
                    raise PaperProcessingError(
                        "graph_indexing", "; ".join(str(item) for item in graph_result["errors"])
                    )
                logger.warning(
                    "Graph indexing omitted for paper %s (Neo4j not required): %s",
                    paper.id,
                    "; ".join(str(item) for item in graph_result["errors"]),
                )

            # Semantic indexing is performed only after graph processing;
            # paper_id identity is preserved across all stores.
            pages = {
                int(page["page_number"]): str(page.get("text") or "")
                for page in extracted.get("pages", [])
                if page.get("page_number") is not None
            }
            semantic = self._semantic_service()
            chunks = semantic.index_preprocessed(
                preprocessing,
                Path(paper.file_path).name,
                page_texts=pages,
                paper_title=paper.title,
                validate_graph=self.settings.neo4j_required,
                source_identifier=paper.content_hash,
            )
            if not chunks:
                raise PaperProcessingError("semantic_indexing", "No semantic chunks were indexed")

            metadata = self._metadata(paper)
            metadata.update(
                {
                    "graph_stats": graph_result,
                    "semantic_chunk_count": len(chunks),
                    "semantic_index_name": getattr(getattr(semantic, "config", None), "index_name", None),
                }
            )
            paper.metadata_json = metadata
            self.db.commit()
            self._transition(paper, "completed", stage="completed")
            return {
                "paper_id": paper.id,
                "status": "completed",
                "entity_count": len(entity_dicts),
                "relation_count": len(relation_dicts),
                "semantic_chunk_count": len(chunks),
                "graph_stats": graph_result,
            }
        except PaperProcessingError as exc:
            self._fail(paper, exc.stage, exc)
            raise
        except Exception as exc:
            # Derive the last recorded state as the failed stage.
            current = paper.status if paper.status in PROCESSING_STATES else "unknown"
            self._fail(paper, current, exc)
            raise PaperProcessingError(current, _json_safe_error(exc)) from exc
