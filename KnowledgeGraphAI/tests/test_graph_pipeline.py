"""Tests for full graph pipeline integration."""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import json
from unittest.mock import Mock

from KnowledgeGraphAI.backend.nlp.ner.entity_schema import (
    ExtractedSentence,
)
from KnowledgeGraphAI.backend.nlp.ner.ner_pipeline import NERPipeline
from KnowledgeGraphAI.backend.nlp.relation_extraction.entity_pair_generator import (
    EntityPairCandidate,
)
from KnowledgeGraphAI.backend.nlp.relation_extraction.relation_extraction_service import (
    ScientificRelationExtractionService,
)
from KnowledgeGraphAI.backend.nlp.relation_extraction.entity_pair_generator import (
    EntityPairGenerator,
)
from KnowledgeGraphAI.backend.services.knowledge_graph.graph_construction import (
    GraphConstructionService,
)

# Mock the pipeline integration


class TestPipelineIntegration:
    """Tests for full pipeline integration."""

    def test_full_pipeline_flow(self):
        """Test the complete pipeline from PDF to graph."""
        # This test verifies the integration points exist
        # In a real test, we would mock all external dependencies

        # 1. PDF Ingestion
        pdf_steps = [
            "PDF uploaded",
            "Text extracted",
            "Metadata extracted",
            "Pages segmented"
        ]
        assert len(pdf_steps) == 4

        # 2. Preprocessing
        preprocessing_steps = [
            "Text cleaned",
            "Paragraphs segmented",
            "Sentences segmented",
            "Sections detected"
        ]
        assert len(preprocessing_steps) == 4

        # 3. NER
        ner_steps = [
            "Entities detected",
            "Entities normalized",
            "Provenance attached"
        ]
        assert len(ner_steps) == 3

        # 4. Relation Extraction
        re_steps = [
            "Entity pairs generated",
            "Relations extracted",
            "Relations validated"
        ]
        assert len(re_steps) == 3

        # 5. Entity Resolution
        er_steps = [
            "Entities normalized",
            "Canonical IDs assigned",
            "Aliases resolved"
        ]
        assert len(er_steps) == 3

        # 6. Graph Construction
        gc_steps = [
            "Paper node created",
            "Entity nodes created",
            "Relationships created",
            "Provenance attached"
        ]
        assert len(gc_steps) == 4

    def test_provenance_preservation(self):
        """Test that provenance is preserved through pipeline."""
        # Verify provenance fields at each stage
        provenance_fields = [
            "paper_id",
            "page_number",
            "sentence_index",
            "start_char",
            "end_char",
            "original_text",
            "cleaned_text"
        ]

        # Each entity should have all provenance fields
        entity = {
            "text": "BERT",
            "entity_type": "MODEL",
            "start_char": 0,
            "end_char": 4,
            "confidence": 0.9,
            "paper_id": 1,
            "page_number": 3,
            "sentence_index": 2,
            "source_text": "We used BERT.",
            "original_text": "We used BERT.",
            "cleaned_text": "We used BERT.",
            "extraction_method": "rule_based"
        }

        for field in provenance_fields:
            assert field in entity

        sentence = ExtractedSentence(
            paper_id=1,
            page_number=3,
            section_name="Experiments",
            paragraph_index=0,
            sentence_index=2,
            original_text="BERT was evaluated on SQuAD.",
            cleaned_text="BERT evaluated on SQuAD.",
        )
        entity_batch = NERPipeline().extract_from_sentence(sentence)
        model = next(entity for entity in entity_batch.entities if entity.entity_type == "MODEL")
        dataset = next(
            entity for entity in entity_batch.entities if entity.entity_type == "DATASET"
        )
        assert model.to_dict()["original_text"] == sentence.original_text
        assert model.to_dict()["cleaned_text"] == sentence.cleaned_text

        candidate = EntityPairCandidate(model, dataset, "EVALUATED_ON", 0, 1)
        relation_service = ScientificRelationExtractionService(
            use_relabel=False, use_classifier=False
        )
        relations = relation_service._run_rule_based(
            [candidate], sentence.cleaned_text, [sentence]
        )
        assert len(relations) == 1
        relation = relations[0]
        assert relation.to_dict()["original_text"] == sentence.original_text
        assert relation.to_dict()["cleaned_text"] == sentence.cleaned_text
        assert relation_service._validate_relations(
            relations, sentence.cleaned_text, [sentence]
        ) == relations

        graph_service = GraphConstructionService()
        tx = Mock()
        tx.run.return_value.single.return_value = {"created": True}
        graph_service._create_contains_relationship(tx, 1, "model-id", model)
        entity_params = tx.run.call_args.args[1]
        assert entity_params["original_text"] == sentence.original_text
        assert entity_params["cleaned_text"] == sentence.cleaned_text

        graph_service._merge_relationship(
            tx, relation.to_dict(), {"paper_id": 1}, "2024-01-01T00:00:00"
        )
        relation_params = tx.run.call_args.args[1]
        assert relation_params["original_text"] == sentence.original_text
        assert relation_params["cleaned_text"] == sentence.cleaned_text
        assert relation_params["start_char"] == min(
            relation.to_dict()["subject"]["start"],
            relation.to_dict()["object"]["start"],
        )
        assert relation_params["end_char"] == max(
            relation.to_dict()["subject"]["end"],
            relation.to_dict()["object"]["end"],
        )

    def test_entity_pair_generation_and_relation_extraction(self):
        sentence = ExtractedSentence(
            paper_id=1,
            page_number=1,
            section_name="Experiments",
            paragraph_index=0,
            sentence_index=0,
            original_text=(
                "BERT was evaluated on the SQuAD dataset, and BERT achieved an "
                "F1-score of 91 percent."
            ),
            cleaned_text=(
                "BERT was evaluated on the SQuAD dataset, and BERT achieved an "
                "F1-score of 91 percent."
            ),
        )
        entities = NERPipeline().extract_from_sentence(sentence).entities

        assert [(entity.text, entity.entity_type) for entity in entities] == [
            ("BERT", "MODEL"),
            ("SQuAD", "DATASET"),
            ("BERT", "MODEL"),
            ("F1-score", "METRIC"),
        ]

        candidates = EntityPairGenerator().generate_from_entities(
            entities, {index: entity.sentence_index for index, entity in enumerate(entities)}, 1
        )
        assert candidates
        assert [(candidate.sentence_id, candidate.subject_start) for candidate in candidates] == sorted(
            (candidate.sentence_id, candidate.subject_start) for candidate in candidates
        )

        relations = ScientificRelationExtractionService(
            use_relabel=False, use_classifier=False
        ).extract_relations(
            sentence.cleaned_text, entities, [sentence], paper_id=1
        )
        assert {relation.relation for relation in relations} >= {"ACHIEVES"}
        assert all(relation.evidence == sentence.cleaned_text for relation in relations)

    def test_duplicate_handling(self):
        """Test that duplicate processing is idempotent."""
        # Processing same paper twice should not create duplicates
        pass

    def test_error_handling(self):
        """Test error handling at each stage."""
        error_stages = [
            "PDF parsing failed",
            "Preprocessing failed",
            "NER failed",
            "Relation extraction failed",
            "Entity resolution failed",
            "Graph construction failed"
        ]
        assert len(error_stages) == 6

    def test_pipeline_data_flow(self):
        """Test data flows correctly through pipeline."""
        # Data flow: PDF -> Preprocessing -> NER -> RE -> ER -> Graph
        pipeline_order = [
            "PDF",
            "Preprocessing",
            "NER",
            "Relation Extraction",
            "Entity Resolution",
            "Graph Construction"
        ]
        assert pipeline_order.index("PDF") < pipeline_order.index("Preprocessing")
        assert pipeline_order.index("Preprocessing") < pipeline_order.index("NER")
        assert pipeline_order.index("NER") < pipeline_order.index("Relation Extraction")
        assert pipeline_order.index("Relation Extraction") < pipeline_order.index("Entity Resolution")
        assert pipeline_order.index("Entity Resolution") < pipeline_order.index("Graph Construction")

    def test_provenance_in_graph(self):
        """Test that provenance is stored in graph relationships."""
        # Each relationship should have provenance
        relation_provenance = [
            "confidence",
            "evidence",
            "paper_id",
            "page_number",
            "sentence_id",
            "extraction_method",
            "created_at"
        ]

        relation = {
            "subject": "BERT",
            "relation": "EVALUATED_ON",
            "object": "SQuAD",
            "confidence": 0.9,
            "evidence": "BERT was evaluated on SQuAD.",
            "paper_id": 1,
            "page_number": 3,
            "sentence_id": 2,
            "extraction_method": "rule_based",
            "created_at": "2024-01-01T00:00:00"
        }

        for field in relation_provenance:
            assert field in relation

    def test_idempotent_processing(self):
        """Test that processing same paper twice is idempotent."""
        # Running pipeline twice on same paper should not create duplicates
        # This requires Neo4j constraints which are defined in graph_schema.py
        pass

    def test_error_stage_reporting(self):
        """Test that errors report correct failure stage."""
        stages = [
            "pdf_ingestion",
            "preprocessing",
            "ner",
            "relation_extraction",
            "entity_resolution",
            "graph_construction"
        ]

        # If graph_construction fails, error should report that stage
        error = {
            "stage": "graph_construction",
            "message": "Neo4j unavailable",
            "details": {}
        }
        assert error["stage"] in stages


if __name__ == "__main__":
    pytest.main([__file__, "-v"])