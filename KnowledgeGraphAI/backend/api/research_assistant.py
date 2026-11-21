"""Evidence-grounded GraphRAG assistant endpoints."""

from __future__ import annotations

from functools import lru_cache
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
import requests
from pydantic import BaseModel, Field

from KnowledgeGraphAI.backend.services.research_assistant.graph_rag import (
    GraphRAGService,
    ResearchAssistantError,
)


router = APIRouter(prefix="/api/assistant", tags=["research assistant"])


class AssistantQuestion(BaseModel):
    question: str = Field(min_length=1, max_length=20_000)
    top_k: int = Field(default=8, ge=1, le=20)


@lru_cache(maxsize=1)
def _assistant() -> GraphRAGService:
    return GraphRAGService()


@router.post("/ask")
def ask_question(payload: AssistantQuestion) -> Dict[str, Any]:
    try:
        return _assistant().ask(payload.question, top_k=payload.top_k)
    except ResearchAssistantError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.get("/status")
def assistant_status() -> Dict[str, Any]:
    """Report capability without forcing a model download or Ollama request."""
    from KnowledgeGraphAI.backend.config import get_settings

    settings = get_settings()
    ollama_available = False
    configured_model_available = False
    try:
        response = requests.get(
            f"{settings.ollama_base_url}/api/tags",
            timeout=min(settings.ollama_timeout_seconds, 3),
        )
        response.raise_for_status()
        models = response.json().get("models", [])
        ollama_available = True
        configured_model_available = any(
            isinstance(model, dict)
            and str(model.get("name", "")).split(":")[0] == settings.ollama_model.split(":")[0]
            for model in models
        )
    except (requests.RequestException, ValueError, TypeError):
        pass
    return {
        "semantic_retrieval_required": True,
        "ollama_available": ollama_available,
        "configured_model": settings.ollama_model,
        "configured_model_available": configured_model_available,
        "citation_policy": "Only retrieved indexed passages are emitted as citations.",
    }
