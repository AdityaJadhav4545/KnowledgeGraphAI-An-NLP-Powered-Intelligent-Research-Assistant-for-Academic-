import os

import pytest

from KnowledgeGraphAI.backend.services.semantic_retrieval.assisted_annotation import (
    suggest_relevance,
)


@pytest.mark.skipif(
    os.getenv("RUN_OLLAMA_ANNOTATION_TESTS") != "1",
    reason="set RUN_OLLAMA_ANNOTATION_TESTS=1 to call local Ollama",
)
def test_live_ollama_relevance_suggestion():
    suggestion = suggest_relevance(
        "Does the paper present a transformer architecture based only on attention?",
        "Attention Is All You Need",
        (
            "We propose the Transformer, a model architecture based solely on "
            "attention mechanisms, dispensing with recurrence and convolutions."
        ),
        (
            "We propose a new simple network architecture, the Transformer, "
            "based solely on attention mechanisms."
        ),
    )

    assert suggestion["label"] in {"relevant", "not_relevant", "uncertain"}
    assert 0.0 <= suggestion["confidence"] <= 1.0
    assert suggestion["explanation"]
    assert suggestion["model"]
