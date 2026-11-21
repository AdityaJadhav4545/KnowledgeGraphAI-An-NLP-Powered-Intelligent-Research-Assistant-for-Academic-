from pathlib import Path

from KnowledgeGraphAI.backend.config import Settings
from KnowledgeGraphAI.backend.services.research_assistant.graph_rag import GraphRAGService


class _Semantic:
    def search(self, *_args, **_kwargs):
        return [{
            "paper_id": 7,
            "chunk_id": "chunk-7",
            "title": "Evidence Paper",
            "text": "BERT was evaluated on the SQuAD dataset.",
            "page_number": 3,
            "section_title": "Results",
            "similarity_score": 0.9,
        }]


class _Graph:
    def get_paper_entities(self, _paper_id):
        return [{"name": "BERT"}]

    def get_paper_relationships(self, _paper_id):
        return [{"relation": "EVALUATED_ON"}]


class _Response:
    def __init__(self, answer):
        self.answer = answer

    def raise_for_status(self):
        return None

    def json(self):
        return {"message": {"content": self.answer}}


class _Http:
    def __init__(self, answer):
        self.answer = answer

    def post(self, *_args, **_kwargs):
        return _Response(self.answer)


def _settings(tmp_path):
    return Settings(
        environment="testing",
        debug=False,
        database_url="sqlite://",
        upload_dir=tmp_path / "raw",
        processed_dir=tmp_path / "processed",
        max_upload_bytes=1024,
        cors_origins=("http://testserver",),
        api_key=None,
        require_authentication=False,
        neo4j_required=False,
        semantic_required=False,
        ollama_base_url="http://localhost:11434",
        ollama_model="llama3.1",
        ollama_timeout_seconds=10,
    )


def test_graph_rag_returns_only_valid_retrieved_citations(tmp_path):
    service = GraphRAGService(
        settings=_settings(tmp_path),
        semantic_service=_Semantic(),
        graph_query_service=_Graph(),
        http_session=_Http("BERT is evaluated on SQuAD. [S1]"),
    )
    result = service.ask("What evaluates BERT?")
    assert result["generation_mode"] == "ollama_grounded"
    assert result["citations"][0]["citation_id"] == "S1"
    assert "[S1]" in result["answer"]


def test_graph_rag_downgrades_invalid_llm_citation_to_evidence_only(tmp_path):
    service = GraphRAGService(
        settings=_settings(tmp_path),
        semantic_service=_Semantic(),
        graph_query_service=_Graph(),
        http_session=_Http("Unsupported claim. [S99]"),
    )
    result = service.ask("What evaluates BERT?")
    assert result["generation_mode"] == "evidence_only"
    assert "[S1]" in result["answer"]


def test_graph_rag_includes_neo4j_entities_and_relationships_in_llm_prompt(tmp_path):
    captured = {}

    class _CapturingHttp:
        def post(self, _url, json=None, timeout=None):
            captured["prompt"] = json["messages"][0]["content"]
            return _Response("BERT was evaluated on SQuAD [S1].")

    class _RichGraph:
        def get_paper_entities(self, _paper_id):
            return [
                {"e": {"canonical_name": "BERT"}, "labels": ["Model"]},
                {"e": {"canonical_name": "SQuAD"}, "labels": ["Dataset"]},
            ]

        def get_paper_relationships(self, _paper_id):
            return [{"subject": "BERT", "relation": "EVALUATED_ON", "object": "SQuAD"}]

        def search_entities(self, _term, limit=2):
            return [{"entity_id": "model_bert", "canonical_name": "BERT", "labels": ["Model"]}]

        def get_entity_neighbors(self, _eid, _etype, limit=8):
            return [{"canonical_name": "SQuAD", "relationship_type": "EVALUATED_ON", "labels": ["Dataset"]}]

    service = GraphRAGService(
        settings=_settings(tmp_path),
        semantic_service=_Semantic(),
        graph_query_service=_RichGraph(),
        http_session=_CapturingHttp(),
    )
    result = service.ask("How is BERT evaluated?")
    assert result["generation_mode"] == "ollama_grounded"
    assert result["graph_context"]["available"] is True
    assert "BERT (Model)" in captured["prompt"]
    assert "BERT -[EVALUATED_ON]-> SQuAD" in captured["prompt"]
