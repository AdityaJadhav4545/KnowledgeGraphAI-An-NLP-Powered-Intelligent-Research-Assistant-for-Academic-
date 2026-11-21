from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, ClassVar

# ---------------------------------------------------------------------------
# Scientific + general-purpose English prose entity categories
# ---------------------------------------------------------------------------
SCIENTIFIC_ENTITY_CATEGORIES: List[str] = [
    "ALGORITHM",
    "MODEL",
    "DATASET",
    "METRIC",
    "TASK",
    "METHODOLOGY",
    "RESEARCH_PROBLEM",
    "OPTIMIZER",
    "FRAMEWORK",
    "ORGANIZATION",
    "AUTHOR",
]

GENERAL_ENTITY_CATEGORIES: List[str] = [
    "PERSON",
    "GROUP",
    "PROJECT",
    "LOCATION",
    "PRODUCT",
    "CONCEPT",
]

ENTITY_CATEGORIES: List[str] = SCIENTIFIC_ENTITY_CATEGORIES + GENERAL_ENTITY_CATEGORIES

# ---------------------------------------------------------------------------
# Shared taxonomy definition
# ---------------------------------------------------------------------------
class EntityTaxonomy:
    """Central taxonomy of scientific entity types.

    Provides lookup by name/index and supports future extension.
    """

    NAMES: ClassVar[List[str]] = ENTITY_CATEGORIES
    INDEX: ClassVar[Dict[str, int]] = {name: i for i, name in enumerate(ENTITY_CATEGORIES)}
    NAMES_BY_INDEX: ClassVar[Dict[int, str]] = {i: name for i, name in enumerate(ENTITY_CATEGORIES)}

    @classmethod
    def is_valid(cls, entity_type: str) -> bool:
        return entity_type in cls.INDEX

    @classmethod
    def valid_names(cls) -> List[str]:
        return list(cls.NAMES)


# ---------------------------------------------------------------------------
# Pydantic / dataclass schemas for extracted entities
# ---------------------------------------------------------------------------
@dataclass
class ExtractedEntity:
    """A scientific entity extracted from a paper, with full provenance."""

    # Surface text and provenance
    text: str
    entity_type: str
    start_char: int
    end_char: int
    confidence: float
    paper_id: int
    page_number: int
    sentence_index: int
    source_text: str

    # Derived / processing metadata
    extraction_method: str = "rule_based"  # rule_based | transformer | hybrid

    # Normalized forms (useful for deduplication / linking)
    normalized_text: Optional[str] = None
    original_text: Optional[str] = None
    cleaned_text: Optional[str] = None

    # Class-level check that the entity type is recognized
    _taxonomy: ClassVar = EntityTaxonomy()

    def __post_init__(self) -> None:
        if self.entity_type not in self._taxonomy.INDEX:
            raise ValueError(
                f"Unknown entity type '{self.entity_type}'. "
                f"Valid types: {self._taxonomy.valid_names()}"
            )
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError("Confidence must be in [0, 1].")
        if self.start_char < 0 or self.end_char <= self.start_char:
            raise ValueError(
                f"Invalid character offsets: start={self.start_char}, end={self.end_char}"
            )
        # Preserve original surface text if normalized_text not set
        if self.normalized_text is None:
            self.normalized_text = self.text.strip()

    def __str__(self) -> str:
        return f"[{self.entity_type}] '{self.text}' at [{self.start_char}-{self.end_char}]"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "entity_type": self.entity_type,
            "start": self.start_char,
            "end": self.end_char,
            "confidence": self.confidence,
            "paper_id": self.paper_id,
            "page_number": self.page_number,
            "sentence_index": self.sentence_index,
            "source_text": self.source_text,
            "extraction_method": self.extraction_method,
            "normalized_text": self.normalized_text,
            "original_text": self.original_text,
            "cleaned_text": self.cleaned_text,
        }


@dataclass
class ExtractedSentence:
    """A sentence extracted from a paper, with full provenance."""

    paper_id: int
    page_number: int
    section_name: str
    paragraph_index: int
    sentence_index: int
    original_text: str
    cleaned_text: str


@dataclass
class EntityBatch:
    """A batch of entities from a single paper / page / sentence."""

    paper_id: int
    page_number: int
    sentence_index: int
    entities: List[ExtractedEntity] = field(default_factory=list)

    def add(self, entity: ExtractedEntity) -> None:
        # Basic deduplication: exact text + type duplicate check
        for existing in self.entities:
            if (
                entity.text == existing.text
                and entity.entity_type == existing.entity_type
                and entity.start_char == existing.start_char
            ):
                return  # skip duplicate
        self.entities.append(entity)

    def by_category(self, category: str) -> List[ExtractedEntity]:
        return [e for e in self.entities if e.entity_type == category]


# ---------------------------------------------------------------------------
# Global taxonomy lookup
# ---------------------------------------------------------------------------
def is_valid_entity_type(entity_type: str) -> bool:
    """Quick check without constructing a dataclass."""
    return EntityTaxonomy.is_valid(entity_type)


def valid_entity_types() -> List[str]:
    """Return sorted list of valid entity type names."""
    return EntityTaxonomy.valid_names()


# ---------------------------------------------------------------------------
# Example / demo entities (for documentation / testing)
# ---------------------------------------------------------------------------
EXAMPLE_ENTITIES: Dict[str, List[ExtractedEntity]] = {
    "sample_paper_123": [
        ExtractedEntity(
            text="BERT",
            entity_type="MODEL",
            start_char=15,
            end_char=19,
            confidence=0.96,
            paper_id=123,
            page_number=3,
            sentence_index=2,
            source_text="We used BERT for text classification.",
            extraction_method="rule_based",
        ),
        ExtractedEntity(
            text="F1-score",
            entity_type="METRIC",
            start_char=42,
            end_char=49,
            confidence=0.91,
            paper_id=123,
            page_number=3,
            sentence_index=2,
            source_text="We used BERT for text classification.",
            extraction_method="rule_based",
        ),
    ],
}