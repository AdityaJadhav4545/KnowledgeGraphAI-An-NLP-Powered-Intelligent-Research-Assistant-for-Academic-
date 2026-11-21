"""Scientific Named Entity Recognition (NER) module for KnowledgeGraphAI."""
from KnowledgeGraphAI.backend.nlp.ner.label_mapping import (
    LabelMapping,
    NER_LABELS,
    LABEL_TO_ID,
    parse_bio_label,
)
from KnowledgeGraphAI.backend.nlp.ner.entity_schema import (
    ExtractedEntity,
    EntityTaxonomy,
)
from KnowledgeGraphAI.backend.nlp.ner.rule_based_ner import RuleBasedNER
from KnowledgeGraphAI.backend.nlp.ner.ner_pipeline import NERPipeline

__all__ = [
    "ExtractedEntity",
    "EntityTaxonomy",
    "LabelMapping",
    "NER_LABELS",
    "ID_TO_LABEL",
    "LABEL_TO_ID",
    "parse_bio_label",
    "RuleBasedNER",
    "NERPipeline",
]