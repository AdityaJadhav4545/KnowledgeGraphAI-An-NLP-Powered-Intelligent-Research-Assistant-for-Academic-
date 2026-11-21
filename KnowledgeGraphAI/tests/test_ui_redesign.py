"""Streamlit AppTest and design-token regression checks for the Industrial UI redesign."""

from __future__ import annotations

import base64
from typing import Any, Dict

from streamlit.testing.v1 import AppTest

from KnowledgeGraphAI.frontend.components.api_client import APIResult
from KnowledgeGraphAI.frontend.components.graph_view import (
    build_interactive_figure,
    filter_subgraph,
)
from KnowledgeGraphAI.frontend.components.theme import (
    ENTITY_PALETTES,
    MAX_SPLIT_PCT,
    MIN_SPLIT_PCT,
    THEMES,
    get_entity_color,
)
from KnowledgeGraphAI.frontend.components.ui import PROCESSING_STAGES, geometric_logo_svg


def _sample_analysis(aid: str = "ana-ui-1", title: str = "Word2Vec Research Study") -> Dict[str, Any]:
    return {
        "analysis_id": aid,
        "source_type": "pdf",
        "title": title,
        "author": "Tomas Mikolov et al.",
        "publication_info": "arXiv:1301.3781",
        "page_count": 12,
        "status": "completed",
        "stage": "completed",
        "entity_count": 3,
        "relationship_count": 2,
        "category_count": 3,
        "passage_count": 5,
        "entities": [
            {
                "id": "n1",
                "label": "Skip-gram",
                "category": "Model",
                "occurrences": 4,
                "degree": 2,
                "confidence": 0.92,
                "aliases": ["Continuous Skip-gram"],
                "source_refs": ["Page 2"],
                "sample_context": "Skip-gram predicts surrounding words given the current word.",
            },
            {
                "id": "n2",
                "label": "Google News",
                "category": "Dataset",
                "occurrences": 2,
                "degree": 1,
                "confidence": 0.88,
                "aliases": [],
                "source_refs": ["Page 4"],
                "sample_context": "Trained on a Google News corpus.",
            },
            {
                "id": "n3",
                "label": "Accuracy",
                "category": "Metric",
                "occurrences": 3,
                "degree": 1,
                "confidence": 0.9,
                "aliases": [],
                "source_refs": ["Page 5"],
                "sample_context": "Semantic-syntactic word relationship accuracy.",
            },
        ],
        "graph": {
            "nodes": [
                {
                    "id": "n1",
                    "label": "Skip-gram",
                    "category": "Model",
                    "occurrences": 4,
                    "degree": 2,
                    "confidence": 0.92,
                    "aliases": ["Continuous Skip-gram"],
                    "source_refs": ["Page 2"],
                    "sample_context": "Skip-gram predicts surrounding words given the current word.",
                },
                {
                    "id": "n2",
                    "label": "Google News",
                    "category": "Dataset",
                    "occurrences": 2,
                    "degree": 1,
                    "confidence": 0.88,
                    "aliases": [],
                    "source_refs": ["Page 4"],
                    "sample_context": "Trained on a Google News corpus.",
                },
                {
                    "id": "n3",
                    "label": "Accuracy",
                    "category": "Metric",
                    "occurrences": 3,
                    "degree": 1,
                    "confidence": 0.9,
                    "aliases": [],
                    "source_refs": ["Page 5"],
                    "sample_context": "Semantic-syntactic word relationship accuracy.",
                },
            ],
            "edges": [
                {
                    "source": "n1",
                    "target": "n2",
                    "source_label": "Skip-gram",
                    "target_label": "Google News",
                    "relation": "TRAINED_ON",
                    "confidence": 0.91,
                    "source_ref": "Page 4",
                    "page_number": 4,
                },
                {
                    "source": "n1",
                    "target": "n3",
                    "source_label": "Skip-gram",
                    "target_label": "Accuracy",
                    "relation": "EVALUATED_ON",
                    "confidence": 0.89,
                    "source_ref": "Page 5",
                    "page_number": 5,
                },
            ],
            "stats": {"total_entities": 3, "total_relationships": 2},
        },
        "chat_history": [
            {
                "question": "Which dataset was Skip-gram trained on?",
                "answer": "Skip-gram was trained on the Google News corpus [S1].",
                "generation_mode": "graph_rag",
                "citations": [
                    {
                        "citation_id": "S1",
                        "source_ref": "Page 4 · Experiments",
                        "page_number": 4,
                        "similarity_score": 0.87,
                        "passage": "We trained Skip-gram on the Google News dataset and evaluated word analogy accuracy.",
                    }
                ],
                "graph_context": {
                    "available": True,
                    "entity_count": 3,
                    "relationship_count": 2,
                    "relationships": [
                        {
                            "subject": "Skip-gram",
                            "relation": "TRAINED_ON",
                            "object": "Google News",
                            "source_ref": "Page 4",
                        }
                    ],
                },
            }
        ],
    }


def _sample_report(aid: str = "ana-ui-1") -> Dict[str, Any]:
    return {
        "generated_at": "2026-11-10T10:00:00Z",
        "document_information": {
            "title": "Word2Vec Research Study",
            "authors": "Tomas Mikolov et al.",
            "publication_info": "arXiv:1301.3781",
            "source_type": "PDF Document",
            "analysis_date": "2026-11-10",
        },
        "executive_summary": "This paper proposes CBOW and Skip-gram architectures for dense word embeddings.",
        "introduction_and_objective": "Goal is learning high-quality vector representations efficiently at scale.",
        "key_concepts_and_entities": [
            {
                "entity": "Skip-gram",
                "category": "Model",
                "occurrences": 4,
                "description": "Predicts surrounding context words.",
            }
        ],
        "knowledge_graph_summary": {"total_entities": 3, "category_count": 3, "total_relationships": 2},
        "important_relationships": [
            {
                "subject": "Skip-gram",
                "relationship": "TRAINED_ON",
                "object": "Google News",
                "source": "Page 4",
            }
        ],
        "methodology_and_techniques": "Log-linear continuous vector architectures trained with negative sampling.",
        "important_findings": "Skip-gram excels on semantic analogies at scale.",
        "limitations": "Word-level representations ignore subword morphology.",
        "conclusion": "Efficient linear architectures outperform deeper neural baselines on analogy tasks.",
        "references_and_traceability": [
            {
                "ref": "[S1]",
                "section": "Page 4 · Experiments",
                "excerpt": "Trained on the Google News corpus.",
            }
        ],
    }


# Tiny 1x1 PNG bytes for embedded graph image preview
_TINY_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


def test_theme_tokens_logo_and_graph_palettes():
    obsidian = THEMES["obsidian"]
    limestone = THEMES["limestone"]

    assert obsidian["bg_main"] == "#171918"
    assert obsidian["surface"] == "#202321"
    assert obsidian["surface_elevated"] == "#2B302D"
    assert obsidian["accent"] == "#B69A60"
    assert obsidian["text_primary"] == "#E8E4DA"

    assert limestone["bg_main"] == "#F2F0E9"
    assert limestone["surface"] == "#FFFFFF"
    assert limestone["surface_elevated"] == "#E7E4DA"
    assert limestone["accent"] == "#927744"
    assert limestone["text_primary"] == "#252925"

    svg = geometric_logo_svg("obsidian")
    assert "<svg" in svg and "KnowledgeGraphAI" in svg
    assert "brain" not in svg.lower()
    assert len(PROCESSING_STAGES) == 6

    sample = _sample_analysis()
    nodes, edges = filter_subgraph(sample["graph"], search_query="Google")
    assert {n["id"] for n in nodes} == {"n1", "n2"}
    assert len(edges) == 1

    for tname in ("obsidian", "limestone"):
        fig, flat_ids = build_interactive_figure(
            sample["graph"]["nodes"],
            sample["graph"]["edges"],
            selected_node_id="n1",
            theme_name=tname,
        )
        assert len(flat_ids) == 3
        assert fig.layout.paper_bgcolor == THEMES[tname]["graph_bg"]
        assert get_entity_color("Model", tname) == ENTITY_PALETTES[tname]["Model"]


def test_streamlit_apptest_navigation_and_dual_themes(monkeypatch):
    analysis = _sample_analysis()
    report = _sample_report()

    class FakeAPIClient:
        def __init__(self, *args, **kwargs):
            self.history = list(analysis["chat_history"])

        def get(self, path: str, *, timeout: int = 10, params=None):
            if path == "/health":
                return APIResult(
                    200,
                    {"status": "ok", "neo4j_available": True, "semantic_indexed": True},
                    None,
                )
            if path == "/api/analyses":
                return APIResult(200, [analysis], None)
            if path.startswith("/api/analyses/ana-ui-1/report/pdf"):
                return APIResult(200, b"%PDF-1.4\n%mock", None, content_type="application/pdf")
            if path.startswith("/api/analyses/ana-ui-1/report"):
                return APIResult(200, report, None)
            if path.startswith("/api/analyses/ana-ui-1/graph/image"):
                return APIResult(200, _TINY_PNG, None, content_type="image/png")
            if path == "/api/analyses/ana-ui-1":
                payload = dict(analysis)
                payload["chat_history"] = list(self.history)
                return APIResult(200, payload, None)
            return APIResult(404, None, "Not found")

        def post(self, path: str, *, timeout: int = 30, files=None, data=None, json_body=None):
            if path == "/api/analyses/ana-ui-1/ask":
                q = (json_body or {}).get("question", "")
                turn = {
                    "question": q,
                    "answer": f"Grounded answer for: {q} [S1]",
                    "generation_mode": "evidence_only",
                    "citations": analysis["chat_history"][0]["citations"],
                    "graph_context": [],
                }
                self.history.append(turn)
                return APIResult(200, turn, None)
            if path == "/api/analyses/text":
                assert timeout == 180
                assert json_body and json_body.get("text")
                return APIResult(201, analysis, None)
            return APIResult(200, {}, None)

        def delete(self, path: str, *, timeout: int = 10):
            if path == "/api/analyses/ana-ui-1/chat":
                self.history.clear()
                return APIResult(200, {"cleared": True}, None)
            return APIResult(200, {}, None)

    monkeypatch.setattr("KnowledgeGraphAI.frontend.components.api_client.APIClient", FakeAPIClient)
    monkeypatch.setattr("KnowledgeGraphAI.frontend.app.APIClient", FakeAPIClient)

    at = AppTest.from_file("frontend/app.py", default_timeout=20)
    at.run()
    assert not at.exception
    assert at.session_state["theme"] == "obsidian"
    assert at.query_params["theme"] in ("obsidian", ["obsidian"])
    assert at.session_state["sidebar_collapsed"] is False
    assert at.query_params["sidebar"] in ("expanded", ["expanded"])
    assert MIN_SPLIT_PCT <= at.session_state["explore_split_pct"] <= MAX_SPLIT_PCT

    # Ask a question from the boxed Ask Me sidebar assistant
    chat_input = [t for t in at.text_input if t.key == "sidebar_askme_input_ana-ui-1"][0]
    chat_input.set_value("How is Skip-gram trained?")
    send_btns = [b for b in at.button if b.label == "Send"]
    assert send_btns
    send_btns[0].click().run()
    assert not at.exception

    # Theme button reflects actual active theme (Obsidian -> click -> Limestone)
    theme_btn = [b for b in at.button if "Theme:" in b.label][0]
    assert theme_btn.label == "Theme: Obsidian (Dark)"
    theme_btn.click().run()
    assert not at.exception
    assert at.session_state["theme"] == "limestone"
    assert at.query_params["theme"] in ("limestone", ["limestone"])
    theme_btn_after = [b for b in at.button if "Theme:" in b.label][0]
    assert theme_btn_after.label == "Theme: Limestone (Light)"

    # Test Paste Text analysis workflow
    text_title = [t for t in at.text_input if t.key == "analyze_text_title"][0]
    text_body = [t for t in at.text_area if t.key == "analyze_text_body"][0]
    text_title.set_value("Word2Vec Short Note")
    text_body.set_value("Skip-gram was trained on Google News and achieved strong accuracy.").run()
    run_text_btn = [b for b in at.button if b.key == "run_text_analysis_btn"][0]
    run_text_btn.click().run()
    assert not at.exception

    # Navigate to Explore Knowledge using left sidebar radio
    nav_radio = [r for r in at.radio if r.key == "nav_section"][0]
    nav_radio.set_value("Explore Knowledge").run()
    assert not at.exception
    assert at.session_state["theme"] == "limestone"

    # Focus an entity in Explore Knowledge via Document Insights button
    insight_ent_btn = [b for b in at.button if str(b.key or "").startswith("insights_focus_ent_")][0]
    insight_ent_btn.click().run()
    assert not at.exception

    # Collapse sidebar -> stays on Explore Knowledge and removes sidebar panel
    collapse_btn = [b for b in at.button if b.key == "sidebar_collapse_btn"][0]
    collapse_btn.click().run()
    assert not at.exception
    assert at.session_state["sidebar_collapsed"] is True
    assert at.query_params["sidebar"] in ("collapsed", ["collapsed"])
    assert at.session_state["active_nav"] == "Explore Knowledge"
    assert at.query_params["nav"] in ("Explore Knowledge", ["Explore Knowledge"])

    # Restore sidebar -> returns sidebar & preserves Explore Knowledge + theme
    restore_btn = [b for b in at.button if b.key == "sidebar_restore_btn"][0]
    restore_btn.click().run()
    assert not at.exception
    assert at.session_state["sidebar_collapsed"] is False
    assert at.query_params["sidebar"] in ("expanded", ["expanded"])
    assert at.session_state["nav_section"] == "Explore Knowledge"

    # Navigate to Generate Report
    nav_radio = [r for r in at.radio if r.key == "nav_section"][0]
    nav_radio.set_value("Generate Report").run()
    assert not at.exception
    html_blocks = at.get("html")
    assert html_blocks and any("11. References" in str(getattr(el, "body", getattr(el, "value", ""))) for el in html_blocks)
    dl_btns = at.get("download_button")
    assert dl_btns and any("Download PDF Report" in str(getattr(d, "label", "")) for d in dl_btns)

