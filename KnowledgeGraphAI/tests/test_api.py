import os
import json
import tempfile
import pytest
from unittest.mock import patch
from reportlab.pdfgen import canvas
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from KnowledgeGraphAI.backend.main import app
from KnowledgeGraphAI.backend.database import get_db, Base
from KnowledgeGraphAI.models.paper import Paper

# Configure SQLite in-memory engine with StaticPool to share connection across threads/sessions
TEST_DATABASE_URL = "sqlite:///"
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Ensure models are loaded before creating tables
from KnowledgeGraphAI.models.paper import Paper  # noqa

# Initialize tables
Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_db():
    # Clear tables before each test
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield
    # No need to drop all here if using StaticPool for shared in-memory DB
    # or you can drop if you want absolute isolation


def make_pdf(path: str, text: str = "Hello world", title: str = "Test", author: str = "A"):
    c = canvas.Canvas(path)
    c.setTitle(title)
    c.setAuthor(author)
    c.drawString(72, 720, text)
    c.showPage()
    c.save()


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_upload_invalid_file_type():
    files = {"file": ("x.txt", b"hello", "text/plain")}
    r = client.post("/api/papers/upload", files=files)
    assert r.status_code == 400


def test_upload_and_list():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "paper.pdf")
        make_pdf(p)
        with open(p, "rb") as f:
            files = {"file": ("paper.pdf", f.read(), "application/pdf")}
        r = client.post("/api/papers/upload", files=files)
        assert r.status_code == 201
        data = r.json()
        assert data["title"] == "Test"
        assert data["page_count"] == 1

    r = client.get("/api/papers")
    assert r.status_code == 200
    papers = r.json()
    assert len(papers) == 1
    assert papers[0]["id"] == data["id"]


def test_duplicate_detection():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "paper.pdf")
        make_pdf(p)
        with open(p, "rb") as f:
            content = f.read()
        files = {"file": ("paper.pdf", content, "application/pdf")}
        r1 = client.post("/api/papers/upload", files=files)
        assert r1.status_code == 201

        # Upload exact duplicate
        files2 = {"file": ("paper_copy.pdf", content, "application/pdf")}
        r2 = client.post("/api/papers/upload", files=files2)
        assert r2.status_code == 409


def test_get_and_delete():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "paper.pdf")
        make_pdf(p)
        with open(p, "rb") as f:
            files = {"file": ("paper.pdf", f.read(), "application/pdf")}
        r = client.post("/api/papers/upload", files=files)
        pid = r.json()["id"]

    r = client.get(f"/api/papers/{pid}")
    assert r.status_code == 200
    assert r.json()["id"] == pid

    r = client.delete(f"/api/papers/{pid}")
    assert r.status_code == 200

    r = client.get(f"/api/papers/{pid}")
    assert r.status_code == 404


def test_get_not_found():
    r = client.get("/api/papers/9999")
    assert r.status_code == 404


def test_process_paper():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "paper.pdf")
        make_pdf(p)
        with open(p, "rb") as f:
            files = {"file": ("paper.pdf", f.read(), "application/pdf")}
        r = client.post("/api/papers/upload", files=files)
        pid = r.json()["id"]

    with patch(
        "KnowledgeGraphAI.backend.api.papers.PaperProcessingService.process",
        return_value={
            "paper_id": pid,
            "status": "completed",
            "entity_count": 2,
            "relation_count": 1,
            "semantic_chunk_count": 3,
        },
    ):
        r = client.post(f"/api/papers/{pid}/process")
    assert r.status_code == 200
    assert r.json()["status"] == "completed"
