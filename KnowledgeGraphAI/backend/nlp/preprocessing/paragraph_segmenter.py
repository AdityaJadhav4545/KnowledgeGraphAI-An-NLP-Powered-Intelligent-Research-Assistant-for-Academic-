import re
from typing import List, Dict, Any, Optional

from KnowledgeGraphAI.backend.nlp.preprocessing.text_cleaner import TextCleaner


class ParagraphSegmenter:
    """
    Segments text into paragraphs with page and sentence provenance.

    Detects paragraph boundaries based on:
    - Double line breaks (empty lines)
    - Single line breaks with content changes
    - Section boundaries
    - Page-level associations
    """

    def __init__(self, paper_id: int = 0):
        self.paper_id = paper_id
        self.paragraphs: List[Dict[str, Any]] = []
        self.last_page_number: int = 0
        self.last_section_name: str = "Unknown"

    def segment_paragraphs(
        self,
        sentences: List[Dict[str, Any]],
        page_number: int
    ) -> List[Dict[str, Any]]:
        """
        Group sentences into paragraphs based on the sentence list.

        Args:
            sentences: List of sentence dicts with paragraph_index info
            page_number: The page number these sentences belong to

        Returns:
            List of paragraph dicts with provenance
        """
        # Group sentences by paragraph_index
        paragraph_groups: Dict[int, List[Dict[str, Any]]] = {}

        for sentence in sentences:
            pidx = sentence.get("paragraph_index", 0)
            if pidx not in paragraph_groups:
                paragraph_groups[pidx] = []
            paragraph_groups[pidx].append(sentence)

        # Build paragraphs from groups
        self.paragraphs = []
        for pidx in sorted(paragraph_groups.keys()):
            group = paragraph_groups[pidx]

            # Build cleaned paragraph text from all sentences
            cleaned_text_parts = []
            original_text_parts = []

            for sent in group:
                cleaned_text_parts.append(sent.get("cleaned_text", ""))
                original_text_parts.append(sent.get("original_text", ""))

            paragraph_text = " ".join(cleaned_text_parts).strip()
            original_paragraph = " ".join(original_text_parts).strip()

            # Skip empty paragraphs
            if not paragraph_text:
                continue

            self.paragraphs.append({
                "paper_id": self.paper_id,
                "page_number": page_number,
                "paragraph_index": pidx,
                "section_name": self.last_section_name,
                "original_text": original_paragraph,
                "cleaned_text": paragraph_text,
                "sentence_count": len(group),
                "sentences": group,
            })

        return self.paragraphs

    def detect_paragraph_boundaries(
        self,
        raw_text: str,
        page_number: int,
        section_name: str = "Unknown"
    ) -> List[Dict[str, Any]]:
        """
        Detect paragraph boundaries from raw text.

        Args:
            raw_text: Raw text from a PDF page
            page_number: The page number
            section_name: The academic section name

        Returns:
            List of paragraph dicts
        """
        self.last_page_number = page_number
        self.last_section_name = section_name

        # Normalize whitespace first
        normalized = TextCleaner.normalize_whitespace(raw_text)

        # Split by double line breaks (paragraph boundaries)
        # Handle various newline conventions
        paragraphs_raw = re.split(r'\n\s*\n', normalized)

        self.paragraphs = []
        for pidx, para_text in enumerate(paragraphs_raw):
            para_text = para_text.strip()
            if not para_text:
                continue

            # Create paragraph entry
            self.paragraphs.append({
                "paper_id": self.paper_id,
                "page_number": page_number,
                "paragraph_index": pidx,
                "section_name": section_name,
                "original_text": para_text,
                "cleaned_text": para_text,
                "sentence_count": 0,
                "sentences": [],
            })

        return self.paragraphs

    def get_paragraph_statistics(self) -> Dict[str, Any]:
        """Return statistics about the segmented paragraphs."""
        if not self.paragraphs:
            return {"total_paragraphs": 0, "avg_sentences_per_paragraph": 0}

        total = len(self.paragraphs)
        total_sentences = sum(p.get("sentence_count", 0) for p in self.paragraphs)
        avg = total_sentences / total if total > 0 else 0

        return {
            "total_paragraphs": total,
            "total_sentences": total_sentences,
            "avg_sentences_per_paragraph": round(avg, 2),
        }
