import os
import time
import atexit
import logging
import threading
from typing import Optional, Dict, Any
from neo4j import GraphDatabase, Driver, Session, Transaction
from neo4j.exceptions import ServiceUnavailable, AuthError

from KnowledgeGraphAI.backend.config import load_environment

logger = logging.getLogger(__name__)


class Neo4jConnectionManager:
    """
    Enhanced Neo4j connection manager with lifecycle management,
    connection pooling, health checks, and graceful shutdown.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return

        load_environment()
        self._initialized = True
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.username = os.getenv("NEO4J_USERNAME", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD")
        self.database = os.getenv("NEO4J_DATABASE", "neo4j")

        # Connection pool settings
        self.max_connection_pool_size = int(os.getenv("NEO4J_MAX_POOL_SIZE", "50"))
        self.max_connection_lifetime = int(os.getenv("NEO4J_MAX_CONNECTION_LIFETIME", "3600"))  # seconds
        self.connection_acquisition_timeout = int(os.getenv("NEO4J_CONNECTION_ACQUISITION_TIMEOUT", "60"))  # seconds

        self._driver: Optional[Driver] = None
        self._driver_lock = threading.Lock()
        self._shutdown = False
        self._last_failure_time: float = 0.0
        self._retry_cooldown_seconds: float = float(os.getenv("NEO4J_RETRY_COOLDOWN_SECONDS", "5.0"))

        # Register shutdown handler
        atexit.register(self.close)

        logger.info(f"Neo4jConnectionManager initialized with URI: {self.uri}")

    def connect(self) -> bool:
        """Establish connection to Neo4j database."""
        if not self.password:
            logger.error(
                "NEO4J_PASSWORD is not configured; refusing to connect with a default credential."
            )
            return False

        with self._driver_lock:
            if self._driver is not None:
                try:
                    self._driver.verify_connectivity()
                    return True
                except Exception:
                    logger.warning("Existing driver connection lost, reconnecting...")
                    self._close_driver()

        try:
            logger.info(f"Connecting to Neo4j at {self.uri} as {self.username}")
            self._driver = GraphDatabase.driver(
                self.uri,
                auth=(self.username, self.password),
                max_connection_pool_size=self.max_connection_pool_size,
                max_connection_lifetime=self.max_connection_lifetime,
                connection_acquisition_timeout=self.connection_acquisition_timeout,
            )

            # Test connection
            self._driver.verify_connectivity()

            # Test database access
            with self._driver.session(database=self.database) as session:
                result = session.run("RETURN 1 AS test")
                record = result.single()
                if record and record["test"] == 1:
                    self._last_failure_time = 0.0
                    logger.info(f"Successfully connected to Neo4j database '{self.database}'")
                    return True

            logger.error("Connection test failed")
            self._last_failure_time = time.monotonic()
            return False

        except AuthError as e:
            logger.error(f"Neo4j authentication failed: {e}")
            self._close_driver()
            self._last_failure_time = time.monotonic()
            return False
        except ServiceUnavailable as e:
            logger.warning(f"Neo4j service unavailable: {e}. Graph features will be unavailable.")
            self._close_driver()
            self._last_failure_time = time.monotonic()
            return False
        except Exception as e:
            logger.error(f"Neo4j connection failed: {e}")
            self._close_driver()
            self._last_failure_time = time.monotonic()
            return False

    def _close_driver(self):
        """Internal method to close driver without lock."""
        if self._driver:
            try:
                self._driver.close()
            except Exception as e:
                logger.warning(f"Error closing Neo4j driver: {e}")
            finally:
                self._driver = None

    def close(self) -> None:
        """Close the Neo4j driver connection."""
        with self._driver_lock:
            if self._driver:
                try:
                    self._driver.close()
                    logger.info("Neo4j driver closed successfully")
                except Exception as e:
                    logger.warning(f"Error closing Neo4j driver: {e}")
                finally:
                    self._driver = None

    def is_available(self) -> bool:
        """Check if Neo4j connection is available."""
        if self._shutdown:
            return False

        with self._driver_lock:
            driver = self._driver

        if driver is None:
            cooldown = getattr(self, "_retry_cooldown_seconds", 5.0)
            last_fail = getattr(self, "_last_failure_time", 0.0)
            if last_fail and (time.monotonic() - last_fail) < cooldown:
                return False
            return self.connect()

        try:
            driver.verify_connectivity()
            return True
        except Exception as e:
            logger.warning(f"Neo4j connectivity check failed: {e}")
            with self._driver_lock:
                if self._driver is driver:
                    self._driver = None
            return False

    def get_driver(self) -> Optional[Driver]:
        """Get the Neo4j driver instance."""
        if self._driver is None:
            if not self.connect():
                return None
        return self._driver

    def session(self, **kwargs) -> Optional[Session]:
        """Create a new session."""
        driver = self.get_driver()
        if driver is None:
            return None
        return driver.session(database=self.database, **kwargs)

    def execute_query(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None,
        database: Optional[str] = None
    ) -> list:
        """Execute a read query and return results as list of records."""
        driver = self.get_driver()
        if driver is None:
            raise RuntimeError("Neo4j session unavailable")
        with driver.session(database=database or self.database) as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

    def execute_write(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None,
        database: Optional[str] = None
    ) -> Any:
        """Execute a write query in a transaction."""
        driver = self.get_driver()
        if driver is None:
            raise RuntimeError("Neo4j driver unavailable")

        def work(tx: Transaction) -> Any:
            result = tx.run(query, parameters or {})
            return result.consume()

        with driver.session(database=database or self.database) as session:
            return session.execute_write(work)

    def execute_transaction(
        self,
        work_func,
        *args,
        **kwargs
    ) -> Any:
        """Execute a custom transaction function."""
        driver = self.get_driver()
        if driver is None:
            raise RuntimeError("Neo4j driver unavailable")

        with driver.session(database=self.database) as session:
            return session.execute_write(work_func, *args, **kwargs)

    def health_check(self) -> Dict[str, Any]:
        """Perform a comprehensive health check."""
        health = {
            "status": "unhealthy",
            "connected": False,
            "database": self.database,
            "uri": self.uri,
            "details": {}
        }

        try:
            if self.is_available():
                health["connected"] = True
                health["status"] = "healthy"

                # Get database info
                with self.session() as session:
                    # Get Neo4j version
                    version_result = session.run("CALL dbms.components() YIELD name, versions, edition")
                    for record in version_result:
                        health["details"]["neo4j_version"] = record["versions"][0] if record["versions"] else "unknown"
                        health["details"]["edition"] = record["edition"]

                    # Get database stats
                    stats = session.run("""
                        CALL () {
                            MATCH (n)
                            RETURN count(n) AS node_count
                        }
                        CALL () {
                            MATCH ()-[r]->()
                            RETURN count(r) AS relationship_count
                        }
                        RETURN node_count, relationship_count
                    """)
                    for record in stats:
                        health["details"]["node_count"] = record["node_count"]
                        health["details"]["relationship_count"] = record["relationship_count"]

                    # Get indexes
                    index_result = session.run("SHOW INDEXES YIELD name, type, state, labelsOrTypes, properties")
                    health["details"]["index_count"] = sum(1 for _ in index_result)

                    # Get constraints
                    constraint_result = session.run("SHOW CONSTRAINTS YIELD name, type")
                    health["details"]["constraint_count"] = sum(1 for _ in constraint_result)

        except Exception as e:
            health["status"] = "unhealthy"
            health["error"] = str(e)
            logger.error(f"Health check failed: {e}")

        return health

    def shutdown(self) -> None:
        """Graceful shutdown."""
        self._shutdown = True
        self.close()


# Global instance
neo4j_manager = Neo4jConnectionManager()


def get_neo4j_manager() -> Neo4jConnectionManager:
    """Get the global Neo4j connection manager instance."""
    return neo4j_manager
