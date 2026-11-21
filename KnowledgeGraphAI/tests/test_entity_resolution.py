"""Tests for entity resolution service."""

import pytest
from datetime import datetime
from KnowledgeGraphAI.backend.services.knowledge_graph.entity_resolution import (
    EntityResolutionService,
    CanonicalEntity,
)
from KnowledgeGraphAI.backend.nlp.ner.entity_schema import ExtractedEntity


class TestEntityResolutionService:
    """Tests for EntityResolutionService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.service = EntityResolutionService()
        self.test_timestamp = datetime.utcnow().isoformat()

    def test_normalize_for_matching(self):
        """Test text normalization for matching."""
        # Test basic normalization
        result = self.service._normalize_for_matching("  BERT  ", "MODEL")
        assert result == "bert"

        # Test unicode normalization
        result = self.service._normalize_for_matching("BERT‑base", "MODEL")
        assert result == "bert-base"

        # Matching normalization is case-insensitive even for model types.
        result = self.service._normalize_for_matching("GPT-3", "MODEL")
        assert result == "gpt-3"

        result = self.service._normalize_for_matching("GPT-4", "MODEL")
        assert result == "gpt-4"

    def test_generate_entity_id(self):
        """Test deterministic entity ID generation."""
        id1 = self.service._generate_entity_id("BERT", "MODEL")
        id2 = self.service._generate_entity_id("BERT", "MODEL")
        assert id1 == id2  # Deterministic
        assert len(id1) == 16  # SHA256 truncated to 16 chars

        # Different entity types should give different IDs
        id3 = self.service._generate_entity_id("BERT", "DATASET")
        assert id1 != id3

    def test_resolve_new_entity(self):
        """Test resolving a new entity."""
        entity = ExtractedEntity(
            text="BERT",
            entity_type="MODEL",
            start_char=0,
            end_char=4,
            confidence=0.9,
            paper_id=1,
            page_number=1,
            sentence_index=0,
            source_text="We used BERT.",
        )

        entity_id, is_new = self.service.resolve_entity(entity, 1, datetime.utcnow().isoformat())

        assert is_new is True
        assert entity_id in self.service.canonical_entities
        canonical = self.service.canonical_entities[entity_id]
        assert canonical.canonical_name == "BERT"
        assert canonical.entity_type == "MODEL"
        assert canonical.occurrence_count == 1
        assert 1 in canonical.source_papers

    def test_resolve_duplicate_entity(self):
        """Test duplicate entity resolution."""
        entity = ExtractedEntity(
            text="BERT",
            entity_type="MODEL",
            start_char=0,
            end_char=4,
            confidence=0.9,
            paper_id=1,
            page_number=1,
            sentence_index=0,
            source_text="We used BERT.",
        )

        # First resolution
        entity_id1, is_new1 = self.service.resolve_entity(
            entity, 1, datetime.utcnow().isoformat()
        )
        assert is_new1 is True

        # Second resolution - same paper
        entity_id2, is_new2 = self.service.resolve_entity(
            entity, 1, datetime.utcnow().isoformat()
        )
        assert is_new2 is False
        assert entity_id1 == entity_id2

        # Third resolution - different paper
        entity_id3, is_new3 = self.service.resolve_entity(
            entity, 2, datetime.utcnow().isoformat()
        )
        assert is_new3 is False
        assert entity_id1 == entity_id3

        canonical = self.service.canonical_entities[entity_id1]
        assert canonical.occurrence_count == 3
        assert 1 in canonical.source_papers
        assert 2 in canonical.source_papers

    def test_alias_management(self):
        """Test alias management."""
        entity = ExtractedEntity(
            text="BERT",
            entity_type="MODEL",
            start_char=0,
            end_char=4,
            confidence=0.9,
            paper_id=1,
            page_number=1,
            sentence_index=0,
            source_text="We used BERT.",
        )

        entity_id, _ = self.service.resolve_entity(entity, 1, datetime.utcnow().isoformat())

        # Add alias
        result = self.service.add_alias(entity_id, "Bidirectional Encoder Representations")
        assert result is True

        # Check alias was added
        canonical = self.service.canonical_entities[entity_id]
        assert "Bidirectional Encoder Representations" in canonical.aliases

        # Verify alias lookup works
        alias_id = self.service._resolve_aliases("bidirectional encoder representations", "MODEL")
        assert alias_id == entity_id
        assert self.service._resolve_aliases(
            "  BIDIRECTIONAL ENCODER REPRESENTATIONS  ", "MODEL"
        ) == entity_id
        assert self.service.get_by_normalized_name(
            "  bidirectional encoder representations "
        ).entity_id == entity_id

    def test_get_canonical(self):
        """Test getting canonical entity by ID."""
        entity = ExtractedEntity(
            text="BERT",
            entity_type="MODEL",
            start_char=0,
            end_char=4,
            confidence=0.9,
            paper_id=1,
            page_number=1,
            sentence_index=0,
            source_text="We used BERT.",
        )

        entity_id, _ = self.service.resolve_entity(entity, 1, datetime.utcnow().isoformat())
        canonical = self.service.get_canonical(entity_id)

        assert canonical is not None
        assert canonical.entity_id == entity_id
        assert canonical.canonical_name == "BERT"

    def test_get_by_normalized_name(self):
        """Test lookup by normalized name."""
        entity = ExtractedEntity(
            text="BERT",
            entity_type="MODEL",
            start_char=0,
            end_char=4,
            confidence=0.9,
            paper_id=1,
            page_number=1,
            sentence_index=0,
            source_text="We used BERT.",
        )

        entity_id, _ = self.service.resolve_entity(entity, 1, datetime.utcnow().isoformat())
        canonical = self.service.get_by_normalized_name("  BERT ")

        assert canonical is not None
        assert canonical.entity_id == entity_id

    def test_ambiguous_match_detection(self):
        """Test ambiguous match flagging for distinct models."""
        # First resolve GPT-3
        entity1 = ExtractedEntity(
            text="GPT-3",
            entity_type="MODEL",
            start_char=0,
            end_char=5,
            confidence=0.9,
            paper_id=1,
            page_number=1,
            sentence_index=0,
            source_text="We used GPT-3.",
        )
        self.service.resolve_entity(entity1, 1, datetime.utcnow().isoformat())

        # Now try GPT-4 - should be flagged as distinct
        entity2 = ExtractedEntity(
            text="GPT-4",
            entity_type="MODEL",
            start_char=0,
            end_char=5,
            confidence=0.9,
            paper_id=2,
            page_number=1,
            sentence_index=0,
            source_text="We used GPT-4.",
        )
        entity_id, is_new = self.service.resolve_entity(entity2, 2, datetime.utcnow().isoformat())
        assert is_new is True  # Should create new entity

        # Check ambiguous match was flagged
        assert len(self.service.ambiguous_matches) > 0

    def test_export_import_canonical_entities(self):
        """Test export and import of canonical entities."""
        entity = ExtractedEntity(
            text="BERT",
            entity_type="MODEL",
            start_char=0,
            end_char=4,
            confidence=0.9,
            paper_id=1,
            page_number=1,
            sentence_index=0,
            source_text="We used BERT.",
        )
        entity_id, _ = self.service.resolve_entity(entity, 1, datetime.utcnow().isoformat())
        self.service.add_alias(entity_id, "Bidirectional Encoder")

        # Export
        exported = self.service.export_canonical_entities()
        assert len(exported) == 1
        assert exported[0]["entity_id"] == entity_id

        # Create new service and import
        new_service = EntityResolutionService()
        count = new_service.import_canonical_entities(exported)
        assert count == 1

        # Verify imported data
        imported = new_service.get_canonical(entity_id)
        assert imported is not None
        assert imported.canonical_name == "BERT"
        assert imported.aliases == ["Bidirectional Encoder"]
        assert imported.source_papers == [1]
        assert imported.occurrence_count == 1
        assert new_service.get_by_normalized_name("  BIDIRECTIONAL ENCODER ").entity_id == entity_id

    def test_stats(self):
        """Test statistics tracking."""
        entity = ExtractedEntity(
            text="BERT",
            entity_type="MODEL",
            start_char=0,
            end_char=4,
            confidence=0.9,
            paper_id=1,
            page_number=1,
            sentence_index=0,
            source_text="We used BERT.",
        )

        self.service.resolve_entity(entity, 1, datetime.utcnow().isoformat())
        self.service.resolve_entity(entity, 2, datetime.utcnow().isoformat())  # duplicate

        stats = self.service.get_stats()
        assert stats["total_processed"] == 2
        assert stats["duplicates_resolved"] == 1
        assert stats["new_canonical"] == 1
        assert stats["total_canonical"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])