"""Paper-library endpoints with safe uploads and real pipeline processing."""

from __future__ import annotations

import json
import logging
import os
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy import or_
from sqlalchemy.orm import Session

from KnowledgeGraphAI.backend.api.security import require_write_access
from KnowledgeGraphAI.backend.config import get_settings
from KnowledgeGraphAI.backend.database import get_db
from KnowledgeGraphAI.backend.services.paper_processing import (
    ACTIVE_PROCESSING_STATES,
    PaperProcessingError,
    PaperProcessingService,
)
from KnowledgeGraphAI.backend.services.pdf_ingestion import PDFIngestionService
from KnowledgeGraphAI.models.paper import Paper


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/papers", tags=["papers"])


def _utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _public_metadata(metadata: Dict[str, Any] | None) -> Dict[str, Any]:
    """Remove local paths and retain useful provenance/counts for clients."""

    metadata = dict(metadata or {})
    for key in (
        "processed_json_path",
        "pipeline_artifact_path",
        "file_path",
        "raw_path",
    ):
        metadata.pop(key, None)
    return metadata


def _paper_summary(paper: Paper) -> Dict[str, Any]:
    metadata = paper.metadata_json or {}
    return {
        "id": paper.id,
        "title": paper.title,
        "author": paper.author,
        "page_count": paper.page_count,
        "status": paper.status,
        "created_at": paper.created_at,
        "updated_at": paper.updated_at,
        "processing_started_at": paper.processing_started_at,
        "processing_completed_at": paper.processing_completed_at,
        "processing_error": paper.processing_error,
        "is_scanned": metadata.get("is_scanned", False),
        "entity_count": metadata.get("entity_count", 0),
        "relation_count": metadata.get("relation_count", 0),
        "semantic_chunk_count": metadata.get("semantic_chunk_count", 0),
    }


def _safe_upload_name(filename: str | None) -> str:
    name = Path(filename or "paper.pdf").name
    if not name or name in {".", ".."}:
        return "paper.pdf"
    # A filename is display provenance only; storage uses a content hash.
    return "".join(char for char in name if char.isprintable())[:255] or "paper.pdf"


async def _save_upload(file: UploadFile, target_dir: Path, max_bytes: int) -> Path:
    """Stream to a unique staging file while enforcing an actual size limit."""

    target_dir.mkdir(parents=True, exist_ok=True)
    staging = target_dir / f".{uuid.uuid4().hex}.upload"
    total = 0
    first_bytes = b""
    try:
        with staging.open("wb") as destination:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                if not first_bytes:
                    first_bytes = chunk[:8]
                total += len(chunk)
                if total > max_bytes:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"Upload exceeds the configured {max_bytes} byte limit.",
                    )
                destination.write(chunk)
        if total == 0:
            raise HTTPException(status_code=400, detail="The uploaded file is empty.")
        if not first_bytes.startswith(b"%PDF-"):
            raise HTTPException(status_code=400, detail="The uploaded file is not a valid PDF.")
        return staging
    except Exception:
        try:
            staging.unlink(missing_ok=True)
        except OSError:
            logger.warning("Could not remove rejected upload staging file")
        raise
    finally:
        await file.close()


def _write_json_atomically(target: Path, payload: Dict[str, Any]) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f"{target.name}.", suffix=".tmp", dir=target.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_paper(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: None = Depends(require_write_access),
) -> Dict[str, Any]:
    """Validate, extract, and persist a PDF without trusting client filenames."""

    settings = get_settings()
    original_name = _safe_upload_name(file.filename)
    if not original_name.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF uploads are allowed.")
    if file.content_type and file.content_type not in {
        "application/pdf",
        "application/octet-stream",
    }:
        raise HTTPException(status_code=400, detail="Only PDF uploads are allowed.")

    staging = await _save_upload(file, settings.upload_dir, settings.max_upload_bytes)
    try:
        file_hash = PDFIngestionService.compute_sha256(str(staging))
        extracted_data = PDFIngestionService.extract_pdf_data(
            str(staging), fallback_title=original_name
        )
        content_hash = PDFIngestionService.compute_content_hash(str(staging))
        existing = db.query(Paper).filter(
            or_(Paper.file_hash == file_hash, Paper.content_hash == content_hash)
        ).first()
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Duplicate paper detected (existing paper ID {existing.id}).",
            )

        # Stable content-addressed storage prevents path traversal and filename
        # collisions.  Do not overwrite an orphaned matching source file.
        stored_path = settings.upload_dir / f"{file_hash}.pdf"
        if stored_path.exists():
            staging.unlink(missing_ok=True)
        else:
            os.replace(staging, stored_path)

        extracted_artifact = settings.processed_dir / f"{content_hash}.extracted.json"
        _write_json_atomically(extracted_artifact, extracted_data)
        paper = Paper(
            title=extracted_data.get("title") or original_name,
            author=extracted_data.get("author") or "Unknown",
            file_path=str(stored_path),
            file_hash=file_hash,
            content_hash=content_hash,
            page_count=extracted_data.get("page_count"),
            metadata_json={
                "original_filename": original_name,
                "extracted_artifact": extracted_artifact.name,
                "is_scanned": bool(extracted_data.get("is_scanned")),
                "has_extractable_text": bool(extracted_data.get("has_extractable_text")),
                "upload_at": _utc_iso(),
            },
            status="uploaded",
        )
        db.add(paper)
        db.commit()
        db.refresh(paper)
        logger.info("Uploaded paper id=%s with %s pages", paper.id, paper.page_count)
        return _paper_summary(paper)
    except HTTPException:
        # A rejected upload is still only an uncommitted staging file; deleting
        # it does not touch any preserved research document.
        staging.unlink(missing_ok=True)
        raise
    except ValueError as exc:
        staging.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        db.rollback()
        logger.exception("Paper upload failed")
        # Keep a successfully moved source file rather than risk deleting a
        # user document; it is content-addressed and can be recovered safely.
        staging.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail="The paper could not be saved.") from exc


@router.get("")
async def list_papers(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    papers = (
        db.query(Paper)
        .filter(Paper.status != "archived")
        .order_by(Paper.created_at.desc())
        .all()
    )
    return [_paper_summary(paper) for paper in papers]


@router.get("/{paper_id}")
async def get_paper(paper_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    paper = (
        db.query(Paper)
        .filter(Paper.id == paper_id, Paper.status != "archived")
        .first()
    )
    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found.")
    metadata = paper.metadata_json or {}
    extracted_content = None
    artifact_name = metadata.get("extracted_artifact")
    if isinstance(artifact_name, str) and artifact_name:
        artifact = get_settings().processed_dir / Path(artifact_name).name
        if artifact.is_file():
            try:
                extracted_content = json.loads(artifact.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                logger.warning("Could not read extracted artifact for paper id=%s", paper.id)
    return {
        **_paper_summary(paper),
        "metadata": _public_metadata(metadata),
        "extracted_content": extracted_content,
    }


@router.get("/{paper_id}/source")
async def download_source(
    paper_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_write_access),
) -> FileResponse:
    paper = (
        db.query(Paper)
        .filter(Paper.id == paper_id, Paper.status != "archived")
        .first()
    )
    if paper is None or not paper.file_path or not Path(paper.file_path).is_file():
        raise HTTPException(status_code=404, detail="Source PDF not found.")
    filename = _safe_upload_name((paper.metadata_json or {}).get("original_filename"))
    return FileResponse(paper.file_path, media_type="application/pdf", filename=filename)


@router.delete("/{paper_id}", status_code=status.HTTP_200_OK)
async def archive_paper(
    paper_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_write_access),
) -> Dict[str, str]:
    """Hide a paper from the library without deleting PDFs, index, or data."""

    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if paper is None or paper.status == "archived":
        raise HTTPException(status_code=404, detail="Paper not found.")
    if paper.status in ACTIVE_PROCESSING_STATES:
        raise HTTPException(status_code=409, detail="A paper cannot be archived while processing.")
    metadata = dict(paper.metadata_json or {})
    metadata["archived_at"] = _utc_iso()
    paper.metadata_json = metadata
    paper.status = "archived"
    paper.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.commit()
    return {"message": f"Paper {paper_id} archived; source data was preserved."}


@router.post("/{paper_id}/process", status_code=status.HTTP_200_OK)
def process_paper(
    paper_id: int,
    force: bool = Query(default=False),
    db: Session = Depends(get_db),
    _: None = Depends(require_write_access),
) -> Dict[str, Any]:
    paper = (
        db.query(Paper)
        .filter(Paper.id == paper_id, Paper.status != "archived")
        .first()
    )
    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found.")
    try:
        return PaperProcessingService(db).process(paper, force=force)
    except PaperProcessingError as exc:
        code = status.HTTP_503_SERVICE_UNAVAILABLE if exc.stage in {
            "graph_indexing",
            "semantic_indexing",
        } else status.HTTP_422_UNPROCESSABLE_ENTITY
        raise HTTPException(
            status_code=code,
            detail={"stage": exc.stage, "message": exc.safe_message},
        ) from exc
