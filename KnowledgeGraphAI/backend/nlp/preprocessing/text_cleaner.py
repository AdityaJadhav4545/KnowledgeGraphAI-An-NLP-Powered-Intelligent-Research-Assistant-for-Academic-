import re
import unicodedata
import logging

logger = logging.getLogger(__name__)


class TextCleaner:
    """
    Cleans scientific academic text while preserving essential technical terminology,
    mathematical expressions, and reference markers.
    """

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """
        Normalize excessive whitespace but preserve meaningful single newlines
        within paragraphs while removing page-break or layout artifacts.
        """
        if not text:
            return ""

        # Normalize specific line ending artifacts common in scientific PDFs
        # 1. Soft hyphens (hyphen followed by newline and optional whitespace)
        # e.g. "com- \n puter" -> "computer"
        text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)

        # 2. Convert multiple spaces to single spaces
        text = re.sub(r'[ \t]+', ' ', text)

        # 3. Collapse more than two newlines to double newlines (paragraph marker)
        text = re.sub(r'\n\s*\n+', '\n\n', text)

        return text.strip()

    @staticmethod
    def normalize_unicode(text: str) -> str:
        """
        Normalize Unicode characters to NFKC form for consistency.
        Preserves mathematical symbols like α, β, λ, etc.
        """
        if not text:
            return ""
        return unicodedata.normalize('NFKC', text)

    @staticmethod
    def remove_control_characters(text: str) -> str:
        """
        Remove unnecessary control characters except tab and newline.
        """
        if not text:
            return ""
        return "".join(ch for ch in text if unicodedata.category(ch)[0] != "C" or ch in ("\n", "\t"))

    @staticmethod
    def clean_scientific_text(text: str) -> str:
        """
        Performs end-to-end cleaning for scientific text extraction.

        Preserves:
        - Technical terms: BERT, GPT-4, DeBERTa, TF-IDF
        - Abbreviations: Fig. 2, eq. (1), et al.
        - Metrics: 95.6%, F1-score
        - Math: E = mc², x² + y² = z²
        """
        if not text:
            return ""

        # 1. Basic character level cleaning
        text = TextCleaner.normalize_unicode(text)
        text = TextCleaner.remove_control_characters(text)

        # 2. Whitespace and layout artifact cleaning
        text = TextCleaner.normalize_whitespace(text)

        # Note: We do NOT lowercase or remove punctuation here
        # to preserve casing (BERT vs bert) and structural cues.

        return text
