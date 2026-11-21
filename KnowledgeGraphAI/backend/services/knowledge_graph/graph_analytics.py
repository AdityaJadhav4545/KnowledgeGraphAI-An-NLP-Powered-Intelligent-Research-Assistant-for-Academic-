"""Graph analytics for KnowledgeGraphAI.

Provides basic analytics on the knowledge graph using Cypher queries.
Fallback to basic analytics if Neo4j Graph Data Science is unavailable.
"""

import logging
from typing import List, Dict, Any, Optional

from KnowledgeGraphAI.backend.services.knowledge_graph.neo4j_connection import get_neo4j_manager
from KnowledgeGraphAI.backend.services.knowledge_graph.graph_schema import NODE_LABELS

logger = logging.getLogger(__name__)


class GraphAnalytics:
    """Analytics for the knowledge graph using Cypher queries."""

    MAX_QUERY_LIMIT = 1000
    MAX_NEIGHBORHOOD_DEPTH = 10

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
            or not 1 <= max_depth <= cls.MAX_NEIGHBORHOOD_DEPTH
        ):
            raise ValueError(
                f"max_depth must be an integer between 1 and {cls.MAX_NEIGHBORHOOD_DEPTH}"
            )
        return max_depth

    def _execute_query(self, query: str, params: dict = None) -> Optional[List[Dict]]:
        """Execute a Cypher query and return results."""
        try:
            result = self.neo4j.execute_query(query, params)
            return result if result else []
        except Exception as e:
            logger.error(f"Analytics query failed: {e}")
            return None

    # ---------------------------------------------------------------------------
    # Basic statistics
    # ---------------------------------------------------------------------------

    def get_stats(self) -> Dict[str, Any]:
        """Get basic graph statistics."""
        # Count nodes
        nodes_query = (
            "MATCH (n) "
            "RETURN labels(n) AS labels, count(n) AS count "
            "ORDER BY labels(n)"
        )
        nodes_result = self._execute_query(nodes_query)
        nodes_summary = {}
        for record in nodes_result or []:
            labels = record.get("labels") or []
            label = labels[0] if labels else "Unknown"
            nodes_summary[label] = record["count"]

        # Count relationships
        rel_query = (
            "MATCH ()-[r]-() "
            "RETURN count(r) AS count, type(r) AS type "
            "ORDER BY count(r) DESC"
        )
        rel_result = self._execute_query(rel_query)
        rel_summary = {}
        for record in rel_result or []:
            rel_type = record["type"]
            count = record["count"]
            rel_summary[rel_type] = count

        return {
            "nodes": {k: v for k, v in nodes_summary.items()},
            "relationships": rel_summary,
            "total_nodes": sum(nodes_summary.values()),
            "total_relationships": sum(rel_summary.values()) if rel_summary else 0,
        }

    # ---------------------------------------------------------------------------
    # Per-category entity counts
    # ---------------------------------------------------------------------------
    def get_entity_counts_by_category(self) -> Dict[str, int]:
        """Count entities by category."""
        query = (
            "MATCH (n) "
            "UNWIND labels(n) AS label "
            "WITH label, count(*) AS count "
            "RETURN label, count "
            "ORDER BY count DESC"
        )
        results = self._execute_query(query)
        return {record["label"]: record["count"] for record in results or []}

    # ---------------------------------------------------------------------------
    # Most frequent entities
    # ---------------------------------------------------------------------------
    def get_most_frequent_models(self, limit: int = 20) -> List[Dict]:
        """Find the most frequently mentioned models."""
        limit = self._validate_limit(limit)
        query = (
            "MATCH (m:Model)-[r:USES]->(d:Dataset) "
            "RETURN m.canonical_name AS model, count(DISTINCT r.paper_id) AS mentions "
            "ORDER BY mentions DESC "
            "LIMIT $limit"
        )
        results = self._execute_query(query, {"limit": limit})
        return [{"model": r["model"], "mentions": r["mentions"]} for r in results]

    def get_most_frequent_datasets(self, limit: int = 20) -> List[Dict]:
        """Find the most frequently mentioned datasets."""
        limit = self._validate_limit(limit)
        query = (
            "MATCH (m:Model)-[r:EVALUATED_ON]->(d:Dataset) "
            "RETURN d.canonical_name AS dataset, count(DISTINCT r.paper_id) AS mentions "
            "ORDER BY mentions DESC "
            "LIMIT $limit"
        )
        results = self._execute_query(query, {"limit": limit})
        return [{"dataset": r["dataset"], "mentions": r["mentions"]} for r in results]

    # ---------------------------------------------------------------------------
    # Centrality and connectivity
    # ---------------------------------------------------------------------------
    def get_most_connected_entities(self, limit: int = 20) -> List[Dict]:
        """Find the most connected entities in the graph."""
        limit = self._validate_limit(limit)
        query = (
            "MATCH (e)-[r]-() "
            "WITH e, count(r) AS degree "
            "RETURN e.canonical_name AS name, labels(e)[0] AS type, e.entity_id, degree "
            "ORDER BY degree DESC "
            "LIMIT $limit"
        )
        results = self._execute_query(query, {"limit": limit})
        return [{"entity": r["name"], "type": r["type"], "entity_id": r["entity_id"], "degree": r["degree"]} for r in results]

    # ---------------------------------------------------------------------------
    # Papers with most entities
    # ---------------------------------------------------------------------------
    def get_papers_with_largest_entity_count(self, limit: int = 20) -> List[Dict]:
        """Find papers with the largest number of extracted entities."""
        limit = self._validate_limit(limit)
        query = """
        MATCH (p:Paper)-[r:CONTAINS_ENTITY]->(e)
        WITH p.paper_id, p.title, count(DISTINCT e) AS entity_count
        ORDER BY entity_count DESC
        LIMIT $limit
        """
        results = self._execute_query(query, {"limit": limit})
        return [{"paper_id": r["paper_id"], "title": r["title"], "entity_count": r["entity_count"]} for r in results]

    # ---------------------------------------------------------------------------
    # Relationship analytics
    # ---------------------------------------------------------------------------
    def get_relation_counts_by_type(self) -> Dict[str, int]:
        """Count relationships by type."""
        query = (
            "MATCH ()-[r]-() "
            "RETURN type(r) AS type, count(r) AS count "
            "ORDER BY count DESC"
        )
        results = self._execute_query(query)
        return {record["type"]: record["count"] for record in results}

    # ---------------------------------------------------------------------------
    # Find models compared with a selected model
    # ---------------------------------------------------------------------------
    def find_compared_models(self, model_id: str, limit: int = 20) -> List[Dict]:
        """Find models compared with the given model."""
        limit = self._validate_limit(limit)
        query = """
        MATCH (m:Model {entity_id: $model_id})-[r:COMPARED_WITH]->(other:Model)
        RETURN other.canonical_name, other.entity_id, r.confidence, r.paper_id
        ORDER BY r.confidence DESC
        LIMIT $limit
        """
        return self._execute_query(query, {"model_id": model_id, "limit": limit})

    # ---------------------------------------------------------------------------
    # Find models that outperform another model
    # ---------------------------------------------------------------------------
    def find_models_outperforming(self, model_id: str, limit: int = 20) -> List[Dict]:
        """Find models that outperform the given model."""
        limit = self._validate_limit(limit)
        query = """
        MATCH (better:Model)-[r:OUTPERFORMS]->(m:Model {entity_id: $model_id})
        RETURN better.canonical_name, better.entity_id, r.confidence, r.paper_id
        ORDER BY r.confidence DESC
        LIMIT $limit
        """
        return self._execute_query(query, {"model_id": model_id, "limit": limit})

    # ---------------------------------------------------------------------------
    # Find models that improve a metric
    # ---------------------------------------------------------------------------
    def find_models_improving_metric(self, metric_id: str, limit: int = 20) -> List[Dict]:
        """Find models that improve a metric."""
        limit = self._validate_limit(limit)
        query = (
            "MATCH (m:Model)-[r:IMPROVES]->(met:Metric {entity_id: $metric_id})"
            " RETURN m.canonical_name, m.entity_id, r.confidence, r.paper_id "
            "ORDER BY r.confidence DESC "
            "LIMIT $limit"
        )
        return self._execute_query(query, {"metric_id": metric_id, "limit": limit})

    # ---------------------------------------------------------------------------
    # Retrieve the neighborhood around a selected entity
    # ---------------------------------------------------------------------------
    def get_entity_neighborhood(
        self, entity_id: str, entity_type: str = None, max_depth: int = 1, limit: int = 100
    ) -> Dict[str, Any]:
        """Get the neighborhood around an entity up to a specified depth."""
        max_depth = self._validate_depth(max_depth)
        limit = self._validate_limit(limit)
        if entity_type is not None and entity_type not in NODE_LABELS:
            raise ValueError(f"Unsupported entity type: {entity_type}")
        type_filter = f":{entity_type}" if entity_type else ""

        query = (
            f"MATCH (e{type_filter} {{entity_id: $entity_id}})"
            f" OPTIONAL MATCH path = (e)-[*1..{max_depth}]-(neighbor)"
            " WHERE length(path) <= $max_depth"
            " WITH e, collect(DISTINCT neighbor)[0..$limit] AS neighbors,"
            "      collect(DISTINCT [rel IN relationships(path) |"
            "          {type: type(rel),"
            "           start_entity_id: startNode(rel).entity_id,"
            "           end_entity_id: endNode(rel).entity_id,"
            "           properties: properties(rel)}]) AS paths"
            " WITH e, neighbors, reduce(all_rels = [], path_rels IN paths |"
            "      reduce(acc = all_rels, rel IN path_rels |"
            "          CASE WHEN rel IN acc THEN acc ELSE acc + rel END)) AS rels"
            " RETURN [e] + neighbors AS nodes, rels AS relationships"
        )
        results = self._execute_query(
            query, {"entity_id": entity_id, "max_depth": max_depth, "limit": limit}
        )
        if results:
            return results[0]
        return {"nodes": [], "relationships": []}