import os
import json
import uuid
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest
import torch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from KnowledgeGraphAI.backend.services.semantic_retrieval.chunking_service import (
    ScientificChunkingService,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.config import (
    SemanticRetrievalConfig,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.embedding_service import (
    Specter2EmbeddingService,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.evaluation import (
    evaluate_dataset,
    retrieval_metrics,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.metadata_store import (
    ChunkMetadataStore,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.retrieval_service import (
    SemanticRetrievalService,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.vector_store import (
    FaissVectorStore,
)
from KnowledgeGraphAI.backend.services.knowledge_graph.neo4j_connection import (
    get_neo4j_manager,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval import validation


def _preprocessing_result():
    return {
        "paper_id": 41,
        "paragraphs": [
            {
                "page_number": 1,
                "paragraph_index": 0,
                "section_name": "Methods",
                "sentences": [
                    {
                        "page_number": 1,
                        "sentence_index": 0,
                        "original_text": "BERT is a transformer.",
                        "cleaned_text": "BERT is a transformer.",
                    },
                    {
                        "page_number": 1,
                        "sentence_index": 1,
                        "original_text": "It was evaluated on SQuAD.",
                        "cleaned_text": "It was evaluated on SQuAD.",
                    },
                ],
            },
            {
                "page_number": 1,
                "paragraph_index": 1,
                "section_name": "Results",
                "sentences": [
                    {
                        "page_number": 1,
                        "sentence_index": 2,
                        "original_text": "Adam improved the F1 score.",
                        "cleaned_text": "Adam improved the F1 score.",
                    }
                ],
            },
        ],
    }


class _FakeTokenizer:
    sep_token = "[SEP]"

    def __call__(self, texts, **_kwargs):
        return {"input_ids": torch.tensor([[len(text), 1] for text in texts])}


class _FakeModel:
    config = SimpleNamespace(hidden_size=3)

    def __init__(self):
        self.active_adapter = None

    def to(self, _device):
        return self

    def eval(self):
        return self

    def set_active_adapters(self, adapter):
        self.active_adapter = adapter

    def __call__(self, input_ids):
        batch, sequence = input_ids.shape
        cls = torch.stack(
            (input_ids[:, 0].float(), torch.ones(batch), torch.full((batch,), 2.0)),
            dim=1,
        )
        return SimpleNamespace(
            last_hidden_state=torch.cat((cls[:, None, :], torch.zeros(batch, sequence - 1, 3)), dim=1)
        )


class _LexicalEmbedding:
    vocabulary = ("bert", "transformer", "squad", "adam", "optimizer", "f1", "score", "neural")

    def _encode(self, texts):
        vectors = np.zeros((len(texts), len(self.vocabulary)), dtype=np.float32)
        for row, text in enumerate(texts):
            lowered = text.lower()
            for column, term in enumerate(self.vocabulary):
                vectors[row, column] = lowered.count(term)
            if not np.any(vectors[row]):
                vectors[row, -1] = 1.0
        return vectors

    def embed_documents(self, texts, titles=None):
        return self._encode(texts)

    def embed_queries(self, texts):
        return self._encode(texts)


class _FakeNeo4jManager:
    def execute_query(self, _query, parameters):
        return [{"paper_id": parameters["paper_id"]}]


def _store(tmp_path, dimension=8):
    database_path = tmp_path / "semantic.sqlite"
    engine = create_engine(
        f"sqlite:///{database_path}",
        connect_args={"check_same_thread": False},
    )
    metadata = ChunkMetadataStore(sessionmaker(bind=engine, expire_on_commit=False))
    vector_store = FaissVectorStore(
        dimension,
        tmp_path / "scientific.index",
        metadata_store=metadata,
    )
    return engine, metadata, vector_store


def test_chunking_is_paragraph_bounded_and_preserves_page_offsets():
    source = (
        "BERT is a transformer. It was evaluated on SQuAD.\n\n"
        "Adam improved the F1 score."
    )
    chunks = ScientificChunkingService(chunk_size=20, overlap=0).chunk(
        _preprocessing_result(),
        "paper.pdf",
        page_texts={1: source},
    )

    assert len(chunks) == 2
    assert chunks[0].text == "BERT is a transformer. It was evaluated on SQuAD."
    assert chunks[0].start_char == source.index("BERT")
    assert chunks[0].end_char == source.index("SQuAD.") + len("SQuAD.")
    assert chunks[1].text == "Adam improved the F1 score."
    assert chunks[1].start_char == source.index("Adam")
    assert chunks[1].end_char == len(source)


def test_chunking_is_deterministic_and_overlap_stays_within_paragraph():
    result = {
        "paper_id": 9,
        "paragraphs": [
            {
                "paragraph_index": 0,
                "sentences": [
                    {"cleaned_text": "one two three", "page_number": 1},
                    {"cleaned_text": "four five six", "page_number": 1},
                ],
            },
            {
                "paragraph_index": 1,
                "sentences": [{"cleaned_text": "seven eight", "page_number": 1}],
            },
        ],
    }
    chunker = ScientificChunkingService(chunk_size=4, overlap=2)
    first = chunker.chunk(result, "source.pdf")
    second = chunker.chunk(result, "source.pdf")

    assert [chunk.chunk_id for chunk in first] == [chunk.chunk_id for chunk in second]
    assert [chunk.text for chunk in first] == ["one two three", "four five six", "seven eight"]


def test_specter2_embedding_uses_separate_adapters_and_normalizes():
    model = _FakeModel()
    service = Specter2EmbeddingService(
        SemanticRetrievalConfig.from_env(),
        tokenizer=_FakeTokenizer(),
        model=model,
    )

    documents = service.embed_documents(["BERT"], titles=["Paper"])
    queries = service.embed_queries(["BERT"])

    assert documents.shape == (1, 3)
    assert queries.shape == (1, 3)
    assert np.linalg.norm(documents[0]) == pytest.approx(1.0)
    assert np.linalg.norm(queries[0]) == pytest.approx(1.0)
    assert model.active_adapter == "specter2_adhoc_query"
    assert service.embed_documents([]).shape == (0, 3)


def test_vector_store_persists_metadata_rebuilds_and_is_idempotent(tmp_path):
    engine, metadata, vector_store = _store(tmp_path)
    chunk = {
        "chunk_id": "stable-id",
        "paper_id": 41,
        "chunk_index": 0,
        "text": "BERT is a transformer.",
        "page_number": 2,
        "section_title": "Methods",
        "start_char": 8,
        "end_char": 30,
        "source_document": "paper.pdf",
    }
    vector = np.array([[1, 0, 0, 0, 0, 0, 0, 0]], dtype=np.float32)

    first_ids = vector_store.add([chunk], vector)
    second_ids = vector_store.add([chunk], vector)

    assert first_ids == second_ids
    assert vector_store.count == 1
    assert vector_store.search(vector[0], 5)[0][0] == first_ids[0]
    assert vector_store.get_metadata(first_ids)[first_ids[0]]["page_number"] == 2

    reopened = FaissVectorStore(
        8,
        tmp_path / "scientific.index",
        metadata_store=ChunkMetadataStore(
            sessionmaker(bind=engine, expire_on_commit=False)
        ),
    )
    assert reopened.count == 1
    assert reopened.search(vector[0], 1)[0][1] == pytest.approx(1.0)
    assert reopened.delete_paper(41) == 1
    assert reopened.count == 0
    engine.dispose()


def test_semantic_search_ranks_and_returns_chunk_metadata(tmp_path):
    _engine, _metadata, vector_store = _store(tmp_path)
    chunker = ScientificChunkingService(chunk_size=30, overlap=0)
    service = SemanticRetrievalService(
        chunker=chunker,
        embedding_service=_LexicalEmbedding(),
        vector_store=vector_store,
        neo4j_manager=_FakeNeo4jManager(),
    )

    chunks = service.index_preprocessed(
        _preprocessing_result(),
        "paper.pdf",
        paper_title="BERT research",
    )
    results = service.search("BERT transformer SQuAD", top_k=3)

    assert chunks
    assert results[0]["text"].startswith("BERT")
    assert results[0]["paper_id"] == 41
    assert results[0]["title"] == "BERT research"
    assert results[0]["page_number"] == 1
    assert results[0]["rank"] == 1
    assert results[0]["similarity_score"] <= 1.0
    assert service.search("BERT transformer SQuAD", top_k=1)[0]["chunk_id"] == results[0]["chunk_id"]
    with pytest.raises(ValueError, match="non-empty"):
        service.search("", top_k=3)


def test_search_filters_similarity_aggregation_and_diversity(tmp_path):
    _engine, _metadata, vector_store = _store(tmp_path, dimension=8)
    embedding = _LexicalEmbedding()
    chunks = [
        {
            "chunk_id": "bert-page-1",
            "paper_id": 1,
            "chunk_index": 0,
            "title": "BERT evaluation",
            "text": "BERT SQuAD",
            "page_number": 1,
            "section_title": "Methods",
            "source_document": "bert-one.pdf",
        },
        {
            "chunk_id": "bert-page-2",
            "paper_id": 1,
            "chunk_index": 1,
            "title": "BERT evaluation",
            "text": "BERT SQuAD",
            "page_number": 2,
            "section_title": "Results",
            "source_document": "bert-one.pdf",
        },
        {
            "chunk_id": "bert-paper-2",
            "paper_id": 2,
            "chunk_index": 0,
            "title": "Transformer evaluation",
            "text": "BERT SQuAD transformer",
            "page_number": 1,
            "section_title": "Methods",
            "source_document": "bert-two.pdf",
        },
        {
            "chunk_id": "adam-paper",
            "paper_id": 3,
            "chunk_index": 0,
            "title": "Adam optimizer",
            "text": "Adam optimizer F1 score",
            "page_number": 1,
            "section_title": "Results",
            "source_document": "adam.pdf",
        },
    ]
    vectors = embedding.embed_documents([chunk["text"] for chunk in chunks])
    vector_store.add(chunks, vectors)
    service = SemanticRetrievalService(
        embedding_service=embedding,
        vector_store=vector_store,
        neo4j_manager=object(),
    )

    assert {
        row["paper_id"]
        for row in service.search("BERT SQuAD", paper_id=1, top_k=5)
    } == {1}
    page_results = service.search("BERT SQuAD", page_number=2, top_k=5)
    assert [row["chunk_id"] for row in page_results] == ["bert-page-2"]
    section_results = service.search(
        "BERT SQuAD", section_title="methods", top_k=5
    )
    assert {row["chunk_id"] for row in section_results} == {
        "bert-page-1",
        "bert-paper-2",
    }
    threshold_results = service.search(
        "BERT SQuAD", min_similarity=0.99, top_k=5
    )
    assert threshold_results
    assert all(row["similarity_score"] >= 0.99 for row in threshold_results)

    aggregated = service.search(
        "BERT SQuAD", top_k=5, aggregate_by_paper=True
    )
    paper_one = next(row for row in aggregated if row["paper_id"] == 1)
    assert paper_one["matched_chunk_count"] == 2
    assert paper_one["title"] == "BERT evaluation"
    diverse = service.search(
        "BERT SQuAD", top_k=2, diversity=True, diversity_lambda=0.6
    )
    assert len({row["paper_id"] for row in diverse}) == 2
    assert all(row["reranking_score"] is not None for row in diverse)
    assert all(-1.0 <= row["similarity_score"] <= 1.0 for row in diverse)

    with pytest.raises(ValueError, match="similarity"):
        service.search("BERT", min_similarity=2)


def test_retrieval_metrics_and_synthetic_evaluation_dataset():
    assert retrieval_metrics(
        ["irrelevant", "relevant", "relevant"],
        ["relevant"],
        3,
    ) == {
        "precision@3": pytest.approx(1 / 3),
        "recall@3": 1.0,
        "reciprocal_rank": 0.5,
        "average_precision@3": 0.5,
    }
    dataset_path = (
        Path(__file__).parents[1]
        / "backend"
        / "services"
        / "semantic_retrieval"
        / "evaluation_dataset.json"
    )
    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
    assert dataset["label_type"] == "synthetic"
    results = evaluate_dataset(
        dataset,
        lambda query, _k: [
            {"chunk_id": dataset["queries"][0]["relevant_chunk_ids"][0]}
        ],
        k=1,
    )
    assert results["label_type"] == "synthetic"
    assert results["aggregate"]["precision@1"] == pytest.approx(1 / 3)
    assert results["aggregate"]["recall@1"] == pytest.approx(1 / 3)
    assert results["aggregate"]["mean_average_precision@1"] == pytest.approx(1 / 3)


@pytest.mark.skipif(
    os.getenv("RUN_SPECTER2_MODEL_TESTS") != "1",
    reason="set RUN_SPECTER2_MODEL_TESTS=1 to load SPECTER2 weights",
)
@pytest.mark.real_model
def test_specter2_real_model_smoke():
    report = validation.run_validation()
    assert report["model"] == "allenai/specter2_base"
    assert report["document_embedding_shape"][1] == 768
    assert report["query_embedding_shape"][1] == 768
    assert report["all_values_finite"]
    assert report["all_vectors_unit_normalized"]
    assert report["document_query_dimensions_compatible"]
    assert "specter2_proximity" in report["active_document_adapter"]
    assert "specter2_adhoc_query" in report["active_query_adapter"]
    assert all(report["retrieval_results"].values())
    assert report["evaluation"]["label_type"] == "synthetic"
    print(json.dumps(report, indent=2))


@pytest.mark.skipif(
    os.getenv("RUN_SEMANTIC_NEO4J_INTEGRATION") != "1",
    reason="set RUN_SEMANTIC_NEO4J_INTEGRATION=1 to run against real Neo4j",
)
def test_pdf_to_faiss_integration_with_real_neo4j(tmp_path):
    import pymupdf

    manager = get_neo4j_manager()
    token = uuid.uuid4().hex
    paper_id = int.from_bytes(uuid.UUID(hex=token).bytes[:6], "big")
    title = f"KGAI semantic retrieval integration {token}"
    pdf_path = tmp_path / f"{token}.pdf"
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text(
        (72, 72),
        "BERT is a transformer model evaluated on the SQuAD dataset. "
        "The Adam optimizer improves the F1 score on neural language tasks.",
    )
    document.save(pdf_path)
    document.close()

    engine, _metadata, vector_store = _store(tmp_path, dimension=8)
    service = SemanticRetrievalService(
        chunker=ScientificChunkingService(100, 0),
        embedding_service=_LexicalEmbedding(),
        vector_store=vector_store,
        neo4j_manager=manager,
    )
    paper_created = False
    try:
        manager.execute_write(
            "CREATE (p:Paper {paper_id: $paper_id, title: $title})",
            {"paper_id": paper_id, "title": title},
        )
        paper_created = True
        chunks = service.index_pdf(str(pdf_path), paper_id)
        initial_count = vector_store.count
        repeated_chunks = service.index_pdf(str(pdf_path), paper_id)
        assert chunks and repeated_chunks
        assert vector_store.count == initial_count
        assert all(chunk.page_number == 1 for chunk in chunks)
        assert all(chunk.start_char is not None and chunk.end_char is not None for chunk in chunks)
        assert service.search("BERT transformer SQuAD", top_k=1)[0]["paper_id"] == paper_id

        reopened = FaissVectorStore(
            8,
            tmp_path / "scientific.index",
            metadata_store=ChunkMetadataStore(
                sessionmaker(bind=engine, expire_on_commit=False)
            ),
        )
        assert reopened.count == initial_count
        assert reopened.search(
            _LexicalEmbedding().embed_queries(["BERT transformer SQuAD"])[0], 1
        )
    finally:
        service.delete_paper(paper_id)
        if paper_created:
            manager.execute_write(
                "MATCH (p:Paper {paper_id: $paper_id, title: $title}) DELETE p",
                {"paper_id": paper_id, "title": title},
            )
        engine.dispose()
