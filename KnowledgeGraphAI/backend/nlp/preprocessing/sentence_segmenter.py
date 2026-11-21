import re
from typing import List, Dict, Any
from KnowledgeGraphAI.backend.nlp.preprocessing.text_cleaner import TextCleaner


class SentenceSegmenter:
    """
    Robust sentence segmentation system for scientific academic text.
    Handles abbreviations, decimal numbers, and citations without incorrectly splitting them.
    """

    # Abbreviations that should not trigger sentence boundary
    ABBREVIATIONS = {
        'dr', 'mr', 'ms', 'mrs', 'prof', 'fig', 'eq', 'et', 'al', 'e', 'g', 'i', 'e', 'vs'
    }

    @staticmethod
    def segment_sentences(cleaned_text: str, paper_id: int, page_number: int, section_name: str) -> List[Dict[str, Any]]:
        """
        Segment text into sentences with full provenance tracking.

        Args:
            cleaned_text: Text already cleaned by TextCleaner
            paper_id: Provenance identifier
            page_number: Provenance identifier
            section_name: Provenance identifier

        Returns:
            List of structured sentence records.
        """
        sentences = []

        # Paragraph segmentation (assumes double-newline separation)
        paragraphs = re.split(r'\n\s*\n', cleaned_text)

        for p_idx, paragraph in enumerate(paragraphs):
            para_text = paragraph.strip()
            if not para_text:
                continue

            # Sentence segmentation logic
            # Use lookbehind for punctuation followed by space.
            # To avoid splitting abbreviations, we look ahead for uppercase.
            # This is a robust heuristic for scientific text.

            # Split on [.!?] followed by whitespace
            # Exclude splitting if the preceding word is a common abbreviation

            # Implementation:
            # 1. Temporarily replace boundaries after common abbreviations with a placeholder
            # 2. Split on remaining boundaries
            # 3. Restore boundaries

            text = para_text
            for abbrev in SentenceSegmenter.ABBREVIATIONS:
                text = re.sub(rf'\b{abbrev}\.', f'{abbrev}<ABBR>', text, flags=re.IGNORECASE)

            # Split on boundaries followed by space
            raw_sentences = re.split(r'(?<=[.!?])\s+', text)

            for s_idx, sent_text in enumerate(raw_sentences):
                # Restore abbreviations
                sent_text = sent_text.replace('<ABBR>', '.')

                cleaned_sent = TextCleaner.clean_scientific_text(sent_text)

                if cleaned_sent:
                    sentences.append({
                        "paper_id": paper_id,
                        "page_number": page_number,
                        "section_name": section_name,
                        "paragraph_index": p_idx,
                        "sentence_index": s_idx,
                        "original_text": sent_text,
                        "cleaned_text": cleaned_sent
                    })

        return sentences
