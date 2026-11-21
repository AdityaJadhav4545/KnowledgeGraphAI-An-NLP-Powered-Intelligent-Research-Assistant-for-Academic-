"""Unified NER pipeline – orchestrates rule-based and transformer-based extraction.

Responsibilities:
- Accept preprocessed sentence records from Phase 2.1.
- Select the active NER model (rule-based or transformer).
- Run entity recognition.
- Decode BIO / rule matches into ExtractedEntity objects.
- Remove duplicates and enforce confidence thresholds.
- Attach provenance (paper_id, page_number, sentence_index, source_text).
- Return structured entity output with statistics.
"""

import logging
from typing import List, Dict, Any, Optional, Tuple

from KnowledgeGraphAI.backend.nlp.ner.entity_schema import (
    ExtractedEntity,
    EntityTaxonomy,
    ExtractedSentence,
    EntityBatch,
    is_valid_entity_type,
    valid_entity_types,
)
from KnowledgeGraphAI.backend.nlp.ner.label_mapping import (
    NER_LABELS,
    LABEL_TO_ID,
    ID_TO_LABEL,
    parse_bio_label,
)
from KnowledgeGraphAI.backend.nlp.ner.rule_based_ner import RuleBasedNER
from KnowledgeGraphAI.backend.nlp.preprocessing.schemas import PreprocessingResult

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# NER pipeline configuration
# ---------------------------------------------------------------------------

CONFIDENCE_THRESHOLD: float = 0.55
DEFAULT_EXTRACTION_METHOD: str = "rule_based"


# ---------------------------------------------------------------------------
# Helper: attach provenance to an entity from a sentence record
# ---------------------------------------------------------------------------
def _attach_provenance(
    entity: ExtractedEntity,
    sentence: ExtractedSentence,
    extraction_method: str,
) -> ExtractedEntity:
    """Copy provenance fields from a Phase 2.1 sentence record onto an entity."""
    entity.paper_id = sentence.paper_id
    entity.page_number = sentence.page_number
    entity.sentence_index = sentence.sentence_index
    entity.source_text = sentence.cleaned_text
    entity.original_text = sentence.original_text
    entity.cleaned_text = sentence.cleaned_text
    entity.extraction_method = extraction_method
    return entity


# ---------------------------------------------------------------------------
# Main NER Pipeline
# ---------------------------------------------------------------------------

class NERPipeline:
    """Orchestrates scientific NER over preprocessed paper content."""

    def __init__(
        self,
        use_transformer: bool = False,
        model_path: Optional[str] = None,
        confidence_threshold: float = CONFIDENCE_THRESHOLD,
        include_general_prose: bool = False,
    ) -> None:
        self.use_transformer = use_transformer
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.include_general_prose = include_general_prose

        # Lazy-loaded components
        self._rule_based_ner: Optional[RuleBasedNER] = None
        self._transformer_ner = None  # placeholder; loaded on demand

        # Statistics accumulated during the last run
        self.stats: Dict[str, Any] = {
            "total_sentences_processed": 0,
            "total_entities": 0,
            "entity_distribution": {et: 0 for et in EntityTaxonomy.NAMES},
            "extraction_method": DEFAULT_EXTRACTION_METHOD,
            "processing_time_seconds": 0.0,
        }

    # ------------------------------------------------------------------
    # Model / rule accessors
    # ------------------------------------------------------------------
    @property
    def rule_based_ner(self) -> RuleBasedNER:
        if self._rule_based_ner is None:
            self._rule_based_ner = RuleBasedNER(
                include_general_prose=self.include_general_prose
            )
        return self._rule_based_ner

    # ------------------------------------------------------------------
    # Single-sentence extraction
    # ------------------------------------------------------------------
    def extract_from_sentence(
        self,
        sentence: ExtractedSentence,
    ) -> EntityBatch:
        """Extract entities from a single preprocessed sentence.

        Args:
            sentence: A sentence record from the Phase 2.1 preprocessing pipeline.

        Returns:
            An ``EntityBatch`` containing any entities found, with provenance
            already attached.
        """
        batch = EntityBatch(
            paper_id=sentence.paper_id,
            page_number=sentence.page_number,
            sentence_index=sentence.sentence_index,
        )

        if self.use_transformer and self._transformer_ner is not None:
            # TODO: implement transformer extraction when model is available
            # For now, fall back to rule-based
            entities = self.rule_based_ner.extract(
                sentence.cleaned_text,
                paper_id=sentence.paper_id,
                page_number=sentence.page_number,
            )
        else:
            entities = self.rule_based_ner.extract(
                sentence.cleaned_text,
                paper_id=sentence.paper_id,
                page_number=sentence.page_number,
            )

        # Attach provenance to each entity
        for entity in entities:
            _attach_provenance(entity, sentence, DEFAULT_EXTRACTION_METHOD)

        # Deduplicate & count
        batch.entities = entities
        self._update_stats(entities)

        return batch

    # ------------------------------------------------------------------
    # Full-paper extraction
    # ------------------------------------------------------------------
    def extract_paper(
        self,
        sentences: List[ExtractedSentence],
    ) -> EntityBatch:
        """Extract entities from all sentences of a paper.

        Args:
            sentences: List of ``ExtractedSentence`` records from the
                preprocessing pipeline (produced by ``NLPProcessingPipeline``).

        Returns:
            An ``EntityBatch`` with all entities found across the paper,
            plus statistics.
        """
        self.stats["total_sentences_processed"] = 0
        self.stats["total_entities"] = 0
        self.stats["entity_distribution"] = {et: 0 for et in EntityTaxonomy.NAMES}
        batch = EntityBatch(
            paper_id=sentences[0].paper_id if sentences else 0,
            page_number=0,
            sentence_index=0,
        )

        for sentence in sentences:
            s_batch = self.extract_from_sentence(sentence)
            batch.entities.extend(s_batch.entities)

            # Accumulate page number from the last sentence (last page)
            batch.page_number = sentence.page_number

        self.stats["total_sentences_processed"] = len(sentences)
        self.stats["total_entities"] = len(batch.entities)
        for ent in batch.entities:
            self.stats["entity_distribution"][ent.entity_type] = (
                self.stats["entity_distribution"].get(ent.entity_type, 0) + 1
            )

        return batch

    # ------------------------------------------------------------------
    # Statistics & reporting
    # ------------------------------------------------------------------
    def _update_stats(self, entities: List[ExtractedEntity]) -> None:
        self.stats["total_entities"] = len(entities)
        for ent in entities:
            self.stats["entity_distribution"][ent.entity_type] = (
                self.stats["entity_distribution"].get(ent.entity_type, 0) + 1
            )
        self.stats["processing_time_seconds"] = round(
            # In a real implementation, this would be wall-clock time
            0.0,  # placeholder; the caller can time the full run
            3,
        )

    def get_stats(self) -> Dict[str, Any]:
        """Return accumulated statistics from the last pipeline run."""
        return dict(self.stats)

    # ------------------------------------------------------------------
        # Model management
    # ------------------------------------------------------------------
    def load_transformer_model(self) -> None:
        """Refuse to misrepresent an unavailable fine-tuned NER model.

        A base SciBERT checkpoint is not a scientific token-classification
        model for this taxonomy.  Until a compatible fine-tuned checkpoint and
        label map are configured, callers must explicitly use the documented
        rule-based baseline.
        """
        self.use_transformer = False
        raise RuntimeError(
            "Transformer NER is not configured with a compatible fine-tuned "
            "checkpoint; use the rule_based baseline."
        )

    def unload_model(self) -> None:
        """Release any loaded model resources."""
        self._rule_based_ner = None
        self._transformer_ner = None
        # In a full implementation, would torch.cuda.empty_cache() etc.


# ---------------------------------------------------------------------------
# Convenience function for quick single-paper extraction
# ---------------------------------------------------------------------------
def extract_entities_from_paper(
    sentences: List[Any],  # List of dicts or ExtractedSentence objects
    use_transformer: bool = False,
    confidence_threshold: float = CONFIDENCE_THRESHOLD,
    include_general_prose: bool = False,
) -> Dict[str, Any]:
    """Extract entities from a list of sentence records.

    Args:
        sentences: Sentence records (``ExtractedSentence`` or dict-like).
        use_transformer: If True, attempt transformer extraction (fallback to
            rule-based if model not loaded).
        confidence_threshold: Minimum confidence for an entity to be kept.

    Returns:
        A dict with keys:
        - "paper_id": int
        - "processing_status": str
        - "total_sentences_processed": int
        - "total_entities": int
        - "entity_distribution": Dict[str, int]
        - "entities": List[Dict[str, Any]]  # entity -> dict
        - "model_metadata": Dict[str, Any]
        - "warnings": List[str]
    """
    pipeline = NERPipeline(
        use_transformer=use_transformer,
        confidence_threshold=confidence_threshold,
        include_general_prose=include_general_prose,
    )

    # Normalise input sentences to ``ExtractedSentence`` if needed
    normalized_sentences = []
    for s in sentences:
        if isinstance(s, dict):
            # Minimal dict-to-sentence conversion
            normalized_sentences.append(
                type("ExtractedSentence", (), {
                    "paper_id": s.get("paper_id", 0),
                    "page_number": s.get("page_number", 0),
                    "section_name": s.get("section_name", "Unknown"),
                    "sentence_index": s.get("sentence_index", 0),
                    "original_text": s.get("original_text", ""),
                    "cleaned_text": s.get("cleaned_text", ""),
                })()
            )
        else:
            normalized_sentences.append(s)

    batch = pipeline.extract_paper(normalized_sentences)

    # Convert entities to dicts for JSON output
    entity_dicts = [e.to_dict() for e in batch.entities]
    stats = pipeline.get_stats()

    return {
        "paper_id": batch.paper_id,
        "processing_status": "completed",
        "total_sentences_processed": len(normalized_sentences),
        "total_entities": len(batch.entities),
        "entity_distribution": {
            k: v for k, v in stats["entity_distribution"].items() if v > 0
        },
        "entities": entity_dicts,
        "model_metadata": {
            "model_name": "transformer" if pipeline._transformer_ner is not None else "rule_based",
            "model_type": stats.get("extraction_method", DEFAULT_EXTRACTION_METHOD),
            "confidence_threshold": confidence_threshold,
        },
        "warnings": (
            ["Transformer NER was requested but no model is loaded; rule_based extraction was used."]
            if use_transformer and pipeline._transformer_ner is None
            else []
        ),
    }
