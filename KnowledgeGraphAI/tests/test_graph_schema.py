"""Tests for graph schema validation."""

import pytest
from KnowledgeGraphAI.backend.services.knowledge_graph.graph_schema import (
    get_node_label,
    validate_relationship,
    get_relationship_properties,
    get_node_properties,
    ENTITY_TYPE_TO_LABEL,
    VALID_RELATIONSHIPS,
    NODE_LABELS,
    RELATIONSHIP_TYPES,
)


class TestGraphSchema:
    """Tests for graph schema validation."""

    def test_node_labels(self):
        """Test node labels are correctly defined."""
        assert len(NODE_LABELS) == 12
        assert "Paper" in NODE_LABELS
        assert "Model" in NODE_LABELS
        assert "Dataset" in NODE_LABELS

    def test_relationship_types(self):
        """Test relationship types are correctly defined."""
        assert len(RELATIONSHIP_TYPES) == 12
        assert "AUTHORED" in RELATIONSHIP_TYPES
        assert "EVALUATED_ON" in RELATIONSHIP_TYPES
        assert "PROPOSES" in RELATIONSHIP_TYPES

    def test_entity_type_to_label(self):
        """Test entity type to label mapping."""
        assert get_node_label("MODEL") == "Model"
        assert get_node_label("DATASET") == "Dataset"
        assert get_node_label("ALGORITHM") == "Algorithm"
        assert get_node_label("UNKNOWN") == "UNKNOWN"

    def test_validate_relationship_valid(self):
        """Test valid relationship validation."""
        assert validate_relationship("PROPOSES", "Model", "Task") is True
        assert validate_relationship("USES", "Model", "Dataset") is True
        assert validate_relationship("USES", "Model", "Algorithm") is True
        assert validate_relationship("EVALUATED_ON", "Model", "Dataset") is True
        assert validate_relationship("ACHIEVES", "Model", "Metric") is True
        assert validate_relationship("COMPARED_WITH", "Model", "Model") is True
        assert validate_relationship("IMPROVES", "Model", "Metric") is True
        assert validate_relationship("APPLIES_TO", "Methodology", "Task") is True
        assert validate_relationship("OUTPERFORMS", "Model", "Model") is True
        assert validate_relationship("BASED_ON", "Model", "Methodology") is True
        assert validate_relationship("AUTHORED", "Author", "Paper") is True
        assert validate_relationship("CONTAINS_ENTITY", "Paper", "Model") is True

    def test_validate_relationship_invalid(self):
        """Test invalid relationship validation."""
        # Wrong direction
        assert validate_relationship("PROPOSES", "Task", "Model") is False
        # Wrong types
        assert validate_relationship("EVALUATED_ON", "Dataset", "Model") is False
        # Invalid relation type
        assert validate_relationship("INVALID", "Model", "Dataset") is False

    def test_relationship_properties(self):
        """Test relationship property definitions."""
        props = get_relationship_properties("EVALUATED_ON")
        assert "confidence" in props
        assert "evidence" in props
        assert "paper_id" in props
        assert "page_number" in props
        assert "sentence_id" in props
        assert "extraction_method" in props
        assert "created_at" in props

    def test_node_properties(self):
        """Test node property definitions."""
        props = get_node_properties("Model")
        assert "entity_id" in props
        assert "canonical_name" in props
        assert "normalized_name" in props
        assert "aliases" in props

    def test_relationship_direction(self):
        """Test relationship direction mapping."""
        from KnowledgeGraphAI.backend.services.knowledge_graph.graph_schema import get_direction
        import pytest

        assert get_direction("EVALUATED_ON") == "subject->object"
        assert get_direction("COMPARED_WITH") == "subject<->object"
        with pytest.raises(ValueError):
            get_direction("UNKNOWN")

    def test_valid_relationships_mapping(self):
        """Test VALID_RELATIONSHIPS mapping."""
        # Check PROPOSES
        proposes = VALID_RELATIONSHIPS["PROPOSES"]
        proposes_from = proposes["from"] if isinstance(proposes["from"], list) else [proposes["from"]]
        proposes_to = proposes["to"] if isinstance(proposes["to"], list) else [proposes["to"]]
        assert "Model" in proposes_from
        assert "Task" in proposes_to

        # Check USES
        uses = VALID_RELATIONSHIPS["USES"]
        uses_from = uses["from"] if isinstance(uses["from"], list) else [uses["from"]]
        uses_to = uses["to"] if isinstance(uses["to"], list) else [uses["to"]]
        assert "Model" in uses_from
        assert "Dataset" in uses_to
        assert "Algorithm" in uses_to

        # Check COMPARED_WITH (symmetric)
        compared = VALID_RELATIONSHIPS["COMPARED_WITH"]
        compared_from = compared["from"] if isinstance(compared["from"], list) else [compared["from"]]
        compared_to = compared["to"] if isinstance(compared["to"], list) else [compared["to"]]
        assert "Model" in compared_from
        assert "Model" in compared_to


if __name__ == "__main__":
    pytest.main([__file__, "-v"])