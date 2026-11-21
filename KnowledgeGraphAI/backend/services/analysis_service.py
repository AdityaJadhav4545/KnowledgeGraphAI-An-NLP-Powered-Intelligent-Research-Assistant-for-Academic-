"""Unified, document-isolated analysis service for PDF uploads and pasted text."""

from __future__ import annotations

import hashlib
import logging
import os
import re
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import or_
from sqlalchemy.orm import Session

from KnowledgeGraphAI.backend.config import Settings, get_settings
from KnowledgeGraphAI.backend.nlp.ner.entity_schema import ExtractedEntity, ExtractedSentence
from KnowledgeGraphAI.backend.nlp.ner.ner_pipeline import NERPipeline
from KnowledgeGraphAI.backend.nlp.preprocessing.pipeline import NLPProcessingPipeline
from KnowledgeGraphAI.backend.nlp.preprocessing.section_extractor import SectionExtractor
from KnowledgeGraphAI.backend.nlp.preprocessing.sentence_segmenter import SentenceSegmenter
from KnowledgeGraphAI.backend.nlp.preprocessing.text_cleaner import TextCleaner
from KnowledgeGraphAI.backend.nlp.relation_extraction.relation_extraction_service import (
    extract_relations_from_paper,
)
from KnowledgeGraphAI.backend.services.knowledge_graph.entity_resolution import (
    EntityResolutionService,
)
from KnowledgeGraphAI.backend.services.knowledge_graph.graph_schema import (
    get_node_label,
    validate_relationship,
)
from KnowledgeGraphAI.backend.services.pdf_ingestion import PDFIngestionService
from KnowledgeGraphAI.models.analysis import AnalysisRecord
from KnowledgeGraphAI.models.paper import Paper

logger = logging.getLogger(__name__)

MIN_TEXT_CHARS = 10
MAX_TEXT_CHARS = 200_000


class AnalysisValidationError(ValueError):
    """Raised for invalid user PDF or text input."""


class AnalysisProcessingError(RuntimeError):
    """Raised when a document analysis stage fails."""

    def __init__(self, stage: str, message: str) -> None:
        self.stage = stage
        self.safe_message = message
        super().__init__(f"{stage}: {message}")


def _utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _safe_filename(filename: Optional[str]) -> str:
    name = Path(filename or "document.pdf").name
    cleaned = "".join(ch for ch in name if ch.isprintable())[:255]
    return cleaned or "document.pdf"


def _human_error(exc: Exception) -> str:
    msg = str(exc).replace("\\", "/")
    root = str(get_settings().upload_dir.parent.parent).replace("\\", "/")
    if root and root in msg:
        msg = msg.replace(root, "[workspace]")
    return msg[:500] or exc.__class__.__name__


class DocumentAnalysisService:
    """Coordinate PDF and pasted-text analysis into isolated ``AnalysisRecord`` entries."""

    def __init__(self, db: Session, *, settings: Optional[Settings] = None) -> None:
        self.db = db
        self.settings = settings or get_settings()

    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------
    def list_analyses(self, limit: int = 50) -> List[Dict[str, Any]]:
        rows = (
            self.db.query(AnalysisRecord)
            .order_by(AnalysisRecord.created_at.desc())
            .limit(limit)
            .all()
        )
        return [self.summary_dict(row) for row in rows]

    def get_analysis(self, analysis_id: str) -> Optional[AnalysisRecord]:
        return (
            self.db.query(AnalysisRecord)
            .filter(AnalysisRecord.id == analysis_id)
            .first()
        )

    @staticmethod
    def summary_dict(record: AnalysisRecord) -> Dict[str, Any]:
        graph = record.graph_json or {}
        stats = graph.get("stats") or {}
        return {
            "analysis_id": record.id,
            "source_type": record.source_type,
            "title": record.title,
            "author": record.author,
            "publication_info": record.publication_info,
            "paper_id": record.paper_id,
            "page_count": record.page_count,
            "status": record.status,
            "stage": record.stage,
            "error_message": record.error_message,
            "entity_count": stats.get("total_entities", len(record.entities_json or [])),
            "relationship_count": stats.get("total_relationships", len(record.relationships_json or [])),
            "category_count": stats.get("category_count", 0),
            "passage_count": len(record.passages_json or []),
            "created_at": record.created_at.isoformat() if record.created_at else None,
            "updated_at": record.updated_at.isoformat() if record.updated_at else None,
        }

    @classmethod
    def detail_dict(cls, record: AnalysisRecord) -> Dict[str, Any]:
        return {
            **cls.summary_dict(record),
            "sections": record.sections_json or [],
            "passages": record.passages_json or [],
            "entities": record.entities_json or [],
            "relationships": record.relationships_json or [],
            "graph": record.graph_json or {"nodes": [], "edges": [], "stats": {}},
            "chat_history": record.chat_history_json or [],
            "report": record.report_json,
        }

    # ------------------------------------------------------------------
    # Public workflows
    # ------------------------------------------------------------------
    def analyze_pdf(
        self,
        filename: str,
        pdf_bytes: bytes,
        *,
        sync_external_stores: bool = True,
    ) -> Dict[str, Any]:
        """Validate, extract, and analyze an uploaded PDF document."""

        safe_name = _safe_filename(filename)
        if not safe_name.lower().endswith(".pdf"):
            raise AnalysisValidationError("Please upload a valid .pdf file.")
        if not pdf_bytes:
            raise AnalysisValidationError("The uploaded PDF file is empty.")
        if len(pdf_bytes) > self.settings.max_upload_bytes:
            limit_mb = self.settings.max_upload_bytes // (1024 * 1024)
            raise AnalysisValidationError(
                f"The uploaded PDF exceeds the {limit_mb} MB size limit."
            )
        if not pdf_bytes[:8].startswith(b"%PDF-"):
            raise AnalysisValidationError("The selected file does not appear to be a valid PDF.")

        self.settings.upload_dir.mkdir(parents=True, exist_ok=True)
        descriptor, temp_path = tempfile.mkstemp(
            prefix=".analysis_", suffix=".pdf", dir=self.settings.upload_dir
        )
        staging = Path(temp_path)
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(pdf_bytes)
                handle.flush()

            file_hash = PDFIngestionService.compute_sha256(str(staging))
            try:
                extracted = PDFIngestionService.extract_pdf_data(
                    str(staging), fallback_title=safe_name
                )
            except ValueError as exc:
                raise AnalysisValidationError(str(exc)) from exc

            if not extracted.get("has_extractable_text"):
                raise AnalysisValidationError(
                    "This PDF contains no extractable text (it may be a scanned image). OCR is required."
                )

            content_hash = PDFIngestionService.compute_content_hash(str(staging))
            stored_path = self.settings.upload_dir / f"{file_hash}.pdf"
            if stored_path.exists():
                staging.unlink(missing_ok=True)
            else:
                os.replace(staging, stored_path)

            # Reuse or create Paper record cleanly so production papers are preserved.
            paper = (
                self.db.query(Paper)
                .filter(
                    or_(Paper.file_hash == file_hash, Paper.content_hash == content_hash)
                )
                .first()
            )
            if paper is None:
                paper = Paper(
                    title=extracted.get("title") or safe_name,
                    author=extracted.get("author") or "Unknown",
                    file_path=str(stored_path),
                    file_hash=file_hash,
                    content_hash=content_hash,
                    page_count=extracted.get("page_count"),
                    metadata_json={
                        "original_filename": safe_name,
                        "is_scanned": bool(extracted.get("is_scanned")),
                        "has_extractable_text": True,
                        "upload_at": _utc_now().isoformat() + "Z",
                    },
                    status="uploaded",
                )
                self.db.add(paper)
                self.db.commit()
                self.db.refresh(paper)

            analysis_id = uuid.uuid4().hex[:16]
            title = extracted.get("title") or paper.title or safe_name
            author = extracted.get("author") or paper.author or None
            if author == "Unknown":
                author = None

            record = AnalysisRecord(
                id=analysis_id,
                source_type="pdf",
                title=title,
                author=author,
                publication_info=f"PDF Document ({extracted.get('page_count', 0)} pages)",
                paper_id=paper.id,
                content_hash=content_hash,
                page_count=int(extracted.get("page_count") or 0),
                status="processing",
                stage="preprocessing",
                chat_history_json=[],
            )
            self.db.add(record)
            self.db.commit()

            try:
                preprocessing = NLPProcessingPipeline(paper.id, str(stored_path)).process()
                sentences, passages, sections = self._rehydrate_from_preprocessing(
                    preprocessing, paper_id=paper.id, source_type="pdf", extracted=extracted
                )
                full_text = "\n".join(
                    str(pg.get("text") or "") for pg in extracted.get("pages", [])
                )
                entities, rel_dicts, graph_json = self._run_nlp_and_build_graph(
                    title=title,
                    author=author,
                    full_text=full_text,
                    sentences=sentences,
                    paper_id=paper.id,
                    source_type="pdf",
                )

                # Optional persistence to Neo4j + FAISS when available (never fails analysis).
                if sync_external_stores:
                    self._sync_optional_stores(
                        paper=paper,
                        extracted=extracted,
                        preprocessing=preprocessing,
                        entities=entities,
                        rel_dicts=rel_dicts,
                    )

                record.full_text = full_text
                record.passages_json = passages
                record.sections_json = sections
                record.entities_json = [e.to_dict() for e in entities]
                record.relationships_json = rel_dicts
                record.graph_json = graph_json
                record.status = "completed"
                record.stage = "completed"
                record.error_message = None
                self.db.commit()
                self.db.refresh(record)
                return self.detail_dict(record)
            except Exception as exc:
                logger.exception("PDF analysis failed id=%s", analysis_id)
                record.status = "failed"
                record.error_message = _human_error(exc)
                self.db.commit()
                raise AnalysisProcessingError(record.stage, record.error_message) from exc
        finally:
            try:
                if staging.exists():
                    staging.unlink(missing_ok=True)
            except OSError:
                pass

    def analyze_text(
        self,
        text: str,
        *,
        title: Optional[str] = None,
        author: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Validate and analyze pasted research text without external DB requirements."""

        if not isinstance(text, str) or not text.strip():
            raise AnalysisValidationError("Please paste some text before generating an analysis.")
        stripped = text.strip()
        if len(stripped) < MIN_TEXT_CHARS:
            raise AnalysisValidationError(
                f"Please enter at least {MIN_TEXT_CHARS} characters for meaningful analysis."
            )
        if len(stripped) > MAX_TEXT_CHARS:
            raise AnalysisValidationError(
                f"Pasted text exceeds the {MAX_TEXT_CHARS:,} character limit."
            )

        clean_title = (title or "").strip() or self._derive_text_title(stripped)
        clean_author = (author or "").strip() or None
        content_hash = hashlib.sha256(
            TextCleaner.normalize_whitespace(stripped).encode("utf-8")
        ).hexdigest()

        analysis_id = uuid.uuid4().hex[:16]
        record = AnalysisRecord(
            id=analysis_id,
            source_type="text",
            title=clean_title,
            author=clean_author,
            publication_info="Pasted text input",
            paper_id=None,
            content_hash=content_hash,
            page_count=0,
            status="processing",
            stage="preprocessing",
            chat_history_json=[],
        )
        self.db.add(record)
        self.db.commit()

        try:
            sentences, passages, sections, cleaned_full = self._preprocess_pasted_text(stripped)
            if not sentences:
                raise AnalysisValidationError("No readable sentences could be extracted from the text.")

            entities, rel_dicts, graph_json = self._run_nlp_and_build_graph(
                title=clean_title,
                author=clean_author,
                full_text=cleaned_full,
                sentences=sentences,
                paper_id=0,
                source_type="text",
            )

            record.full_text = stripped
            record.passages_json = passages
            record.sections_json = sections
            record.entities_json = [e.to_dict() for e in entities]
            record.relationships_json = rel_dicts
            record.graph_json = graph_json
            record.status = "completed"
            record.stage = "completed"
            record.error_message = None
            self.db.commit()
            self.db.refresh(record)
            return self.detail_dict(record)
        except AnalysisValidationError:
            record.status = "failed"
            record.error_message = "Input text did not contain extractable sentences."
            self.db.commit()
            raise
        except Exception as exc:
            logger.exception("Text analysis failed id=%s", analysis_id)
            record.status = "failed"
            record.error_message = _human_error(exc)
            self.db.commit()
            raise AnalysisProcessingError(record.stage, record.error_message) from exc

    # ------------------------------------------------------------------
    # Shared preprocessing, NER, relation, and isolated graph builders
    # ------------------------------------------------------------------
    @staticmethod
    def _derive_text_title(text: str) -> str:
        first_line = text.splitlines()[0].strip()
        if 4 <= len(first_line) <= 90 and not first_line.endswith("."):
            return first_line
        words = first_line.split()[:8]
        snippet = " ".join(words)
        return (snippet + "...") if len(first_line.split()) > 8 else (snippet or "Pasted Research Text")

    @staticmethod
    def _rehydrate_from_preprocessing(
        preprocessing: Dict[str, Any],
        *,
        paper_id: int,
        source_type: str,
        extracted: Dict[str, Any],
    ) -> Tuple[List[ExtractedSentence], List[Dict[str, Any]], List[Dict[str, Any]]]:
        sentences: List[ExtractedSentence] = []
        passages: List[Dict[str, Any]] = []
        section_map: Dict[str, List[str]] = {}

        for p_idx, paragraph in enumerate(preprocessing.get("paragraphs", [])):
            para_sentences = paragraph.get("sentences", [])
            para_texts: List[str] = []
            page_number = paragraph.get("page_number")
            section_name = str(paragraph.get("section_name") or "Body")
            if section_name == "UNKNOWN":
                section_name = "Body"

            for sent in para_sentences:
                cleaned = str(sent.get("cleaned_text") or "").strip()
                if not cleaned:
                    continue
                para_texts.append(cleaned)
                sentences.append(
                    ExtractedSentence(
                        paper_id=paper_id,
                        page_number=int(sent.get("page_number") or 0),
                        section_name=section_name,
                        paragraph_index=int(sent.get("paragraph_index", p_idx)),
                        sentence_index=int(sent.get("sentence_index", len(sentences))),
                        original_text=str(sent.get("original_text") or cleaned),
                        cleaned_text=cleaned,
                    )
                )

            combined = " ".join(para_texts).strip()
            if not combined:
                continue
            source_ref = (
                f"Page {page_number}, Para {p_idx + 1}"
                if source_type == "pdf" and page_number
                else f"Paragraph {p_idx + 1}"
            )
            passages.append(
                {
                    "passage_id": f"P{len(passages) + 1}",
                    "paragraph_index": p_idx,
                    "page_number": page_number if source_type == "pdf" else None,
                    "section_title": section_name,
                    "source_ref": source_ref,
                    "text": combined,
                }
            )
            section_map.setdefault(section_name, []).append(combined)

        sections = [
            {"section_name": name, "text": "\n\n".join(parts)}
            for name, parts in section_map.items()
        ]
        return sentences, passages, sections

    @staticmethod
    def _preprocess_pasted_text(
        raw_text: str,
    ) -> Tuple[List[ExtractedSentence], List[Dict[str, Any]], List[Dict[str, Any]], str]:
        cleaned_doc = TextCleaner.clean_scientific_text(raw_text)
        raw_sections = SectionExtractor.extract_sections(cleaned_doc)
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", cleaned_doc) if p.strip()]
        if not paragraphs:
            paragraphs = [cleaned_doc]

        sentences: List[ExtractedSentence] = []
        passages: List[Dict[str, Any]] = []
        section_map: Dict[str, List[str]] = {}
        cursor = 0
        total_sent = 0

        for p_idx, para in enumerate(paragraphs):
            line_offset = cleaned_doc[:cursor].count("\n")
            cursor += len(para) + 2
            sec = next(
                (
                    s["section_name"]
                    for s in raw_sections
                    if s["start_line"] <= line_offset < s["end_line"]
                ),
                "UNKNOWN",
            )
            if sec == "UNKNOWN":
                sec = "Body"

            seg_list = SentenceSegmenter.segment_sentences(
                cleaned_text=para, paper_id=0, page_number=0, section_name=sec
            )
            para_cleaned_sents: List[str] = []
            for seg in seg_list:
                cleaned_sent = str(seg.get("cleaned_text") or "").strip()
                if not cleaned_sent:
                    continue
                para_cleaned_sents.append(cleaned_sent)
                sentences.append(
                    ExtractedSentence(
                        paper_id=0,
                        page_number=0,
                        section_name=sec,
                        paragraph_index=p_idx,
                        sentence_index=total_sent,
                        original_text=str(seg.get("original_text") or cleaned_sent),
                        cleaned_text=cleaned_sent,
                    )
                )
                total_sent += 1

            combined = " ".join(para_cleaned_sents).strip()
            if combined:
                passages.append(
                    {
                        "passage_id": f"P{len(passages) + 1}",
                        "paragraph_index": p_idx,
                        "page_number": None,
                        "section_title": sec,
                        "source_ref": f"Paragraph {p_idx + 1}",
                        "text": combined,
                    }
                )
                section_map.setdefault(sec, []).append(combined)

        sections = [
            {"section_name": name, "text": "\n\n".join(parts)}
            for name, parts in section_map.items()
        ]
        return sentences, passages, sections, cleaned_doc

    @staticmethod
    def _run_nlp_and_build_graph(
        *,
        title: str,
        author: Optional[str],
        full_text: str,
        sentences: List[ExtractedSentence],
        paper_id: int,
        source_type: str,
    ) -> Tuple[List[ExtractedEntity], List[Dict[str, Any]], Dict[str, Any]]:
        ner = NERPipeline(use_transformer=False, include_general_prose=True)
        entities = ner.extract_paper(sentences).entities

        relations = extract_relations_from_paper(
            full_text,
            entities,
            sentences,
            paper_id,
            use_relabel=False,
            use_rebel=False,
            use_classifier=False,
        )

        # Isolated EntityResolutionService per analysis ensures zero cross-document mixing.
        resolver = EntityResolutionService()
        nodes_by_id: Dict[str, Dict[str, Any]] = {}
        now_iso = _utc_now().isoformat()

        def _match_anaphor_project_id(ent: ExtractedEntity) -> Optional[str]:
            """Map bare project/head mentions ('project', 'garden') to an established qualified Project."""
            if ent.entity_type != "PROJECT":
                return None
            low = resolver._normalize_for_matching(ent.text, ent.entity_type)
            if not low or " " in low:
                return None
            project_canonicals = [
                c
                for c in resolver.canonical_entities.values()
                if c.entity_type == "PROJECT"
                and resolver._normalize_for_matching(c.canonical_name, "PROJECT") != low
            ]
            if not project_canonicals:
                return None
            head_matches = [
                c
                for c in project_canonicals
                if resolver._normalize_for_matching(c.canonical_name, "PROJECT").endswith(f" {low}")
            ]
            if len(head_matches) == 1:
                return head_matches[0].entity_id
            if low in {"project", "initiative", "program", "programme"}:
                qualified = [
                    c
                    for c in project_canonicals
                    if " " in resolver._normalize_for_matching(c.canonical_name, "PROJECT")
                ]
                if len(qualified) == 1:
                    return qualified[0].entity_id
            return None

        for ent in entities:
            anaphor_id = _match_anaphor_project_id(ent)
            if anaphor_id and anaphor_id in resolver.canonical_entities:
                canonical = resolver.canonical_entities[anaphor_id]
                canonical.occurrence_count += 1
                resolver.add_alias(anaphor_id, ent.text.strip())
                canonical_id = anaphor_id
            else:
                canonical_id, _ = resolver.resolve_entity(ent, paper_id, now_iso)
                canonical = resolver.canonical_entities[canonical_id]
            label = get_node_label(ent.entity_type)
            node = nodes_by_id.get(canonical.entity_id)
            ref = (
                f"Page {ent.page_number}"
                if source_type == "pdf" and ent.page_number
                else f"Sent {ent.sentence_index + 1}"
            )
            if node is None:
                nodes_by_id[canonical.entity_id] = {
                    "id": canonical.entity_id,
                    "label": canonical.canonical_name,
                    "category": label,
                    "entity_type": ent.entity_type,
                    "occurrences": 1,
                    "aliases": list(canonical.aliases),
                    "confidence": round(float(ent.confidence), 3),
                    "source_refs": [ref],
                    "sample_context": (ent.source_text or "")[:240],
                }
            else:
                node["occurrences"] += 1
                node["aliases"] = list(canonical.aliases)
                node["confidence"] = round(max(node["confidence"], float(ent.confidence)), 3)
                if ref not in node["source_refs"] and len(node["source_refs"]) < 10:
                    node["source_refs"].append(ref)

        # Include Author node(s) from metadata when present, linked to Document node via AUTHORED.
        if author:
            author_names = [
                a.strip() for a in re.split(r"[,;]", author) if a.strip() and a.strip().lower() != "unknown"
            ]
            if author_names:
                doc_node_id = f"doc_{hashlib.sha256(title.encode('utf-8')).hexdigest()[:12]}"
                nodes_by_id[doc_node_id] = {
                    "id": doc_node_id,
                    "label": title[:80],
                    "category": "Paper",
                    "entity_type": "PAPER",
                    "occurrences": 1,
                    "aliases": [],
                    "confidence": 1.0,
                    "source_refs": ["Metadata"],
                    "sample_context": title,
                }
                for a_name in author_names[:8]:
                    a_id = f"author_{hashlib.sha256(a_name.casefold().encode('utf-8')).hexdigest()[:12]}"
                    nodes_by_id[a_id] = {
                        "id": a_id,
                        "label": a_name,
                        "category": "Author",
                        "entity_type": "AUTHOR",
                        "occurrences": 1,
                        "aliases": [],
                        "confidence": 1.0,
                        "source_refs": ["Metadata"],
                        "sample_context": f"Author of {title}",
                    }

        # Build validated edges using canonical entity IDs.
        edges: List[Dict[str, Any]] = []
        rel_dicts: List[Dict[str, Any]] = []
        seen_edges: set[Tuple[str, str, str]] = set()
        degree: Dict[str, int] = {nid: 0 for nid in nodes_by_id}

        for rel in relations:
            subj_label = get_node_label(rel.subject_entity_type)
            obj_label = get_node_label(rel.object_entity_type)
            if not validate_relationship(rel.relation, subj_label, obj_label):
                continue

            subj_norm = resolver._normalize_for_matching(rel.subject_text, rel.subject_entity_type)
            obj_norm = resolver._normalize_for_matching(rel.object_text, rel.object_entity_type)
            subj_id = (
                resolver.name_index.get(f"{rel.subject_entity_type}:{subj_norm}")
                or resolver.name_index.get(subj_norm)
                or resolver.aliases.get(subj_norm)
                or resolver._generate_entity_id(rel.subject_text, rel.subject_entity_type)
            )
            obj_id = (
                resolver.name_index.get(f"{rel.object_entity_type}:{obj_norm}")
                or resolver.name_index.get(obj_norm)
                or resolver.aliases.get(obj_norm)
                or resolver._generate_entity_id(rel.object_text, rel.object_entity_type)
            )
            if subj_id not in nodes_by_id or obj_id not in nodes_by_id or subj_id == obj_id:
                continue

            key = (subj_id, rel.relation, obj_id)
            if key in seen_edges:
                continue
            seen_edges.add(key)

            src_ref = (
                f"Page {rel.page_number}"
                if source_type == "pdf" and rel.page_number
                else f"Sent {rel.sentence_id + 1}"
            )
            edge_obj = {
                "source": subj_id,
                "target": obj_id,
                "source_label": nodes_by_id[subj_id]["label"],
                "target_label": nodes_by_id[obj_id]["label"],
                "relation": rel.relation,
                "confidence": round(float(rel.confidence), 3),
                "evidence": rel.evidence,
                "page_number": rel.page_number if source_type == "pdf" else None,
                "sentence_id": rel.sentence_id,
                "source_ref": src_ref,
            }
            edges.append(edge_obj)
            rel_dicts.append({**rel.to_dict(), "source_ref": src_ref})
            degree[subj_id] = degree.get(subj_id, 0) + 1
            degree[obj_id] = degree.get(obj_id, 0) + 1

        # Add AUTHORED edges for metadata authors
        if author:
            doc_node_id = f"doc_{hashlib.sha256(title.encode('utf-8')).hexdigest()[:12]}"
            if doc_node_id in nodes_by_id:
                for nid, n in list(nodes_by_id.items()):
                    if n["category"] == "Author" and nid != doc_node_id:
                        edges.append(
                            {
                                "source": nid,
                                "target": doc_node_id,
                                "source_label": n["label"],
                                "target_label": nodes_by_id[doc_node_id]["label"],
                                "relation": "AUTHORED",
                                "confidence": 1.0,
                                "evidence": f"Document metadata author: {n['label']}",
                                "page_number": None,
                                "sentence_id": 0,
                                "source_ref": "Metadata",
                            }
                        )
                        degree[nid] = degree.get(nid, 0) + 1
                        degree[doc_node_id] = degree.get(doc_node_id, 0) + 1

        categories: Dict[str, int] = {}
        for nid, node in nodes_by_id.items():
            node["degree"] = degree.get(nid, 0)
            categories[node["category"]] = categories.get(node["category"], 0) + 1

        most_connected = sorted(
            (
                {
                    "id": n["id"],
                    "label": n["label"],
                    "category": n["category"],
                    "degree": n["degree"],
                    "occurrences": n["occurrences"],
                }
                for n in nodes_by_id.values()
            ),
            key=lambda x: (x["degree"], x["occurrences"]),
            reverse=True,
        )[:10]

        graph_json = {
            "nodes": sorted(
                nodes_by_id.values(),
                key=lambda x: (x["degree"], x["occurrences"]),
                reverse=True,
            ),
            "edges": edges,
            "stats": {
                "total_entities": len(nodes_by_id),
                "total_relationships": len(edges),
                "category_count": len(categories),
                "categories": categories,
                "most_connected": most_connected,
            },
        }
        return entities, rel_dicts, graph_json

    def _sync_optional_stores(
        self,
        *,
        paper: Paper,
        extracted: Dict[str, Any],
        preprocessing: Dict[str, Any],
        entities: List[ExtractedEntity],
        rel_dicts: List[Dict[str, Any]],
    ) -> None:
        """Persist PDF artifacts to Neo4j and FAISS when available without blocking analysis."""

        try:
            from KnowledgeGraphAI.backend.services.knowledge_graph.neo4j_connection import (
                get_neo4j_manager,
            )

            if get_neo4j_manager().is_available():
                from KnowledgeGraphAI.backend.services.knowledge_graph.graph_construction import (
                    GraphConstructionService,
                )

                GraphConstructionService().build_graph_for_paper(
                    {
                        "paper_id": paper.id,
                        "title": paper.title or "Untitled",
                        "author": paper.author or "Unknown",
                        "file_path": Path(paper.file_path).name,
                        "file_hash": paper.file_hash,
                        "content_hash": paper.content_hash,
                        "page_count": paper.page_count or 0,
                        "status": "completed",
                    },
                    entities,
                    rel_dicts,
                )
        except Exception as exc:
            logger.warning("Optional Neo4j sync skipped for paper_id=%s: %s", paper.id, exc)

        try:
            from KnowledgeGraphAI.backend.services.semantic_retrieval.retrieval_service import (
                SemanticRetrievalService,
            )

            pages = {
                int(pg["page_number"]): str(pg.get("text") or "")
                for pg in extracted.get("pages", [])
                if pg.get("page_number") is not None
            }
            semantic = SemanticRetrievalService()
            chunks = semantic.index_preprocessed(
                preprocessing,
                Path(paper.file_path).name,
                page_texts=pages,
                paper_title=paper.title,
                validate_graph=False,
                source_identifier=paper.content_hash,
            )
            if chunks:
                metadata = dict(paper.metadata_json or {})
                metadata.update(
                    {
                        "entity_count": len(entities),
                        "relation_count": len(rel_dicts),
                        "semantic_chunk_count": len(chunks),
                    }
                )
                paper.metadata_json = metadata
                paper.status = "completed"
                paper.processing_completed_at = _utc_now()
                self.db.commit()
        except Exception as exc:
            logger.warning("Optional FAISS sync skipped for paper_id=%s: %s", paper.id, exc)
