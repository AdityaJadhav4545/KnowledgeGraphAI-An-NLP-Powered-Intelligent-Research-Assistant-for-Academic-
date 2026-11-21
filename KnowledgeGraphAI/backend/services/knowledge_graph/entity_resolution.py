import re
import logging
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict
import hashlib
import unicodedata
from difflib import SequenceMatcher

from KnowledgeGraphAI.backend.nlp.ner.entity_schema import ExtractedEntity, EntityTaxonomy

logger = logging.getLogger(__name__)


@dataclass
class CanonicalEntity:
    """A canonical (normalized) entity in the knowledge graph."""
    entity_id: str
    canonical_name: str
    entity_type: str
    aliases: List[str] = field(default_factory=list)
    first_seen: Optional[str] = None
    source_papers: List[int] = field(default_factory=list)
    occurrence_count: int = 0

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "canonical_name": self.canonical_name,
            "entity_type": self.entity_type,
            "aliases": list(self.aliases),
            "first_seen": self.first_seen,
            "source_papers": list(self.source_papers),
            "occurrence_count": self.occurrence_count,
        }


class EntityResolutionService:
    """
    Service for resolving and normalizing scientific entities.

    Handles:
    - Whitespace normalization
    - Case normalization for matching
    - Punctuation variations
    - Configurable aliases
    - Duplicate canonical entity detection
    - Original surface form preservation
    - Deterministic resolution
    - Ambiguous match flagging
    """

    def __init__(
        self,
        similarity_threshold: float = 0.85,
        enable_aliases: bool = True,
        case_sensitive_types: Optional[Set[str]] = None,
    ):
        self.similarity_threshold = similarity_threshold
        self.enable_aliases = enable_aliases

        # Retained for constructor compatibility; matching is case-insensitive
        # for every entity type. Version differences are handled separately.
        self.case_sensitive_types = case_sensitive_types or {
            "MODEL", "ALGORITHM", "DATASET", "FRAMEWORK"
        }

        # Canonical entity store: entity_id -> CanonicalEntity
        self.canonical_entities: Dict[str, CanonicalEntity] = {}

        # Normalized name -> entity_id lookup for fast matching
        self.name_index: Dict[str, str] = {}  # normalized_name -> entity_id

        # Alias management: alias -> canonical entity_id
        self.aliases: Dict[str, str] = {}

        # Ambiguous matches flagged for review
        self.ambiguous_matches: List[Dict] = []

        # Statistics
        self.stats = {
            "total_processed": 0,
            "duplicates_resolved": 0,
            "new_canonical": 0,
            "aliases_added": 0,
            "ambiguous_flagged": 0,
        }

    def _normalize_for_matching(self, text: str, entity_type: str) -> str:
        """
        Normalize text for entity matching.

        Handles:
        - Whitespace normalization
        - Case normalization (respecting case-sensitive types)
        - Punctuation normalization
        - Unicode normalization
        """
        if not text:
            return ""

        # Unicode normalization
        text = unicodedata.normalize("NFKC", text)
        text = re.sub(r"[\u2010-\u2015\u2212]", "-", text)

        # Whitespace normalization
        text = re.sub(r"\s+", " ", text).strip()

        text = text.lower()

        # Punctuation normalization for matching
        # Remove trailing punctuation that doesn't affect identity
        text = text.strip(".,;:!?()[]{}'\"")

        return text

    def _generate_entity_id(self, canonical_name: str, entity_type: str) -> str:
        """Generate deterministic entity ID from canonical name and type."""
        key = f"{entity_type}:{canonical_name}"
        return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]

    def _resolve_aliases(self, normalized_name: str, entity_type: str) -> Optional[str]:
        """Check if the normalized name matches a known alias."""
        if not self.enable_aliases:
            return None

        # Check direct alias mapping
        alias_key = self._normalize_for_matching(normalized_name, entity_type)
        if alias_key in self.aliases:
            return self.aliases[alias_key]

        return None

    def resolve_entity(self, entity: ExtractedEntity, paper_id: int, timestamp: str) -> Tuple[str, bool]:
        """
        Resolve an extracted entity to a canonical entity.

        Returns:
            Tuple of (canonical_entity_id, is_new)
        """
        self.stats["total_processed"] += 1

        # Normalize the entity text for matching
        normalized = self._normalize_for_matching(entity.text, entity.entity_type)
        if not normalized:
            # Fallback: use original text
            normalized = entity.text.strip().lower()

        # Check for exact canonical-name and alias matches.
        if normalized in self.name_index:
            entity_id = self.name_index[normalized]
            canonical = self.canonical_entities[entity_id]
            canonical.occurrence_count += 1
            if paper_id not in canonical.source_papers:
                canonical.source_papers.append(paper_id)
            self.stats["duplicates_resolved"] += 1
            return entity_id, False

        # Check aliases
        alias_id = self._resolve_aliases(self._normalize_for_matching(entity.text, entity.entity_type), entity.entity_type)
        if alias_id:
            canonical = self.canonical_entities[alias_id]
            canonical.occurrence_count += 1
            if paper_id not in canonical.source_papers:
                canonical.source_papers.append(paper_id)
            self.stats["duplicates_resolved"] += 1
            # Add this surface form as an alias if different
            if entity.text.strip() != canonical.canonical_name:
                self.add_alias(alias_id, entity.text.strip())
            return alias_id, False

        # Check for similar existing entities (fuzzy matching)
        similar_id = self._find_similar_entity(normalized, entity.entity_type)
        if similar_id:
            # Flag as ambiguous for review
            self._flag_ambiguous(entity, similar_id, normalized)
            # For now, create new entity but flag it
            pass

        # Create new canonical entity
        entity_id = self._generate_entity_id(normalized, entity.entity_type)

        # Use the original surface form as canonical name (preserving case)
        canonical_name = entity.text.strip()

        canonical = CanonicalEntity(
            entity_id=entity_id,
            canonical_name=canonical_name,
            entity_type=entity.entity_type,
            first_seen=timestamp,
            source_papers=[paper_id],
            occurrence_count=1,
        )

        # Add original text as alias if different from canonical
        if entity.text.strip() != canonical_name:
            canonical.aliases.append(entity.text.strip())
            self.aliases[self._normalize_for_matching(entity.text, entity.entity_type)] = entity_id

        self.canonical_entities[entity_id] = canonical
        self.name_index[normalized] = entity_id
        self.stats["new_canonical"] += 1

        return entity_id, True

    def _find_similar_entity(self, normalized_name: str, entity_type: str) -> Optional[str]:
        """Find potentially similar existing canonical entities."""
        # Flag related names for review, but never merge based on fuzzy matches.
        for entity_id, canonical in self.canonical_entities.items():
            if canonical.entity_type != entity_type:
                continue

            canonical_normalized = self._normalize_for_matching(canonical.canonical_name, entity_type)

            if normalized_name == canonical_normalized:
                continue
            if (
                self._are_distinct_models(normalized_name, canonical_normalized)
                or normalized_name in canonical_normalized
                or canonical_normalized in normalized_name
                or SequenceMatcher(None, normalized_name, canonical_normalized).ratio()
                >= self.similarity_threshold
            ):
                return entity_id

        return None

    def _are_distinct_models(self, name1: str, name2: str) -> bool:
        """Check if two model names are distinct versions (e.g., GPT-3 vs GPT-4)."""
        # Pattern for versioned models: name + number
        version_pattern = re.compile(r"^(.+?)[-\s]?(\d+(\.\d+)*)$")

        m1 = version_pattern.match(name1)
        m2 = version_pattern.match(name2)

        if m1 and m2:
            base1, ver1 = m1.group(1), m1.group(2)
            base2, ver2 = m2.group(1), m2.group(2)
            if base1 == base2 and ver1 != ver2:
                return True

        return False

    def _flag_ambiguous(self, entity: ExtractedEntity, similar_id: str, normalized: str) -> None:
        """Flag an ambiguous match for review."""
        similar = self.canonical_entities[similar_id]
        self.ambiguous_matches.append({
            "new_entity": entity.text,
            "new_normalized": normalized,
            "existing_entity": similar.canonical_name,
            "existing_id": similar_id,
            "entity_type": entity.entity_type,
        })
        self.stats["ambiguous_flagged"] += 1
        logger.warning(
            f"Ambiguous entity match: '{entity.text}' ({entity.entity_type}) "
            f"may match existing '{similar.canonical_name}' ({similar_id})"
        )

    def add_alias(self, entity_id: str, alias: str) -> bool:
        """Add an alias for a canonical entity."""
        if entity_id not in self.canonical_entities:
            return False

        canonical = self.canonical_entities[entity_id]
        normalized_alias = self._normalize_for_matching(alias, canonical.entity_type)
        if not normalized_alias:
            return False

        existing_name_id = self.name_index.get(normalized_alias)
        existing_alias_id = self.aliases.get(normalized_alias)
        if existing_name_id not in (None, entity_id) or existing_alias_id not in (None, entity_id):
            return False

        if existing_name_id == entity_id or existing_alias_id == entity_id:
            return False

        canonical.aliases.append(alias.strip())
        self.aliases[normalized_alias] = entity_id
        self.name_index[normalized_alias] = entity_id
        self.stats["aliases_added"] += 1
        return True

    def get_canonical(self, entity_id: str) -> Optional[CanonicalEntity]:
        """Get a canonical entity by ID."""
        return self.canonical_entities.get(entity_id)

    def get_by_normalized_name(self, normalized_name: str) -> Optional[CanonicalEntity]:
        """Get canonical entity by normalized name."""
        normalized = self._normalize_for_matching(normalized_name, "")
        entity_id = self.name_index.get(normalized) or self.aliases.get(normalized)
        if entity_id:
            return self.canonical_entities.get(entity_id)
        return None

    def get_ambiguous_matches(self) -> List[Dict]:
        """Get all ambiguous matches flagged for review."""
        return self.ambiguous_matches.copy()

    def get_stats(self) -> Dict[str, Any]:
        """Get resolution statistics."""
        return {
            **self.stats,
            "total_canonical": len(self.canonical_entities),
            "total_aliases": len(self.aliases),
        }

    def export_canonical_entities(self) -> List[Dict]:
        """Export all canonical entities for persistence."""
        return [c.to_dict() for c in self.canonical_entities.values()]

    def import_canonical_entities(self, entities: List[Dict]) -> int:
        """Import canonical entities from persistence."""
        self.canonical_entities.clear()
        self.name_index.clear()
        self.aliases.clear()
        count = 0
        for data in entities:
            entity_id = data["entity_id"]
            canonical = CanonicalEntity(
                entity_id=data["entity_id"],
                canonical_name=data["canonical_name"],
                entity_type=data["entity_type"],
                aliases=list(data.get("aliases", [])),
                first_seen=data.get("first_seen"),
                source_papers=list(data.get("source_papers", [])),
                occurrence_count=data.get("occurrence_count", 0),
            )

            self.canonical_entities[entity_id] = canonical

            # Rebuild indexes
            normalized = self._normalize_for_matching(data["canonical_name"], data["entity_type"])
            self.name_index[normalized] = entity_id

            for alias in data.get("aliases", []):
                normalized_alias = self._normalize_for_matching(alias, data["entity_type"])
                self.aliases[normalized_alias] = entity_id
                self.name_index.setdefault(normalized_alias, entity_id)

            count += 1

        return count