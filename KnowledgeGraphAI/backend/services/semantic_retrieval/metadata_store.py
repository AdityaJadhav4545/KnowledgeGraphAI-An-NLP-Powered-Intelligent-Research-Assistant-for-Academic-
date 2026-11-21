"""SQLAlchemy persistence for chunk metadata and recoverable vector payloads."""

from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Sequence

import numpy as np
from sqlalchemy import func, inspect, select, text
from sqlalchemy.orm import sessionmaker

from KnowledgeGraphAI.models.paper import Base
from KnowledgeGraphAI.models.semantic_chunk import SemanticChunkRecord


class ChunkMetadataStore:
    """Store chunk records in the project's configured relational database."""

    def __init__(
        self,
        session_factory: Optional[sessionmaker] = None,
    ) -> None:
        if session_factory is None:
            from KnowledgeGraphAI.backend.database import SessionLocal, engine

            self._session_factory = SessionLocal
            bind = engine
        else:
            self._session_factory = session_factory
            bind = session_factory.kw.get("bind")
        if bind is None:
            raise ValueError("metadata session factory must be bound to an engine")
        Base.metadata.create_all(bind=bind, tables=[SemanticChunkRecord.__table__])
        if "title" not in {
            column["name"]
            for column in inspect(bind).get_columns(SemanticChunkRecord.__tablename__)
        }:
            with bind.begin() as connection:
                connection.execute(
                    text("ALTER TABLE semantic_chunks ADD COLUMN title VARCHAR")
                )
        columns = {
            column["name"]
            for column in inspect(bind).get_columns(SemanticChunkRecord.__tablename__)
        }
        if "source_identifier" not in columns:
            with bind.begin() as connection:
                connection.execute(
                    text("ALTER TABLE semantic_chunks ADD COLUMN source_identifier VARCHAR")
                )

    @staticmethod
    def _metadata(record: SemanticChunkRecord) -> Dict[str, Any]:
        return {
            "vector_id": record.vector_id,
            "chunk_id": record.chunk_id,
            "paper_id": record.paper_id,
            "source_identifier": record.source_identifier,
            "chunk_index": record.chunk_index,
            "text": record.text,
            "title": record.title,
            "page_number": record.page_number,
            "section_title": record.section_title,
            "start_char": record.start_char,
            "end_char": record.end_char,
            "source_document": record.source_document,
            "created_at": record.created_at.isoformat(),
        }

    def upsert_chunks(
        self,
        chunks: Sequence[Dict[str, Any]],
        vectors: np.ndarray,
    ) -> List[int]:
        vectors = np.ascontiguousarray(vectors, dtype=np.float32)
        if vectors.ndim != 2 or vectors.shape[0] != len(chunks):
            raise ValueError("chunk and embedding counts must match")
        if not chunks:
            return []
        chunk_ids = [chunk.get("chunk_id") for chunk in chunks]
        if any(not isinstance(chunk_id, str) or not chunk_id for chunk_id in chunk_ids):
            raise ValueError("each chunk must have a non-empty chunk_id")
        if len(set(chunk_ids)) != len(chunk_ids):
            raise ValueError("chunk IDs must be unique within an upsert")

        vector_ids: List[int] = []
        with self._session_factory() as session:
            with session.begin():
                for chunk, vector in zip(chunks, vectors):
                    chunk_id = chunk.get("chunk_id")
                    record = session.scalar(
                        select(SemanticChunkRecord).where(
                            SemanticChunkRecord.chunk_id == chunk_id
                        )
                    )
                    if record is None:
                        record = SemanticChunkRecord(
                            chunk_id=chunk_id,
                            paper_id=int(chunk["paper_id"]),
                            source_identifier=chunk.get("source_identifier"),
                            chunk_index=int(chunk["chunk_index"]),
                            text=str(chunk["text"]),
                            title=chunk.get("title"),
                            page_number=chunk.get("page_number"),
                            section_title=chunk.get("section_title"),
                            start_char=chunk.get("start_char"),
                            end_char=chunk.get("end_char"),
                            source_document=str(chunk.get("source_document", "")),
                            created_at=datetime.fromisoformat(
                                chunk["created_at"]
                            ) if chunk.get("created_at") else datetime.now(
                                timezone.utc
                            ).replace(tzinfo=None),
                            embedding_dimension=vector.size,
                            embedding=vector.tobytes(),
                        )
                        session.add(record)
                    else:
                        record.paper_id = int(chunk["paper_id"])
                        record.source_identifier = chunk.get("source_identifier")
                        record.chunk_index = int(chunk["chunk_index"])
                        record.text = str(chunk["text"])
                        record.title = chunk.get("title")
                        record.page_number = chunk.get("page_number")
                        record.section_title = chunk.get("section_title")
                        record.start_char = chunk.get("start_char")
                        record.end_char = chunk.get("end_char")
                        record.source_document = str(chunk.get("source_document", ""))
                        record.embedding_dimension = vector.size
                        record.embedding = vector.tobytes()
                    session.flush()
                    vector_ids.append(record.vector_id)
        return vector_ids

    def get_many(self, vector_ids: Iterable[int]) -> Dict[int, Dict[str, Any]]:
        ids = list(dict.fromkeys(int(value) for value in vector_ids))
        if not ids:
            return {}
        with self._session_factory() as session:
            records = session.scalars(
                select(SemanticChunkRecord).where(
                    SemanticChunkRecord.vector_id.in_(ids)
                )
            ).all()
            return {record.vector_id: self._metadata(record) for record in records}

    def get_vectors(self, vector_ids: Iterable[int]) -> Dict[int, np.ndarray]:
        ids = list(dict.fromkeys(int(value) for value in vector_ids))
        if not ids:
            return {}
        with self._session_factory() as session:
            records = session.scalars(
                select(SemanticChunkRecord).where(
                    SemanticChunkRecord.vector_id.in_(ids)
                )
            ).all()
            return {
                record.vector_id: np.frombuffer(
                    record.embedding, dtype=np.float32
                ).copy()
                for record in records
            }

    def all_records(self) -> List[Dict[str, Any]]:
        with self._session_factory() as session:
            records = session.scalars(
                select(SemanticChunkRecord).order_by(SemanticChunkRecord.vector_id)
            ).all()
            result = []
            for record in records:
                item = self._metadata(record)
                item["embedding_dimension"] = record.embedding_dimension
                item["embedding"] = record.embedding
                result.append(item)
            return result

    def chunk_ids(self) -> List[str]:
        with self._session_factory() as session:
            return list(
                session.scalars(
                    select(SemanticChunkRecord.chunk_id).order_by(
                        SemanticChunkRecord.chunk_id
                    )
                ).all()
            )

    def delete_paper(self, paper_id: int) -> List[int]:
        with self._session_factory() as session:
            with session.begin():
                records = session.scalars(
                    select(SemanticChunkRecord).where(
                        SemanticChunkRecord.paper_id == paper_id
                    )
                ).all()
                vector_ids = [record.vector_id for record in records]
                for record in records:
                    session.delete(record)
            return vector_ids

    def count(self) -> int:
        with self._session_factory() as session:
            return int(
                session.scalar(select(func.count()).select_from(SemanticChunkRecord)) or 0
            )
