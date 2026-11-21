"""Tests for graph query service."""

import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime
from KnowledgeGraphAI.backend.services.knowledge_graph.graph_query import GraphQueryService, QueryResult


class TestGraphQueryService:
    """Tests for GraphQueryService."""

    def setup_method(self):
        """Set up test fixtures with mocked Neo4j."""
        self.mock_neo4j = Mock()
        self.service = GraphQueryService()
        self.service.neo4j = self.mock_neo4j

    def test_execute_query(self):
        """Test query execution."""
        self.mock_neo4j.execute_query.return_value = [{"test": "result"}]

        result = self.service._execute_query("MATCH (n) RETURN n", {"param": "value"})

        assert result == [{"test": "result"}]
        self.mock_neo4j.execute_query.assert_called_once_with("MATCH (n) RETURN n", {"param": "value"})

    def test_execute_query_error(self):
        """Test query execution error handling."""
        self.mock_neo4j.execute_query.side_effect = Exception("Connection failed")

        with pytest.raises(Exception):
            self.service._execute_query("MATCH (n) RETURN n")

    def test_get_paper_entities(self):
        """Test getting entities for a paper."""
        self.mock_neo4j.execute_query.return_value = [
            {"e": {"canonical_name": "BERT", "entity_type": "Model"}, "labels": ["Model"], "confidence": 0.9, "evidence": "We used BERT."}
        ]

        entities = self.service.get_paper_entities(1)

        assert len(entities) == 1
        assert entities[0]["e"]["canonical_name"] == "BERT"

    def test_get_papers_for_entity(self):
        """Test getting papers for an entity."""
        self.mock_neo4j.execute_query.return_value = [
            {"p": {"paper_id": 1, "title": "Test Paper"}, "confidence": 0.9}
        ]

        papers = self.service.get_papers_for_entity("entity_123", "Model")

        assert len(papers) == 1
        assert papers[0]["p"]["paper_id"] == 1

    def test_get_entity_details(self):
        """Test getting entity details."""
        self.mock_neo4j.execute_query.return_value = [
            {"e": {"canonical_name": "BERT", "entity_id": "abc123"}}
        ]

        result = self.service.get_entity_details("entity_123", "Model")

        assert result is not None
        assert result["e"]["canonical_name"] == "BERT"

    def test_find_models_for_dataset(self):
        """Test finding models for a dataset."""
        self.mock_neo4j.execute_query.return_value = [
            {"m": {"canonical_name": "BERT", "entity_id": "m1"}, "confidence": 0.9}
        ]

        models = self.service.find_models_for_dataset("dataset_123")

        assert len(models) == 1
        assert models[0]["canonical_name"] == "BERT"

    def test_find_algorithms_for_model(self):
        """Test finding algorithms for a model."""
        self.mock_neo4j.execute_query.return_value = [
            {"a": {"canonical_name": "Adam", "entity_id": "a1"}, "confidence": 0.9}
        ]

        algos = self.service.find_algorithms_for_model("model_123")

        assert len(algos) == 1
        assert algos[0]["canonical_name"] == "Adam"

    def test_find_models_for_task(self):
        """Test finding models for a task."""
        self.mock_neo4j.execute_query.return_value = [
            {"m": {"canonical_name": "BERT", "entity_id": "m1"}, "confidence": 0.9}
        ]

        models = self.service.find_models_for_task("task_123")

        assert len(models) == 1
        assert models[0]["canonical_name"] == "BERT"

    def test_find_models_compared_with(self):
        """Test finding models compared with a model."""
        self.mock_neo4j.execute_query.return_value = [
            {"other": {"canonical_name": "RoBERTa", "entity_id": "m2"}, "confidence": 0.8}
        ]

        models = self.service.find_models_compared_with("model_123")

        assert len(models) == 1
        assert models[0]["canonical_name"] == "RoBERTa"

    def test_find_methods_outperforming(self):
        """Test finding models that outperform a model."""
        self.mock_neo4j.execute_query.return_value = [
            {"better": {"canonical_name": "RoBERTa", "entity_id": "m2"}, "confidence": 0.85}
        ]

        models = self.service.find_methods_outperforming("model_123")

        assert len(models) == 1
        assert models[0]["canonical_name"] == "RoBERTa"

    def test_find_methods_improving_metric(self):
        """Test finding methods that improve a metric."""
        self.mock_neo4j.execute_query.return_value = [
            {"m": {"canonical_name": "RoBERTa", "entity_id": "m2"}, "confidence": 0.9}
        ]

        models = self.service.find_methods_improving_metric("metric_123")

        assert len(models) == 1
        assert models[0]["canonical_name"] == "RoBERTa"

    def test_find_metrics_for_model(self):
        """Test finding metrics for a model."""
        self.mock_neo4j.execute_query.return_value = [
            {"met": {"canonical_name": "F1-score", "entity_id": "met1"}, "confidence": 0.9}
        ]

        metrics = self.service.find_metrics_for_model("model_123")

        assert len(metrics) == 1
        assert metrics[0]["canonical_name"] == "F1-score"

    def test_find_models_by_task(self):
        """Test finding models by task name."""
        self.mock_neo4j.execute_query.return_value = [
            {"m": {"canonical_name": "BERT", "entity_id": "m1"}, "confidence": 0.9, "task": "Text Classification"}
        ]

        models = self.service.find_models_by_task("Classification")

        assert len(models) == 1
        assert models[0]["canonical_name"] == "BERT"

    def test_find_relationships_supported_by_multiple_papers(self):
        """Test finding relationships supported by multiple papers."""
        self.mock_neo4j.execute_query.return_value = [
            {"s": {"canonical_name": "BERT"}, "o": {"canonical_name": "SQuAD"}, "rel_type": "EVALUATED_ON", "avg_confidence": 0.9, "paper_count": 3}
        ]

        rels = self.service.find_relationships_supported_by_multiple_papers(min_papers=2)

        assert len(rels) == 1
        assert rels[0]["subject"] == "BERT"
        assert rels[0]["object"] == "SQuAD"
        assert rels[0]["paper_count"] == 3

    def test_get_entity_neighbors(self):
        """Test getting entity neighbors."""
        self.mock_neo4j.execute_query.return_value = [
            {"neighbor": {"canonical_name": "SQuAD", "entity_id": "d1"}, "relation": "EVALUATED_ON", "confidence": 0.9}
        ]

        neighbors = self.service.get_entity_neighbors("m1", "Model", limit=50)

        assert len(neighbors) == 1
        assert neighbors[0]["neighbor"]["canonical_name"] == "SQuAD"

    def test_find_path_between_entities(self):
        """Test finding path between entities."""
        self.mock_neo4j.execute_query.return_value = [
            {"path": ["BERT", "EVALUATED_ON", "SQuAD"]}
        ]

        path = self.service.find_path_between_entities("m1", "d1", max_depth=4)

        assert len(path) == 1

    def test_find_path_between_entities_with_types(self):
        """The explicit typed path form remains supported."""
        self.mock_neo4j.execute_query.return_value = [{"path": []}]

        self.service.find_path_between_entities(
            "m1", "Model", "d1", "Dataset", max_depth=4
        )

        query = self.mock_neo4j.execute_query.call_args.args[0]
        assert "(source:Model" in query
        assert "(target:Dataset" in query
        assert self.mock_neo4j.execute_query.call_args.args[1]["max_depth"] == 4

    def test_find_most_connected_entities(self):
        """Test finding most connected entities."""
        self.mock_neo4j.execute_query.return_value = [
            {"e": {"canonical_name": "BERT", "entity_id": "m1"}, "degree": 10}
        ]

        entities = self.service.find_most_connected_entities(limit=5)

        assert len(entities) == 1
        assert entities[0]["entity"] == "BERT"
        assert entities[0]["degree"] == 10

    def test_search_entities(self):
        """Test searching entities."""
        self.mock_neo4j.execute_query.return_value = [
            {"e": {"canonical_name": "BERT", "type": "Model", "entity_id": "m1"}}
        ]

        results = self.service.search_entities("BERT", limit=10)

        assert len(results) == 1
        assert results[0]["canonical_name"] == "BERT"

    def test_search_papers(self):
        """Test searching papers."""
        self.mock_neo4j.execute_query.return_value = [
            {"p": {"paper_id": 1, "title": "BERT Paper", "author": "Devlin et al."}}
        ]

        papers = self.service.search_papers("BERT", limit=10)

        assert len(papers) == 1
        assert papers[0]["title"] == "BERT Paper"

    def test_query_limits_and_labels_are_validated(self):
        with pytest.raises(ValueError):
            self.service.search_entities("BERT", entity_types=["Model) MATCH (n)"])
        with pytest.raises(ValueError):
            self.service.find_models_for_task("task", limit=0)
        self.mock_neo4j.execute_query.assert_not_called()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])