from pathlib import Path
from types import SimpleNamespace

from KnowledgeGraphAI.backend.config import Settings
from KnowledgeGraphAI.backend.services.paper_processing import (
    PaperProcessingService,
)


class _Session:
    def __init__(self):
        self.commits = 0

    def add(self, _value):
        pass

    def commit(self):
        self.commits += 1

    def refresh(self, _value):
        pass


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


def test_transition_records_state_and_never_claims_completion(tmp_path):
    paper = SimpleNamespace(
        id=1,
        metadata_json={},
        status="uploaded",
        updated_at=None,
        processing_started_at=None,
        processing_completed_at=None,
        processing_error=None,
    )
    session = _Session()
    service = PaperProcessingService(session, settings=_settings(tmp_path))

    service._transition(paper, "extracting")
    assert paper.status == "extracting"
    assert paper.processing_started_at is not None
    assert paper.processing_completed_at is None

    service._transition(paper, "failed", stage="graph_indexing", error="Neo4j unavailable")
    assert paper.status == "failed"
    assert paper.processing_error == "Neo4j unavailable"
    assert paper.metadata_json["processing_events"][-1]["stage"] == "graph_indexing"


def test_sentence_rehydration_preserves_global_provenance():
    result = {
        "paper_id": 9,
        "paragraphs": [
            {
                "sentences": [
                    {
                        "paper_id": 9,
                        "page_number": 2,
                        "section_name": "Results",
                        "paragraph_index": 4,
                        "sentence_index": 7,
                        "original_text": "BERT achieved F1.",
                        "cleaned_text": "BERT achieved F1.",
                    }
                ]
            }
        ],
    }
    sentence = PaperProcessingService._sentences(result)[0]
    assert (sentence.paper_id, sentence.page_number, sentence.sentence_index) == (9, 2, 7)
