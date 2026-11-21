"""Create deterministic scientific-text chunks with source metadata."""

import hashlib
import re
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from KnowledgeGraphAI.backend.services.semantic_retrieval.schemas import ScientificChunk


def _normalized_with_offsets(text: str) -> Tuple[str, List[int]]:
    """Collapse whitespace and retain a normalized-character to source map."""
    normalized_chars: List[str] = []
    offsets: List[int] = []
    pending_space = False
    for index, character in enumerate(text):
        if character.isspace():
            pending_space = bool(normalized_chars)
            continue
        if pending_space:
            normalized_chars.append(" ")
            offsets.append(index - 1)
            pending_space = False
        normalized_chars.append(character)
        offsets.append(index)
    return "".join(normalized_chars), offsets


class ScientificChunkingService:
    """Chunk preprocessed papers without mixing separate paragraphs.

    A larger target reduces per-chunk indexing cost but may dilute a focused
    passage; smaller targets improve passage precision at the cost of more
    vectors and potentially less context. Overlap preserves boundary context
    but increases storage and embedding work. A sentence longer than the target
    is kept intact rather than split.
    """

    def __init__(self, chunk_size: int = 400, overlap: int = 50) -> None:
        if isinstance(chunk_size, bool) or not isinstance(chunk_size, int) or chunk_size < 1:
            raise ValueError("chunk_size must be a positive integer")
        if isinstance(overlap, bool) or not isinstance(overlap, int) or not 0 <= overlap < chunk_size:
            raise ValueError("overlap must be non-negative and smaller than chunk_size")
        self.chunk_size = chunk_size
        self.overlap = overlap

    @staticmethod
    def _word_count(text: str) -> int:
        return len(re.findall(r"\S+", text))

    @staticmethod
    def _locate(
        text: str, page_text: Optional[str], cursor: int
    ) -> Tuple[Optional[int], Optional[int], int]:
        if not page_text:
            return None, None, cursor
        normalized_page, offset_map = _normalized_with_offsets(page_text)
        normalized_text, _ = _normalized_with_offsets(text.strip())
        if not normalized_text:
            return None, None, cursor
        match_at = normalized_page.find(normalized_text, cursor)
        if match_at < 0:
            match_at = normalized_page.find(normalized_text)
        if match_at < 0:
            return None, None, cursor
        start = offset_map[match_at]
        end = offset_map[match_at + len(normalized_text) - 1] + 1
        return start, end, match_at + len(normalized_text)

    def _groups(self, sentences: Sequence[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        groups: List[List[Dict[str, Any]]] = []
        current: List[Dict[str, Any]] = []
        current_words = 0
        for sentence in sentences:
            text = str(sentence.get("cleaned_text") or "").strip()
            if not text:
                continue
            words = self._word_count(text)
            if current and current_words + words > self.chunk_size:
                groups.append(current)
                if self.overlap:
                    carry: List[Dict[str, Any]] = []
                    carry_words = 0
                    for previous in reversed(current):
                        previous_words = self._word_count(previous["cleaned_text"])
                        if carry_words + previous_words > self.overlap:
                            break
                        carry.insert(0, previous)
                        carry_words += previous_words
                    current = carry
                    current_words = carry_words
                else:
                    current = []
                    current_words = 0
            current.append({**sentence, "cleaned_text": text})
            current_words += words
        if current:
            groups.append(current)
        return groups

    def chunk(
        self,
        preprocessing_result: Dict[str, Any],
        source_document: str,
        page_texts: Optional[Dict[int, str]] = None,
    ) -> List[ScientificChunk]:
        """Chunk an ``NLPProcessingPipeline.process`` result."""
        paper_id = preprocessing_result.get("paper_id")
        if isinstance(paper_id, bool) or not isinstance(paper_id, int) or paper_id < 0:
            raise ValueError("preprocessing_result must contain a non-negative integer paper_id")

        page_texts = page_texts or {}
        paragraph_groups: List[Tuple[Dict[str, Any], List[Dict[str, Any]]]] = []
        for paragraph in preprocessing_result.get("paragraphs", []):
            sentences = list(paragraph.get("sentences") or [])
            if not sentences and paragraph.get("cleaned_text"):
                sentences = [{
                    "paper_id": paper_id,
                    "page_number": paragraph.get("page_number"),
                    "section_name": paragraph.get("section_name"),
                    "paragraph_index": paragraph.get("paragraph_index", 0),
                    "sentence_index": 0,
                    "original_text": paragraph.get("original_text", ""),
                    "cleaned_text": paragraph["cleaned_text"],
                }]
            paragraph_groups.append((paragraph, sentences))

        chunks: List[ScientificChunk] = []
        page_cursors: Dict[int, int] = {}
        next_chunk_index = 0
        for paragraph, sentences in paragraph_groups:
            for group in self._groups(sentences):
                text = " ".join(sentence["cleaned_text"] for sentence in group).strip()
                if not text:
                    continue
                page_number = group[0].get("page_number", paragraph.get("page_number"))
                section = group[0].get(
                    "section_name", paragraph.get("section_name")
                )
                page_text = page_texts.get(page_number) if page_number is not None else None
                first_start: Optional[int] = None
                last_end: Optional[int] = None
                for sentence in group:
                    original = sentence.get("original_text") or sentence["cleaned_text"]
                    start, end, cursor = self._locate(
                        original,
                        page_text,
                        page_cursors.get(page_number, 0) if page_number is not None else 0,
                    )
                    if page_number is not None:
                        page_cursors[page_number] = cursor
                    if start is not None and end is not None:
                        first_start = start if first_start is None else min(first_start, start)
                        last_end = end if last_end is None else max(last_end, end)

                identity = "\0".join((
                    str(paper_id),
                    str(page_number or ""),
                    str(paragraph.get("paragraph_index", "")),
                    str(next_chunk_index),
                    text,
                ))
                chunk_id = hashlib.sha256(identity.encode("utf-8")).hexdigest()
                chunks.append(ScientificChunk.create(
                    chunk_id=chunk_id,
                    paper_id=paper_id,
                    chunk_index=next_chunk_index,
                    text=text,
                    page_number=page_number,
                    section_title=section,
                    start_char=first_start,
                    end_char=last_end,
                    source_document=source_document,
                ))
                next_chunk_index += 1
        return chunks
