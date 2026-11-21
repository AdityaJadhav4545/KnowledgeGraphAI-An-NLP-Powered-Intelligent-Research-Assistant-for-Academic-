"""Opt-in real SPECTER2, FAISS, and synthetic-label retrieval validation."""

import ctypes
import json
import os
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, Optional
from ctypes import wintypes

import numpy as np
import torch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from KnowledgeGraphAI.backend.services.semantic_retrieval.config import (
    SemanticRetrievalConfig,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.embedding_service import (
    Specter2EmbeddingService,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.evaluation import (
    evaluate_dataset,
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


_DATASET_PATH = Path(__file__).with_name("evaluation_dataset.json")
_EXPECTED_MODEL = "allenai/specter2_base"
_EXPECTED_DOCUMENT_ADAPTER = "allenai/specter2"
_EXPECTED_QUERY_ADAPTER = "allenai/specter2_adhoc_query"


def _process_memory_bytes() -> Optional[Dict[str, int]]:
    try:
        import psutil

        process = psutil.Process()
        return {
            "working_set_bytes": process.memory_info().rss,
            "peak_working_set_bytes": process.memory_info().peak_wset,
        }
    except (ImportError, AttributeError):
        pass

    if os.name != "nt":
        return None

    class ProcessMemoryCounters(ctypes.Structure):
        _fields_ = [
            ("cb", ctypes.c_ulong),
            ("PageFaultCount", ctypes.c_ulong),
            ("PeakWorkingSetSize", ctypes.c_size_t),
            ("WorkingSetSize", ctypes.c_size_t),
            ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
            ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
            ("PagefileUsage", ctypes.c_size_t),
            ("PeakPagefileUsage", ctypes.c_size_t),
        ]

    counters = ProcessMemoryCounters()
    counters.cb = ctypes.sizeof(counters)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    kernel32.GetCurrentProcess.restype = wintypes.HANDLE
    psapi.GetProcessMemoryInfo.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(ProcessMemoryCounters),
        wintypes.DWORD,
    ]
    psapi.GetProcessMemoryInfo.restype = wintypes.BOOL
    process_handle = kernel32.GetCurrentProcess()
    succeeded = psapi.GetProcessMemoryInfo(
        process_handle,
        ctypes.byref(counters),
        counters.cb,
    )
    if not succeeded:
        return None
    return {
        "working_set_bytes": int(counters.WorkingSetSize),
        "peak_working_set_bytes": int(counters.PeakWorkingSetSize),
    }


def run_validation() -> Dict[str, Any]:
    """Download/load configured weights and run document-to-query FAISS search."""
    config = SemanticRetrievalConfig.from_env()
    expected = (
        _EXPECTED_MODEL,
        _EXPECTED_DOCUMENT_ADAPTER,
        _EXPECTED_QUERY_ADAPTER,
    )
    configured = (
        config.model_name,
        config.document_adapter,
        config.query_adapter,
    )
    if configured != expected:
        raise ValueError(
            "Real-model validation requires the canonical SPECTER2 model and adapters: "
            f"{expected!r}; configured {configured!r}"
        )

    dataset = json.loads(_DATASET_PATH.read_text(encoding="utf-8"))
    documents = dataset["documents"]
    queries = dataset["queries"]
    memory_before = _process_memory_bytes()
    embedding_service = Specter2EmbeddingService(config)

    load_started = time.perf_counter()
    dimension = embedding_service.dimension
    load_seconds = time.perf_counter() - load_started
    if embedding_service._device is not None and embedding_service._device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(embedding_service._device)

    document_started = time.perf_counter()
    document_vectors = embedding_service.embed_documents(
        [document["text"] for document in documents],
        titles=[document["title"] for document in documents],
    )
    document_inference_seconds = time.perf_counter() - document_started
    active_document_adapter = str(embedding_service._model.active_adapters)

    query_started = time.perf_counter()
    query_vectors = embedding_service.embed_queries(
        [query["query"] for query in queries]
    )
    query_inference_seconds = time.perf_counter() - query_started
    active_query_adapter = str(embedding_service._model.active_adapters)
    if "specter2_proximity" not in active_document_adapter:
        raise AssertionError("SPECTER2 proximity adapter was not active for documents")
    if "specter2_adhoc_query" not in active_query_adapter:
        raise AssertionError("SPECTER2 adhoc-query adapter was not active for queries")

    if document_vectors.shape != (len(documents), dimension):
        raise AssertionError(f"Unexpected document embedding shape: {document_vectors.shape}")
    if query_vectors.shape != (len(queries), dimension):
        raise AssertionError(f"Unexpected query embedding shape: {query_vectors.shape}")
    if not np.isfinite(document_vectors).all() or not np.isfinite(query_vectors).all():
        raise AssertionError("SPECTER2 produced non-finite embeddings")
    if not np.allclose(np.linalg.norm(document_vectors, axis=1), 1.0, atol=1e-5):
        raise AssertionError("Document embeddings are not unit-normalized")
    if not np.allclose(np.linalg.norm(query_vectors, axis=1), 1.0, atol=1e-5):
        raise AssertionError("Query embeddings are not unit-normalized")

    with tempfile.TemporaryDirectory(prefix="kgai-specter2-validation-") as directory:
        root = Path(directory)
        engine = create_engine(
            f"sqlite:///{root / 'evaluation.sqlite'}",
            connect_args={"check_same_thread": False},
        )
        metadata_store = ChunkMetadataStore(
            sessionmaker(bind=engine, expire_on_commit=False)
        )
        vector_store = FaissVectorStore(
            dimension,
            root / "evaluation.index",
            metadata_store=metadata_store,
        )
        vector_store.add(documents, document_vectors)
        retrieval = SemanticRetrievalService(
            config=config,
            embedding_service=embedding_service,
            vector_store=vector_store,
            neo4j_manager=object(),
        )

        search_started = time.perf_counter()
        real_results = {
            item["query"]: retrieval.search(item["query"], top_k=3)
            for item in queries
        }
        search_seconds = time.perf_counter() - search_started
        evaluation = evaluate_dataset(
            dataset,
            lambda query, k: retrieval.search(query, top_k=k),
            k=3,
        )
        engine.dispose()

    cuda_peak_bytes = None
    if embedding_service._device is not None and embedding_service._device.type == "cuda":
        cuda_peak_bytes = int(torch.cuda.max_memory_allocated(embedding_service._device))
    return {
        "model": config.model_name,
        "document_adapter": config.document_adapter,
        "query_adapter": config.query_adapter,
        "device": str(embedding_service._device),
        "embedding_dimension": dimension,
        "document_embedding_shape": list(document_vectors.shape),
        "query_embedding_shape": list(query_vectors.shape),
        "active_document_adapter": active_document_adapter,
        "active_query_adapter": active_query_adapter,
        "all_values_finite": True,
        "all_vectors_unit_normalized": True,
        "document_query_dimensions_compatible": (
            document_vectors.shape[1] == query_vectors.shape[1]
        ),
        "model_load_and_download_seconds": load_seconds,
        "repository_download_or_cache_resolution_seconds": (
            embedding_service.repository_resolution_seconds
        ),
        "document_inference_seconds": document_inference_seconds,
        "query_inference_seconds": query_inference_seconds,
        "faiss_search_seconds": search_seconds,
        "process_memory_before_bytes": memory_before,
        "process_memory_after_bytes": _process_memory_bytes(),
        "cuda_peak_allocated_bytes": cuda_peak_bytes,
        "retrieval_results": {
            query: [
                {
                    "chunk_id": result["chunk_id"],
                    "title": result["title"],
                    "similarity_score": result["similarity_score"],
                }
                for result in results
            ]
            for query, results in real_results.items()
        },
        "evaluation": evaluation,
    }


def main() -> None:
    report = run_validation()
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
