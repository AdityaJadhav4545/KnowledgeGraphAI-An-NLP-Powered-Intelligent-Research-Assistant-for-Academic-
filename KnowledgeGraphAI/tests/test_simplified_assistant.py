"""Comprehensive tests for the simplified KnowledgeGraphAI analysis, GraphRAG, and PDF report workflows."""

from __future__ import annotations

import io
from pathlib import Path
from unittest.mock import patch

import pymupdf
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from KnowledgeGraphAI.backend.database import get_db
from KnowledgeGraphAI.backend.main import app
from KnowledgeGraphAI.backend.services.analysis_assistant import AnalysisAssistantService
from KnowledgeGraphAI.backend.services.report_generator import ReportGenerationService
from KnowledgeGraphAI.frontend.components.graph_view import (
    build_interactive_figure,
    filter_subgraph,
)
from KnowledgeGraphAI.models.paper import Base


@pytest.fixture()
def isolated_client(tmp_path, monkeypatch):
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path / "raw"))
    monkeypatch.setenv("PROCESSED_DIR", str(tmp_path / "processed"))
    monkeypatch.setenv("FAISS_INDEX_DIR", str(tmp_path / "vector_store"))
    monkeypatch.setenv("REQUIRE_NEO4J", "false")
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://127.0.0.1:19999")

    from KnowledgeGraphAI.backend.config import get_settings

    get_settings.cache_clear()

    engine = create_engine(
        "sqlite:///",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def _override_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    previous_override = app.dependency_overrides.get(get_db)
    app.dependency_overrides[get_db] = _override_db
    try:
        yield TestClient(app), TestingSessionLocal
    finally:
        if previous_override is not None:
            app.dependency_overrides[get_db] = previous_override
        else:
            app.dependency_overrides.pop(get_db, None)
        get_settings.cache_clear()


def _make_pdf_bytes(text: str, *, title: str = "Test Research Paper", author: str = "Jane Researcher") -> bytes:
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    doc.set_metadata({"title": title, "author": author})
    data = doc.tobytes()
    doc.close()
    return data


def _make_blank_pdf_bytes() -> bytes:
    doc = pymupdf.open()
    doc.new_page()
    data = doc.tobytes()
    doc.close()
    return data


def test_pdf_workflow_end_to_end_and_report_download(isolated_client):
    client, _ = isolated_client
    pdf_bytes = _make_pdf_bytes(
        "Abstract\n"
        "BERT was evaluated on the SQuAD dataset using the Adam optimizer and achieved an F1-score of 91.2.\n\n"
        "Limitations\n"
        "Training requires substantial memory and compute resources.\n",
        title="BERT Evaluation Study",
        author="Alice Smith",
    )

    resp = client.post(
        "/api/analyses/pdf?sync_external_stores=false",
        files={"file": ("bert_study.pdf", pdf_bytes, "application/pdf")},
    )
    assert resp.status_code == 201, resp.text
    data = resp.json()
    aid = data["analysis_id"]
    assert data["status"] == "completed"
    assert data["source_type"] == "pdf"
    assert data["title"] == "BERT Evaluation Study"
    assert data["entity_count"] >= 3
    assert data["relationship_count"] >= 1
    assert data["graph"]["stats"]["total_entities"] == data["entity_count"]

    # Interactive Plotly graph helper works with extracted graph
    nodes, edges = filter_subgraph(data["graph"])
    fig, flat_ids = build_interactive_figure(nodes, edges)
    assert len(flat_ids) == len(nodes)
    assert len(fig.data) >= 1

    # Ask assistant (graceful fallback if Ollama unavailable)
    ask = client.post(f"/api/analyses/{aid}/ask", json={"question": "What dataset was BERT evaluated on?"})
    assert ask.status_code == 200
    ans = ask.json()
    assert ans["citations"]
    assert "SQuAD" in ans["answer"] or "[S1]" in ans["answer"]

    # Report JSON + PDF download
    rep = client.get(f"/api/analyses/{aid}/report")
    assert rep.status_code == 200
    rep_data = rep.json()
    for key in (
        "document_information",
        "executive_summary",
        "introduction_and_objective",
        "key_concepts_and_entities",
        "knowledge_graph_summary",
        "important_relationships",
        "methodology_and_techniques",
        "important_findings",
        "limitations",
        "conclusion",
        "references_and_traceability",
    ):
        assert key in rep_data

    pdf_dl = client.get(f"/api/analyses/{aid}/report/pdf")
    assert pdf_dl.status_code == 200
    assert pdf_dl.headers["content-type"] == "application/pdf"
    assert pdf_dl.content[:5] == b"%PDF-"
    parsed = pymupdf.open(stream=pdf_dl.content, filetype="pdf")
    assert len(parsed) >= 1
    parsed.close()


def test_pasted_text_workflow_without_neo4j_or_faiss(isolated_client):
    client, _ = isolated_client
    paragraph = (
        "CBOW and Skip-gram were evaluated on the Google News dataset for Word Representation. "
        "Skip-gram outperforms NNLM on Accuracy using Adagrad optimization."
    )
    resp = client.post(
        "/api/analyses/text",
        json={"text": paragraph, "title": "Word Vector Comparison"},
    )
    assert resp.status_code == 201, resp.text
    data = resp.json()
    aid = data["analysis_id"]
    assert data["source_type"] == "text"
    assert data["paper_id"] is None
    assert data["entity_count"] >= 4
    assert data["relationship_count"] >= 1

    # Assistant question on pasted text
    ask = client.post(f"/api/analyses/{aid}/ask", json={"question": "How does Skip-gram perform?"})
    assert ask.status_code == 200
    assert ask.json()["citations"][0]["source_ref"].startswith("Paragraph")

    # Report adapts to pasted text without fabricating publication metadata
    rep = client.get(f"/api/analyses/{aid}/report").json()
    assert rep["document_information"]["source_type"] == "Pasted Text"
    assert "Not specified in pasted text" in rep["document_information"]["authors"]

    pdf_dl = client.get(f"/api/analyses/{aid}/report/pdf")
    assert pdf_dl.status_code == 200
    assert pdf_dl.content[:5] == b"%PDF-"


def test_document_isolation_across_two_unrelated_analyses(isolated_client):
    client, _ = isolated_client

    r1 = client.post(
        "/api/analyses/text",
        json={
            "title": "Transformer QA Paper",
            "text": "BERT was evaluated on SQuAD and achieved strong F1-score using Adam.",
        },
    )
    r2 = client.post(
        "/api/analyses/text",
        json={
            "title": "Vision Classification Paper",
            "text": "ResNet-50 was evaluated on ImageNet and achieved high Accuracy using SGD.",
        },
    )
    assert r1.status_code == 201 and r2.status_code == 201
    a1, a2 = r1.json(), r2.json()

    labels_1 = {n["label"] for n in a1["graph"]["nodes"]}
    labels_2 = {n["label"] for n in a2["graph"]["nodes"]}
    assert "BERT" in labels_1 and "ResNet-50" not in labels_1
    assert "ResNet-50" in labels_2 and "BERT" not in labels_2

    ask1 = client.post(f"/api/analyses/{a1['analysis_id']}/ask", json={"question": "Which model and dataset are studied?"}).json()
    ask2 = client.post(f"/api/analyses/{a2['analysis_id']}/ask", json={"question": "Which model and dataset are studied?"}).json()
    assert "SQuAD" in str(ask1["citations"]) and "ImageNet" not in str(ask1["citations"])
    assert "ImageNet" in str(ask2["citations"]) and "SQuAD" not in str(ask2["citations"])

    detail1 = client.get(f"/api/analyses/{a1['analysis_id']}").json()
    detail2 = client.get(f"/api/analyses/{a2['analysis_id']}").json()
    assert len(detail1["chat_history"]) == 1
    assert len(detail2["chat_history"]) == 1
    assert detail1["chat_history"][0]["answer"] != detail2["chat_history"][0]["answer"]


def test_failure_handling_and_graceful_degradation(isolated_client):
    client, SessionLocal = isolated_client

    # Empty text & too short text
    assert client.post("/api/analyses/text", json={"text": "   "}).status_code == 400
    assert client.post("/api/analyses/text", json={"text": "short"}).status_code == 400

    # Invalid file extension
    assert (
        client.post(
            "/api/analyses/pdf",
            files={"file": ("notes.txt", b"hello", "text/plain")},
        ).status_code
        == 400
    )

    # Empty PDF bytes
    assert (
        client.post(
            "/api/analyses/pdf",
            files={"file": ("empty.pdf", b"", "application/pdf")},
        ).status_code
        == 400
    )

    # Corrupted PDF
    assert (
        client.post(
            "/api/analyses/pdf",
            files={"file": ("corrupt.pdf", b"%PDF-1.4 broken binary garbage", "application/pdf")},
        ).status_code
        == 400
    )

    # Blank / no-text PDF
    assert (
        client.post(
            "/api/analyses/pdf",
            files={"file": ("blank.pdf", _make_blank_pdf_bytes(), "application/pdf")},
        ).status_code
        == 400
    )

    # Text with zero extracted relations still succeeds cleanly and produces valid PDF report
    no_rel = client.post(
        "/api/analyses/text",
        json={"text": "This short paragraph discusses general scientific inquiry and experimental observations."},
    )
    assert no_rel.status_code == 201
    aid = no_rel.json()["analysis_id"]
    assert no_rel.json()["relationship_count"] == 0
    assert client.get(f"/api/analyses/{aid}/report/pdf").status_code == 200

    # Ollama unavailable falls back cleanly to evidence_only
    with patch("requests.post", side_effect=OSError("Ollama offline")):
        db = SessionLocal()
        try:
            ans = AnalysisAssistantService(db).ask(aid, "What does this paragraph discuss?")
            assert ans["generation_mode"] == "evidence_only"
            assert "[S1]" in ans["answer"]
            rep = ReportGenerationService(db).build_report_data(aid, refresh=True)
            assert rep["executive_summary"]
        finally:
            db.close()
