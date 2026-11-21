"""Graph schema definitions, constraints, and indexes for KnowledgeGraphAI."""

from typing import List, Dict, Any

# ---------------------------------------------------------------------------
# Node Labels
# ---------------------------------------------------------------------------
NODE_LABELS = [
    "Paper",
    "Author",
    "Algorithm",
    "Model",
    "Dataset",
    "Metric",
    "Task",
    "Methodology",
    "ResearchProblem",
    "Optimizer",
    "Framework",
    "Organization",
]

# ---------------------------------------------------------------------------
# Relationship Types
# ---------------------------------------------------------------------------
RELATIONSHIP_TYPES = [
    "AUTHORED",
    "CONTAINS_ENTITY",
    "PROPOSES",
    "USES",
    "EVALUATED_ON",
    "ACHIEVES",
    "COMPARED_WITH",
    "IMPROVES",
    "APPLIES_TO",
    "OUTPERFORMS",
    "BASED_ON",
    "HAS_EVIDENCE",  # For evidence nodes
]

# ---------------------------------------------------------------------------
# Node Property Definitions
# ---------------------------------------------------------------------------
NODE_PROPERTIES = {
    "Paper": {
        "paper_id": "INTEGER",
        "arxiv_id": "STRING",
        "title": "STRING",
        "author": "STRING",
        "file_path": "STRING",
        "file_hash": "STRING",
        "content_hash": "STRING",
        "page_count": "INTEGER",
        "status": "STRING",
        "created_at": "DATETIME",
        "updated_at": "DATETIME",
    },
    "Author": {
        "author_id": "STRING",
        "name": "STRING",
        "normalized_name": "STRING",
        "affiliation": "STRING",
        "created_at": "DATETIME",
        "updated_at": "DATETIME",
    },
    "Algorithm": {
        "entity_id": "STRING",
        "canonical_name": "STRING",
        "normalized_name": "STRING",
        "aliases": "LIST",
        "description": "STRING",
        "first_seen": "DATETIME",
        "updated_at": "DATETIME",
    },
    "Model": {
        "entity_id": "STRING",
        "canonical_name": "STRING",
        "normalized_name": "STRING",
        "aliases": "LIST",
        "architecture": "STRING",
        "parameters": "STRING",
        "first_seen": "DATETIME",
        "updated_at": "DATETIME",
    },
    "Dataset": {
        "entity_id": "STRING",
        "canonical_name": "STRING",
        "normalized_name": "STRING",
        "aliases": "LIST",
        "domain": "STRING",
        "size": "STRING",
        "first_seen": "DATETIME",
        "updated_at": "DATETIME",
    },
    "Metric": {
        "entity_id": "STRING",
        "canonical_name": "STRING",
        "normalized_name": "STRING",
        "aliases": "LIST",
        "type": "STRING",  # classification, regression, etc.
        "first_seen": "DATETIME",
        "updated_at": "DATETIME",
    },
    "Task": {
        "entity_id": "STRING",
        "canonical_name": "STRING",
        "normalized_name": "STRING",
        "aliases": "LIST",
        "domain": "STRING",  # NLP, CV, RL, etc.
        "first_seen": "DATETIME",
        "updated_at": "DATETIME",
    },
    "Methodology": {
        "entity_id": "STRING",
        "canonical_name": "STRING",
        "normalized_name": "STRING",
        "aliases": "LIST",
        "description": "STRING",
        "first_seen": "DATETIME",
        "updated_at": "DATETIME",
    },
    "ResearchProblem": {
        "entity_id": "STRING",
        "canonical_name": "STRING",
        "normalized_name": "STRING",
        "aliases": "LIST",
        "domain": "STRING",
        "first_seen": "DATETIME",
        "updated_at": "DATETIME",
    },
    "Optimizer": {
        "entity_id": "STRING",
        "canonical_name": "STRING",
        "normalized_name": "STRING",
        "aliases": "LIST",
        "type": "STRING",  # gradient-based, evolutionary, etc.
        "first_seen": "DATETIME",
        "updated_at": "DATETIME",
    },
    "Framework": {
        "entity_id": "STRING",
        "canonical_name": "STRING",
        "normalized_name": "STRING",
        "aliases": "LIST",
        "language": "STRING",  # Python, C++, etc.
        "first_seen": "DATETIME",
        "updated_at": "DATETIME",
    },
    "Organization": {
        "entity_id": "STRING",
        "canonical_name": "STRING",
        "normalized_name": "STRING",
        "aliases": "LIST",
        "type": "STRING",  # academic, industry, government
        "location": "STRING",
        "first_seen": "DATETIME",
        "updated_at": "DATETIME",
    },
    "Author": {
        "entity_id": "STRING",
        "canonical_name": "STRING",
        "normalized_name": "STRING",
        "aliases": "LIST",
        "affiliation": "STRING",
        "first_seen": "DATETIME",
        "updated_at": "DATETIME",
    },
}

# ---------------------------------------------------------------------------
# Relationship Property Definitions
# ---------------------------------------------------------------------------
RELATIONSHIP_PROPERTIES = {
    "CONTAINS_ENTITY": {
        "confidence": "FLOAT",
        "extraction_method": "STRING",
        "paper_id": "INTEGER",
        "page_number": "INTEGER",
        "sentence_id": "INTEGER",
        "start_char": "INTEGER",
        "end_char": "INTEGER",
        "evidence": "STRING",
        "original_text": "STRING",
        "cleaned_text": "STRING",
        "created_at": "DATETIME",
    },
    "AUTHORED": {
        "order": "INTEGER",
        "created_at": "DATETIME",
    },
    "PROPOSES": {
        "confidence": "FLOAT",
        "evidence": "STRING",
        "paper_id": "INTEGER",
        "page_number": "INTEGER",
        "sentence_id": "INTEGER",
        "extraction_method": "STRING",
        "created_at": "DATETIME",
    },
    "USES": {
        "confidence": "FLOAT",
        "evidence": "STRING",
        "paper_id": "INTEGER",
        "page_number": "INTEGER",
        "sentence_id": "INTEGER",
        "extraction_method": "STRING",
        "created_at": "DATETIME",
    },
    "EVALUATED_ON": {
        "confidence": "FLOAT",
        "evidence": "STRING",
        "paper_id": "INTEGER",
        "page_number": "INTEGER",
        "sentence_id": "INTEGER",
        "extraction_method": "STRING",
        "created_at": "DATETIME",
    },
    "ACHIEVES": {
        "confidence": "FLOAT",
        "evidence": "STRING",
        "paper_id": "INTEGER",
        "page_number": "INTEGER",
        "sentence_id": "INTEGER",
        "extraction_method": "STRING",
        "created_at": "DATETIME",
    },
    "COMPARED_WITH": {
        "confidence": "FLOAT",
        "evidence": "STRING",
        "paper_id": "INTEGER",
        "page_number": "INTEGER",
        "sentence_id": "INTEGER",
        "extraction_method": "STRING",
        "created_at": "DATETIME",
    },
    "IMPROVES": {
        "confidence": "FLOAT",
        "evidence": "STRING",
        "paper_id": "INTEGER",
        "page_number": "INTEGER",
        "sentence_id": "INTEGER",
        "extraction_method": "STRING",
        "created_at": "DATETIME",
    },
    "APPLIES_TO": {
        "confidence": "FLOAT",
        "evidence": "STRING",
        "paper_id": "INTEGER",
        "page_number": "INTEGER",
        "sentence_id": "INTEGER",
        "extraction_method": "STRING",
        "created_at": "DATETIME",
    },
    "OUTPERFORMS": {
        "confidence": "FLOAT",
        "evidence": "STRING",
        "paper_id": "INTEGER",
        "page_number": "INTEGER",
        "sentence_id": "INTEGER",
        "extraction_method": "STRING",
        "created_at": "DATETIME",
    },
    "BASED_ON": {
        "confidence": "FLOAT",
        "evidence": "STRING",
        "paper_id": "INTEGER",
        "page_number": "INTEGER",
        "sentence_id": "INTEGER",
        "extraction_method": "STRING",
        "created_at": "DATETIME",
    },
    "HAS_EVIDENCE": {
        "confidence": "FLOAT",
        "evidence": "STRING",
        "paper_id": "INTEGER",
        "page_number": "INTEGER",
        "sentence_id": "INTEGER",
        "extraction_method": "STRING",
        "created_at": "DATETIME",
    },
}

# ---------------------------------------------------------------------------
# Relationship Direction Mapping (subject -> object)
# ---------------------------------------------------------------------------
RELATIONSHIP_DIRECTIONS = {
    "AUTHORED": ("Author", "Paper"),
    "CONTAINS_ENTITY": ("Paper", "Entity"),  # Entity can be any entity type
    "PROPOSES": ("Model", "Task"),
    "USES": ("Model", "Dataset"),
    "EVALUATED_ON": ("Model", "Dataset"),
    "ACHIEVES": ("Model", "Metric"),
    "COMPARED_WITH": ("Model", "Model"),
    "IMPROVES": ("Model", "Metric"),
    "APPLIES_TO": ("Methodology", "Task"),
    "OUTPERFORMS": ("Model", "Model"),
    "BASED_ON": ("Model", "Methodology"),
}

# ---------------------------------------------------------------------------
# Cypher Statements for Constraints and Indexes
# ---------------------------------------------------------------------------

CONSTRAINT_STATEMENTS = [
    # Paper constraints
    "CREATE CONSTRAINT paper_id_unique IF NOT EXISTS FOR (p:Paper) REQUIRE p.paper_id IS UNIQUE",
    "CREATE CONSTRAINT paper_file_hash_unique IF NOT EXISTS FOR (p:Paper) REQUIRE p.file_hash IS UNIQUE",
    "CREATE CONSTRAINT paper_content_hash_unique IF NOT EXISTS FOR (p:Paper) REQUIRE p.content_hash IS UNIQUE",

    # Author constraints
    "CREATE CONSTRAINT author_id_unique IF NOT EXISTS FOR (a:Author) REQUIRE a.author_id IS UNIQUE",

    # Entity constraints (using entity_id as unique identifier)
    "CREATE CONSTRAINT algorithm_id_unique IF NOT EXISTS FOR (a:Algorithm) REQUIRE a.entity_id IS UNIQUE",
    "CREATE CONSTRAINT model_id_unique IF NOT EXISTS FOR (m:Model) REQUIRE m.entity_id IS UNIQUE",
    "CREATE CONSTRAINT dataset_id_unique IF NOT EXISTS FOR (d:Dataset) REQUIRE d.entity_id IS UNIQUE",
    "CREATE CONSTRAINT metric_id_unique IF NOT EXISTS FOR (m:Metric) REQUIRE m.entity_id IS UNIQUE",
    "CREATE CONSTRAINT task_id_unique IF NOT EXISTS FOR (t:Task) REQUIRE t.entity_id IS UNIQUE",
    "CREATE CONSTRAINT methodology_id_unique IF NOT EXISTS FOR (m:Methodology) REQUIRE m.entity_id IS UNIQUE",
    "CREATE CONSTRAINT researchproblem_id_unique IF NOT EXISTS FOR (r:ResearchProblem) REQUIRE r.entity_id IS UNIQUE",
    "CREATE CONSTRAINT optimizer_id_unique IF NOT EXISTS FOR (o:Optimizer) REQUIRE o.entity_id IS UNIQUE",
    "CREATE CONSTRAINT framework_id_unique IF NOT EXISTS FOR (f:Framework) REQUIRE f.entity_id IS UNIQUE",
    "CREATE CONSTRAINT organization_id_unique IF NOT EXISTS FOR (o:Organization) REQUIRE o.entity_id IS UNIQUE",
    # Author metadata uses ``author_id`` while NER-originated author mentions
    # may retain ``entity_id``.  Constraint names must be distinct in Neo4j.
    "CREATE CONSTRAINT author_entity_id_unique IF NOT EXISTS FOR (a:Author) REQUIRE a.entity_id IS UNIQUE",
]

INDEX_STATEMENTS = [
    # Paper indexes
    "CREATE INDEX paper_title_idx IF NOT EXISTS FOR (p:Paper) ON (p.title)",
    "CREATE INDEX paper_author_idx IF NOT EXISTS FOR (p:Paper) ON (p.author)",
    "CREATE INDEX paper_status_idx IF NOT EXISTS FOR (p:Paper) ON (p.status)",
    "CREATE INDEX paper_created_at_idx IF NOT EXISTS FOR (p:Paper) ON (p.created_at)",

    # Author indexes
    "CREATE INDEX author_name_idx IF NOT EXISTS FOR (a:Author) ON (a.name)",
    "CREATE INDEX author_normalized_name_idx IF NOT EXISTS FOR (a:Author) ON (a.normalized_name)",

    # Entity canonical name indexes (for fast lookup by name)
    "CREATE INDEX algorithm_canonical_name_idx IF NOT EXISTS FOR (a:Algorithm) ON (a.canonical_name)",
    "CREATE INDEX algorithm_normalized_name_idx IF NOT EXISTS FOR (a:Algorithm) ON (a.normalized_name)",
    "CREATE INDEX model_canonical_name_idx IF NOT EXISTS FOR (m:Model) ON (m.canonical_name)",
    "CREATE INDEX model_normalized_name_idx IF NOT EXISTS FOR (m:Model) ON (m.normalized_name)",
    "CREATE INDEX dataset_canonical_name_idx IF NOT EXISTS FOR (d:Dataset) ON (d.canonical_name)",
    "CREATE INDEX dataset_normalized_name_idx IF NOT EXISTS FOR (d:Dataset) ON (d.normalized_name)",
    "CREATE INDEX metric_canonical_name_idx IF NOT EXISTS FOR (m:Metric) ON (m.canonical_name)",
    "CREATE INDEX metric_normalized_name_idx IF NOT EXISTS FOR (m:Metric) ON (m.normalized_name)",
    "CREATE INDEX task_canonical_name_idx IF NOT EXISTS FOR (t:Task) ON (t.canonical_name)",
    "CREATE INDEX task_normalized_name_idx IF NOT EXISTS FOR (t:Task) ON (t.normalized_name)",
    "CREATE INDEX methodology_canonical_name_idx IF NOT EXISTS FOR (m:Methodology) ON (m.canonical_name)",
    "CREATE INDEX methodology_normalized_name_idx IF NOT EXISTS FOR (m:Methodology) ON (m.normalized_name)",
    "CREATE INDEX researchproblem_canonical_name_idx IF NOT EXISTS FOR (r:ResearchProblem) ON (r.canonical_name)",
    "CREATE INDEX researchproblem_normalized_name_idx IF NOT EXISTS FOR (r:ResearchProblem) ON (r.normalized_name)",
    "CREATE INDEX optimizer_canonical_name_idx IF NOT EXISTS FOR (o:Optimizer) ON (o.canonical_name)",
    "CREATE INDEX optimizer_normalized_name_idx IF NOT EXISTS FOR (o:Optimizer) ON (o.normalized_name)",
    "CREATE INDEX framework_canonical_name_idx IF NOT EXISTS FOR (f:Framework) ON (f.canonical_name)",
    "CREATE INDEX framework_normalized_name_idx IF NOT EXISTS FOR (f:Framework) ON (f.normalized_name)",
    "CREATE INDEX organization_canonical_name_idx IF NOT EXISTS FOR (o:Organization) ON (o.canonical_name)",
    "CREATE INDEX organization_normalized_name_idx IF NOT EXISTS FOR (o:Organization) ON (o.normalized_name)",
    "CREATE INDEX author_canonical_name_idx IF NOT EXISTS FOR (a:Author) ON (a.canonical_name)",
    "CREATE INDEX author_normalized_name_idx IF NOT EXISTS FOR (a:Author) ON (a.normalized_name)",

    # Relationship property indexes
    "CREATE INDEX relation_paper_id_idx IF NOT EXISTS FOR ()-[r:CONTAINS_ENTITY]-() ON (r.paper_id)",
    "CREATE INDEX relation_confidence_idx IF NOT EXISTS FOR ()-[r]-() ON (r.confidence)",
    "CREATE INDEX relation_extraction_method_idx IF NOT EXISTS FOR ()-[r]-() ON (r.extraction_method)",
]

# ---------------------------------------------------------------------------
# Entity Label Mapping (from NER categories to Neo4j labels)
# ---------------------------------------------------------------------------
ENTITY_TYPE_TO_LABEL = {
    "ALGORITHM": "Algorithm",
    "MODEL": "Model",
    "DATASET": "Dataset",
    "METRIC": "Metric",
    "TASK": "Task",
    "METHODOLOGY": "Methodology",
    "RESEARCH_PROBLEM": "ResearchProblem",
    "OPTIMIZER": "Optimizer",
    "FRAMEWORK": "Framework",
    "ORGANIZATION": "Organization",
    "AUTHOR": "Author",
    "PERSON": "Person",
    "GROUP": "Group",
    "PROJECT": "Project",
    "LOCATION": "Location",
    "PRODUCT": "Product",
    "CONCEPT": "Concept",
}

GENERAL_NODE_LABELS = [
    "Person",
    "Group",
    "Project",
    "Location",
    "Product",
    "Concept",
]

# ---------------------------------------------------------------------------
# Relationship Type Validation
# ---------------------------------------------------------------------------
VALID_RELATIONSHIPS = {
    "CONTAINS_ENTITY": {"from": "Paper", "to": ["Algorithm", "Model", "Dataset", "Metric", "Task", "Methodology", "ResearchProblem", "Optimizer", "Framework", "Organization", "Author", *GENERAL_NODE_LABELS]},
    "AUTHORED": {"from": "Author", "to": "Paper"},
    "PROPOSES": {
        "from": ["Model", "Methodology", "Framework"],
        "to": ["Task", "ResearchProblem"],
    },
    "USES": {
        "from": ["Model", "Framework", "Algorithm", "Project", "Group", "Person"],
        "to": ["Dataset", "Algorithm", "Product", "Location", "Concept"],
    },
    "EVALUATED_ON": {"from": ["Model", "Algorithm"], "to": "Dataset"},
    "ACHIEVES": {"from": ["Model", "Algorithm"], "to": "Metric"},
    "COMPARED_WITH": {
        "from": ["Model", "Algorithm", "Dataset"],
        "to": ["Model", "Algorithm", "Dataset"],
    },
    "IMPROVES": {
        "from": ["Model", "Algorithm", "Methodology", "Project", "Group", "Organization", "Person"],
        "to": ["Metric", "Concept"],
    },
    "APPLIES_TO": {"from": ["Methodology", "Framework"], "to": ["Task", "Dataset"]},
    "OUTPERFORMS": {"from": ["Model", "Algorithm"], "to": ["Model", "Algorithm", "Metric"]},
    "BASED_ON": {"from": ["Model", "Algorithm", "Framework", "Project"], "to": ["Methodology", "Concept"]},
}

GENERAL_VALID_RELATIONSHIPS = {
    "STARTED": {"from": ["Group", "Person", "Organization"], "to": ["Project", "Concept"]},
    "LED_BY": {"from": ["Project", "Group", "Organization"], "to": ["Person", "Organization", "Group"]},
    "WORKED_WITH": {"from": ["Person", "Group", "Organization"], "to": ["Person", "Group", "Organization"]},
    "CREATED": {"from": ["Person", "Group", "Project", "Organization", "Location"], "to": ["Location", "Project", "Product"]},
    "PROVIDED": {"from": ["Organization", "Person", "Group", "Project"], "to": ["Product", "Concept", "Location"]},
    "SHARED": {"from": ["Group", "Person", "Product", "Project"], "to": ["Product", "Concept", "Group"]},
    "PRODUCED": {"from": ["Project", "Location", "Group", "Organization"], "to": ["Product", "Concept"]},
    "HELPED": {"from": ["Group", "Person", "Project", "Organization"], "to": ["Product", "Project", "Concept", "Group"]},
    "ENCOURAGED": {"from": ["Project", "Person", "Organization"], "to": ["Concept", "Group"]},
    "REDUCED": {"from": ["Project", "Organization", "Group", "Person"], "to": ["Concept"]},
    "LOCATED_IN": {"from": ["Group", "Project", "Organization", "Person", "Product"], "to": ["Location"]},
    "BELIEVES_IN": {"from": ["Person", "Group", "Organization"], "to": ["Concept"]},
    "PARTICIPATED_IN": {"from": ["Group", "Person", "Organization"], "to": ["Project", "Concept"]},
    "AFFECTS": {"from": ["Project", "Concept", "Organization"], "to": ["Group", "Concept", "Project"]},
}

# Evidence relationship
EVIDENCE_RELATIONSHIP = "HAS_EVIDENCE"

# ---------------------------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------------------------

def get_node_label(entity_type: str) -> str:
    """Convert NER entity type to Neo4j node label."""
    return ENTITY_TYPE_TO_LABEL.get(entity_type, entity_type)

def _matches_rule_pair(rule: Dict[str, Any], from_label: str, to_label: str) -> bool:
    allowed_from = rule["from"]
    if isinstance(allowed_from, list):
        if from_label not in allowed_from:
            return False
    elif allowed_from != from_label:
        return False

    allowed_to = rule["to"]
    if isinstance(allowed_to, list):
        return to_label in allowed_to
    return allowed_to == to_label

def validate_relationship(rel_type: str, from_label: str, to_label: str) -> bool:
    """Validate if a relationship is allowed between node types."""
    rule = VALID_RELATIONSHIPS.get(rel_type) or GENERAL_VALID_RELATIONSHIPS.get(rel_type)
    if rule is None:
        return False
    return _matches_rule_pair(rule, from_label, to_label)

def get_relationship_properties(rel_type: str) -> Dict[str, str]:
    """Get expected properties for a relationship type."""
    return RELATIONSHIP_PROPERTIES.get(rel_type, {})

def get_node_properties(label: str) -> Dict[str, str]:
    """Get expected properties for a node label."""
    return NODE_PROPERTIES.get(label, {})


def get_direction(rel_type: str) -> str:
    """Return the declared direction for a supported relationship."""
    if rel_type not in VALID_RELATIONSHIPS or rel_type not in RELATIONSHIP_DIRECTIONS:
        raise ValueError(f"Unknown or directionless relationship: {rel_type}")
    if rel_type == "COMPARED_WITH":
        return "subject<->object"
    return "subject->object"

# ---------------------------------------------------------------------------
# Initialization Script
# ---------------------------------------------------------------------------

def get_initialization_script() -> str:
    """Generate the full initialization script for Neo4j."""
    statements = []

    # Add constraints
    statements.extend(CONSTRAINT_STATEMENTS)

    # Add indexes
    statements.extend(INDEX_STATEMENTS)

    return "\n".join(statements)

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Graph Schema Definitions")
    print("=" * 50)
    print(f"Node Labels: {len(NODE_LABELS)}")
    print(f"Relationship Types: {len(RELATIONSHIP_TYPES)}")
    print(f"Constraints: {len(CONSTRAINT_STATEMENTS)}")
    print(f"Indexes: {len(INDEX_STATEMENTS)}")
    print(f"Entity Type Mappings: {len(ENTITY_TYPE_TO_LABEL)}")
