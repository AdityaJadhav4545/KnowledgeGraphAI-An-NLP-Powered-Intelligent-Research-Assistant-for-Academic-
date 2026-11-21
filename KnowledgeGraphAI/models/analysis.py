"""SQLAlchemy model for isolated PDF and pasted-text document analyses."""

import datetime

from sqlalchemy import DateTime, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from KnowledgeGraphAI.models.paper import Base


def _utcnow() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)


class AnalysisRecord(Base):
    __tablename__ = "analyses"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    source_type: Mapped[str] = mapped_column(String(16), nullable=False)  # "pdf" | "text"
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str | None] = mapped_column(String, nullable=True)
    publication_info: Mapped[str | None] = mapped_column(String, nullable=True)
    paper_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    content_hash: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    page_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="processing", nullable=False)
    stage: Mapped[str] = mapped_column(String(64), default="validating", nullable=False)
    error_message: Mapped[str | None] = mapped_column(String, nullable=True)
    full_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    passages_json: Mapped[list | None] = mapped_column(JSON, nullable=True)
    sections_json: Mapped[list | None] = mapped_column(JSON, nullable=True)
    entities_json: Mapped[list | None] = mapped_column(JSON, nullable=True)
    relationships_json: Mapped[list | None] = mapped_column(JSON, nullable=True)
    graph_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    chat_history_json: Mapped[list | None] = mapped_column(JSON, nullable=True)
    report_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=_utcnow, onupdate=_utcnow, nullable=False
    )

