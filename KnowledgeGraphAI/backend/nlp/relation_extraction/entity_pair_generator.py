"""Entity pair generator for KnowledgeGraphAI Phase 2.3.

Generates subject-object candidate pairs from Phase 2.2 NER entities,
respecting category compatibility, sentence proximity, and token distance
constraints.
"""

from __future__ import annotations

from typing import List, Dict, Any, Optional, FrozenSet, Set, Tuple

from KnowledgeGraphAI.backend.nlp.ner.entity_schema import ExtractedEntity, EntityTaxonomy
from KnowledgeGraphAI.backend.nlp.relation_extraction.taxonomy import (
    RELATION_TYPES,
    is_valid_relation,
    get_allowed_pairs,
    get_direction,
)


class EntityPairCandidate:
    """A subject-object candidate pair with compatibility metadata."""

    def __init__(
        self,
        subject: ExtractedEntity,
        object_: ExtractedEntity,
        relation: str,
        sentence_id: int,
        paper_id: int,
    ) -> None:
        self.subject = subject
        self.object = object_
        self.relation = relation
        self.sentence_id = sentence_id
        self.paper_id = paper_id

        # Derived metadata
        self.subject_start = subject.start_char
        self.subject_end = subject.end_char
        self.object_start = object_.start_char
        self.object_end = object_.end_char
        self.subject_text = subject.text
        self.object_text = object_.text
        self.subject_category = subject.entity_type
        self.object_category = object_.entity_type
        self.direction = get_direction(relation)
        self.compatible = self._check_category_compatibility()

    def _check_category_compatibility(self) -> bool:
        """Verify that the subject-object pair falls into allowed categories."""
        allowed = get_allowed_pairs(self.relation)
        if not allowed:
            # Empty set means any categories are permitted
            return True
        return (self.subject_category, self.object_category) in allowed

    def __repr__(self) -> str:
        return (
            f"EntityPairCandidate(subject={self.subject.text!r} "
            f"({self.subject_category}), object={self.object_text!r} "
            f"({self.object_category}), relation={self.relation})"
        )


class EntityPairGenerator:
    """Generates subject-object candidate pairs from NER entities.

    Rules:
    1. Prefer entities occurring in the same sentence.
    2. Support configurable cross-sentence candidate generation.
    3. Apply a configurable maximum token distance.
    4. Respect entity category compatibility via taxonomy.
    5. Avoid pairing an entity with itself.
    6. Avoid duplicate candidate pairs.
    7. Preserve original entity offsets.
    8. Maintain subject-object direction.
    """

    def __init__(
        self,
        max_sentence_distance: int = 1,  # 0 = same sentence only, 1 = adjacent sentences, etc.
        max_token_distance: Optional[int] = None,
        allow_cross_sentence: bool = True,
    ) -> None:
        self.max_sentence_distance = max_sentence_distance
        self.max_token_distance = max_token_distance
        self.allow_cross_sentence = allow_cross_sentence

    def generate_candidates(
        self,
        entities: List[ExtractedEntity],
        sentences: List[dict],
        paper_id: int,
    ) -> List[EntityPairCandidate]:
        """Generate subject-object candidate pairs from NER entities.

        Args:
            entities: List of ``ExtractedEntity`` objects from Phase 2.2 NER.
            sentences: List of sentence dicts from preprocessing (each with
                ``sentence_index``, ``page_number``, etc.).
            paper_id: Identifier of the paper.

        Returns:
            A list of ``EntityPairCandidate`` objects sorted by sentence
            proximity and then by token offset.
        """
        # Map sentence_index -> list of entities in that sentence
        entities_by_sentence: Dict[int, List[ExtractedEntity]] = {}
        for ent in entities:
            si = ent.sentence_index
            entities_by_sentence.setdefault(si, []).append(ent)

        # Also map sentence_index to total token count (approximate)
        # We'll use entity start_char as a proxy for token position.
        candidates: List[EntityPairCandidate] = []

        # 1. Same-sentence candidates
        same_sentence_candidates = self._generate_same_sentence_candidates(
            entities_by_sentence, paper_id
        )
        candidates.extend(same_sentence_candidates)

        # 2. Cross-sentence candidates (if allowed)
        if self.allow_cross_sentence:
            cross_candidates = self._generate_cross_sentence_candidates(
                entities_by_sentence, sentences, paper_id
            )
            candidates.extend(cross_candidates)

        # Preserve one candidate per subject-object-relation combination so
        # evidence, rather than iteration order, determines the relation.
        seen: Set[tuple] = set()
        unique_candidates: List[EntityPairCandidate] = []
        for cand in candidates:
            key = (
                cand.subject_start,
                cand.subject_end,
                cand.object_start,
                cand.object_end,
                cand.relation,
            )
            if key not in seen:
                seen.add(key)
                unique_candidates.append(cand)

        # Sort by sentence proximity, then by token offset
        unique_candidates.sort(key=lambda c: (c.sentence_id, c.subject_start))

        return unique_candidates

    # ------------------------------------------------------------------
    # Same‑sentence candidate generation
    # ------------------------------------------------------------------
    def _generate_same_sentence_candidates(
        self,
        entities_by_sentence: Dict[int, List[ExtractedEntity]],
        paper_id: int,
    ) -> List[EntityPairCandidate]:
        candidates: List[EntityPairCandidate] = []

        for sent_idx, ents in entities_by_sentence.items():
            # Generate all ordered pairs (subject, object) where subject ≠ object
            for i, subj in enumerate(ents):
                for obj in ents:
                    if obj is subj:
                        # Skip pairing an entity with itself
                        continue

                    # Try every supported relation type
                    for rel in RELATION_TYPES:
                        cand = EntityPairCandidate(
                            subject=subj,
                            object_=obj,
                            relation=rel,
                            sentence_id=sent_idx,
                            paper_id=paper_id,
                        )
                        if cand.compatible:
                            candidates.append(cand)

            # Also allow cross‑sentence when distance is within bounds
            # (handled by the cross‑sentence method below)

        return candidates

    # ------------------------------------------------------------------
    # Cross‑sentence candidate generation
    # ------------------------------------------------------------------
    def _generate_cross_sentence_candidates(
        self,
        entities_by_sentence: Dict[int, List[ExtractedEntity]],
        sentences: List[dict],
        paper_id: int,
    ) -> List[EntityPairCandidate]:
        candidates: List[EntityPairCandidate] = []

        sent_indices = sorted(entities_by_sentence.keys())

        for i, si in enumerate(sent_indices):
            for si2 in sent_indices[i + 1 : min(i + self.max_sentence_distance + 1, len(sent_indices))]:
                # Get the two sentences' worth of token-approximate positions
                # We'll use entity start_char as a proxy; compute approximate distance
                for subj in entities_by_sentence[si]:
                    for obj in entities_by_sentence[si2]:
                        # Compute approximate token distance as absolute
                        # difference of start_char values (rough proxy)
                        token_dist = abs(subj.start_char - obj.start_char)

                        if self.max_token_distance is not None and token_dist > self.max_token_distance:
                            continue

                        # Try every supported relation type
                        for rel in RELATION_TYPES:
                            cand = EntityPairCandidate(
                                subject=subj,
                                object_=obj,
                                relation=rel,
                                sentence_id=si,
                                paper_id=paper_id,
                            )
                            if cand.compatible:
                                candidates.append(cand)

        return candidates

    # ------------------------------------------------------------------
    # Public helper: given flat entity list + sentence metadata, produce
    # candidates respecting the configured rules.
    # ------------------------------------------------------------------
    def generate_from_entities(
        self,
        entities: List[ExtractedEntity],
        sentence_index_map: Dict[int, int],  # maps global entity index -> sentence_index
        paper_id: int,
    ) -> List[EntityPairCandidate]:
        """Entry point that normalises the input and calls the main generator.

        *sentence_index_map* maps the positional index of an entity in the
        original entity list to its sentence_index (as produced by the
        preprocessing pipeline).
        """
        # Build the sentences dict expected by the generator:
        # key = sentence_index, value = list of entities in that sentence
        entities_by_sentence: Dict[int, List[ExtractedEntity]] = {}
        for idx, ent in enumerate(entities):
            si = sentence_index_map.get(idx, 0)  # default to sentence 0
            entities_by_sentence.setdefault(si, []).append(ent)

        # Build a minimal sentences list (only needed for cross-sentence logic)
        # We approximate sentence count from the number of distinct sentence indices.
        sentences = [
            {"sentence_index": si, "page_number": 0}
            for si in range(max(entities_by_sentence.keys()) + 1 if entities_by_sentence else 1)
        ]

        return self.generate_candidates(entities, sentences, paper_id)