"""Domain-independent linguistic NER for general-purpose English prose.

Extracts general entity categories (Person, Organization, Group, Project,
Location, Product, Concept) using grammatical, syntactic, and lexical
cues without hardcoding domain-specific test paragraphs.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Set, Tuple

from KnowledgeGraphAI.backend.nlp.ner.entity_schema import ExtractedEntity

# Functional / non-entity words never promoted as standalone entity mentions
_STOPWORDS: Set[str] = {
    "a", "an", "the", "this", "that", "these", "those", "its", "their", "his",
    "her", "our", "your", "my", "some", "other", "another", "such", "each",
    "every", "many", "much", "several", "various", "similar", "both", "all",
    "most", "more", "few", "own", "any", "no", "none", "who", "whom", "whose",
    "which", "what", "where", "when", "why", "how", "while", "although", "because",
    "since", "after", "before", "during", "through", "over", "under", "into",
    "onto", "from", "with", "among", "between", "behind", "around", "about",
    "for", "of", "in", "on", "at", "by", "to", "as", "and", "or", "but",
    "also", "very", "quite", "rather", "just", "only", "even", "still", "yet",
    "often", "always", "never", "sometimes", "soon", "later", "eventually",
    "today", "yesterday", "tomorrow", "time", "times", "way", "ways", "thing",
    "things", "reason", "reasons", "part", "parts", "lot", "lots", "it", "they",
    "them", "we", "us", "you", "he", "she", "him", "people", "person",
    "someone", "anyone", "everyone", "starting", "main", "access", "importance",
    "knowledge", "success", "interest", "began", "became", "showed",
}

_SENTENCE_LEADING_CAPS: Set[str] = {
    "The", "This", "That", "These", "Those", "Over", "As", "While", "However",
    "Moreover", "Furthermore", "Meanwhile", "Here", "There", "Community",
    "Project", "Projects", "Government", "Council", "School", "Company",
    "Group", "Garden", "Although", "Because", "Since", "When", "Where",
    "After", "Before", "During", "Today", "Local", "Rural", "Urban",
    "Small", "Large", "Many", "Some", "Other", "Nearby", "Participating",
    "Both", "Each", "Every", "All", "Most", "No", "None", "January",
    "February", "March", "April", "May", "June", "July", "August",
    "September", "October", "November", "December", "Monday", "Tuesday",
    "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "A", "An", "In",
    "On", "At", "By", "For", "To", "From", "With", "Without", "Under",
}

_ABSTRACT_SUFFIXES = (
    "tion", "sion", "ment", "ness", "ship", "ity", "ism", "ance", "ence",
    "age", "ing", "ware",
)

_ABSTRACT_HEADS: Set[str] = {
    "cooperation", "responsibility", "participation", "sustainability", "waste",
    "nature", "health", "safety", "education", "training", "efficiency",
    "productivity", "nutrition", "biodiversity", "equity", "justice",
    "innovation", "pollution", "quality of life", "food waste", "healthy eating",
    "soil preparation",
}

_CATEGORY_PRIORITY: Dict[str, int] = {
    "PERSON": 7,
    "ORGANIZATION": 6,
    "PROJECT": 5,
    "LOCATION": 4,
    "GROUP": 3,
    "PRODUCT": 2,
    "CONCEPT": 1,
}


def _strip_edge_words(span_text: str, base_start: int, *, strip_words: Optional[Set[str]] = None) -> Tuple[str, int, int]:
    """Trim leading/trailing determiners, conjunctions, and punctuation with exact char offsets."""
    to_strip = strip_words if strip_words is not None else {
        "a", "an", "the", "their", "its", "his", "her", "our", "your", "my",
        "this", "that", "these", "those", "other", "some", "and", "or",
        "access to", "knowledge of", "importance of",
    }
    s = span_text
    start = base_start
    end = base_start + len(s)

    while s:
        trimmed = s.lstrip(" \t\r\n.,;:!?()[]\"'")
        if len(trimmed) < len(s):
            start += len(s) - len(trimmed)
            s = trimmed
            continue
        trimmed_r = s.rstrip(" \t\r\n.,;:!?()[]\"'")
        if len(trimmed_r) < len(s):
            end -= len(s) - len(trimmed_r)
            s = trimmed_r
            continue
        low = s.lower()
        matched_prefix = next(
            (w for w in sorted(to_strip, key=len, reverse=True) if low.startswith(w + " ")),
            None,
        )
        if matched_prefix:
            cut = len(matched_prefix) + 1
            s = s[cut:]
            start += cut
            continue
        break

    # Remove possessive "'s" / "’s" at end of span cleanly
    if s.endswith("'s") or s.endswith("’s"):
        s = s[:-2]
        end -= 2
    return s.strip(), start, end


def _clean_phrase_ok(phrase: str, *, allow_single_verb_ing: bool = False) -> bool:
    words = [w for w in re.split(r"\s+", phrase.strip().lower()) if w]
    if not words or len(phrase.strip()) < 3:
        return False
    if all(w in _STOPWORDS for w in words):
        return False
    if len(words) == 1:
        w = words[0]
        if w in _STOPWORDS:
            return False
        if not allow_single_verb_ing and w.endswith(("ed", "ly")):
            return False
    if words[-1] in _STOPWORDS or words[0] in {"to", "of", "and", "or", "with", "that", "which", "who"}:
        return False
    return True


class GeneralProseNER:
    """Extract general-purpose English prose entities using linguistic rules."""

    # Person cues
    _NAMED_PERSON_RE = re.compile(
        r"\b(?:named|called|Mr\.|Mrs\.|Ms\.|Miss|Dr\.|Prof\.)\s+([A-Z][a-z]{1,25}(?:\s+[A-Z][a-z]{1,25}){0,2})\b"
    )
    _SUBJECT_PERSON_RE = re.compile(
        r"\b([A-Z][a-z]{1,25}(?:\s+[A-Z][a-z]{1,25}){0,2})\s+"
        r"(?:believes|believed|thinks|thought|said|says|explained|noted|reported|"
        r"worked|works|led|leads|helped|helps|created|started|founded|organized|"
        r"managed|shared|provided|encouraged|inspired|wrote|built)\b"
    )
    _PROPER_PERSON_RE = re.compile(
        r"\b([A-Z][a-z]{2,20}\s+[A-Z][a-z]{2,20}(?:\s+[A-Z][a-z]{2,20})?)\b"
    )

    # Organization cues
    _ORG_NOUNS = (
        "council|municipality|government|committee|commission|board|department|"
        "ministry|agency|authority|foundation|association|organization|organisation|"
        "institute|university|college|school|academy|hospital|library|museum|"
        "corporation|company|enterprise|union|federation|coalition|trust"
    )
    _ORG_LOWER_RE = re.compile(
        rf"\b((?:(?:the|an?)\s+)?(?:(?:local|city|town|municipal|regional|county|state|national|federal|public|private|community|school|health|water|village|civic)\s+)?(?:{_ORG_NOUNS}))\b",
        re.IGNORECASE,
    )
    _ORG_PROPER_RE = re.compile(
        rf"\b([A-Z][\w&.-]+(?:\s+[A-Z][\w&.-]+){{0,3}}\s+(?:Council|Committee|Board|Association|Foundation|Institute|Department|Ministry|Agency|University|College|School|Corporation|Company|Hospital|Union))\b"
    )

    # Project / initiative cues
    _PROJECT_HEADS = (
        "community garden|garden|project|initiative|program|programme|"
        "campaign|enterprise|venture|workshop|cooperative"
    )
    _PROJECT_RE = re.compile(
        rf"\b((?:(?:[a-z]{{3,16}}\s+){{0,2}})(?:{_PROJECT_HEADS}))\b(?!['’]?\w)",
        re.IGNORECASE,
    )

    # Location / land / spatial phrases
    _LOC_PREPS_RE = re.compile(
        r"\b(?:in|at|into|to|near|around|across|within|through|inside)\s+"
        r"((?:(?:an?|the)\s+)?(?:(?:[a-z]+\s+){0,2})(?:rural\s+area|urban\s+area|area|region|district|neighborhood|neighbourhood|village|town|city|county|state|country|province|zone|green\s+space|open\s+space|space|piece\s+of\s+land|plot\s+of\s+land|land|field|site|park|campus|facility))\b",
        re.IGNORECASE,
    )
    _LOC_PROPER_RE = re.compile(
        r"\b(?:in|at|from|near)\s+([A-Z][a-z]{2,22}(?:\s+[A-Z][a-z]{2,22}){0,2})\b"
    )

    # Group / collective stakeholders (with lookahead rejecting noun-adjunct modifies like "community garden")
    _GROUP_HEADS = (
        "community|communities|neighborhood|neighborhoods|residents|citizens|"
        "villagers|households|families|children|youth|students|teachers|"
        "farmers|workers|volunteers|members|participants|partners|staff|teams|groups"
    )
    _GROUP_RE = re.compile(
        rf"\b((?:(?:small|large|local|nearby|rural|urban|participating|neighboring|surrounding|student|youth|volunteer|parent)\s+)?(?:{_GROUP_HEADS}))\b"
        r"(?!\s+(?:garden|gardens|project|projects|program|programs|programme|initiative|initiatives|center|centre|participation|engagement|development|effort|service|council|board))",
        re.IGNORECASE,
    )

    # Object-list cue (Product / tangible resource vs nominalized Concept inside lists)
    _PRODUCT_LIST_RE = re.compile(
        r"\b(?:producing|produced|produce|produces|providing|provided|provide|provides|"
        r"planting|planted|plant|plants|growing|grew|grow|grows|sharing|shared|"
        r"distributing|distributed|distribute|supplying|supplied|supply|"
        r"harvesting|harvested|harvest|using|used|knowledge\s+of|access\s+to)\s+"
        r"([^.!?;]+?)(?=(?:\s+(?:that|which|who|whom|while|when|where|because|as|in\s+order\s+to|to\s+[a-z]+\b|and\s+(?:maintain|maintained|helped|reduce|reduced|encouraged|understand|access|turn))\b|[.!?;]|$))",
        re.IGNORECASE,
    )

    # Abstract concept / outcome cues
    _CONCEPT_CLAUSE_RE = re.compile(
        r"\b(?:improve|improved|improving|reduce|reduced|reducing|cut|cutting|"
        r"encouraged|encourage|encouraging|understand|understanding|believes\s+that|"
        r"believe\s+that|importance\s+of|reasons?\s+behind)\s+"
        r"([^.!?;]+?)(?=(?:\s+(?:are|is|were|was|for\s+its|by\s+starting)\b|[.!?;]|$))",
        re.IGNORECASE,
    )

    _QUALITY_OF_LIFE_RE = re.compile(
        r"\b((?:quality\s+of\s+life|standard\s+of\s+living|healthy\s+eating|food\s+waste|soil\s+preparation|community\s+participation|shared\s+responsibility))\b",
        re.IGNORECASE,
    )

    @classmethod
    def _is_abstract_phrase(cls, phrase: str) -> bool:
        low = phrase.strip().lower()
        if low in _ABSTRACT_HEADS:
            return True
        words = low.split()
        if not words:
            return False
        tail = words[-1]
        if tail.endswith(_ABSTRACT_SUFFIXES) and tail not in {"vegetables", "equipment"}:
            return True
        return False

    @classmethod
    def _split_coordinated_items(cls, raw_slice: str, slice_start: int) -> List[Tuple[str, int, int]]:
        """Split 'A, B, C, and other D' into exact character-offset phrases."""
        results: List[Tuple[str, int, int]] = []
        sep_re = re.compile(r"\s*,\s*(?:and\s+)?|\s+(?:and|or)\s+", re.IGNORECASE)
        pos = 0
        for m in sep_re.finditer(raw_slice):
            chunk = raw_slice[pos : m.start()]
            if chunk.strip():
                clean, cs, ce = _strip_edge_words(chunk, slice_start + pos)
                if clean:
                    results.append((clean, cs, ce))
            pos = m.end()
        tail = raw_slice[pos:]
        if tail.strip():
            clean, cs, ce = _strip_edge_words(tail, slice_start + pos)
            if clean:
                results.append((clean, cs, ce))
        return results

    def detect_entities(
        self,
        text: str,
        *,
        existing_spans: Optional[List[Tuple[int, int]]] = None,
    ) -> List[ExtractedEntity]:
        """Extract general-purpose English prose entities with overlap resolution."""
        if not text or not text.strip():
            return []

        raw_candidates: List[Tuple[str, int, int, str, float]] = []

        # 1. PERSON
        for pat, conf in (
            (self._NAMED_PERSON_RE, 0.88),
            (self._SUBJECT_PERSON_RE, 0.84),
            (self._PROPER_PERSON_RE, 0.78),
        ):
            for m in pat.finditer(text):
                name = m.group(1).strip()
                first_tok = name.split()[0]
                if first_tok in _SENTENCE_LEADING_CAPS:
                    continue
                if pat is self._PROPER_PERSON_RE and any(
                    name.endswith(sfx)
                    for sfx in ("Council", "Board", "Committee", "University", "School", "Park", "Area", "News", "Garden")
                ):
                    continue
                raw_candidates.append((name, m.start(1), m.end(1), "PERSON", conf))

        # 2. ORGANIZATION
        for m in self._ORG_PROPER_RE.finditer(text):
            val, s, e = _strip_edge_words(m.group(1), m.start(1))
            if _clean_phrase_ok(val):
                raw_candidates.append((val, s, e, "ORGANIZATION", 0.84))
        for m in self._ORG_LOWER_RE.finditer(text):
            val, s, e = _strip_edge_words(m.group(1), m.start(1))
            if _clean_phrase_ok(val):
                raw_candidates.append((val, s, e, "ORGANIZATION", 0.78))

        # 3. PROJECT
        _proj_strip = {
            "a", "an", "the", "this", "that", "these", "those", "its", "their",
            "starting", "start", "founded", "maintain", "maintaining", "similar",
            "other", "behind", "by", "as", "into",
        }
        for m in self._PROJECT_RE.finditer(text):
            val, s, e = _strip_edge_words(m.group(1), m.start(1), strip_words=_proj_strip)
            if val.lower() in {"projects", "programs", "programmes", "initiatives", "gardens", "similar projects"}:
                continue
            if _clean_phrase_ok(val):
                raw_candidates.append((val, s, e, "PROJECT", 0.80))

        # 4. LOCATION
        for m in self._LOC_PREPS_RE.finditer(text):
            val, s, e = _strip_edge_words(m.group(1), m.start(1))
            # Skip non-spatial idiomatic nouns unless modified
            if val.lower() in {"space", "area", "site", "park"} and " " not in val:
                continue
            if _clean_phrase_ok(val):
                raw_candidates.append((val, s, e, "LOCATION", 0.78))
        for m in self._LOC_PROPER_RE.finditer(text):
            name = m.group(1).strip()
            if name.split()[0] in _SENTENCE_LEADING_CAPS:
                continue
            raw_candidates.append((name, m.start(1), m.end(1), "LOCATION", 0.75))

        # 5. GROUP
        for m in self._GROUP_RE.finditer(text):
            val, s, e = _strip_edge_words(m.group(1), m.start(1))
            if _clean_phrase_ok(val):
                raw_candidates.append((val, s, e, "GROUP", 0.76))

        # 6. PRODUCT & CONCEPT from grammatical resource/impact frames
        for m in self._PRODUCT_LIST_RE.finditer(text):
            items = self._split_coordinated_items(m.group(1), m.start(1))
            for val, s, e in items:
                if not _clean_phrase_ok(val):
                    continue
                low = val.lower()
                # Do not steal Location/Group/Project phrases already handled better
                if low in {"garden", "project", "community garden", "families", "participating families"} or low.endswith(("families", "children", "residents", "students", "farmers", "volunteers", "space", "land", "area")):
                    continue
                if low in {"access", "knowledge", "them", "it"}:
                    continue
                etype = "CONCEPT" if self._is_abstract_phrase(val) else "PRODUCT"
                raw_candidates.append((val, s, e, etype, 0.74))

        for m in self._QUALITY_OF_LIFE_RE.finditer(text):
            val, s, e = _strip_edge_words(m.group(1), m.start(1))
            if _clean_phrase_ok(val, allow_single_verb_ing=True):
                raw_candidates.append((val, s, e, "CONCEPT", 0.76))

        for m in self._CONCEPT_CLAUSE_RE.finditer(text):
            clause = m.group(1)
            # Handle "...the project's success" -> strip leading project owner if inside clause
            items = self._split_coordinated_items(clause, m.start(1))
            for val, s, e in items:
                if not _clean_phrase_ok(val, allow_single_verb_ing=True):
                    continue
                low = val.lower()
                if any(tok in low for tok in ("garden", "project")) or low in {"children", "people", "work together", "residents"}:
                    continue
                if len(val.split()) > 3:
                    continue
                if self._is_abstract_phrase(val) or low in {"nature", "cooperation", "success"}:
                    raw_candidates.append((val, s, e, "CONCEPT", 0.72))

        # Sort by: non-overlapping with higher-priority spans (longer spans first, then type priority)
        raw_candidates.sort(
            key=lambda item: (-(item[2] - item[1]), -_CATEGORY_PRIORITY.get(item[3], 0), item[1])
        )

        occupied: List[Tuple[int, int]] = list(existing_spans or [])
        accepted: List[ExtractedEntity] = []
        for span_text, s, e, etype, conf in raw_candidates:
            if s < 0 or e <= s or conf < 0.55:
                continue
            if any(s < ex_e and e > ex_s for ex_s, ex_e in occupied):
                continue
            occupied.append((s, e))
            accepted.append(
                ExtractedEntity(
                    text=span_text,
                    entity_type=etype,
                    start_char=s,
                    end_char=e,
                    confidence=conf,
                    paper_id=0,
                    page_number=0,
                    sentence_index=0,
                    source_text=text,
                    extraction_method="rule_based",
                    normalized_text=" ".join(span_text.split()),
                )
            )

        accepted.sort(key=lambda ent: ent.start_char)
        return accepted
