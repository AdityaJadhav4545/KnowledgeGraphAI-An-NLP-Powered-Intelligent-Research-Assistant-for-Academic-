from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from KnowledgeGraphAI.backend.nlp.ner.entity_schema import ExtractedEntity
from KnowledgeGraphAI.backend.nlp.relation_extraction.taxonomy import (
    RELATION_TYPES,
    is_valid_relation,
)


@dataclass
class ExtractedRelation:
    """A extracted relation with full provenance."""

    # The relation type, from the supported taxonomy
    relation: str

    # Subject entity provenance
    subject_entity_id: str
    subject_text: str
    subject_start: int
    subject_end: int
    subject_entity_type: str

    # Object entity provenance
    object_entity_id: str
    object_text: str
    object_start: int
    object_end: int
    object_entity_type: str

    # Provenance
    paper_id: int
    sentence_id: int
    page_number: int
    evidence: str

    # Confidence score from the extraction model / rule
    confidence: float

    # Extraction method provenance
    extraction_method: str = "relabel"  # rule_based | rebel | classifier

    # Normalized forms
    subject_normalized: Optional[str] = None
    object_normalized: Optional[str] = None
    original_text: Optional[str] = None
    cleaned_text: Optional[str] = None

    def __post_init__(self) -> None:
        if self.confidence < 0.0 or self.confidence > 1.0:
            raise ValueError("Confidence must be in [0, 1].")
        if not is_valid_relation(self.relation):
            raise ValueError(
                f"Unknown relation type '{self.relation}'. "
                f"Valid types: {', '.join(sorted(RELATION_TYPES))}"
            )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "subject": {
                "text": self.subject_text,
                "label": self.subject_entity_type,
                "start": self.subject_start,
                "end": self.subject_end,
            },
            "relation": self.relation,
            "object": {
                "text": self.object_text,
                "label": self.object_entity_type,
                "start": self.object_start,
                "end": self.object_end,
            },
            "confidence": self.confidence,
            "paper_id": self.paper_id,
            "sentence_id": self.sentence_id,
            "page_number": self.page_number,
            "evidence": self.evidence,
            "extraction_method": self.extraction_method,
            "original_text": self.original_text,
            "cleaned_text": self.cleaned_text,
        }