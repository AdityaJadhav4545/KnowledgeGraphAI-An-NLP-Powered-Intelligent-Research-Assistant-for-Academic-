"""Persistent exact cosine-similarity search backed by a FAISS flat index."""

import logging
import os
import tempfile
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from KnowledgeGraphAI.backend.services.semantic_retrieval.metadata_store import (
    ChunkMetadataStore,
)

logger = logging.getLogger(__name__)


class FaissVectorStore:
    """Index normalized vectors with ``IndexIDMap2(IndexFlatIP)``.

    SQLite chunk records, including vector payloads, are canonical. The FAISS
    file is a rebuildable search artifact and is repaired on startup if stale.
    """

    def __init__(
        self,
        dimension: int,
        index_path: Path,
        metadata_store: Optional[ChunkMetadataStore] = None,
        faiss_module: Any = None,
    ) -> None:
        if isinstance(dimension, bool) or not isinstance(dimension, int) or dimension < 1:
            raise ValueError("dimension must be a positive integer")
        self.dimension = dimension
        self.index_path = Path(index_path)
        self.metadata_store = metadata_store or ChunkMetadataStore()
        if faiss_module is None:
            try:
                import faiss as faiss_module
            except ImportError as exc:
                raise RuntimeError(
                    "FAISS vector search requires faiss-cpu; install project requirements"
                ) from exc
        self.faiss = faiss_module
        self._lock = threading.RLock()
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.index = self._new_index()
        self._load_or_rebuild()

    def _new_index(self):
        return self.faiss.IndexIDMap2(self.faiss.IndexFlatIP(self.dimension))

    @staticmethod
    def normalize(vectors: np.ndarray) -> np.ndarray:
        values = np.asarray(vectors, dtype=np.float32)
        if values.ndim != 2:
            raise ValueError("vectors must be a two-dimensional array")
        if not np.all(np.isfinite(values)):
            raise ValueError("vectors must contain only finite values")
        norms = np.linalg.norm(values, axis=1, keepdims=True)
        if np.any(norms == 0):
            raise ValueError("zero-length vectors cannot be indexed")
        return np.ascontiguousarray(values / norms, dtype=np.float32)

    def _load_or_rebuild(self) -> None:
        records = self.metadata_store.all_records()
        stored_ids = [int(record["vector_id"]) for record in records]
        if self.index_path.exists():
            try:
                loaded = self.faiss.read_index(str(self.index_path))
                if loaded.d == self.dimension and self._loaded_ids(loaded) == stored_ids:
                    self.index = loaded
                    return
                logger.warning("FAISS file does not match metadata; rebuilding it.")
            except Exception:
                logger.warning("Unable to load FAISS file; rebuilding from metadata.", exc_info=True)
        self._rebuild(records)
        self.save()

    def _loaded_ids(self, index) -> List[int]:
        if index.ntotal == 0:
            return []
        return [
            int(value) for value in self.faiss.vector_to_array(index.id_map)
        ]

    def _rebuild(self, records: Sequence[Dict[str, Any]]) -> None:
        rebuilt = self._new_index()
        if records:
            vectors = []
            ids = []
            for record in records:
                if record["embedding_dimension"] != self.dimension:
                    raise ValueError(
                        f"stored vector {record['vector_id']} has dimension "
                        f"{record['embedding_dimension']}, expected {self.dimension}"
                    )
                vector = np.frombuffer(record["embedding"], dtype=np.float32)
                if vector.size != self.dimension:
                    raise ValueError(f"stored vector {record['vector_id']} is corrupted")
                vectors.append(vector)
                ids.append(record["vector_id"])
            rebuilt.add_with_ids(
                self.normalize(np.vstack(vectors)),
                np.asarray(ids, dtype=np.int64),
            )
        self.index = rebuilt

    def add(
        self,
        chunks: Sequence[Dict[str, Any]],
        vectors: np.ndarray,
    ) -> List[int]:
        normalized = self.normalize(vectors)
        if normalized.shape != (len(chunks), self.dimension):
            raise ValueError(
                f"expected ({len(chunks)}, {self.dimension}) vectors, got {normalized.shape}"
            )
        if not chunks:
            return []
        with self._lock:
            vector_ids = self.metadata_store.upsert_chunks(chunks, normalized)
            self._rebuild(self.metadata_store.all_records())
            self.save()
            return vector_ids

    def search(self, query_vector: np.ndarray, top_k: int) -> List[Tuple[int, float]]:
        if isinstance(top_k, bool) or not isinstance(top_k, int) or top_k < 1:
            raise ValueError("top_k must be a positive integer")
        query = self.normalize(np.asarray(query_vector, dtype=np.float32).reshape(1, -1))
        if query.shape[1] != self.dimension:
            raise ValueError(
                f"query dimension {query.shape[1]} does not match index dimension {self.dimension}"
            )
        with self._lock:
            if self.index.ntotal == 0:
                return []
            scores, ids = self.index.search(query, min(top_k, self.index.ntotal))
        return [
            (int(vector_id), float(score))
            for vector_id, score in zip(ids[0], scores[0])
            if vector_id >= 0
        ]

    def get_metadata(self, vector_ids: Sequence[int]) -> Dict[int, Dict[str, Any]]:
        return self.metadata_store.get_many(vector_ids)

    def get_vectors(self, vector_ids: Sequence[int]) -> Dict[int, np.ndarray]:
        return self.metadata_store.get_vectors(vector_ids)

    def delete_paper(self, paper_id: int) -> int:
        with self._lock:
            removed = self.metadata_store.delete_paper(paper_id)
            if removed:
                self._rebuild(self.metadata_store.all_records())
                self.save()
            return len(removed)

    @property
    def count(self) -> int:
        return int(self.index.ntotal)

    def save(self) -> None:
        with self._lock:
            self.index_path.parent.mkdir(parents=True, exist_ok=True)
            temporary_path: Optional[str] = None
            try:
                with tempfile.NamedTemporaryFile(
                    prefix=self.index_path.name,
                    suffix=".tmp",
                    dir=self.index_path.parent,
                    delete=False,
                ) as temporary:
                    temporary_path = temporary.name
                self.faiss.write_index(self.index, temporary_path)
                os.replace(temporary_path, self.index_path)
            except Exception:
                if temporary_path and os.path.exists(temporary_path):
                    os.unlink(temporary_path)
                raise

    def reload(self) -> None:
        with self._lock:
            self._load_or_rebuild()
