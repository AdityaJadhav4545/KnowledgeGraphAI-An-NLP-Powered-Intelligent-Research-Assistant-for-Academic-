"""Application configuration and startup validation.

The project previously read environment variables independently in several
modules.  Keeping the small settings object in one place makes local
development predictable while avoiding accidental disclosure of configuration
values through API responses or logs.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_environment() -> None:
    """Load a local ``.env`` file without overwriting real environment values.

    ``python-dotenv`` remains optional so importing the backend does not fail in
    constrained test environments.  Production deployments should inject
    configuration through their process environment instead.
    """

    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv(PROJECT_ROOT / ".env", override=False)


def _bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name, str(default)).strip().lower()
    if value in {"1", "true", "yes", "on"}:
        return True
    if value in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{name} must be a boolean value")


def _positive_int(name: str, default: int, maximum: int) -> int:
    raw = os.getenv(name, str(default)).strip()
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if not 1 <= value <= maximum:
        raise ValueError(f"{name} must be between 1 and {maximum}")
    return value


def _path(name: str, default: Path) -> Path:
    raw = os.getenv(name)
    path = Path(raw).expanduser() if raw else default
    if not path.is_absolute():
        # Existing examples use ./KnowledgeGraphAI/... when the parent folder
        # is the working directory.  Resolve both common launch locations.
        candidate = (Path.cwd() / path).resolve()
        if not candidate.exists() and str(path).startswith("KnowledgeGraphAI"):
            candidate = (PROJECT_ROOT.parent / path).resolve()
        path = candidate
    return path.resolve()


def _database_url() -> str:
    """Resolve relative SQLite URLs consistently from either supported cwd."""

    default = f"sqlite:///{(PROJECT_ROOT / 'data' / 'knowledge_graph_ai.db').as_posix()}"
    url = os.getenv("DATABASE_URL", default).strip()
    prefix = "sqlite:///"
    if not url.startswith(prefix):
        return url
    raw_path = url[len(prefix):]
    if raw_path in {"", ":memory:"} or Path(raw_path).is_absolute():
        return url
    path = Path(raw_path)
    candidate = (Path.cwd() / path).resolve()
    if str(path).replace("\\", "/").startswith("KnowledgeGraphAI/"):
        parent_candidate = (PROJECT_ROOT.parent / path).resolve()
        if parent_candidate.exists() or not candidate.exists():
            candidate = parent_candidate
    return f"sqlite:///{candidate.as_posix()}"


@dataclass(frozen=True)
class Settings:
    environment: str
    debug: bool
    database_url: str
    upload_dir: Path
    processed_dir: Path
    max_upload_bytes: int
    cors_origins: Tuple[str, ...]
    api_key: str | None
    require_authentication: bool
    neo4j_required: bool
    semantic_required: bool
    ollama_base_url: str
    ollama_model: str
    ollama_timeout_seconds: int
    ollama_keep_alive: str = "15m"
    ollama_num_ctx: int = 2048
    ollama_num_predict: int = 220
    ollama_num_thread: int = 8

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    def validate(self) -> None:
        """Fail early for unsafe production settings, never logging secrets."""

        if self.environment not in {"development", "testing", "production"}:
            raise ValueError("APP_ENV must be development, testing, or production")
        if self.is_production:
            if not self.api_key:
                raise ValueError("API_KEY is required when APP_ENV=production")
            if "*" in self.cors_origins:
                raise ValueError("CORS_ORIGINS cannot contain '*' in production")
            if not os.getenv("NEO4J_PASSWORD") and self.neo4j_required:
                raise ValueError("NEO4J_PASSWORD is required when Neo4j is required")
        if self.max_upload_bytes < 1024:
            raise ValueError("MAX_UPLOAD_BYTES must be at least 1024")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    load_environment()
    environment = os.getenv("APP_ENV", "development").strip().lower()
    origins = tuple(
        item.strip()
        for item in os.getenv(
            "CORS_ORIGINS", "http://localhost:8501,http://127.0.0.1:8501"
        ).split(",")
        if item.strip()
    )
    settings = Settings(
        environment=environment,
        debug=_bool("DEBUG", environment == "development"),
        database_url=_database_url(),
        upload_dir=_path("UPLOAD_DIR", PROJECT_ROOT / "data" / "raw"),
        processed_dir=_path("PROCESSED_DIR", PROJECT_ROOT / "data" / "processed"),
        max_upload_bytes=_positive_int("MAX_UPLOAD_BYTES", 50 * 1024 * 1024, 1024 * 1024 * 1024),
        cors_origins=origins,
        api_key=os.getenv("API_KEY") or None,
        require_authentication=_bool("REQUIRE_AUTHENTICATION", environment == "production"),
        neo4j_required=_bool("REQUIRE_NEO4J", environment == "production"),
        semantic_required=_bool("REQUIRE_SEMANTIC_RETRIEVAL", environment == "production"),
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/"),
        ollama_model=os.getenv("OLLAMA_MODEL", "llama3.1").strip(),
        ollama_timeout_seconds=_positive_int("OLLAMA_TIMEOUT_SECONDS", 120, 600),
        ollama_keep_alive=os.getenv("OLLAMA_KEEP_ALIVE", "15m").strip() or "15m",
        ollama_num_ctx=_positive_int("OLLAMA_NUM_CTX", 2048, 16384),
        ollama_num_predict=_positive_int("OLLAMA_NUM_PREDICT", 220, 4096),
        ollama_num_thread=_positive_int("OLLAMA_NUM_THREAD", 8, 64),
    )
    settings.validate()
    return settings
