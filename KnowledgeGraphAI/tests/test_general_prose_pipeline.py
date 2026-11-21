"""Regression tests for general-purpose English prose NER, normalization, RE, and KG rendering."""

from __future__ import annotations

import pymupdf
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from KnowledgeGraphAI.backend.database import get_db
from KnowledgeGraphAI.backend.main import app
from KnowledgeGraphAI.backend.nlp.ner.entity_schema import ExtractedSentence
from KnowledgeGraphAI.backend.nlp.ner.ner_pipeline import NERPipeline
from KnowledgeGraphAI.backend.nlp.relation_extraction.relation_extraction_service import (
    extract_relations_from_paper,
)
from KnowledgeGraphAI.backend.services.knowledge_graph.graph_schema import (
    get_node_label,
    validate_relationship,
)
from KnowledgeGraphAI.frontend.components.graph_view import (
    build_interactive_figure,
    filter_subgraph,
)
from KnowledgeGraphAI.models.paper import Base

COMMUNITY_GARDEN_TEXT = (
    "A small community in a rural area decided to improve the quality of life for its residents "
    "by starting a community garden. The project was led by a local teacher named Sarah, who worked "
    "with farmers, students, and volunteers to turn an unused piece of land into a productive green "
    "space. The farmers shared their knowledge of seasonal crops and soil preparation, while students "
    "helped plant vegetables and maintain the garden. The local council provided basic equipment and "
    "access to clean water. Over time, the garden began producing tomatoes, spinach, carrots, and "
    "other vegetables that were shared among participating families. The project also encouraged "
    "people to work together, reduced food waste, and helped children understand the importance of "
    "nature and healthy eating. As the garden became successful, nearby communities showed interest in "
    "starting similar projects. Sarah believes that cooperation, shared responsibility, and community "
    "participation are the main reasons behind the project's success."
)


@pytest.fixture()
def isolated_prose_client(tmp_path, monkeypatch):
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
        yield TestClient(app)
    finally:
        if previous_override is not None:
            app.dependency_overrides[get_db] = previous_override
        else:
            app.dependency_overrides.pop(get_db, None)
        get_settings.cache_clear()


def test_general_prose_ner_and_relation_extraction_units():
    sentence = ExtractedSentence(
        paper_id=0,
        page_number=0,
        section_name="Body",
        paragraph_index=0,
        sentence_index=0,
        original_text=(
            "The project was led by a local teacher named Sarah, who worked with "
            "farmers, students, and volunteers to turn an unused piece of land into "
            "a productive green space."
        ),
        cleaned_text=(
            "The project was led by a local teacher named Sarah, who worked with "
            "farmers, students, and volunteers to turn an unused piece of land into "
            "a productive green space."
        ),
    )

    entities = NERPipeline(use_transformer=False, include_general_prose=True).extract_from_sentence(sentence).entities
    found = {(e.text, e.entity_type) for e in entities}

    assert ("project", "PROJECT") in found
    assert ("Sarah", "PERSON") in found
    assert ("farmers", "GROUP") in found
    assert ("students", "GROUP") in found
    assert ("volunteers", "GROUP") in found
    assert ("productive green space", "LOCATION") in found

    relations = extract_relations_from_paper(sentence.cleaned_text, entities, [sentence], paper_id=0)
    triples = {(r.subject_text, r.relation, r.object_text) for r in relations}

    assert ("project", "LED_BY", "Sarah") in triples
    assert ("Sarah", "WORKED_WITH", "farmers") in triples
    assert ("Sarah", "WORKED_WITH", "students") in triples
    assert ("Sarah", "WORKED_WITH", "volunteers") in triples
    assert ("Sarah", "CREATED", "productive green space") in triples
    # Cross-clause false positive must not leak LED_BY onto co-workers after ", who worked with".
    assert ("project", "LED_BY", "farmers") not in triples

    for rel in relations:
        assert validate_relationship(
            rel.relation,
            get_node_label(rel.subject_entity_type),
            get_node_label(rel.object_entity_type),
        )


def test_community_garden_end_to_end_analysis_graph_report_and_chat(isolated_prose_client):
    resp = isolated_prose_client.post(
        "/api/analyses/text",
        json={"text": COMMUNITY_GARDEN_TEXT},
    )
    assert resp.status_code == 201, resp.text
    data = resp.json()
    aid = data["analysis_id"]

    assert data["status"] == "completed"
    assert data["passage_count"] == 1
    assert data["entity_count"] >= 15
    assert data["relationship_count"] >= 15

    nodes = data["graph"]["nodes"]
    edges = data["graph"]["edges"]
    assert len(nodes) == data["entity_count"]
    assert len(edges) == data["relationship_count"]

    nodes_by_label = {n["label"]: n for n in nodes}
    for expected in (
        "Sarah",
        "local council",
        "community garden",
        "rural area",
        "farmers",
        "students",
        "volunteers",
        "tomatoes",
        "spinach",
        "carrots",
        "basic equipment",
        "clean water",
        "food waste",
        "healthy eating",
        "cooperation",
    ):
        assert expected in nodes_by_label, f"Missing expected entity {expected!r}: {list(nodes_by_label)}"

    assert nodes_by_label["Sarah"]["category"] == "Person"
    assert nodes_by_label["local council"]["category"] == "Organization"
    assert nodes_by_label["community garden"]["category"] == "Project"
    assert nodes_by_label["rural area"]["category"] == "Location"
    assert nodes_by_label["tomatoes"]["category"] == "Product"
    assert nodes_by_label["cooperation"]["category"] == "Concept"

    # Generic anaphoric mentions ("project", "garden") must normalize onto "community garden".
    assert "project" not in nodes_by_label
    assert "garden" not in nodes_by_label
    assert nodes_by_label["community garden"]["occurrences"] >= 4
    assert {"project", "garden"}.issubset(set(nodes_by_label["community garden"]["aliases"]))

    edge_triples = {(e["source_label"], e["relation"], e["target_label"]) for e in edges}
    assert ("community garden", "LED_BY", "Sarah") in edge_triples
    assert ("Sarah", "WORKED_WITH", "farmers") in edge_triples
    assert ("local council", "PROVIDED", "basic equipment") in edge_triples
    assert ("local council", "PROVIDED", "clean water") in edge_triples
    assert ("community garden", "PRODUCED", "tomatoes") in edge_triples
    assert ("community garden", "REDUCED", "food waste") in edge_triples
    assert ("Sarah", "BELIEVES_IN", "cooperation") in edge_triples

    # Frontend fetches the same persisted graph & renders non-empty interactive figure.
    fetched = isolated_prose_client.get(f"/api/analyses/{aid}").json()
    assert fetched["graph"]["stats"]["total_entities"] == len(nodes)
    assert fetched["graph"]["stats"]["total_relationships"] == len(edges)

    filtered_nodes, filtered_edges = filter_subgraph(fetched["graph"])
    assert len(filtered_nodes) >= 15
    assert len(filtered_edges) >= 10
    fig, flat_ids = build_interactive_figure(filtered_nodes, filtered_edges, theme_name="obsidian")
    assert len(flat_ids) == len(filtered_nodes)
    assert len(fig.data) >= 2

    # Assistant QA & PDF report continue working cleanly.
    ask = isolated_prose_client.post(f"/api/analyses/{aid}/ask", json={"question": "Who led the project and what did the local council provide?"})
    assert ask.status_code == 200
    assert ask.json()["citations"]

    pdf_dl = isolated_prose_client.get(f"/api/analyses/{aid}/report/pdf")
    assert pdf_dl.status_code == 200
    assert pdf_dl.content[:5] == b"%PDF-"
    doc = pymupdf.open(stream=pdf_dl.content, filetype="pdf")
    assert len(doc) >= 1
    doc.close()


def test_unrelated_general_prose_works_without_hardcoding(isolated_prose_client):
    coastal_text = (
        "Maya founded a coastal recycling program in Brighton to cut plastic pollution. "
        "The town council provided collection bins and electric vans, while local students "
        "worked with volunteers to sort glass, paper, and aluminum cans."
    )
    resp = isolated_prose_client.post(
        "/api/analyses/text",
        json={"text": coastal_text, "title": "Coastal Recycling Program"},
    )
    assert resp.status_code == 201, resp.text
    data = resp.json()
    labels = {n["label"] for n in data["graph"]["nodes"]}
    triples = {(e["source_label"], e["relation"], e["target_label"]) for e in data["graph"]["edges"]}

    assert {"Maya", "coastal recycling program", "Brighton", "town council", "collection bins", "electric vans", "local students", "volunteers", "plastic pollution"}.issubset(labels)
    assert ("Maya", "STARTED", "coastal recycling program") in triples
    assert ("coastal recycling program", "LOCATED_IN", "Brighton") in triples
    assert ("town council", "PROVIDED", "collection bins") in triples
    assert ("town council", "PROVIDED", "electric vans") in triples
    assert ("local students", "WORKED_WITH", "volunteers") in triples

