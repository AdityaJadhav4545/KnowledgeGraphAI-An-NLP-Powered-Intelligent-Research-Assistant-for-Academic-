"""Database setup plus small, additive SQLite migrations.

The project predates Alembic.  Until a formal migration history is introduced,
the migration routine below only adds nullable columns, takes a verified backup
before touching an on-disk SQLite database, and never drops or rewrites user
records.
"""

import hashlib
import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from KnowledgeGraphAI.models.paper import Base
from KnowledgeGraphAI.models.semantic_chunk import SemanticChunkRecord  # noqa: F401
from KnowledgeGraphAI.models.analysis import AnalysisRecord  # noqa: F401
from KnowledgeGraphAI.backend.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()
DATABASE_URL = settings.database_url


def _sqlite_file_path(database_url: str) -> Path | None:
    """Return an on-disk SQLite path, excluding memory databases."""

    if not database_url.startswith("sqlite:///"):
        return None
    raw_path = database_url[len("sqlite:///"):]
    if raw_path in {"", ":memory:"}:
        return None
    return Path(raw_path).expanduser().resolve()


sqlite_path = _sqlite_file_path(DATABASE_URL)
if sqlite_path is not None:
    sqlite_path.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    pool_pre_ping=not DATABASE_URL.startswith("sqlite"),
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


_PAPER_ADDITIVE_COLUMNS = {
    "updated_at": "DATETIME",
    "processing_error": "VARCHAR",
    "processing_started_at": "DATETIME",
    "processing_completed_at": "DATETIME",
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _backup_sqlite_database(path: Path) -> Path:
    """Create and verify a pre-migration snapshot without overwriting one."""

    backup_dir = path.parent / ".backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = backup_dir / f"{path.stem}.pre_migration_{stamp}{path.suffix}"
    shutil.copy2(path, backup)
    if _sha256(path) != _sha256(backup):
        backup.unlink(missing_ok=True)
        raise RuntimeError("SQLite pre-migration backup verification failed")
    logger.info("Verified additive-migration backup at %s", backup)
    return backup


def _run_additive_migrations() -> None:
    """Add only missing nullable Paper columns on supported SQLite databases."""

    if not DATABASE_URL.startswith("sqlite"):
        return
    inspector = inspect(engine)
    if "papers" not in inspector.get_table_names():
        return
    existing = {column["name"] for column in inspector.get_columns("papers")}
    missing = {
        name: definition
        for name, definition in _PAPER_ADDITIVE_COLUMNS.items()
        if name not in existing
    }
    if not missing:
        return
    if sqlite_path is not None and sqlite_path.exists():
        _backup_sqlite_database(sqlite_path)
    with engine.begin() as connection:
        for name, definition in missing.items():
            connection.execute(text(f"ALTER TABLE papers ADD COLUMN {name} {definition}"))
    logger.info("Applied additive Paper columns: %s", ", ".join(missing))


def init_db():
    Base.metadata.create_all(bind=engine)
    _run_additive_migrations()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
