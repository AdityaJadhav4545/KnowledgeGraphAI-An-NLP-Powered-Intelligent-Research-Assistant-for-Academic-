import re
from typing import List, Dict, Any

class SectionExtractor:
    """Detects and assigns academic sections to text segments."""

    # Patterns to identify scientific section headings
    SECTION_PATTERNS = {
        "Abstract": r'^\s*(abstract)\b',
        "Introduction": r'^\s*(introduction)\b',
        "Related Work": r'^\s*(related\s+work|literature\s+review)\b',
        "Methodology": r'^\s*(methodology|methods|materials\s+and\s+methods)\b',
        "Results": r'^\s*(results|experimental\s+results)\b',
        "Discussion": r'^\s*(discussion)\b',
        "Conclusion": r'^\s*(conclusion)\b',
        "References": r'^\s*(references|bibliography)\b',
        "Appendix": r'^\s*(appendix)\b',
    }

    @staticmethod
    def identify_section(text: str) -> str:
        """
        Identify section from heading text.
        """
        text = text.lower().strip()
        for section, pattern in SectionExtractor.SECTION_PATTERNS.items():
            if re.match(pattern, text, re.IGNORECASE):
                return section
        return "UNKNOWN"

    @staticmethod
    def extract_sections(text: str) -> List[Dict[str, Any]]:
        """
        Segment text into sections based on structural markers.
        """
        # Simplification: In a real PDF, section extraction needs
        # formatting cues (bold, font size). Heuristic: look for lines
        # that look like headings.
        lines = text.split('\n')
        sections = []
        current_section = "UNKNOWN"
        start_line = 0

        for i, line in enumerate(lines):
            line_cleaned = line.strip()
            # Heuristic: Heading lines are typically short
            if len(line_cleaned) < 50:
                identified = SectionExtractor.identify_section(line_cleaned)
                if identified != "UNKNOWN":
                    # Close previous section
                    if i > start_line:
                        sections.append({
                            "section_name": current_section,
                            "start_line": start_line,
                            "end_line": i
                        })
                    current_section = identified
                    start_line = i

        # Close final section
        sections.append({
            "section_name": current_section,
            "start_line": start_line,
            "end_line": len(lines)
        })

        return sections
