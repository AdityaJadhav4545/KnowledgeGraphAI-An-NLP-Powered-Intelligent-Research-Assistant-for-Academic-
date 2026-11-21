"""Relational metadata for FAISS-indexed scientific-paper chunks."""

import datetime
from typing import Optional

from sqlalchemy import BigInteger, DateTime, Integer, LargeBinary, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from KnowledgeGraphAI.models.paper import Base


class SemanticChunkRecord(Base):
    """Canonical chunk metadata and vector payload used to rebuild FAISS."""

    __tablename__ = "semantic_chunks"
    __table_args__ = (
        UniqueConstraint("chunk_id", name="uq_semantic_chunks_chunk_id"),
    )

    vector_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chunk_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    paper_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    source_identifier: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    page_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    section_title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    start_char: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    end_char: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    source_document: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow, nullable=False
    )
    embedding_dimension: Mapped[int] = mapped_column(Integer, nullable=False)
    embedding: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
