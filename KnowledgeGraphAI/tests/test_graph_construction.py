"""Tests for graph construction service."""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
from KnowledgeGraphAI.backend.services.knowledge_graph.graph_construction import GraphConstructionService, GraphConstructionStats
from KnowledgeGraphAI.backend.services.knowledge_graph.entity_resolution import EntityResolutionService, CanonicalEntity
from KnowledgeGraphAI.backend.nlp.ner.entity_schema import ExtractedEntity


class TestGraphConstructionService:
    """Tests for GraphConstructionService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.service = GraphConstructionService()
        self.service.neo4j = Mock()

    def test_generate_entity_id(self):
        """Test entity ID generation."""
        entity_id = self.service._generate_entity_id("BERT", "MODEL")
        assert len(entity_id) == 16
        # Deterministic
        assert self.service._generate_entity_id("BERT", "MODEL") == entity_id
        # Different for different types
        assert self.service._generate_entity_id("BERT", "DATASET") != entity_id

    def test_normalize_name(self):
        """Test name normalization."""
        result = self.service._normalize_name("  BERT  ")
        assert result == "bert"
        result = self.service._normalize_name("BERT-base")
        assert result == "bert-base"

    def test_generate_author_id(self):
        """Test author ID generation."""
        author_id = self.service._generate_author_id("John Smith")
        assert len(author_id) == 16
        # Deterministic
        assert self.service._generate_author_id("John Smith") == self.service._generate_author_id("John Smith")

    def test_parse_authors(self):
        """Test author parsing."""
        authors = self.service._parse_authors("John Smith, Jane Doe and Bob Wilson")
        assert len(authors) == 3
        assert "John Smith" in authors
        assert "Jane Doe" in authors
        assert "Bob Wilson" in authors
        assert self.service._parse_authors("  Alice A AND Bob B,  ,  ") == [
            "Alice A", "Bob B"
        ]
        assert self.service._parse_authors("") == []
        assert self.service._parse_authors(None) == []

    def test_stats_tracking(self):
        """Test statistics tracking."""
        stats = GraphConstructionStats()
        assert stats.papers_processed == 0
        assert stats.entities_created == 0
        assert stats.relationships_created == 0

        stats.papers_processed = 1
        stats.entities_created = 5
        stats.entities_merged = 2
        stats.relationships_created = 3

        d = stats.to_dict()
        assert d["papers_processed"] == 1
        assert d["entities_created"] == 5
        assert d["entities_merged"] == 2
        assert d["relationships_created"] == 3


class TestGraphConstructionServiceWithMock:
    """Tests with mocked Neo4j."""

    def setup_method(self):
        """Set up test fixtures with mocked Neo4j."""
        self.mock_neo4j = Mock()
        self.service = GraphConstructionService()
        self.service.neo4j = self.mock_neo4j
        self.service.entity_resolver = Mock()
        self.service.stats = GraphConstructionStats()

        self.paper_metadata = {
            "paper_id": 1,
            "title": "Test Paper",
            "author": "John Smith",
            "file_path": "/path/to/paper.pdf",
            "file_hash": "abc123",
            "content_hash": "def456",
            "page_count": 5,
            "status": "processed",
        }

        self.entities = [
            ExtractedEntity(
                text="BERT",
                entity_type="MODEL",
                start_char=0,
                end_char=4,
                confidence=0.9,
                paper_id=1,
                page_number=1,
                sentence_index=0,
                source_text="We used BERT.",
                extraction_method="rule_based",
            ),
            ExtractedEntity(
                text="SQuAD",
                entity_type="DATASET",
                start_char=20,
                end_char=25,
                confidence=0.85,
                paper_id=1,
                page_number=1,
                sentence_index=1,
                source_text="Tested on SQuAD.",
                extraction_method="rule_based",
            ),
        ]

        self.relations = [
            {
                "relation": "EVALUATED_ON",
                "subject": {"text": "BERT", "label": "MODEL"},
                "object": {"text": "SQuAD", "label": "DATASET"},
                "confidence": 0.9,
                "evidence": "BERT was evaluated on SQuAD.",
                "page_number": 1,
                "sentence_id": 0,
                "extraction_method": "rule_based",
            }
        ]

    def test_build_graph_for_paper_success(self):
        """Test successful graph construction."""
        mock_tx = Mock()
        self.service.neo4j.execute_transaction.return_value = True

        result = self.service.build_graph_for_paper(
            self.paper_metadata, self.entities, self.relations
        )

        assert result["papers_processed"] == 1
        self.service.neo4j.execute_transaction.assert_called_once()

    def test_build_graph_missing_paper_id(self):
        """Test error handling for missing paper_id."""
        bad_metadata = {"title": "Test"}  # Missing paper_id

        result = self.service.build_graph_for_paper(bad_metadata, [], [])

        assert result["papers_processed"] == 0
        assert len(result["errors"]) > 0
        assert "Missing paper_id" in result["errors"][0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])