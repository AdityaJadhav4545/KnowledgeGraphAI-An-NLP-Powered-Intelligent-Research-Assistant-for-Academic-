"""Regression tests for RuleBasedNER terminology coverage and relation extraction."""

from KnowledgeGraphAI.backend.nlp.ner.entity_schema import ExtractedSentence
from KnowledgeGraphAI.backend.nlp.ner.ner_pipeline import NERPipeline
from KnowledgeGraphAI.backend.nlp.relation_extraction.relation_extraction_service import (
    ScientificRelationExtractionService,
)
from KnowledgeGraphAI.backend.services.knowledge_graph.graph_schema import (
    get_node_label,
    validate_relationship,
)


def test_rule_based_ner_covers_word_representation_and_avoids_lowercase_false_positives():
    sentence = ExtractedSentence(
        paper_id=13,
        page_number=4,
        section_name="Model Architectures",
        paragraph_index=0,
        sentence_index=0,
        original_text=(
            "The Skip-gram and CBOW models are evaluated on the Google News dataset "
            "and compared with NNLM for Word Representation, while adam talked about a ray of light."
        ),
        cleaned_text=(
            "The Skip-gram and CBOW models are evaluated on the Google News dataset "
            "and compared with NNLM for Word Representation, while adam talked about a ray of light."
        ),
    )

    entities = NERPipeline(use_transformer=False).extract_from_sentence(sentence).entities
    found = {(entity.text, entity.entity_type) for entity in entities}

    assert ("Skip-gram", "MODEL") in found
    assert ("CBOW", "MODEL") in found
    assert ("NNLM", "MODEL") in found
    assert ("Google News", "DATASET") in found
    assert ("Word Representation", "TASK") in found
    # Lowercase common words must not trigger optimizer/framework false positives.
    assert ("adam", "OPTIMIZER") not in found
    assert ("ray", "FRAMEWORK") not in found


def test_rule_based_relation_extraction_produces_schema_valid_relations():
    sentence = ExtractedSentence(
        paper_id=13,
        page_number=8,
        section_name="Experiments",
        paragraph_index=0,
        sentence_index=0,
        original_text=(
            "CBOW and Skip-gram were evaluated on the Google News dataset, "
            "and Skip-gram outperforms NNLM on Accuracy."
        ),
        cleaned_text=(
            "CBOW and Skip-gram were evaluated on the Google News dataset, "
            "and Skip-gram outperforms NNLM on Accuracy."
        ),
    )

    entities = NERPipeline(use_transformer=False).extract_from_sentence(sentence).entities
    relations = ScientificRelationExtractionService(
        use_relabel=False,
        use_rebel=False,
        use_classifier=False,
    ).extract_relations(sentence.cleaned_text, entities, [sentence], paper_id=13)

    rel_triples = {
        (rel.subject_text, rel.relation, rel.object_text)
        for rel in relations
    }
    assert ("CBOW", "EVALUATED_ON", "Google News") in rel_triples
    assert ("Skip-gram", "EVALUATED_ON", "Google News") in rel_triples
    assert ("Skip-gram", "OUTPERFORMS", "NNLM") in rel_triples
    assert ("Skip-gram", "ACHIEVES", "Accuracy") in rel_triples

    for rel in relations:
        assert validate_relationship(
            rel.relation,
            get_node_label(rel.subject_entity_type),
            get_node_label(rel.object_entity_type),
        )

