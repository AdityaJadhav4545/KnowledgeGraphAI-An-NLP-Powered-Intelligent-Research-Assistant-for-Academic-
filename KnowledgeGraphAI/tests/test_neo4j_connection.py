import threading
from unittest.mock import Mock

from KnowledgeGraphAI.backend.services.knowledge_graph import neo4j_connection
from KnowledgeGraphAI.backend.services.knowledge_graph.neo4j_connection import (
    Neo4jConnectionManager,
)


def test_connection_refuses_default_password(monkeypatch, caplog):
    manager = object.__new__(Neo4jConnectionManager)
    manager.password = None
    driver = Mock()
    monkeypatch.setattr(
        "KnowledgeGraphAI.backend.services.knowledge_graph.neo4j_connection.GraphDatabase.driver",
        driver,
    )

    assert manager.connect() is False
    driver.assert_not_called()
    assert "NEO4J_PASSWORD is not configured" in caplog.text


def test_manager_loads_dotenv_before_reading_neo4j_credentials(monkeypatch):
    monkeypatch.setattr(Neo4jConnectionManager, "_instance", None)
    monkeypatch.delenv("NEO4J_PASSWORD", raising=False)

    def load_test_environment():
        monkeypatch.setenv("NEO4J_PASSWORD", "configured-by-dotenv")

    monkeypatch.setattr(neo4j_connection, "load_environment", load_test_environment)

    manager = Neo4jConnectionManager()

    assert manager.password == "configured-by-dotenv"


def test_connection_uses_configured_credentials(monkeypatch):
    manager = object.__new__(Neo4jConnectionManager)
    manager.uri = "bolt://localhost:7687"
    manager.username = "neo4j"
    manager.password = "configured-test-password"
    manager.database = "neo4j"
    manager.max_connection_pool_size = 50
    manager.max_connection_lifetime = 3600
    manager.connection_acquisition_timeout = 60
    manager._driver = None
    manager._driver_lock = threading.Lock()

    session = Mock()
    session.run.return_value.single.return_value = {"test": 1}
    session_context = Mock()
    session_context.__enter__ = Mock(return_value=session)
    session_context.__exit__ = Mock(return_value=False)
    driver = Mock()
    driver.session.return_value = session_context
    monkeypatch.setattr(neo4j_connection.GraphDatabase, "driver", Mock(return_value=driver))

    assert manager.connect() is True
    neo4j_connection.GraphDatabase.driver.assert_called_once_with(
        "bolt://localhost:7687",
        auth=("neo4j", "configured-test-password"),
        max_connection_pool_size=50,
        max_connection_lifetime=3600,
        connection_acquisition_timeout=60,
    )


def test_health_check_uses_neo4j_community_graph_counts(monkeypatch):
    manager = Neo4jConnectionManager.__new__(Neo4jConnectionManager)
    manager.database = "neo4j"
    manager.uri = "bolt://localhost:7687"
    monkeypatch.setattr(manager, "is_available", lambda: True)

    session = Mock()
    session.run.side_effect = [
        [{"versions": ["5.26.32"], "edition": "community"}],
        [{"node_count": 5, "relationship_count": 7}],
        [],
        [],
    ]
    session_context = Mock()
    session_context.__enter__ = Mock(return_value=session)
    session_context.__exit__ = Mock(return_value=False)
    monkeypatch.setattr(manager, "session", lambda: session_context)

    health = manager.health_check()

    assert health["status"] == "healthy"
    assert health["details"]["neo4j_version"] == "5.26.32"
    assert health["details"]["node_count"] == 5
    assert health["details"]["relationship_count"] == 7
    stats_query = session.run.call_args_list[1].args[0]
    assert "CALL () {" in stats_query
    assert "MATCH ()-[r]->()" in stats_query
