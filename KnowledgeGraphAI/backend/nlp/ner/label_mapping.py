from __future__ import annotations

from typing import Dict, List, Tuple, ClassVar

# Scientific + general-purpose English prose entity categories
ENTITY_CATEGORIES: List[str] = [
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
    "PERSON",
    "GROUP",
    "PROJECT",
    "LOCATION",
    "PRODUCT",
    "CONCEPT",
]

# BIO label scheme matching all supported entity categories
NER_LABELS: List[str] = [
    *[
        bio
        for cat in ENTITY_CATEGORIES
        for bio in (f"B-{cat}", f"I-{cat}")
    ],
    "O",
]

# Mapping from label string <-> id
LABEL_TO_ID: Dict[str, int] = {label: i for i, label in enumerate(NER_LABELS)}
ID_TO_LABEL: Dict[int, str] = {i: label for i, label in enumerate(NER_LABELS)}

# Human-readable mapping from entity type to BIO labels
ENTITY_TYPE_LABELS: Dict[str, List[str]] = {}
for entity_type in ENTITY_CATEGORIES:
    ENTITY_TYPE_LABELS[entity_type] = [f"B-{entity_type}", f"I-{entity_type}"]


# ---------------------------------------------------------------------------
# LabelMapping class for backward compatibility
# ---------------------------------------------------------------------------
class LabelMapping:
    """Central label mapping for BIO tagging scheme."""

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
# Helper: given a BIO label, return the entity type if it's a B or I label,
# otherwise return None.
# ---------------------------------------------------------------------------
def parse_bio_label(label: str) -> Tuple[Optional[str], Optional[str]]:
    """Return (entity_type, role) from a BIO label, e.g. 'B-MODEL' -> ('MODEL', 'B')."""
    if label == "O":
        return (None, None)
    # Strip the B- or I- prefix
    parts = label.split("-", 1)
    if len(parts) != 2:
        return (None, None)
    role, entity_type = parts
    if entity_type not in ENTITY_CATEGORIES:
        return (None, None)
    return (entity_type, role)