"""Unified API router for PDF and pasted-text research document analyses."""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, Iterator, List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, Query, Response, UploadFile, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from KnowledgeGraphAI.backend.api.security import require_write_access
from KnowledgeGraphAI.backend.config import get_settings
from KnowledgeGraphAI.backend.database import get_db
from KnowledgeGraphAI.backend.services.analysis_assistant import (
    AnalysisAssistantError,
    AnalysisAssistantService,
)
from KnowledgeGraphAI.backend.services.analysis_service import (
    AnalysisProcessingError,
    AnalysisValidationError,
    DocumentAnalysisService,
)
from KnowledgeGraphAI.backend.services.report_generator import ReportGenerationService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/analyses", tags=["analyses"])


class TextAnalysisRequest(BaseModel):
    text: str = Field(min_length=1, max_length=250_000)
    title: Optional[str] = Field(default=None, max_length=300)
    author: Optional[str] = Field(default=None, max_length=200)


class AskAnalysisRequest(BaseModel):
    question: str = Field(min_length=1, max_length=10_000)
    top_k: int = Field(default=5, ge=1, le=12)


@router.post("/pdf", status_code=status.HTTP_201_CREATED)
def analyze_pdf_upload(
    file: UploadFile = File(...),
    sync_external_stores: bool = Query(default=True),
    db: Session = Depends(get_db),
    _: None = Depends(require_write_access),
) -> Dict[str, Any]:
    settings = get_settings()
    max_bytes = settings.max_upload_bytes
    chunks: List[bytes] = []
    total = 0
    try:
        while True:
            block = file.file.read(1024 * 1024)
            if not block:
                break
            total += len(block)
            if total > max_bytes:
                limit_mb = max_bytes // (1024 * 1024)
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"The uploaded PDF exceeds the {limit_mb} MB limit.",
                )
            chunks.append(block)
        payload = b"".join(chunks)
    finally:
        file.file.close()

    try:
        return DocumentAnalysisService(db, settings=settings).analyze_pdf(
            file.filename or "document.pdf",
            payload,
            sync_external_stores=sync_external_stores,
        )
    except AnalysisValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except AnalysisProcessingError as exc:
        raise HTTPException(status_code=422, detail=exc.safe_message) from exc


@router.post("/text", status_code=status.HTTP_201_CREATED)
def analyze_pasted_text(
    payload: TextAnalysisRequest,
    db: Session = Depends(get_db),
    _: None = Depends(require_write_access),
) -> Dict[str, Any]:
    try:
        return DocumentAnalysisService(db).analyze_text(
            payload.text,
            title=payload.title,
            author=payload.author,
        )
    except AnalysisValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except AnalysisProcessingError as exc:
        raise HTTPException(status_code=422, detail=exc.safe_message) from exc


@router.get("")
def list_analyses(
    limit: int = Query(default=30, ge=1, le=100),
    db: Session = Depends(get_db),
) -> List[Dict[str, Any]]:
    return DocumentAnalysisService(db).list_analyses(limit=limit)


@router.get("/{analysis_id}")
def get_analysis(analysis_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    service = DocumentAnalysisService(db)
    record = service.get_analysis(analysis_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    return service.detail_dict(record)


@router.post("/{analysis_id}/ask")
def ask_analysis_assistant(
    analysis_id: str,
    payload: AskAnalysisRequest,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    try:
        return AnalysisAssistantService(db).ask(
            analysis_id, payload.question, top_k=payload.top_k
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Analysis not found.") from exc
    except AnalysisAssistantError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{analysis_id}/ask/stream")
def ask_analysis_assistant_stream(
    analysis_id: str,
    payload: AskAnalysisRequest,
    db: Session = Depends(get_db),
) -> StreamingResponse:
    service = AnalysisAssistantService(db)
    try:
        prepared = service.prepare_stream(
            analysis_id, payload.question, top_k=payload.top_k
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Analysis not found.") from exc
    except AnalysisAssistantError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    def _event_stream() -> Iterator[str]:
        for event in service.stream_events(prepared):
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(
        _event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.delete("/{analysis_id}/chat")
def clear_analysis_chat(
    analysis_id: str,
    db: Session = Depends(get_db),
    _: None = Depends(require_write_access),
) -> Dict[str, str]:
    try:
        AnalysisAssistantService(db).clear_chat(analysis_id)
        return {"status": "cleared"}
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Analysis not found.") from exc


@router.get("/{analysis_id}/report")
def get_analysis_report(
    analysis_id: str,
    refresh: bool = Query(default=False),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    try:
        return ReportGenerationService(db).build_report_data(analysis_id, refresh=refresh)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Analysis not found.") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{analysis_id}/report/pdf")
def download_analysis_report_pdf(
    analysis_id: str,
    refresh: bool = Query(default=False),
    db: Session = Depends(get_db),
) -> Response:
    try:
        pdf_bytes = ReportGenerationService(db).generate_pdf_bytes(analysis_id, refresh=refresh)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Analysis not found.") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="analysis_{analysis_id}_report.pdf"'
        },
    )


@router.get("/{analysis_id}/graph/image")
def get_analysis_graph_image(analysis_id: str, db: Session = Depends(get_db)) -> Response:
    record = DocumentAnalysisService(db).get_analysis(analysis_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    png_bytes = ReportGenerationService.render_graph_png(record.graph_json or {})
    return Response(content=png_bytes, media_type="image/png")

