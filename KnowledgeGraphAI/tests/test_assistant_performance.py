"""Tests for Ask Me telemetry, prompt optimization, semantic caching, and SSE streaming."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from KnowledgeGraphAI.backend.database import get_db
from KnowledgeGraphAI.backend.main import app
from KnowledgeGraphAI.backend.services.analysis_assistant import (
    AnalysisAssistantService,
    get_shared_semantic_service,
)
from KnowledgeGraphAI.frontend.components.api_client import APIClient
from KnowledgeGraphAI.models.paper import Base


@pytest.fixture()
def perf_client(tmp_path, monkeypatch):
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

    prev = app.dependency_overrides.get(get_db)
    app.dependency_overrides[get_db] = _override_db
    try:
        yield TestClient(app), TestingSessionLocal
    finally:
        if prev is not None:
            app.dependency_overrides[get_db] = prev
        else:
            app.dependency_overrides.pop(get_db, None)
        get_settings.cache_clear()


class _FakeStreamResponse:
    def __init__(self, lines, *, ok=True, status_code=200, headers=None, json_body=None):
        self._lines = lines
        self.ok = ok
        self.status_code = status_code
        self.headers = headers or {"content-type": "text/event-stream"}
        self._json_body = json_body

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def raise_for_status(self):
        if not self.ok:
            raise RuntimeError(f"HTTP {self.status_code}")

    def iter_lines(self, decode_unicode=True):
        del decode_unicode
        yield from self._lines

    def json(self):
        return self._json_body


class _FakeOllamaSyncResponse:
    def __init__(self, content: str):
        self._content = content

    def raise_for_status(self):
        return None

    def json(self):
        return {
            "message": {"content": self._content},
            "load_duration": 15_000_000,
            "prompt_eval_count": 120,
            "prompt_eval_duration": 180_000_000,
            "eval_count": 16,
            "eval_duration": 2_400_000_000,
        }


def _create_sample_analysis(client: TestClient) -> str:
    text = (
        "In 2022, Sarah Jenkins started the Oakwood Community Garden on an abandoned lot "
        "donated by the local council. She partnered with GreenFuture Volunteers, who built "
        "twenty raised beds and installed a rainwater harvesting system. By summer 2023, "
        "the garden was producing organic tomatoes, spinach, and herbs for thirty neighborhood families."
    )
    resp = client.post(
        "/api/analyses/text",
        json={"title": "Oakwood Community Garden", "text": text},
    )
    assert resp.status_code == 201
    return resp.json()["analysis_id"]


def test_sync_ask_records_timing_and_preserves_unbracketed_grounded_answer(perf_client):
    client, SessionLocal = perf_client
    aid = _create_sample_analysis(client)

    class _MockHttp:
        def __init__(self):
            self.last_payload = None

        def post(self, _url, json=None, timeout=None, **_kwargs):
            self.last_payload = json
            return _FakeOllamaSyncResponse(
                "The garden produced organic tomatoes, spinach, and herbs."
            )

    mock_http = _MockHttp()
    db = SessionLocal()
    try:
        turn = AnalysisAssistantService(db, http_session=mock_http).ask(
            aid, "What vegetables did the garden produce?"
        )
    finally:
        db.close()

    assert turn["generation_mode"] == "ollama_grounded"
    assert "[S1]" in turn["answer"]
    assert "tomatoes" in turn["answer"]
    assert mock_http.last_payload["keep_alive"] == "15m"
    assert mock_http.last_payload["options"]["num_ctx"] == 2048
    assert mock_http.last_payload["options"]["num_predict"] == 220
    assert turn["timing"]["prompt_tokens"] == 120
    assert turn["timing"]["generated_tokens"] == 16
    assert turn["timing"]["tokens_per_second"] > 0
    assert turn["timing"]["total_ms"] >= 0


def test_finalize_answer_still_rejects_fabricated_citations():
    result = AnalysisAssistantService._finalize_grounded_answer(
        "Fabricated claim [S99].",
        {"S1"},
        primary_citation_id="S1",
    )
    assert result is None


def test_sse_stream_endpoint_emits_tokens_and_persists_turn(perf_client):
    client, _ = perf_client
    aid = _create_sample_analysis(client)

    ollama_lines = [
        json.dumps({"message": {"content": "Sarah Jenkins "}, "done": False}),
        json.dumps({"message": {"content": "started the garden [S1]."}, "done": False}),
        json.dumps(
            {
                "message": {"content": ""},
                "done": True,
                "load_duration": 10_000_000,
                "prompt_eval_count": 110,
                "prompt_eval_duration": 200_000_000,
                "eval_count": 10,
                "eval_duration": 1_500_000_000,
            }
        ),
    ]

    def _fake_post(*_args, **_kwargs):
        return _FakeStreamResponse(ollama_lines)

    with patch("requests.post", side_effect=_fake_post):
        with client.stream(
            "POST",
            f"/api/analyses/{aid}/ask/stream",
            json={"question": "What was Sarah's role in the project?"},
        ) as resp:
            assert resp.status_code == 200
            assert "text/event-stream" in resp.headers["content-type"]
            events = []
            for line in resp.iter_lines():
                if line and line.startswith("data:"):
                    events.append(json.loads(line[5:].strip()))

    types = [e["type"] for e in events]
    assert types[0] == "meta"
    assert types.count("token") == 2
    assert types[-1] == "done"
    done_turn = events[-1]["turn"]
    assert done_turn["generation_mode"] == "ollama_grounded"
    assert done_turn["answer"] == "Sarah Jenkins started the garden [S1]."
    assert done_turn["timing"]["ttft_ms"] is not None

    detail = client.get(f"/api/analyses/{aid}").json()
    assert len(detail["chat_history"]) == 1
    assert detail["chat_history"][0]["answer"] == "Sarah Jenkins started the garden [S1]."


def test_sse_stream_validates_errors_and_handles_offline_fallback(perf_client):
    client, _ = perf_client
    assert (
        client.post(
            "/api/analyses/missing-id/ask/stream", json={"question": "Hello?"}
        ).status_code
        == 404
    )
    aid = _create_sample_analysis(client)
    assert (
        client.post(
            f"/api/analyses/{aid}/ask/stream", json={"question": "   "}
        ).status_code
        == 400
    )

    with patch("requests.post", side_effect=OSError("Ollama offline")):
        with client.stream(
            "POST",
            f"/api/analyses/{aid}/ask/stream",
            json={"question": "How did the council help?"},
        ) as resp:
            assert resp.status_code == 200
            events = [
                json.loads(line[5:].strip())
                for line in resp.iter_lines()
                if line and line.startswith("data:")
            ]
    assert events[-1]["type"] == "done"
    assert events[-1]["turn"]["generation_mode"] == "evidence_only"
    assert "[S1]" in events[-1]["turn"]["answer"]


def test_frontend_api_client_stream_post_parses_sse_and_http_errors():
    sse_lines = [
        'data: {"type": "meta", "citations": []}',
        "",
        'data: {"type": "token", "content": "Hello "}',
        'data: {"type": "done", "turn": {"answer": "Hello [S1]"}}',
    ]

    class _Session:
        def __init__(self, resp):
            self._resp = resp

        def request(self, *_args, **_kwargs):
            return self._resp

    ok_client = APIClient("http://backend.test", session=_Session(_FakeStreamResponse(sse_lines)))
    ok_events = list(ok_client.stream_post("/api/analyses/a1/ask/stream", json_body={"question": "Hi"}))
    assert [e["type"] for e in ok_events] == ["meta", "token", "done"]

    err_client = APIClient(
        "http://backend.test",
        session=_Session(
            _FakeStreamResponse(
                [],
                ok=False,
                status_code=404,
                headers={"content-type": "application/json"},
                json_body={"detail": "Analysis not found."},
            )
        ),
    )
    err_events = list(err_client.stream_post("/api/analyses/a1/ask/stream", json_body={"question": "Hi"}))
    assert err_events == [
        {"type": "error", "status_code": 404, "detail": "Analysis not found."}
    ]


def test_shared_semantic_service_reuses_instance_per_config(tmp_path, monkeypatch):
    monkeypatch.setenv("FAISS_INDEX_DIR", str(tmp_path / "idx_a"))
    with patch(
        "KnowledgeGraphAI.backend.services.semantic_retrieval.retrieval_service.SemanticRetrievalService"
    ) as mock_cls:
        s1 = get_shared_semantic_service()
        s2 = get_shared_semantic_service()
        assert s1 is s2
        assert mock_cls.call_count == 1


def test_streamlit_askme_streaming_ui_apptest(monkeypatch):
    from streamlit.testing.v1 import AppTest
    from KnowledgeGraphAI.frontend.components.api_client import APIResult

    sample_doc = {
        "analysis_id": "ana-stream-1",
        "title": "Oakwood Community Garden",
        "source_type": "text",
        "status": "completed",
        "entity_count": 9,
        "relationship_count": 3,
        "summary": "Summary of the community garden project.",
        "graph": {
            "nodes": [
                {"id": "n1", "label": "Sarah Jenkins", "category": "Person", "occurrences": 1, "source_refs": ["Paragraph 1"]},
                {"id": "n2", "label": "Oakwood Community Garden", "category": "Project", "occurrences": 1, "source_refs": ["Paragraph 1"]},
            ],
            "edges": [
                {"source": "n1", "target": "n2", "source_label": "Sarah Jenkins", "target_label": "Oakwood Community Garden", "relation": "STARTED", "source_ref": "Paragraph 1"},
            ],
            "stats": {"total_entities": 2, "total_relationships": 1},
        },
        "passages": [{"passage_id": "p1", "source_ref": "Paragraph 1", "text": "Sarah Jenkins started the Oakwood Community Garden."}],
        "chat_history": [],
    }

    class _StreamingFakeClient:
        def __init__(self, *args, **kwargs):
            self.history = sample_doc["chat_history"]

        def get(self, path: str, *, timeout: int = 10, params=None):
            if path == "/health":
                return APIResult(200, {"status": "ok", "neo4j_available": False, "semantic_indexed": False})
            if path == "/api/analyses":
                return APIResult(200, [sample_doc])
            if path == "/api/analyses/ana-stream-1":
                return APIResult(200, {**sample_doc, "chat_history": list(self.history)})
            return APIResult(404, None, "Not found")

        def stream_post(self, path: str, *, timeout: int = 180, json_body=None):
            q = (json_body or {}).get("question", "")
            yield {"type": "meta", "citations": [{"citation_id": "S1", "source_ref": "Paragraph 1", "passage": "Sarah Jenkins started..."}], "graph_context": {"relationships": []}, "timing": {"retrieval_ms": 0.4}}
            yield {"type": "token", "content": "Sarah Jenkins "}
            yield {"type": "token", "content": "started the garden [S1]."}
            turn = {
                "question": q,
                "answer": "Sarah Jenkins started the garden [S1].",
                "generation_mode": "ollama_grounded",
                "citations": [{"citation_id": "S1", "source_ref": "Paragraph 1", "passage": "Sarah Jenkins started..."}],
                "graph_context": {"relationships": []},
                "timing": {"total_ms": 2100.0, "ttft_ms": 320.0},
            }
            self.history.append(turn)
            yield {"type": "done", "turn": turn}

        def delete(self, path: str, *, timeout: int = 10):
            self.history.clear()
            return APIResult(200, {"status": "cleared"})

    monkeypatch.setattr("KnowledgeGraphAI.frontend.components.api_client.APIClient", _StreamingFakeClient)
    monkeypatch.setattr("KnowledgeGraphAI.frontend.app.APIClient", _StreamingFakeClient)

    app_path = Path(__file__).resolve().parent.parent / "frontend" / "app.py"
    at = AppTest.from_file(str(app_path), default_timeout=20).run()
    assert not at.exception

    ask_inputs = [ti for ti in at.text_input if ti.key == "sidebar_askme_input_ana-stream-1"]
    assert ask_inputs
    ask_inputs[0].set_value("What was Sarah's role?")
    send_btns = [btn for btn in at.button if btn.label == "Send"]
    assert send_btns
    send_btns[0].click().run()
    assert not at.exception

    rendered_html = "\n".join(m.value for m in at.markdown)
    assert "What was Sarah" in rendered_html
    assert "Sarah Jenkins started the garden [S1]." in rendered_html
    assert "OLLAMA GROUNDED" in rendered_html


