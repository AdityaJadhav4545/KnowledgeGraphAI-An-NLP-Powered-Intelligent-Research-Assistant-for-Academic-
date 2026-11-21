"""FastAPI application entry point for KnowledgeGraphAI."""

from __future__ import annotations

from contextlib import asynccontextmanager
import logging
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from KnowledgeGraphAI.backend.api.analyses import router as analyses_router
from KnowledgeGraphAI.backend.api.health import router as health_router
from KnowledgeGraphAI.backend.api.evaluation import router as evaluation_router
from KnowledgeGraphAI.backend.api.experiments import router as experiments_router
from KnowledgeGraphAI.backend.api.knowledge_graph import router as graph_router
from KnowledgeGraphAI.backend.api.nlp import router as nlp_router
from KnowledgeGraphAI.backend.api.nlp_ner import router as ner_router
from KnowledgeGraphAI.backend.api.papers import router as papers_router
from KnowledgeGraphAI.backend.api.research_assistant import router as assistant_router
from KnowledgeGraphAI.backend.api.semantic_search import router as semantic_search_router
from KnowledgeGraphAI.backend.config import get_settings
from KnowledgeGraphAI.backend.database import init_db


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)
settings = get_settings()


def on_startup() -> None:
    settings.validate()
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    settings.processed_dir.mkdir(parents=True, exist_ok=True)
    init_db()
    logger.info("KnowledgeGraph AI backend started in %s mode", settings.environment)


@asynccontextmanager
async def lifespan(_: FastAPI):
    on_startup()
    yield


app = FastAPI(
    title="KnowledgeGraph AI",
    version="1.0.0",
    description="Evidence-grounded scientific NLP, graph, and retrieval backend",
    debug=settings.debug,
    lifespan=lifespan,
)

allow_all_origins = "*" in settings.cors_origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    # Browsers reject wildcard origins plus credentials.  Production settings
    # validation forbids wildcard origins altogether.
    allow_credentials=not allow_all_origins,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type", "X-API-Key"],
)

app.include_router(health_router)
app.include_router(analyses_router)
app.include_router(papers_router)
app.include_router(nlp_router)
app.include_router(ner_router)
app.include_router(graph_router)
app.include_router(semantic_search_router)
app.include_router(assistant_router)
app.include_router(evaluation_router)
app.include_router(experiments_router)


@app.middleware("http")
async def request_context(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or uuid4().hex
    try:
        response = await call_next(request)
    except Exception:
        logger.exception("Unhandled request failure id=%s path=%s", request_id, request.url.path)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error.", "request_id": request_id},
        )
    response.headers["X-Request-ID"] = request_id
    return response


@app.exception_handler(RequestValidationError)
async def validation_error_handler(_: Request, exc: RequestValidationError):
    # Validation locations/messages are helpful, while raw request bodies can
    # contain uploaded content or secrets and therefore must not be echoed.
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Request validation failed.", "errors": exc.errors()},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("KnowledgeGraphAI.backend.main:app", host="127.0.0.1", port=8000)
