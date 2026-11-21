"""Typed data structures shared by semantic-retrieval components."""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class ScientificChunk:
    """A stable passage and its source-paper location."""

    chunk_id: str
    paper_id: int
    chunk_index: int
    text: str
    page_number: Optional[int]
    section_title: Optional[str]
    start_char: Optional[int]
    end_char: Optional[int]
    source_document: str
    created_at: str

    @classmethod
    def create(
        cls,
        chunk_id: str,
        paper_id: int,
        chunk_index: int,
        text: str,
        page_number: Optional[int],
        section_title: Optional[str],
        start_char: Optional[int],
        end_char: Optional[int],
        source_document: str,
    ) -> "ScientificChunk":
        return cls(
            chunk_id=chunk_id,
            paper_id=paper_id,
            chunk_index=chunk_index,
            text=text,
            page_number=page_number,
            section_title=section_title,
            start_char=start_char,
            end_char=end_char,
            source_document=source_document,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SearchResult:
    """A ranked semantic match with its original chunk metadata."""

    rank: int
    paper_id: int
    chunk_id: str
    text: str
    similarity_score: float
    page_number: Optional[int]
    section_title: Optional[str]
    chunk_index: int
    start_char: Optional[int] = None
    end_char: Optional[int] = None
    source_document: Optional[str] = None
    title: Optional[str] = None
    source_identifier: Optional[str] = None
    reranking_score: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
