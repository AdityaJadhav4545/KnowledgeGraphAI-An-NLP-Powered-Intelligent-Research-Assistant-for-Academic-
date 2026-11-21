"""Environment-backed configuration for semantic retrieval."""

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]


def _positive_int(name: str, default: int, maximum: int) -> int:
    raw_value = os.getenv(name, str(default))
    try:
        value = int(raw_value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if not 1 <= value <= maximum:
        raise ValueError(f"{name} must be between 1 and {maximum}")
    return value


@dataclass(frozen=True)
class SemanticRetrievalConfig:
    model_name: str
    document_adapter: str
    query_adapter: str
    device: str
    batch_size: int
    max_length: int
    embedding_dimension: int
    chunk_size: int
    chunk_overlap: int
    index_dir: Path
    index_name: str

    @classmethod
    def from_env(cls) -> "SemanticRetrievalConfig":
        chunk_size = _positive_int("SEMANTIC_CHUNK_SIZE", 400, 100_000)
        overlap_raw = os.getenv("SEMANTIC_CHUNK_OVERLAP", "50")
        try:
            overlap = int(overlap_raw)
        except ValueError as exc:
            raise ValueError("SEMANTIC_CHUNK_OVERLAP must be an integer") from exc
        if not 0 <= overlap < chunk_size:
            raise ValueError(
                "SEMANTIC_CHUNK_OVERLAP must be non-negative and smaller than chunk size"
            )

        model_name = os.getenv("SPECTER2_MODEL_NAME", "allenai/specter2_base").strip()
        document_adapter = os.getenv(
            "SPECTER2_DOCUMENT_ADAPTER", "allenai/specter2"
        ).strip()
        query_adapter = os.getenv(
            "SPECTER2_QUERY_ADAPTER", "allenai/specter2_adhoc_query"
        ).strip()
        device = os.getenv("SPECTER2_DEVICE", "auto").strip().lower()
        if not model_name or not document_adapter or not query_adapter:
            raise ValueError("SPECTER2 model and adapter identifiers cannot be empty")
        if device not in {"auto", "cpu", "cuda"}:
            raise ValueError("SPECTER2_DEVICE must be one of: auto, cpu, cuda")

        index_dir = Path(
            os.getenv(
                "FAISS_INDEX_DIR",
                str(PROJECT_ROOT / "data" / "vector_store"),
            )
        ).expanduser()
        if not index_dir.is_absolute():
            cwd_candidate = (Path.cwd() / index_dir).resolve()
            if str(index_dir).replace("\\", "/").startswith("KnowledgeGraphAI/"):
                parent_candidate = (PROJECT_ROOT.parent / index_dir).resolve()
                index_dir = parent_candidate if parent_candidate.exists() or not cwd_candidate.exists() else cwd_candidate
            else:
                index_dir = cwd_candidate
        index_name = os.getenv("FAISS_INDEX_NAME", "scientific_papers.index").strip()
        if not index_name or Path(index_name).name != index_name:
            raise ValueError("FAISS_INDEX_NAME must be a filename, not a path")

        return cls(
            model_name=model_name,
            document_adapter=document_adapter,
            query_adapter=query_adapter,
            device=device,
            batch_size=_positive_int("SPECTER2_BATCH_SIZE", 16, 1024),
            max_length=_positive_int("SPECTER2_MAX_LENGTH", 512, 512),
            embedding_dimension=_positive_int(
                "SPECTER2_EMBEDDING_DIMENSION", 768, 65_536
            ),
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            index_dir=index_dir,
            index_name=index_name,
        )
