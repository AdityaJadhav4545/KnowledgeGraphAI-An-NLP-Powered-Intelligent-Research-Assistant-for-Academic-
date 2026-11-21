import logging
from collections.abc import Mapping
from typing import Dict, List, Optional, Any, Iterable
from dataclasses import dataclass

from KnowledgeGraphAI.backend.services.knowledge_graph.neo4j_connection import get_neo4j_manager
from KnowledgeGraphAI.backend.services.knowledge_graph.graph_schema import (
    ENTITY_TYPE_TO_LABEL,
    NODE_LABELS,
    RELATIONSHIP_TYPES,
)

logger = logging.getLogger(__name__)


@dataclass
class QueryResult:
    """Standardized query result."""
    data: List[Dict]
    count: int
    query_time_ms: float


class GraphQueryService:
    """
    Service for querying the knowledge graph.

    Provides high-level query methods for common research tasks:
    - Find entities associated with a paper
    - Find papers associated with an entity
    - Find models evaluated on a dataset
    - Find algorithms used by a model
    - Find models associated with a task
    - Find models compared with a model
    - Find methods that outperform another method
    - Find metrics achieved by a model
    - Retrieve neighborhood around an entity
    - Find paths connecting two entities
    - Find most connected entities
    """

    MAX_QUERY_LIMIT = 1000
    MAX_PATH_DEPTH = 10

    def __init__(self):
        self.neo4j = get_neo4j_manager()

    @classmethod
    def _validate_limit(cls, limit: int) -> int:
        if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= cls.MAX_QUERY_LIMIT:
            raise ValueError(f"limit must be an integer between 1 and {cls.MAX_QUERY_LIMIT}")
        return limit

    @classmethod
    def _validate_depth(cls, max_depth: int) -> int:
        if (
            isinstance(max_depth, bool)
            or not isinstance(max_depth, int)
            or not 1 <= max_depth <= cls.MAX_PATH_DEPTH
        ):
            raise ValueError(
                f"max_depth must be an integer between 1 and {cls.MAX_PATH_DEPTH}"
            )
        return max_depth

    @staticmethod
    def _entity_label(entity_type: str) -> str:
        if entity_type in NODE_LABELS:
            return entity_type
        label = ENTITY_TYPE_TO_LABEL.get(
            entity_type.upper(),
            next(
                (known for known in NODE_LABELS if known.lower() == entity_type.lower()),
                entity_type,
            ),
        )
        if label not in NODE_LABELS:
            raise ValueError(f"Unsupported entity type: {entity_type}")
        return label

    @staticmethod
    def _properties(value: Any) -> Dict[str, Any]:
        if isinstance(value, Mapping):
            return dict(value.items())
        items = getattr(value, "items", None)
        if callable(items):
            try:
                return dict(items())
            except (TypeError, ValueError):
                return {}
        return {}

    @classmethod
    def _flatten_entity_rows(
        cls,
        records: Optional[Iterable[Dict[str, Any]]],
        node_aliases: List[str],
        rename: Optional[Dict[str, str]] = None,
    ) -> List[Dict[str, Any]]:
        """Flatten node-valued records while retaining relationship fields."""
        flattened = []
        aliases = set(node_aliases)
        rename = rename or {}
        for record in records or []:
            if not isinstance(record, Mapping):
                continue
            row = dict(record.items())
            node_properties: Dict[str, Any] = {}
            for alias in node_aliases:
                if alias in row:
                    node_properties = cls._properties(row[alias])
                    if node_properties:
                        break

            result = dict(node_properties)
            for key, value in row.items():
                if key in aliases:
                    continue
                result[rename.get(key, key)] = value
            if result:
                flattened.append(result)
        return flattened

    def _execute_query(self, query: str, params: Dict = None) -> list:
        """Execute a read query and return results."""
        try:
            return self.neo4j.execute_query(query, params)
        except Exception as e:
            logger.error(f"Query failed: {e}")
            raise

    # ---------------------------------------------------------------------------
    # Paper-centric queries
    # ---------------------------------------------------------------------------
    def get_paper_entities(self, paper_id: int, entity_types: List[str] = None) -> List[Dict]:
        """Get all entities associated with a paper."""
        params = {"paper_id": paper_id}
        types_filter = ""
        if entity_types:
            labels = [self._entity_label(entity_type) for entity_type in entity_types]
            types_filter = "WHERE any(label IN labels(e) WHERE label IN $entity_types)"
            params["entity_types"] = labels

        query = f"""
        MATCH (p:Paper {{paper_id: $paper_id}})-[r:CONTAINS_ENTITY]->(e)
        {types_filter}
        RETURN e, labels(e) AS labels, r.confidence AS confidence, r.evidence AS evidence,
               r.page_number AS page_number, r.sentence_id AS sentence_id,
               r.paper_id AS paper_id, r.start_char AS start_char,
               r.end_char AS end_char, r.original_text AS original_text,
               r.cleaned_text AS cleaned_text, r.extraction_method AS method
        ORDER BY e.canonical_name
        """
        return self._execute_query(query, params)

    def get_paper_relationships(self, paper_id: int) -> List[Dict]:
        """Get all relationships extracted from a paper."""
        query = """
        MATCH (p:Paper {paper_id: $paper_id})-[:CONTAINS_ENTITY]->(subject)
        MATCH (subject)-[rel]->(object)
        WHERE rel.paper_id = $paper_id
        RETURN subject.canonical_name AS subject, labels(subject) AS subject_type,
               type(rel) AS relation, type(rel) AS relationship_type,
               object.canonical_name AS object, labels(object) AS object_type,
               rel.paper_id AS paper_id, rel.confidence AS confidence,
               rel.evidence AS evidence, rel.page_number AS page_number,
               rel.sentence_id AS sentence_id, rel.start_char AS start_char,
               rel.end_char AS end_char, rel.original_text AS original_text,
               rel.cleaned_text AS cleaned_text
        ORDER BY rel.page_number, rel.sentence_id
        """
        return self._execute_query(query, {"paper_id": paper_id})

    # ---------------------------------------------------------------------------
    # Entity-centric queries
    # ---------------------------------------------------------------------------
    def get_papers_for_entity(self, entity_id: str, entity_type: str, limit: int = 50) -> List[Dict]:
        """Get all papers associated with an entity."""
        label = self._entity_label(entity_type)
        limit = self._validate_limit(limit)
        query = f"""
        MATCH (e:{label} {{entity_id: $entity_id}})<-[r:CONTAINS_ENTITY]-(p:Paper)
        RETURN p.paper_id, p.title, p.author, p.created_at, r.confidence, r.evidence
        ORDER BY p.created_at DESC
        LIMIT $limit
        """
        return self._execute_query(query, {"entity_id": entity_id, "limit": limit})

    def get_entity_details(self, entity_id: str, entity_type: str) -> Optional[Dict]:
        """Get full details of an entity."""
        label = self._entity_label(entity_type)
        query = f"""
        MATCH (e:{label} {{entity_id: $entity_id}})
        RETURN e AS e
        """
        results = self._execute_query(query, {"entity_id": entity_id})
        return results[0] if results else None

    # ---------------------------------------------------------------------------
    # Specific research queries
    # ---------------------------------------------------------------------------

    def find_models_for_dataset(self, dataset_id: str, limit: int = 50) -> List[Dict]:
        """Find all models evaluated on a particular dataset."""
        limit = self._validate_limit(limit)
        query = """
        MATCH (m:Model)-[r:EVALUATED_ON]->(d:Dataset {entity_id: $dataset_id})
        RETURN m AS m, labels(m)[0] AS type, r.confidence AS confidence,
               r.evidence AS evidence, r.paper_id AS paper_id
        ORDER BY r.confidence DESC
        LIMIT $limit
        """
        return self._flatten_entity_rows(
            self._execute_query(query, {"dataset_id": dataset_id, "limit": limit}), ["m"]
        )

    def find_algorithms_for_model(self, model_id: str, limit: int = 50) -> List[Dict]:
        """Find algorithms used by a model."""
        limit = self._validate_limit(limit)
        query = """
        MATCH (m:Model {entity_id: $model_id})-[r:USES]->(a:Algorithm)
        RETURN a AS a, labels(a)[0] AS type, r.confidence AS confidence,
               r.evidence AS evidence
        ORDER BY r.confidence DESC
        LIMIT $limit
        """
        return self._flatten_entity_rows(
            self._execute_query(query, {"model_id": model_id, "limit": limit}), ["a"]
        )

    def find_models_for_task(self, task_id: str, limit: int = 50) -> List[Dict]:
        """Find models associated with a task (proposed for the task)."""
        limit = self._validate_limit(limit)
        query = """
        MATCH (m:Model)-[r:PROPOSES]->(t:Task {entity_id: $task_id})
        RETURN m AS m, labels(m)[0] AS type, r.confidence AS confidence,
               r.evidence AS evidence, r.paper_id AS paper_id
        ORDER BY r.confidence DESC
        LIMIT $limit
        """
        return self._flatten_entity_rows(
            self._execute_query(query, {"task_id": task_id, "limit": limit}), ["m"]
        )

    def find_models_compared_with(self, model_id: str, limit: int = 50) -> List[Dict]:
        """Find models compared with the given model."""
        limit = self._validate_limit(limit)
        query = """
        MATCH (m:Model {entity_id: $model_id})-[r:COMPARED_WITH]-(other:Model)
        RETURN other AS other, labels(other)[0] AS type, r.confidence AS confidence,
               r.evidence AS evidence, r.paper_id AS paper_id
        ORDER BY r.confidence DESC
        LIMIT $limit
        """
        return self._flatten_entity_rows(
            self._execute_query(query, {"model_id": model_id, "limit": limit}), ["other"]
        )

    def find_methods_outperforming(self, model_id: str, limit: int = 50) -> List[Dict]:
        """Find methods/models that outperform the given model."""
        limit = self._validate_limit(limit)
        query = """
        MATCH (better:Model)-[r:OUTPERFORMS]->(m:Model {entity_id: $model_id})
        RETURN better AS better, labels(better)[0] AS type, r.confidence AS confidence,
               r.evidence AS evidence, r.paper_id AS paper_id
        ORDER BY r.confidence DESC
        LIMIT $limit
        """
        return self._flatten_entity_rows(
            self._execute_query(query, {"model_id": model_id, "limit": limit}), ["better"]
        )

    def find_methods_improving_metric(self, metric_id: str, limit: int = 50) -> List[Dict]:
        """Find methods that improve a particular metric."""
        limit = self._validate_limit(limit)
        query = """
        MATCH (m:Model)-[r:IMPROVES]->(met:Metric {entity_id: $metric_id})
        RETURN m AS m, labels(m)[0] AS type, r.confidence AS confidence,
               r.evidence AS evidence, r.paper_id AS paper_id
        ORDER BY r.confidence DESC
        LIMIT $limit
        """
        return self._flatten_entity_rows(
            self._execute_query(query, {"metric_id": metric_id, "limit": limit}), ["m"]
        )

    def find_models_by_task(self, task_name: str, limit: int = 50) -> List[Dict]:
        """Find models associated with a task (by name)."""
        limit = self._validate_limit(limit)
        query = """
        MATCH (m:Model)-[r:PROPOSES]->(t:Task)
        WHERE t.canonical_name CONTAINS $task_name
        RETURN m AS m, labels(m)[0] AS type, r.confidence AS confidence,
               r.evidence AS evidence, r.paper_id AS paper_id,
               t.canonical_name AS task_name
        ORDER BY r.confidence DESC
        LIMIT $limit
        """
        return self._flatten_entity_rows(
            self._execute_query(query, {"task_name": task_name, "limit": limit}),
            ["m"],
            {"task": "task_name"},
        )

    def find_metrics_for_model(self, model_id: str, limit: int = 50) -> List[Dict]:
        """Find metrics achieved by a model."""
        limit = self._validate_limit(limit)
        query = """
        MATCH (m:Model {entity_id: $model_id})-[r:ACHIEVES]->(met:Metric)
        RETURN met AS met, labels(met)[0] AS type, r.confidence AS confidence,
               r.evidence AS evidence, r.paper_id AS paper_id
        ORDER BY r.confidence DESC
        LIMIT $limit
        """
        return self._flatten_entity_rows(
            self._execute_query(query, {"model_id": model_id, "limit": limit}), ["met"]
        )

    def find_relationships_supported_by_multiple_papers(
        self, relation_type: str = None, min_papers: int = 2
    ) -> List[Dict]:
        """Find relationships supported by multiple papers."""
        if isinstance(min_papers, bool) or not isinstance(min_papers, int) or min_papers < 1:
            raise ValueError("min_papers must be a positive integer")
        rel_filter = ""
        if relation_type:
            if relation_type not in RELATIONSHIP_TYPES:
                raise ValueError(f"Unsupported relationship type: {relation_type}")
            rel_filter = "WHERE type(r) = $relation_type"

        query = f"""
        MATCH (s)-[r]->(o)
        {rel_filter}
        WITH s, o, type(r) AS rel_type, collect(DISTINCT r.paper_id) AS papers,
             avg(r.confidence) AS avg_confidence, count(DISTINCT r.paper_id) AS paper_count
        WHERE paper_count >= $min_papers
        RETURN s AS s, labels(s)[0] AS subject_type,
               o AS o, labels(o)[0] AS object_type,
               rel_type AS relationship_type, avg_confidence AS confidence,
               paper_count AS supporting_paper_count, papers
        ORDER BY paper_count DESC, avg_confidence DESC
        """
        params = {"min_papers": min_papers}
        if relation_type:
            params["relation_type"] = relation_type
        records = self._execute_query(query, params)
        relationships = []
        for record in records or []:
            if not isinstance(record, Mapping):
                continue
            row = dict(record.items())
            subject_props = self._properties(row.get("s"))
            object_props = self._properties(row.get("o"))
            subject = subject_props.get("canonical_name", row.get("subject"))
            object_ = object_props.get("canonical_name", row.get("object"))
            relation_type = row.get(
                "relationship_type", row.get("rel_type", row.get("relation"))
            )
            confidence = row.get("confidence", row.get("avg_confidence"))
            paper_count = row.get(
                "supporting_paper_count", row.get("paper_count")
            )
            if subject is None or object_ is None or relation_type is None:
                continue
            relationships.append({
                "subject": subject,
                "subject_type": row.get("subject_type"),
                "object": object_,
                "object_type": row.get("object_type"),
                "relationship_type": relation_type,
                "confidence": confidence,
                "supporting_paper_count": paper_count,
                "papers": row.get("papers", []),
                # Legacy keys retained for existing API consumers.
                "relation": relation_type,
                "avg_confidence": confidence,
                "paper_count": paper_count,
            })
        return relationships

    # ---------------------------------------------------------------------------
    # Graph traversal queries
    # ---------------------------------------------------------------------------

    def get_entity_neighborhood(
        self, entity_id: str, entity_type: str, depth: int = 1, limit: int = 100
    ) -> Dict[str, Any]:
        """Get the neighborhood around an entity up to specified depth."""
        label = self._entity_label(entity_type)
        depth = self._validate_depth(depth)
        limit = self._validate_limit(limit)
        query = f"""
        MATCH (e:{label} {{entity_id: $entity_id}})
        OPTIONAL MATCH path = (e)-[*1..{depth}]-(neighbor)
        WHERE length(path) <= $depth
        WITH e, collect(DISTINCT neighbor)[0..$limit] AS neighbors,
             collect(DISTINCT [
                 rel IN relationships(path) |
                 {{
                     type: type(rel),
                     start_entity_id: startNode(rel).entity_id,
                     end_entity_id: endNode(rel).entity_id,
                     properties: properties(rel)
                 }}
             ]) AS paths
        WITH e, neighbors, reduce(all_rels = [], path_rels IN paths |
             reduce(acc = all_rels, rel IN path_rels |
                 CASE WHEN rel IN acc THEN acc ELSE acc + rel END)) AS rels
        RETURN [e] + neighbors AS nodes, rels AS relationships
        """
        results = self._execute_query(query, {"entity_id": entity_id, "depth": depth, "limit": limit})
        if results:
            return results[0]
        return {"nodes": [], "relationships": []}

    def get_entity_neighbors(
        self, entity_id: str, entity_type: str, relationship_types: List[str] = None, limit: int = 50
    ) -> List[Dict]:
        """Get direct neighbors of an entity."""
        label = self._entity_label(entity_type)
        limit = self._validate_limit(limit)
        rel_filter = ""
        if relationship_types:
            invalid_types = set(relationship_types).difference(RELATIONSHIP_TYPES)
            if invalid_types:
                raise ValueError(f"Unsupported relationship types: {sorted(invalid_types)}")
            rel_types = "|".join(relationship_types)
            rel_filter = f":{rel_types}"

        query = f"""
        MATCH (e:{label} {{entity_id: $entity_id}})-[r{rel_filter}]-(neighbor)
        RETURN neighbor, labels(neighbor) AS labels, type(r) AS relation,
               r.confidence AS confidence, r.evidence AS evidence
        LIMIT $limit
        """
        return self._execute_query(query, {"entity_id": entity_id, "limit": limit})

    def find_path_between_entities(
        self,
        source_id: str,
        target_id_or_source_type: Optional[str] = None,
        target_id: Optional[str] = None,
        target_type: Optional[str] = None,
        max_depth: int = 4,
        *,
        source_type: Optional[str] = None,
    ) -> List[Dict]:
        """Find a shortest path using two IDs or explicit source/target types.

        Use ``(source_id, target_id, max_depth=...)`` for the compact form, or
        ``(source_id, source_type, target_id, target_type, max_depth)`` when
        label-constrained matching is required.
        """
        if source_type is not None:
            if target_id is None:
                raise TypeError("target_id is required when source_type is specified")
        elif isinstance(target_id, int) and not isinstance(target_id, bool) and target_type is None:
            max_depth = target_id
            target_id = target_id_or_source_type
        elif target_id is None:
            target_id = target_id_or_source_type
        else:
            source_type = target_id_or_source_type

        if target_id is None:
            raise TypeError("target_id is required")

        max_depth = self._validate_depth(max_depth)
        source_label = f":{self._entity_label(source_type)}" if source_type else ""
        target_label = f":{self._entity_label(target_type)}" if target_type else ""
        query = """
        MATCH (source{source_label} {{entity_id: $source_id}})
        MATCH (target{target_label} {{entity_id: $target_id}})
        MATCH path = shortestPath((source)-[*0..10]-(target))
        WHERE length(path) <= $max_depth
        RETURN path
        LIMIT $limit
        """
        query = query.format(source_label=source_label, target_label=target_label)
        return self._execute_query(query, {
            "source_id": source_id,
            "target_id": target_id,
            "max_depth": max_depth,
            "limit": 10,
        })

    def find_most_connected_entities(
        self, entity_type: str = None, limit: int = 20
    ) -> List[Dict]:
        """Find the most connected entities in the graph."""
        limit = self._validate_limit(limit)
        type_filter = f":{self._entity_label(entity_type)}" if entity_type else ""
        query = f"""
        MATCH (e{type_filter})-[r]-()
        WITH e, count(r) AS degree
        RETURN e AS e, labels(e)[0] AS type, degree
        ORDER BY degree DESC
        LIMIT $limit
        """
        rows = self._flatten_entity_rows(
            self._execute_query(query, {"limit": limit}), ["e"]
        )
        results = []
        for row in rows:
            name = row.get("canonical_name", row.get("name", row.get("entity")))
            if name is None:
                continue
            row["entity"] = name
            results.append(row)
        return results

    # ---------------------------------------------------------------------------
    # Search queries
    # ---------------------------------------------------------------------------

    def search_entities(
        self, query_text: str, entity_types: List[str] = None, limit: int = 20
    ) -> List[Dict]:
        """Search entities by name (text search)."""
        limit = self._validate_limit(limit)
        params = {"query_text": query_text, "limit": limit}
        type_filter = "WHERE"
        if entity_types:
            params["entity_types"] = [
                self._entity_label(entity_type) for entity_type in entity_types
            ]
            type_filter = (
                "WHERE any(label IN labels(e) WHERE label IN $entity_types) AND"
            )

        query = f"""
        MATCH (e)
        {type_filter}
           (toLower(e.canonical_name) CONTAINS toLower($query_text)
           OR any(alias IN coalesce(e.aliases, []) WHERE toLower(alias) CONTAINS toLower($query_text)))
        RETURN e AS e, labels(e)[0] AS type
        LIMIT $limit
        """
        return self._flatten_entity_rows(
            self._execute_query(query, params), ["e"]
        )

    def search_papers(self, query_text: str, limit: int = 20) -> List[Dict]:
        """Search papers by title or author."""
        limit = self._validate_limit(limit)
        query = """
        MATCH (p:Paper)
        WHERE toLower(p.title) CONTAINS toLower($query_text)
           OR toLower(p.author) CONTAINS toLower($query_text)
        RETURN p AS p
        ORDER BY p.created_at DESC
        LIMIT $limit
        """
        return self._flatten_entity_rows(
            self._execute_query(query, {"query_text": query_text, "limit": limit}), ["p"]
        )


# Convenience function
def get_graph_query_service() -> 'GraphQueryService':
    """Get a GraphQueryService instance."""
    return GraphQueryService()
