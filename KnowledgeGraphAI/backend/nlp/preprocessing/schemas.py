from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ExtractedSentence:
    """A sentence extracted from a PDF with full provenance."""
    paper_id: int
    page_number: int
    section_name: str
    paragraph_index: int
    sentence_index: int
    original_text: str
    cleaned_text: str

@dataclass
class ExtractedParagraph:
    """A paragraph extracted from a PDF with full provenance."""
    paper_id: int
    page_number: int
    paragraph_index: int
    section_name: str
    original_text: str
    cleaned_text: str
    sentence_count: int = 0
    sentences: List[ExtractedSentence] = field(default_factory=list)

@dataclass
class PreprocessingResult:
    """Result of the full preprocessing pipeline."""
    paper_id: int
    processing_status: str = "pending"
    statistics: Dict[str, Any] = field(default_factory=dict)
    paragraphs: List[ExtractedParagraph] = field(default_factory=list)
    processing_metadata: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)