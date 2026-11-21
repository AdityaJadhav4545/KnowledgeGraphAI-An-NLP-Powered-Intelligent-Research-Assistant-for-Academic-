"""Relation taxonomy for KnowledgeGraphAI Phase 2.3.

Defines the 9 supported relation types with metadata for validation,
compatibility checking, and directionality.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, FrozenSet, Optional, Set

# ---------------------------------------------------------------------------
# 9 Scientific relation types + general-purpose English prose relation types
# ---------------------------------------------------------------------------
SCIENTIFIC_RELATION_TYPES: FrozenSet[str] = frozenset({
    "PROPOSES",
    "USES",
    "EVALUATED_ON",
    "ACHIEVES",
    "COMPARED_WITH",
    "IMPROVES",
    "APPLIES_TO",
    "OUTPERFORMS",
    "BASED_ON",
})

GENERAL_RELATION_TYPES: FrozenSet[str] = frozenset({
    "STARTED",
    "LED_BY",
    "WORKED_WITH",
    "CREATED",
    "PROVIDED",
    "SHARED",
    "PRODUCED",
    "HELPED",
    "ENCOURAGED",
    "REDUCED",
    "LOCATED_IN",
    "BELIEVES_IN",
    "PARTICIPATED_IN",
    "AFFECTS",
})

RELATION_TYPES: FrozenSet[str] = SCIENTIFIC_RELATION_TYPES | GENERAL_RELATION_TYPES

# Human-readable descriptions
RELATION_DESCRIPTIONS: Dict[str, str] = {
    "PROPOSES": "The subject entity is proposed as a solution or approach for the object's problem/context.",
    "USES": "The subject entity is used or employed by the object in the research.",
    "EVALUATED_ON": "The object entity was used as an evaluation benchmark or dataset for the subject.",
    "ACHIEVES": "The subject entity achieves a performance metric or result relative to the object.",
    "COMPARED_WITH": "The subject entity is compared against the object entity in the research.",
    "IMPROVES": "The subject entity improves upon or enhances the object entity's performance.",
    "APPLIES_TO": "The subject entity's methodology or framework is applied to the object context.",
    "OUTPERFORMS": "The subject entity outperforms the object entity on a given metric.",
    "BASED_ON": "The subject entity's architecture or approach is based upon or derived from the object.",
    "STARTED": "The subject initiates, launches, or establishes the object project or activity.",
    "LED_BY": "The subject initiative or group is led, organized, or directed by the object person or body.",
    "WORKED_WITH": "The subject collaborates or works alongside the object.",
    "CREATED": "The subject transforms, creates, or establishes the object place, project, or outcome.",
    "PROVIDED": "The subject supplies or provides the object resource, equipment, or support.",
    "SHARED": "The subject shares the object resource, knowledge, or product with others.",
    "PRODUCED": "The subject yields, cultivates, or produces the object product or outcome.",
    "HELPED": "The subject assists, maintains, plants, or supports the object.",
    "ENCOURAGED": "The subject fosters or encourages the object behavior, value, or group.",
    "REDUCED": "The subject decreases or mitigates the object condition or issue.",
    "LOCATED_IN": "The subject is situated or operates within the object location.",
    "BELIEVES_IN": "The subject holds or advocates the object principle, value, or concept.",
    "PARTICIPATED_IN": "The subject takes part in or contributes to the object project or group.",
    "AFFECTS": "The subject influences or benefits the object community, group, or concept.",
}

# Allowed subject-object entity category pairs per relation type.
# Each relation maps to a set of (subject_category, object_category) tuples.
# If the set is empty, any categories are allowed for that relation.
RELATION_CATEGORY_COMPATIBILITY: Dict[str, FrozenSet[tuple]] = {
    "PROPOSES": frozenset({
        ("MODEL", "TASK"),
        ("METHODOLOGY", "RESEARCH_PROBLEM"),
        ("FRAMEWORK", "TASK"),
    }),
    "USES": frozenset({
        ("MODEL", "DATASET"),
        ("MODEL", "ALGORITHM"),
        ("FRAMEWORK", "DATASET"),
        ("FRAMEWORK", "ALGORITHM"),
        ("ALGORITHM", "DATASET"),
        ("PROJECT", "PRODUCT"),
        ("GROUP", "PRODUCT"),
        ("PERSON", "PRODUCT"),
        ("PROJECT", "LOCATION"),
    }),
    "EVALUATED_ON": frozenset({
        ("MODEL", "DATASET"),
        ("ALGORITHM", "DATASET"),
    }),
    "ACHIEVES": frozenset({
        ("MODEL", "METRIC"),
        ("ALGORITHM", "METRIC"),
    }),
    "COMPARED_WITH": frozenset({
        ("MODEL", "MODEL"),
        ("ALGORITHM", "ALGORITHM"),
        ("DATASET", "DATASET"),
    }),
    "IMPROVES": frozenset({
        ("MODEL", "METRIC"),
        ("ALGORITHM", "METRIC"),
        ("METHODOLOGY", "METRIC"),
        ("PROJECT", "CONCEPT"),
        ("GROUP", "CONCEPT"),
        ("ORGANIZATION", "CONCEPT"),
        ("PERSON", "CONCEPT"),
    }),
    "APPLIES_TO": frozenset({
        ("METHODOLOGY", "TASK"),
        ("METHODOLOGY", "DATASET"),
        ("FRAMEWORK", "TASK"),
        ("FRAMEWORK", "DATASET"),
    }),
    "OUTPERFORMS": frozenset({
        ("MODEL", "MODEL"),
        ("MODEL", "METRIC"),
        ("ALGORITHM", "ALGORITHM"),
        ("ALGORITHM", "METRIC"),
    }),
    "BASED_ON": frozenset({
        ("MODEL", "METHODOLOGY"),
        ("ALGORITHM", "METHODOLOGY"),
        ("FRAMEWORK", "METHODOLOGY"),
        ("PROJECT", "CONCEPT"),
    }),
    "STARTED": frozenset({
        ("GROUP", "PROJECT"),
        ("PERSON", "PROJECT"),
        ("ORGANIZATION", "PROJECT"),
        ("GROUP", "CONCEPT"),
    }),
    "LED_BY": frozenset({
        ("PROJECT", "PERSON"),
        ("GROUP", "PERSON"),
        ("ORGANIZATION", "PERSON"),
        ("PROJECT", "ORGANIZATION"),
        ("PROJECT", "GROUP"),
    }),
    "WORKED_WITH": frozenset({
        ("PERSON", "GROUP"),
        ("PERSON", "PERSON"),
        ("PERSON", "ORGANIZATION"),
        ("GROUP", "GROUP"),
        ("GROUP", "ORGANIZATION"),
        ("ORGANIZATION", "GROUP"),
    }),
    "CREATED": frozenset({
        ("PERSON", "LOCATION"),
        ("GROUP", "LOCATION"),
        ("PROJECT", "LOCATION"),
        ("ORGANIZATION", "LOCATION"),
        ("LOCATION", "LOCATION"),
        ("PERSON", "PROJECT"),
        ("GROUP", "PROJECT"),
        ("ORGANIZATION", "PROJECT"),
    }),
    "PROVIDED": frozenset({
        ("ORGANIZATION", "PRODUCT"),
        ("ORGANIZATION", "CONCEPT"),
        ("PERSON", "PRODUCT"),
        ("GROUP", "PRODUCT"),
        ("PROJECT", "PRODUCT"),
        ("PROJECT", "CONCEPT"),
    }),
    "SHARED": frozenset({
        ("GROUP", "PRODUCT"),
        ("GROUP", "CONCEPT"),
        ("PERSON", "PRODUCT"),
        ("PERSON", "CONCEPT"),
        ("PRODUCT", "GROUP"),
        ("PROJECT", "GROUP"),
        ("PROJECT", "PRODUCT"),
    }),
    "PRODUCED": frozenset({
        ("PROJECT", "PRODUCT"),
        ("LOCATION", "PRODUCT"),
        ("GROUP", "PRODUCT"),
        ("ORGANIZATION", "PRODUCT"),
        ("PROJECT", "CONCEPT"),
    }),
    "HELPED": frozenset({
        ("GROUP", "PRODUCT"),
        ("GROUP", "PROJECT"),
        ("GROUP", "CONCEPT"),
        ("PERSON", "GROUP"),
        ("PERSON", "PROJECT"),
        ("PROJECT", "GROUP"),
        ("PROJECT", "CONCEPT"),
        ("ORGANIZATION", "GROUP"),
    }),
    "ENCOURAGED": frozenset({
        ("PROJECT", "CONCEPT"),
        ("PROJECT", "GROUP"),
        ("PERSON", "CONCEPT"),
        ("ORGANIZATION", "CONCEPT"),
    }),
    "REDUCED": frozenset({
        ("PROJECT", "CONCEPT"),
        ("ORGANIZATION", "CONCEPT"),
        ("GROUP", "CONCEPT"),
        ("PERSON", "CONCEPT"),
    }),
    "LOCATED_IN": frozenset({
        ("GROUP", "LOCATION"),
        ("PROJECT", "LOCATION"),
        ("ORGANIZATION", "LOCATION"),
        ("PERSON", "LOCATION"),
        ("PRODUCT", "LOCATION"),
    }),
    "BELIEVES_IN": frozenset({
        ("PERSON", "CONCEPT"),
        ("GROUP", "CONCEPT"),
        ("ORGANIZATION", "CONCEPT"),
    }),
    "PARTICIPATED_IN": frozenset({
        ("GROUP", "PROJECT"),
        ("PERSON", "PROJECT"),
        ("ORGANIZATION", "PROJECT"),
        ("GROUP", "CONCEPT"),
    }),
    "AFFECTS": frozenset({
        ("PROJECT", "GROUP"),
        ("PROJECT", "CONCEPT"),
        ("CONCEPT", "PROJECT"),
        ("ORGANIZATION", "GROUP"),
    }),
}

# Directionality: subject -> object or symmetric
RELATION_DIRECTION: Dict[str, str] = {
    "PROPOSES": "subject->object",
    "USES": "subject->object",
    "EVALUATED_ON": "subject->object",
    "ACHIEVES": "subject->object",
    "COMPARED_WITH": "subject<->object",  # symmetric comparison
    "IMPROVES": "subject->object",
    "APPLIES_TO": "subject->object",
    "OUTPERFORMS": "subject->object",
    "BASED_ON": "subject->object",
    "WORKED_WITH": "subject<->object",
}

# ---------------------------------------------------------------------------
# Convenience helpers
# ---------------------------------------------------------------------------

def is_valid_relation(relation: str) -> bool:
    """Check if *relation* is an supported type."""
    return relation in RELATION_TYPES

def get_description(relation: str) -> str:
    """Return the human-readable description for *relation*."""
    return RELATION_DESCRIPTIONS.get(relation, "")

def get_allowed_pairs(relation: str) -> FrozenSet[tuple]:
    """Return the allowed (subject_category, object_category) tuples."""
    return RELATION_CATEGORY_COMPATIBILITY.get(relation, frozenset())

def get_direction(relation: str) -> str:
    """Return the directionality string for *relation*."""
    return RELATION_DIRECTION.get(relation, "subject->object")


# ---------------------------------------------------------------------------
# Quick sanity check
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Supported relations: %s" % ", ".join(sorted(RELATION_TYPES)))
    print("Allowed pairs for EVALUATED_ON: %s" % RELATION_CATEGORY_COMPATIBILITY["EVALUATED_ON"])
    print("Direction for OUTPERFORMS: %s" % RELATION_DIRECTION["OUTPERFORMS"])