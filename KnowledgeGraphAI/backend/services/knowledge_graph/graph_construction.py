import logging
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass, field

from KnowledgeGraphAI.backend.services.knowledge_graph.neo4j_connection import get_neo4j_manager
from KnowledgeGraphAI.backend.services.knowledge_graph.entity_resolution import EntityResolutionService, CanonicalEntity
from KnowledgeGraphAI.backend.services.knowledge_graph.graph_schema import (
    get_node_label,
    validate_relationship,
    get_relationship_properties,
    get_node_properties,
    ENTITY_TYPE_TO_LABEL,
    VALID_RELATIONSHIPS,
)
from KnowledgeGraphAI.backend.nlp.ner.entity_schema import ExtractedEntity
from KnowledgeGraphAI.backend.nlp.relation_extraction.relation_schema import ExtractedRelation

logger = logging.getLogger(__name__)


@dataclass
class GraphConstructionStats:
    """Statistics from graph construction."""
    papers_processed: int = 0
    entities_created: int = 0
    entities_merged: int = 0
    relationships_created: int = 0
    relationships_merged: int = 0
    papers_created: int = 0
    authors_created: int = 0
    organizations_created: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "papers_processed": self.papers_processed,
            "entities_created": self.entities_created,
            "entities_merged": self.entities_merged,
            "relationships_created": self.relationships_created,
            "relationships_merged": self.relationships_merged,
            "papers_created": self.papers_created,
            "authors_created": self.authors_created,
            "organizations_created": self.organizations_created,
            "errors": self.errors,
            "warnings": self.warnings,
        }


class GraphConstructionService:
    """
    Service for constructing the knowledge graph from extracted entities and relations.

    Responsibilities:
    1. Accept paper and its metadata
    2. Accept extracted entities and relationships
    3. Validate input schemas
    4. Resolve canonical entities
    5. Create/merge Paper nodes
    6. Create/merge entity nodes
    7. Create author and organization nodes
    8. Create graph relationships
    9. Attach provenance and evidence
    10. Execute writes transactionally
    11. Return construction statistics
    """

    def __init__(self, entity_resolution_service: Optional[EntityResolutionService] = None):
        self.neo4j = get_neo4j_manager()
        self.entity_resolver = entity_resolution_service or EntityResolutionService()
        self.stats = GraphConstructionStats()

    def build_graph_for_paper(
        self,
        paper_metadata: Dict[str, Any],
        entities: List[ExtractedEntity],
        relations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Build graph for a single paper.

        Args:
            paper_metadata: Dict with paper metadata (paper_id, title, author, etc.)
            entities: List of ExtractedEntity from Phase 2.2
            relations: List of relation dicts from Phase 2.3

        Returns:
            Dictionary with construction statistics
        """
        self.stats = GraphConstructionStats()
        paper_id = paper_metadata.get("paper_id")

        if paper_id is None:
            self.stats.errors.append("Missing paper_id in metadata")
            return self.stats.to_dict()

        try:
            # Execute in a single transaction for consistency
            self.neo4j.execute_transaction(
                self._build_paper_transaction,
                paper_metadata,
                entities,
                relations,
            )
            self.stats.papers_processed = 1
        except Exception as e:
            logger.exception(f"Graph construction failed for paper {paper_id}: {e}")
            self.stats.errors.append(str(e))

        return self.stats.to_dict()

    def _build_paper_transaction(
        self,
        tx,
        paper_metadata: Dict[str, Any],
        entities: List,
        relations: List[Dict],
    ) -> None:
        """Transaction function to build graph for a paper."""
        paper_id = paper_metadata["paper_id"]
        timestamp = datetime.utcnow().isoformat()

        # 1. Create/merge Paper node
        paper_created = self._merge_paper_node(tx, paper_metadata, timestamp)
        if paper_metadata.get("author"):
            self._create_authors(tx, paper_metadata, timestamp)

        # Merge repeated mentions once per paper so retries do not inflate counts.
        entity_mentions: Dict[str, List[ExtractedEntity]] = {}
        for entity in entities:
            entity_id = self._generate_entity_id(entity.text, entity.entity_type)
            entity_mentions.setdefault(entity_id, []).append(entity)

        for mentions in entity_mentions.values():
            entity = mentions[0]
            canonical_id, is_new = self._merge_entity_node(
                tx,
                entity,
                paper_metadata,
                timestamp,
                occurrence_count=len({
                    (
                        mention.page_number,
                        mention.sentence_index,
                        mention.start_char,
                        mention.end_char,
                    )
                    for mention in mentions
                }),
                aliases=list(dict.fromkeys(
                    mention.text for mention in mentions if mention.text != entity.text
                )),
            )
            if is_new:
                self.stats.entities_created += 1
            else:
                self.stats.entities_merged += 1
            self._create_contains_relationship(
                tx,
                paper_metadata["paper_id"],
                canonical_id,
                entity,
                occurrence_count=len(mentions),
            )

        # 4. Create author/organization relationships
        self._create_author_relationships(tx, paper_metadata, timestamp)

        # 5. Process relationships
        for relation in relations:
            try:
                rel_data = relation.to_dict() if hasattr(relation, "to_dict") else relation
                self._merge_relationship(tx, rel_data, paper_metadata, timestamp)
            except Exception as e:
                logger.warning(f"Failed to create relationship: {e}")
                self.stats.warnings.append(f"Failed relationship: {e}")

    def _merge_paper_node(self, tx, paper_metadata: Dict, timestamp: str) -> bool:
        """Create or merge Paper node."""
        paper_id = paper_metadata["paper_id"]
        file_hash = paper_metadata.get("file_hash", "")
        content_hash = paper_metadata.get("content_hash", "")

        query = """
        MERGE (p:Paper {paper_id: $paper_id})
        ON CREATE SET
            p.title = $title,
            p.arxiv_id = $arxiv_id,
            p.author = $author,
            p.file_path = $file_path,
            p.file_hash = $file_hash,
            p.content_hash = $content_hash,
            p.page_count = $page_count,
            p.status = $status,
            p.created_at = $created_at,
            p.updated_at = $updated_at
        ON MATCH SET
            p.title = $title,
            p.arxiv_id = CASE
                WHEN $arxiv_id IS NULL OR $arxiv_id = '' THEN p.arxiv_id
                ELSE $arxiv_id
            END,
            p.author = $author,
            p.file_path = $file_path,
            p.file_hash = $file_hash,
            p.content_hash = $content_hash,
            p.page_count = $page_count,
            p.status = $status,
            p.updated_at = $updated_at
        RETURN p.paper_id AS id, p.created_at = $created_at AS created
        """

        params = {
            "paper_id": paper_metadata.get("paper_id"),
            "arxiv_id": paper_metadata.get("arxiv_id"),
            "title": paper_metadata.get("title", ""),
            "author": paper_metadata.get("author", ""),
            "file_path": paper_metadata.get("file_path", ""),
            "file_hash": paper_metadata.get("file_hash", ""),
            "content_hash": paper_metadata.get("content_hash", ""),
            "page_count": paper_metadata.get("page_count", 0),
            "status": paper_metadata.get("status", "processed"),
            "created_at": timestamp,
            "updated_at": timestamp,
        }

        result = tx.run(query, params)
        record = result.single()
        if record and record["created"]:
            self.stats.papers_created += 1
        return True

    def _create_authors(self, tx, paper_metadata: Dict, timestamp: str) -> None:
        """Create author nodes from paper author metadata."""
        author_text = paper_metadata.get("author", "")
        if not author_text:
            return

        # Parse authors (comma-separated or "and" separated)
        authors = self._parse_authors(paper_metadata.get("author", ""))

        for i, author_name in enumerate(authors):
            # Create author node
            author_id = self._generate_author_id(author_name)
            query = """
            MERGE (a:Author {author_id: $author_id})
            ON CREATE SET
                a.name = $name,
                a.normalized_name = $normalized_name,
                a.created_at = $created_at,
                a.updated_at = $updated_at
            ON MATCH SET
                a.name = $name,
                a.updated_at = $updated_at
            RETURN a.author_id
            """
            tx.run(query, {
                "author_id": self._generate_author_id(author_name),
                "name": author_name,
                "normalized_name": author_name.lower().strip(),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            })
            self.stats.authors_created += 1

    def _parse_authors(self, author_text: str) -> List[str]:
        """Parse author names from text."""
        if not isinstance(author_text, str) or not author_text.strip():
            return []
        authors = re.split(r",|\s+and\s+", author_text, flags=re.IGNORECASE)
        return [a.strip() for a in authors if a.strip()]

    def _generate_author_id(self, name: str) -> str:
        """Generate deterministic author ID."""
        import hashlib
        return hashlib.sha256(f"author:{name.lower().strip()}".encode()).hexdigest()[:16]

    def _create_author_relationships(self, tx, paper_metadata: Dict, timestamp: str) -> None:
        """Create AUTHORED relationships between authors and paper."""
        authors = self._parse_authors(paper_metadata.get("author", ""))
        paper_id = paper_metadata["paper_id"]

        for i, author_name in enumerate(authors):
            author_id = self._generate_author_id(author_name)
            query = """
            MATCH (a:Author {author_id: $author_id})
            MATCH (p:Paper {paper_id: $paper_id})
            MERGE (a)-[r:AUTHORED]->(p)
            ON CREATE SET
                r.order = $order,
                r.created_at = $created_at
            """
            tx.run(query, {
                "author_id": self._generate_author_id(author_name),
                "paper_id": paper_id,
                "order": i,
                "created_at": timestamp,
            })

    def _merge_entity_node(
        self,
        tx,
        entity,
        paper_metadata: Dict,
        timestamp: str,
        occurrence_count: int = 1,
        aliases: Optional[List[str]] = None,
    ) -> Tuple[str, bool]:
        """Create or merge an entity node. Returns (entity_id, is_new)."""
        entity_type = entity.entity_type
        label = get_node_label(entity_type)

        # Generate deterministic entity ID
        entity_id = self._generate_entity_id(entity.text, entity.entity_type)
        normalized = self._normalize_name(entity.text)

        query = f"""
        MERGE (e:{label} {{entity_id: $entity_id}})
        ON CREATE SET
            e.canonical_name = $canonical_name,
            e.normalized_name = $normalized_name,
            e.aliases = $aliases,
            e.first_seen = $first_seen,
            e.updated_at = $updated_at,
            e.occurrence_count = $occurrence_count,
            e.source_paper_ids = [$paper_id]
        ON MATCH SET
            e.canonical_name = CASE WHEN e.canonical_name IS NULL OR e.canonical_name = '' THEN $canonical_name ELSE e.canonical_name END,
            e.normalized_name = $normalized_name,
            e.aliases = reduce(
                acc = coalesce(e.aliases, []),
                alias IN $aliases |
                CASE WHEN alias IN acc THEN acc ELSE acc + alias END
            ),
            e.updated_at = $updated_at,
            e.occurrence_count = coalesce(e.occurrence_count, 0) +
                CASE WHEN $paper_id IN coalesce(e.source_paper_ids, [])
                     THEN 0 ELSE $occurrence_count END,
            e.source_paper_ids = CASE
                WHEN $paper_id IN coalesce(e.source_paper_ids, [])
                THEN coalesce(e.source_paper_ids, [])
                ELSE coalesce(e.source_paper_ids, []) + $paper_id
            END
        RETURN e.entity_id AS id, e.first_seen = $first_seen AS is_new
        """

        canonical_name = entity.text.strip()
        entity_aliases = list(aliases or [])
        if entity.text.strip() != entity.normalized_text:
            entity_aliases.append(entity.text.strip())

        result = tx.run(query, {
            "entity_id": self._generate_entity_id(entity.text, entity.entity_type),
            "canonical_name": canonical_name,
            "normalized_name": self._normalize_name(canonical_name),
            "aliases": list(dict.fromkeys(entity_aliases)),
            "paper_id": paper_metadata["paper_id"],
            "occurrence_count": occurrence_count,
            "first_seen": datetime.utcnow().isoformat(),
            "updated_at": timestamp,
        })

        record = result.single()
        is_new = record["is_new"] if record else True
        entity_id = self._generate_entity_id(entity.text, entity.entity_type)
        return entity_id, is_new

    def _generate_entity_id(self, text: str, entity_type: str) -> str:
        """Generate deterministic entity ID from text and type."""
        import hashlib
        key = f"{entity_type}:{text.strip().lower()}"
        return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]

    def _normalize_name(self, name: str) -> str:
        """Normalize name for matching."""
        if not isinstance(name, str):
            return ""
        return re.sub(r"\s+", " ", name.strip().lower())

    def _create_contains_relationship(
        self,
        tx,
        paper_id: int,
        entity_id: str,
        entity,
        occurrence_count: int = 1,
    ) -> None:
        """Create CONTAINS_ENTITY relationship between Paper and Entity."""
        entity_type = entity.entity_type

        query = """
        MATCH (p:Paper {paper_id: $paper_id})
        MATCH (e {entity_id: $entity_id})
        MERGE (p)-[r:CONTAINS_ENTITY]->(e)
        ON CREATE SET
            r.confidence = $confidence,
            r.extraction_method = $extraction_method,
            r.paper_id = $paper_id,
            r.page_number = $page_number,
            r.sentence_id = $sentence_id,
            r.start_char = $start_char,
            r.end_char = $end_char,
            r.evidence = $evidence,
            r.original_text = $original_text,
            r.cleaned_text = $cleaned_text,
            r.occurrence_count = $occurrence_count,
            r.created_at = $created_at
        ON MATCH SET
            r.confidence = CASE WHEN r.confidence < $confidence THEN $confidence ELSE r.confidence END,
            r.original_text = $original_text,
            r.cleaned_text = $cleaned_text,
            r.occurrence_count = $occurrence_count,
            r.updated_at = $created_at
        RETURN r.created_at = $created_at AS created
        """

        record = tx.run(query, {
            "paper_id": paper_id,
            "entity_id": entity_id,
            "confidence": entity.confidence,
            "extraction_method": entity.extraction_method,
            "page_number": entity.page_number,
            "sentence_id": entity.sentence_index,
            "start_char": entity.start_char,
            "end_char": entity.end_char,
            "evidence": entity.source_text,
            "original_text": entity.original_text or entity.source_text,
            "cleaned_text": entity.cleaned_text or entity.source_text,
            "occurrence_count": occurrence_count,
            "created_at": datetime.utcnow().isoformat(),
        }).single()
        if record and record["created"]:
            self.stats.relationships_created += 1
        else:
            self.stats.relationships_merged += 1

    def _merge_relationship(self, tx, rel_data: Dict, paper_metadata: Dict, timestamp: str) -> None:
        """Merge a relationship between two entities."""
        relation = rel_data.get("relation")
        if not relation:
            return

        subject_text = rel_data.get("subject", {}).get("text", "")
        object_text = rel_data.get("object", {}).get("text", "")
        subject_type = rel_data.get("subject", {}).get("label", "")
        object_type = rel_data.get("object", {}).get("label", "")

        if not all([subject_text, object_text, subject_type, object_type]):
            self.stats.warnings.append(f"Incomplete relation data: {rel_data}")
            return

        # Validate relationship
        subject_label = get_node_label(subject_type)
        object_label = get_node_label(object_type)
        if not validate_relationship(relation, subject_label, object_label):
            self.stats.warnings.append(f"Invalid relation: {relation} {subject_label} -> {object_label}")
            return

        query = f"""
        MATCH (s:{subject_label} {{entity_id: $subject_id}})
        MATCH (o:{object_label} {{entity_id: $object_id}})
        // Evidence identity makes repeated ingestion idempotent while keeping
        // independent provenance from different papers/sentences intact.
        MERGE (s)-[r:{relation} {{
            paper_id: $paper_id,
            sentence_id: $sentence_id,
            page_number: $page_number,
            start_char: $start_char,
            end_char: $end_char
        }}]->(o)
        ON CREATE SET
            r.confidence = $confidence,
            r.evidence = $evidence,
            r.extraction_method = $extraction_method,
            r.original_text = $original_text,
            r.cleaned_text = $cleaned_text,
            r.created_at = $created_at
        ON MATCH SET
            r.confidence = CASE WHEN r.confidence < $confidence THEN $confidence ELSE r.confidence END,
            r.evidence = CASE
                WHEN r.evidence IS NULL OR r.evidence = '' THEN $evidence
                ELSE r.evidence
            END,
            r.start_char = $start_char,
            r.end_char = $end_char,
            r.original_text = $original_text,
            r.cleaned_text = $cleaned_text,
            r.updated_at = $created_at
        RETURN r.created_at = $created_at AS created
        """

        record = tx.run(query, {
            "subject_id": self._generate_entity_id(rel_data["subject"]["text"], rel_data["subject"]["label"]),
            "object_id": self._generate_entity_id(rel_data["object"]["text"], rel_data["object"]["label"]),
            "confidence": rel_data.get("confidence", 0.5),
            "evidence": rel_data.get("evidence", ""),
            "paper_id": paper_metadata["paper_id"],
            "page_number": rel_data.get("page_number", 0),
            "sentence_id": rel_data.get("sentence_id", 0),
            "start_char": rel_data.get(
                "start_char",
                min(
                    rel_data.get("subject", {}).get("start", 0),
                    rel_data.get("object", {}).get("start", 0),
                ),
            ),
            "end_char": rel_data.get(
                "end_char",
                max(
                    rel_data.get("subject", {}).get("end", 0),
                    rel_data.get("object", {}).get("end", 0),
                ),
            ),
            "extraction_method": rel_data.get("extraction_method", "rule_based"),
            "original_text": rel_data.get("original_text", rel_data.get("evidence", "")),
            "cleaned_text": rel_data.get("cleaned_text", rel_data.get("evidence", "")),
            "created_at": datetime.utcnow().isoformat(),
        }).single()
        if record and record["created"]:
            self.stats.relationships_created += 1
        else:
            self.stats.relationships_merged += 1


# Convenience function
def build_graph_for_paper(
    paper_metadata: Dict[str, Any],
    entities: List,
    relations: List[Dict],
    entity_resolver: Optional[EntityResolutionService] = None
) -> Dict[str, Any]:
    """Convenience function to build graph for a paper."""
    service = GraphConstructionService(entity_resolver)
    return service.build_graph_for_paper(paper_metadata, entities, relations)
