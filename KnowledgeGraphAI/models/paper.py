from sqlalchemy import Integer, String, DateTime, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime


class Base(DeclarativeBase):
    pass


class Paper(Base):
    __tablename__ = "papers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    author: Mapped[str] = mapped_column(String, nullable=True)
    file_path: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    file_hash: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    content_hash: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    page_count: Mapped[int] = mapped_column(Integer, nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
    # Processing states are deliberately persisted as text for backwards
    # compatibility with the existing SQLite database.  New code uses the
    # documented transitions in ``paper_processing.py``.
    status: Mapped[str] = mapped_column(String, default="uploaded", nullable=False)
    processing_error: Mapped[str | None] = mapped_column(String, nullable=True)
    processing_started_at: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)
    processing_completed_at: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)
