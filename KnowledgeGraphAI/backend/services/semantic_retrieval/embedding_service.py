"""Lazy SPECTER2 embedding with task-appropriate adapters."""

import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import numpy as np
import torch

from KnowledgeGraphAI.backend.services.semantic_retrieval.config import (
    SemanticRetrievalConfig,
)

logger = logging.getLogger(__name__)


class Specter2EmbeddingService:
    """Encode paper passages and text queries with SPECTER2 adapters.

    Paper chunks use the SciRepEval proximity adapter; free-text queries use
    SPECTER2's adhoc-query adapter. Both use the model-card CLS representation.
    """

    def __init__(
        self,
        config: Optional[SemanticRetrievalConfig] = None,
        tokenizer: Any = None,
        model: Any = None,
    ) -> None:
        self.config = config or SemanticRetrievalConfig.from_env()
        self._tokenizer = tokenizer
        self._model = model
        self._device: Optional[torch.device] = None
        self._active_adapter: Optional[str] = None
        self._embedding_dimension: Optional[int] = None
        self.repository_resolution_seconds: Dict[str, float] = {}

    @property
    def dimension(self) -> int:
        if self._embedding_dimension is None:
            self._ensure_loaded()
        if self._embedding_dimension is None:
            raise RuntimeError("SPECTER2 did not report an embedding dimension")
        return self._embedding_dimension

    def _resolve_device(self) -> torch.device:
        requested = self.config.device
        if requested == "auto":
            return torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if requested == "cuda" and not torch.cuda.is_available():
            raise RuntimeError("SPECTER2_DEVICE=cuda was requested but CUDA is unavailable")
        return torch.device(requested)

    def _model_repository(self, identifier: str) -> str:
        """Use regular local files on Windows where cache symlinks may be denied."""
        if os.name != "nt":
            return identifier
        from huggingface_hub import snapshot_download

        hub_home = Path(
            os.getenv("HF_HOME", str(Path.home() / ".cache" / "huggingface"))
        ).expanduser()
        local_dir = hub_home / "local-repos" / identifier.replace("/", "--")
        started = time.perf_counter()
        try:
            if (local_dir / "config.json").is_file() or (local_dir / "adapter_config.json").is_file():
                try:
                    return snapshot_download(
                        repo_id=identifier,
                        local_dir=str(local_dir),
                        local_files_only=True,
                    )
                except Exception:
                    pass
            return snapshot_download(repo_id=identifier, local_dir=str(local_dir))
        finally:
            self.repository_resolution_seconds[identifier] = (
                time.perf_counter() - started
            )

    def _ensure_loaded(self) -> None:
        if self._model is not None and self._tokenizer is not None:
            if self._device is None:
                self._device = self._resolve_device()
                self._model.to(self._device)
                self._model.eval()
                self._embedding_dimension = int(self._model.config.hidden_size)
            return
        if self._model is not None or self._tokenizer is not None:
            raise ValueError("tokenizer and model must be supplied together")

        try:
            from adapters import AutoAdapterModel
            from transformers import AutoTokenizer
        except ImportError as exc:
            raise RuntimeError(
                "SPECTER2 inference requires the 'transformers' and 'adapters' packages"
            ) from exc

        logger.info("Loading SPECTER2 base model and task adapters on first use.")
        model_repository = self._model_repository(self.config.model_name)
        self._tokenizer = AutoTokenizer.from_pretrained(model_repository)
        self._model = AutoAdapterModel.from_pretrained(model_repository)
        document_adapter = self._model_repository(self.config.document_adapter)
        query_adapter = self._model_repository(self.config.query_adapter)
        adapter_source = {} if os.name == "nt" else {"source": "hf"}
        self._model.load_adapter(
            document_adapter,
            load_as="specter2_proximity",
            set_active=True,
            **adapter_source,
        )
        self._active_adapter = "specter2_proximity"
        self._model.load_adapter(
            query_adapter,
            load_as="specter2_adhoc_query",
            set_active=False,
            **adapter_source,
        )
        self._device = self._resolve_device()
        self._model.to(self._device)
        self._model.eval()
        self._embedding_dimension = int(self._model.config.hidden_size)
        logger.info("SPECTER2 initialized on %s with dimension %s.", self._device, self._embedding_dimension)

    def _activate_adapter(self, adapter: str) -> None:
        self._ensure_loaded()
        assert self._model is not None
        if self._active_adapter != adapter:
            self._model.set_active_adapters(adapter)
            self._active_adapter = adapter

    @staticmethod
    def _normalize(vectors: np.ndarray) -> np.ndarray:
        vectors = np.asarray(vectors, dtype=np.float32)
        if vectors.ndim != 2:
            raise ValueError("Embeddings must be a two-dimensional array")
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        if np.any(~np.isfinite(vectors)) or np.any(norms == 0):
            raise ValueError("Embeddings must be finite and have non-zero norms")
        return np.ascontiguousarray(vectors / norms, dtype=np.float32)

    def _encode(
        self,
        texts: Sequence[str],
        adapter: str,
        titles: Optional[Sequence[Optional[str]]] = None,
    ) -> np.ndarray:
        if not texts:
            dimension = self._embedding_dimension or self.config.embedding_dimension
            return np.empty((0, dimension), dtype=np.float32)
        if any(not isinstance(text, str) or not text.strip() for text in texts):
            raise ValueError("Embedding inputs must be non-empty strings")
        if titles is not None and len(titles) != len(texts):
            raise ValueError("titles and texts must have equal lengths")
        self._activate_adapter(adapter)
        assert self._tokenizer is not None and self._model is not None
        assert self._device is not None

        inputs_text: List[str] = []
        for index, text in enumerate(texts):
            title = (titles[index] or "").strip() if titles is not None else ""
            if adapter == "specter2_proximity" and title:
                text = f"{title}{self._tokenizer.sep_token}{text.strip()}"
            inputs_text.append(text.strip())

        outputs: List[np.ndarray] = []
        for offset in range(0, len(inputs_text), self.config.batch_size):
            batch = inputs_text[offset:offset + self.config.batch_size]
            encoded = self._tokenizer(
                batch,
                padding=True,
                truncation=True,
                max_length=self.config.max_length,
                return_tensors="pt",
                return_token_type_ids=False,
            )
            encoded = {key: value.to(self._device) for key, value in encoded.items()}
            with torch.inference_mode():
                model_output = self._model(**encoded)
                vectors = model_output.last_hidden_state[:, 0, :]
            outputs.append(vectors.detach().to("cpu").numpy().astype(np.float32, copy=False))
        combined = np.concatenate(outputs, axis=0)
        if combined.shape[1] != self.dimension:
            raise ValueError("SPECTER2 returned an inconsistent embedding dimension")
        return self._normalize(combined)

    def embed_documents(
        self,
        texts: Sequence[str],
        titles: Optional[Sequence[Optional[str]]] = None,
    ) -> np.ndarray:
        """Embed paper passages with the proximity adapter."""
        return self._encode(texts, "specter2_proximity", titles)

    def embed_queries(self, queries: Sequence[str]) -> np.ndarray:
        """Embed short search queries with the adhoc-query adapter."""
        return self._encode(queries, "specter2_adhoc_query")
