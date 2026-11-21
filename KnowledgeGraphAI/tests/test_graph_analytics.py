"""Tests for graph analytics service."""

import pytest
from unittest.mock import Mock, MagicMock
from KnowledgeGraphAI.backend.services.knowledge_graph.graph_analytics import GraphAnalytics


class TestGraphAnalytics:
    """Tests for GraphAnalytics."""

    def setup_method(self):
        """Set up test fixtures with mocked Neo4j."""
        self.mock_neo4j = Mock()
        self.service = GraphAnalytics()
        self.service.neo4j = self.mock_neo4j

    def test_execute_query(self):
        """Test query execution."""
        self.service.neo4j.execute_query.return_value = [{"test": "result"}]

        result = self.service._execute_query("MATCH (n) RETURN n", {"param": "value"})

        assert result == [{"test": "result"}]
        self.service.neo4j.execute_query.assert_called_once_with("MATCH (n) RETURN n", {"param": "value"})

    def test_execute_query_error(self):
        """Test query execution error handling."""
        self.service.neo4j.execute_query.side_effect = Exception("Connection failed")

        result = self.service._execute_query("MATCH (n) RETURN n")
        assert result is None

    def test_get_stats(self):
        """Test getting graph statistics."""
        self.service.neo4j.execute_query.side_effect = [
            [{"labels": ["Model"], "count": 10}, {"labels": ["Dataset"], "count": 5}],
            [{"type": "EVALUATED_ON", "count": 15}, {"type": "USES", "count": 10}]
        ]

        stats = self.service.get_stats()

        assert stats["total_nodes"] == 15
        assert stats["total_relationships"] == 25
        assert stats["nodes"]["Model"] == 10
        assert stats["nodes"]["Dataset"] == 5
        assert stats["relationships"]["EVALUATED_ON"] == 15
        assert stats["relationships"]["USES"] == 10

    def test_get_entity_counts_by_category(self):
        """Test entity counts by category."""
        self.service.neo4j.execute_query.return_value = [
            {"label": "Model", "count": 10},
            {"label": "Dataset", "count": 5}
        ]

        counts = self.service.get_entity_counts_by_category()

        assert counts["Model"] == 10
        assert counts["Dataset"] == 5

    def test_get_most_frequent_models(self):
        """Test most frequent models."""
        self.service.neo4j.execute_query.return_value = [
            {"model": "BERT", "mentions": 5},
            {"model": "RoBERTa", "mentions": 3}
        ]

        models = self.service.get_most_frequent_models(limit=10)

        assert len(models) == 2
        assert models[0]["model"] == "BERT"
        assert models[0]["mentions"] == 5

    def test_get_most_frequent_datasets(self):
        """Test most frequent datasets."""
        self.service.neo4j.execute_query.return_value = [
            {"dataset": "SQuAD", "mentions": 5},
            {"dataset": "GLUE", "mentions": 3}
        ]

        datasets = self.service.get_most_frequent_datasets(limit=10)

        assert len(datasets) == 2
        assert datasets[0]["dataset"] == "SQuAD"

    def test_get_most_connected_entities(self):
        """Test most connected entities."""
        self.service.neo4j.execute_query.return_value = [
            {"name": "BERT", "type": "Model", "entity_id": "m1", "degree": 10}
        ]

        entities = self.service.get_most_connected_entities(limit=10)

        assert len(entities) == 1
        assert entities[0]["entity"] == "BERT"
        assert entities[0]["degree"] == 10

    def test_get_papers_with_largest_entity_count(self):
        """Test papers with largest entity count."""
        self.service.neo4j.execute_query.return_value = [
            {"paper_id": 1, "title": "BERT Paper", "entity_count": 20}
        ]

        papers = self.service.get_papers_with_largest_entity_count(limit=10)

        assert len(papers) == 1
        assert papers[0]["paper_id"] == 1
        assert papers[0]["entity_count"] == 20

    def test_get_relation_counts_by_type(self):
        """Test relation counts by type."""
        self.service.neo4j.execute_query.return_value = [
            {"type": "EVALUATED_ON", "count": 15},
            {"type": "USES", "count": 10}
        ]

        counts = self.service.get_relation_counts_by_type()

        assert counts["EVALUATED_ON"] == 15
        assert counts["USES"] == 10

    def test_find_compared_models(self):
        """Test finding compared models."""
        self.service.neo4j.execute_query.return_value = [
            {"other": {"canonical_name": "RoBERTa", "entity_id": "m2"}, "confidence": 0.8, "paper_id": 1}
        ]

        models = self.service.find_compared_models("m1", limit=10)

        assert len(models) == 1
        assert models[0]["other"]["canonical_name"] == "RoBERTa"

    def test_find_models_outperforming(self):
        """Test finding models that outperform."""
        self.service.neo4j.execute_query.return_value = [
            {"better": {"canonical_name": "RoBERTa", "entity_id": "m2"}, "confidence": 0.9, "paper_id": 1}
        ]

        models = self.service.find_models_outperforming("m1", limit=10)

        assert len(models) == 1
        assert models[0]["better"]["canonical_name"] == "RoBERTa"

    def test_find_models_improving_metric(self):
        """Test finding models improving a metric."""
        self.service.neo4j.execute_query.return_value = [
            {"m": {"canonical_name": "RoBERTa", "entity_id": "m2"}, "confidence": 0.9, "paper_id": 1}
        ]

        models = self.service.find_models_improving_metric("met1", limit=10)

        assert len(models) == 1
        assert models[0]["m"]["canonical_name"] == "RoBERTa"

    def test_get_entity_neighborhood(self):
        """Test getting entity neighborhood."""
        self.service.neo4j.execute_query.return_value = [
            {"nodes": [{"canonical_name": "BERT"}], "relationships": [{"type": "EVALUATED_ON"}]}
        ]

        neighborhood = self.service.get_entity_neighborhood("m1", "Model", max_depth=1, limit=100)

        assert "nodes" in neighborhood
        assert "relationships" in neighborhood

    def test_get_entity_neighborhood_error(self):
        """Test neighborhood with error."""
        self.service.neo4j.execute_query.side_effect = Exception("APOC not available")

        neighborhood = self.service.get_entity_neighborhood("m1")
        assert neighborhood == {"nodes": [], "relationships": []}

    def test_neighborhood_rejects_invalid_depth_and_limit(self):
        with pytest.raises(ValueError):
            self.service.get_entity_neighborhood("m1", max_depth=0)
        with pytest.raises(ValueError):
            self.service.get_entity_neighborhood("m1", limit=0)
        self.mock_neo4j.execute_query.assert_not_called()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])