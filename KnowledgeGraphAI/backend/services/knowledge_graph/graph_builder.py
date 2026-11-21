import logging
from KnowledgeGraphAI.backend.services.knowledge_graph.neo4j_connection import neo4j_manager

logger = logging.getLogger(__name__)

class GraphBuilder:
    """Compatibility façade for legacy callers.

    New ingestion goes through ``GraphConstructionService``.  This helper uses
    the same ``Paper.paper_id`` identity so old callers cannot create a second
    class of Paper nodes keyed by ``id``.
    """

    @staticmethod
    def create_paper_node(paper_id: int, title: str, author: str, file_hash: str):
        if not neo4j_manager.is_available():
            logger.warning("Neo4j is not available. Cannot create paper node in graph.")
            return False

        query = """
        MERGE (p:Paper {paper_id: $paper_id})
        ON CREATE SET p.title = $title, p.author = $author, p.file_hash = $file_hash
        ON MATCH SET p.title = $title, p.author = $author, p.file_hash = $file_hash
        """
        try:
            neo4j_manager.execute_write(
                query,
                {
                    "paper_id": paper_id,
                    "title": title,
                    "author": author,
                    "file_hash": file_hash,
                },
            )
            return True
        except Exception as e:
            logger.error(f"Failed to create paper node in Neo4j: {e}")
            return False
