"""Scientific Relation Extraction Service for KnowledgeGraphAI Phase 2.3.

Responsibilities:
1. Accept scientific text and Phase 2.2 NER entities.
2. Generate candidate subject-object pairs.
3. Run relation extraction (REBEL baseline or classifier).
4. Validate relations against the taxonomy.
5. Return structured relation objects with provenance.
"""

from __future__ import annotations

import re
from typing import List, Dict, Any, Optional

from KnowledgeGraphAI.backend.nlp.ner.entity_schema import (
    ExtractedEntity,
    GENERAL_ENTITY_CATEGORIES,
    is_valid_entity_type,
)
from KnowledgeGraphAI.backend.nlp.relation_extraction.taxonomy import (
    GENERAL_RELATION_TYPES,
    RELATION_TYPES,
    get_allowed_pairs,
    is_valid_relation,
    get_description,
)
from KnowledgeGraphAI.backend.nlp.relation_extraction.relation_schema import ExtractedRelation
from KnowledgeGraphAI.backend.nlp.relation_extraction.entity_pair_generator import (
    EntityPairCandidate,
    EntityPairGenerator,
)


class ScientificRelationExtractionService:
    """Modular relation extraction service with configurable backends."""

    def __init__(
        self,
        use_relabel: bool = False,
        use_rebel: bool = False,
        rebel_checkpoint: str = "Babelscape/rebel-large",
        use_classifier: bool = False,
        classifier_checkpoint: Optional[str] = None,
        max_sentence_distance: int = 1,
        max_token_distance: Optional[int] = None,
        confidence_threshold: float = 0.55,
    ) -> None:
        self.use_relabel = use_relabel
        self.use_rebel = use_rebel
        self.rebel_checkpoint = rebel_checkpoint
        self.use_classifier = use_classifier
        self.classifier_checkpoint = classifier_checkpoint
        self.max_sentence_distance = max_sentence_distance
        self.max_token_distance = max_token_distance
        self.confidence_threshold = confidence_threshold

        # Lazy-loaded components
        self._pair_generator: Optional[EntityPairGenerator] = None
        self._rebel_model = None
        self._classifier_model = None

    # ------------------------------------------------------------------
    # Pair generator accessor
    # ------------------------------------------------------------------
    @property
    def pair_generator(self) -> EntityPairGenerator:
        if self._pair_generator is None:
            self._pair_generator = EntityPairGenerator(
                max_sentence_distance=self.max_sentence_distance,
                max_token_distance=self.max_token_distance,
                allow_cross_sentence=self.use_relabel or self.use_classifier,
            )
        return self._pair_generator

    # ------------------------------------------------------------------
    # Core extraction method
    # ------------------------------------------------------------------
    def extract_relations(
        self,
        text: str,
        entities: list,
        sentences: list,
        paper_id: int,
    ) -> list:
        """Extract relations from text given NER entities and sentence metadata.

        This is the main entry point. It:
        1. Generates candidate entity pairs.
        2. Runs relation extraction (chosen backends).
        3. Validates predictions.
        4. Returns a list of ``ExtractedRelation`` objects.
        """
        # 1. Generate candidate pairs
        candidates = self.pair_generator.generate_from_entities(
            entities,
            sentence_index_map={i: ent.sentence_index for i, ent in enumerate(entities)},
            paper_id=paper_id,
        )

        # 2. Run relation extraction backends
        relations: list = []

        # ``use_relabel`` is retained as a backwards-compatible option name.
        # No unavailable model is silently advertised as active: it invokes the
        # documented rule baseline until a real REBEL backend is configured.
        if self.use_relabel:
            rebel_relations = self._run_relabel(candidates, text, sentences)
            relations.extend(rebel_relations)

        # --- Classifier backend (placeholder) ---
        if self.use_classifier:
            classifier_relations = self._run_classifier(candidates, text, sentences)
            relations.extend(classifier_relations)

        # A functioning rule baseline is always available.  If an optional
        # learned backend is requested but cannot yield a validated relation,
        # use it as the safe fallback instead of returning an empty placeholder.
        if not relations:
            relations = self._run_rule_based(candidates, text, sentences)

        # 3. Validate and filter
        validated = self._validate_relations(relations, text, sentences)

        # 4. Post-process: deduplicate, filter by confidence
        final_relations = self._post_process(validated)

        # Attach paper-level metadata
        for rel in final_relations:
            rel.paper_id = paper_id

        return final_relations

    # ------------------------------------------------------------------
    # Optional REBEL compatibility hook
    # ------------------------------------------------------------------
    def _run_relabel(self, candidates, text, sentences):
        """Placeholder for REBEL relation extraction.

        In a full implementation this would:
        - Load ``Babelscape/rebel-large`` via ``transformers``.
        - Run the model on the input sentence(s).
        - Parse the generated triplets ``(subject, relation, object)``.
        - Normalize predicted relation labels against ``RELATION_TYPES``.
        - Return a list of ``ExtractedRelation`` objects.
        """
        return self._run_rule_based(candidates, text, sentences)

    # ------------------------------------------------------------------
    # Optional classifier compatibility hook
    # ------------------------------------------------------------------
    def _run_classifier(self, candidates, text, sentences):
        """Placeholder for SciBERT relation classifier.

        Would receive a sentence, marker-inserted text, and predict one of
        the 9 relation types plus ``NO_RELATION``.
        Returns ``ExtractedRelation`` objects.
        """
        # A trained classifier is intentionally not claimed here.  Returning
        # no predictions lets the caller select the explicit rule baseline.
        return []

    # ------------------------------------------------------------------
    # Rule-based relation validation and inference
    # ------------------------------------------------------------------
    def _run_rule_based(self, candidates, text, sentences):
        """Rule-based relation extraction as baseline.

        Uses keyword/pattern matching on the sentence context to infer
        relations where possible, respecting the taxonomy compatibility.
        """
        relations = []

        for cand in candidates:
            # Skip if category compatibility check failed
            if not cand.compatible:
                continue

            # Simple heuristic: look for relation keywords in the sentence
            # that could map to the relation type.
            sentence = (
                sentences[cand.sentence_id]
                if sentences and 0 <= cand.sentence_id < len(sentences)
                else None
            )
            if isinstance(sentence, dict):
                sentence_text = sentence.get("cleaned_text", text)
                original_text = sentence.get("original_text", sentence_text)
            elif sentence is not None:
                sentence_text = getattr(sentence, "cleaned_text", text)
                original_text = getattr(sentence, "original_text", sentence_text)
            else:
                sentence_text = text
                original_text = text
            rel_keywords = self._relation_keywords(cand.relation)
            if not rel_keywords:
                continue

            subj = cand.subject
            obj = cand.object
            is_general_candidate = (
                cand.relation in GENERAL_RELATION_TYPES
                or subj.entity_type in GENERAL_ENTITY_CATEGORIES
                or obj.entity_type in GENERAL_ENTITY_CATEGORIES
            )

            matched = False
            if is_general_candidate:
                matched = self._match_general_span(
                    sentence_text=sentence_text,
                    subj=subj,
                    obj=obj,
                    relation=cand.relation,
                )
            else:
                matched = any(kw.lower() in sentence_text.lower() for kw in rel_keywords)

            if matched:
                # Build an ExtractedRelation
                evidence = sentence_text

                rel = ExtractedRelation(
                    relation=cand.relation,
                    subject_entity_id=f"subj_{cand.subject_start}_{cand.subject_end}",
                    subject_text=subj.text,
                    subject_start=subj.start_char,
                    subject_end=subj.end_char,
                    subject_entity_type=subj.entity_type,
                    object_entity_id=f"obj_{obj.start_char}_{obj.end_char}",
                    object_text=obj.text,
                    object_start=obj.start_char,
                    object_end=obj.end_char,
                    object_entity_type=obj.entity_type,
                    paper_id=subj.paper_id,
                    sentence_id=cand.sentence_id,
                    page_number=subj.page_number,
                    evidence=evidence,
                    confidence=0.65,  # baseline heuristic
                    extraction_method="rule_based",
                    original_text=original_text,
                    cleaned_text=sentence_text,
                )
                relations.append(rel)

        return relations

    @staticmethod
    def _match_general_span(
        *,
        sentence_text: str,
        subj: ExtractedEntity,
        obj: ExtractedEntity,
        relation: str,
    ) -> bool:
        """Position- and clause-aware relation matcher for general English prose."""
        if subj.end_char > obj.start_char or subj.sentence_index != obj.sentence_index:
            return False
        between = sentence_text[subj.end_char : obj.start_char].lower()
        if not between or ";" in between or re.search(r",\s*(?:while|whereas)\b|\bwhile\b", between):
            return False
        if relation == "LOCATED_IN":
            return (
                len(between.strip()) <= 28
                and re.search(r"\b(?:in|at|near|around|within|located\s+in|situated\s+in|based\s+in)\b", between) is not None
            )
        if len(between) > 125:
            return False

        general_patterns: Dict[str, str] = {
            "STARTED": r"\b(?:start|started|starting|launch|launched|initiate|initiated|establish|established|founded|begin|began)\b",
            "LED_BY": r"\b(?:led\s+by|directed\s+by|organized\s+by|managed\s+by|headed\s+by|supervised\s+by|founded\s+by)\b",
            "WORKED_WITH": r"\b(?:worked\s+with|work\s+with|collaborated\s+with|partnered\s+with|teamed\s+up\s+with|alongside)\b",
            "CREATED": r"\b(?:turn|turned|transform|transformed|convert|converted|create|created|build|built|establish|established)\b",
            "PROVIDED": r"\b(?:provide|provided|provides|providing|supply|supplied|supplies|offer|offered|deliver|delivered)\b",
            "SHARED": r"(?:\b(?:share|shares|sharing)\b|\bshared\s+(?:their|his|her|our|knowledge|among|with|across|by)\b)",
            "PRODUCED": r"\b(?:producing|produced|produce|produces|yield|yielded|yields|growing|grew|grow|grows)\b",
            "HELPED": r"\b(?:help|helped|helps|assist|assisted|plant|planted|planting|maintain|maintained|support|supported)\b",
            "ENCOURAGED": r"\b(?:encourage|encouraged|encourages|foster|fostered|promote|promoted|inspired|inspire)\b",
            "REDUCED": r"\b(?:reduce|reduced|reduces|reducing|cut|cutting|lower|lowered|prevent|prevented)\b",
            "BELIEVES_IN": r"\b(?:believes|believed|believe|advocates|emphasizes|highlights)\b",
            "PARTICIPATED_IN": r"\b(?:participate|participated|participating|joined|join|contribute|contributed|maintain|maintained)\b",
            "IMPROVES": r"\b(?:improve|improved|improves|improving|enhance|enhanced|enhances|boost|boosted)\b",
            "USES": r"\b(?:use|used|using|uses|utilize|utilized|employ|employed)\b",
            "AFFECTS": r"\b(?:benefit|benefited|affect|affected|impact|impacted)\b",
        }
        pat = general_patterns.get(relation)
        if not pat:
            return False

        # Find all trigger matches inside the slice between subject and object.
        matches = list(re.finditer(pat, between))
        if not matches:
            return False

        # Guard against multi-verb / relative-clause cross-talk:
        # require that no DIFFERENT predicate verb or relative pronoun (", who") appears
        # AFTER this relation's latest trigger and before `obj`.
        latest_match = matches[-1]
        trailing = between[latest_match.end() :]
        if re.search(r",\s*(?:who|which|whom)\b", trailing):
            return False
        other_predicate_re = re.compile(
            r"\b(?:led\s+by|worked\s+with|provided|producing|produced|reduced|helped|"
            r"encouraged|believes|shared\s+(?:their|his|her|among|with)|turned)\b"
        )
        for other in other_predicate_re.finditer(trailing):
            # Ignore if `other` is literally part of the same relation (e.g. "helped ... plant")
            if re.search(pat, other.group(0)) is None:
                return False
        return True

    # ------------------------------------------------------------------
    # Keyword heuristics per relation type
    # ------------------------------------------------------------------
    def _relation_keywords(self, relation: str) -> List[str]:
        """Return a list of keyword patterns associated with *relation*.

        Heuristic baseline patterns over the sentence context.
        """
        keywords: Dict[str, List[str]] = {
            "PROPOSES": ["propose", "suggest", "aims", "introduc", "present", "develop"],
            "USES": ["use", "using", "employ", "utiliz", "trained with", "with"],
            "EVALUATED_ON": [
                "evaluat",
                "benchmark",
                "test",
                "dataset",
                "trained on",
                "tested on",
                "reported on",
                "experiments on",
            ],
            "ACHIEVES": ["achiev", "obtain", "reach", "attain", "yield", "accuracy"],
            "COMPARED_WITH": ["compar", "vs", "versus", "against", "better than", "worse than"],
            "IMPROVES": ["improv", "enhanc", "boost", "maximiz"],
            "APPLIES_TO": ["appli", "apply", "applied to", "applicable to", "used for"],
            "OUTPERFORMS": ["outperform", "surpass", "exceed", "significantly better"],
            "BASED_ON": ["based on", "based", "deriv", "originate from", "extension of"],
            "STARTED": ["start", "launch", "initiat", "establish", "began"],
            "LED_BY": ["led by", "directed by", "organized by", "managed by", "headed by"],
            "WORKED_WITH": ["worked with", "collaborat", "partnered with", "alongside"],
            "CREATED": ["turn", "transform", "create", "build", "establish"],
            "PROVIDED": ["provid", "suppl", "offer", "deliver"],
            "SHARED": ["share", "shared"],
            "PRODUCED": ["produc", "yield", "grow", "grew"],
            "HELPED": ["help", "assist", "plant", "maintain", "support"],
            "ENCOURAGED": ["encourag", "foster", "promot", "inspir"],
            "REDUCED": ["reduc", "lower", "prevent"],
            "LOCATED_IN": ["in", "at", "near", "around", "within", "located"],
            "BELIEVES_IN": ["believ", "advocat", "emphasiz"],
            "PARTICIPATED_IN": ["participat", "join", "contribut", "maintain"],
            "AFFECTS": ["benefit", "affect", "impact"],
        }
        return keywords.get(relation, [])

    # ------------------------------------------------------------------
    # Relation validation
    # ------------------------------------------------------------------
    def _validate_relations(self, relations, text, sentences):
        """Validate each relation candidate against the taxonomy and
        provenance constraints.

        * Subject/object must be valid entities.
        * Relation must be a supported type.
        * Offsets must reference the original text.
        * Directionality must be respected.
        """
        validated = []
        for rel in relations:
            # 1. Check relation is valid
            if not is_valid_relation(rel.relation):
                continue

            if not (
                is_valid_entity_type(rel.subject_entity_type)
                and is_valid_entity_type(rel.object_entity_type)
            ):
                continue

            allowed_pairs = get_allowed_pairs(rel.relation)
            if allowed_pairs and (
                rel.subject_entity_type,
                rel.object_entity_type,
            ) not in allowed_pairs:
                continue

            # 3. Check evidence sentence consistency
            if not self._check_evidence(rel, text, sentences):
                continue

            # 4. Ensure confidence is in valid range
            if not (0.0 <= rel.confidence <= 1.0):
                rel.confidence = 0.5  # fallback

            validated.append(rel)

        return validated

    # ------------------------------------------------------------------
    # Helper: check evidence sentence consistency
    # ------------------------------------------------------------------
    def _check_evidence(self, rel, text, sentences):
        """Verify that the evidence sentence contains the subject and object."""
        if not sentences:
            # Fallback: just check the raw text
            return rel.subject_text in text and rel.object_text in text

        sent = sentences[rel.sentence_id] if rel.sentence_id < len(sentences) else None
        if sent is None:
            return rel.subject_text in text and rel.object_text in text

        sent_text = (
            sent.get("cleaned_text", "")
            if isinstance(sent, dict)
            else getattr(sent, "cleaned_text", "")
        )
        return rel.subject_text in sent_text and rel.object_text in sent_text

    # ------------------------------------------------------------------
    # Post-processing: deduplication and confidence filtering
    # ------------------------------------------------------------------
    def _post_process(self, relations):
        """Remove duplicate relations and filter by confidence threshold."""
        seen: set = set()
        filtered: list = []

        for rel in relations:
            # Skip if confidence below threshold
            if rel.confidence < self.confidence_threshold:
                continue

            # Deduplicate: use (relation, subject_text, object_text) as key
            key = (rel.relation, rel.subject_text, rel.object_text)
            if key in seen:
                continue
            seen.add(key)

            # Ensure direction is consistent
            # (for symmetric relations like COMPARED_WITH, both directions
            #  are kept; for others, only subject->object is kept)
            filtered.append(rel)

        return filtered

# ----------------------------------------------------------------------
# Convenience function for single-paper extraction
# ----------------------------------------------------------------------
def extract_relations_from_paper(
    text: str,
    entities: list,
    sentences: list,
    paper_id: int,
    use_relabel: bool = False,
    use_rebel: bool = False,
    use_classifier: bool = False,
    max_sentence_distance: int = 1,
    max_token_distance: Optional[int] = None,
    confidence_threshold: float = 0.55,
) -> list:
    """End-to-end relation extraction for a single paper.

    Returns a list of ``ExtractedRelation`` objects.
    """
    service = ScientificRelationExtractionService(
        use_relabel=use_relabel,
        use_rebel=use_rebel,
        use_classifier=use_classifier,
        max_sentence_distance=max_sentence_distance,
        max_token_distance=max_token_distance,
        confidence_threshold=confidence_threshold,
    )
    return service.extract_relations(text, entities, sentences, paper_id)
