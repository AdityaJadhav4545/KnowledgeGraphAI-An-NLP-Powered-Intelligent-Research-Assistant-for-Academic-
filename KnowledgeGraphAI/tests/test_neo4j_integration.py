"""Real-Neo4j integration tests; no database operations are mocked."""

import hashlib
import os
import time
import uuid
from pathlib import Path

import pytest
import pymupdf

from KnowledgeGraphAI.backend.nlp.ner.entity_schema import ExtractedEntity
from KnowledgeGraphAI.backend.nlp.ner.entity_schema import ExtractedSentence
from KnowledgeGraphAI.backend.nlp.ner.ner_pipeline import NERPipeline
from KnowledgeGraphAI.backend.nlp.preprocessing.pipeline import NLPProcessingPipeline
from KnowledgeGraphAI.backend.nlp.relation_extraction.relation_extraction_service import (
    ScientificRelationExtractionService,
)
from KnowledgeGraphAI.backend.services.knowledge_graph.graph_analytics import GraphAnalytics
from KnowledgeGraphAI.backend.services.knowledge_graph.graph_construction import (
    GraphConstructionService,
)
from KnowledgeGraphAI.backend.services.knowledge_graph.graph_query import GraphQueryService
from KnowledgeGraphAI.backend.services.knowledge_graph.neo4j_connection import (
    get_neo4j_manager,
)
from KnowledgeGraphAI.backend.services.pdf_ingestion import PDFIngestionService


def _test_token() -> str:
    return os.environ.get("KGAI_NEO4J_TEST_TOKEN", str(uuid.uuid4()))


def _fixture(token: str):
    paper_id = int.from_bytes(hashlib.sha256(token.encode()).digest()[:6], "big")
    suffix = token.replace("-", "")[:12]
    names = {
        "MODEL": f"KGAI BERT {suffix}",
        "DATASET": f"KGAI SQuAD {suffix}",
        "ALGORITHM": f"KGAI Adam {suffix}",
        "METRIC": f"KGAI F1-score {suffix}",
    }
    original_text = (
        f"{names['MODEL']} was evaluated on {names['DATASET']}, "
        f"used {names['ALGORITHM']}, and achieved {names['METRIC']}."
    )
    cleaned_text = " ".join(original_text.split())
    entities = []
    for entity_type, text in names.items():
        start = original_text.index(text)
        entities.append(
            ExtractedEntity(
                text=text,
                entity_type=entity_type,
                start_char=start,
                end_char=start + len(text),
                confidence=0.97,
                paper_id=paper_id,
                page_number=2,
                sentence_index=3,
                source_text=original_text,
                original_text=original_text,
                cleaned_text=cleaned_text,
            )
        )

    relations = [
        {
            "relation": relationship,
            "subject": {"text": names["MODEL"], "label": "MODEL"},
            "object": {"text": names[object_type], "label": object_type},
            "confidence": 0.96,
            "evidence": original_text,
            "page_number": 2,
            "sentence_id": 3,
            "start_char": 0,
            "end_char": len(original_text),
            "original_text": original_text,
            "cleaned_text": cleaned_text,
        }
        for relationship, object_type in (
            ("EVALUATED_ON", "DATASET"),
            ("USES", "ALGORITHM"),
            ("ACHIEVES", "METRIC"),
        )
    ]
    metadata = {
        "paper_id": paper_id,
        "title": f"KnowledgeGraphAI Integration Test {suffix}",
        "author": "",
        "file_path": "",
        "file_hash": "",
        "content_hash": "",
        "page_count": 2,
        "status": "processed",
    }
    entity_ids = {
        entity_type: GraphConstructionService()._generate_entity_id(text, entity_type)
        for entity_type, text in names.items()
    }
    return paper_id, names, original_text, cleaned_text, entities, relations, metadata, entity_ids


def _counts(manager):
    return manager.execute_query(
        """
        CALL () {
            MATCH (n)
            RETURN count(n) AS nodes
        }
        CALL () {
            MATCH ()-[r]->()
            RETURN count(r) AS relationships
        }
        RETURN nodes, relationships
        """
    )[0]


def _delete_fixture(manager, paper_id, entity_ids):
    manager.execute_write(
        "MATCH (p:Paper {paper_id: $paper_id}) DETACH DELETE p",
        {"paper_id": paper_id},
    )
    manager.execute_write(
        "MATCH (e) WHERE e.entity_id IN $entity_ids DETACH DELETE e",
        {"entity_ids": list(entity_ids.values())},
    )


def _delete_pdf_fixture(manager, paper_id, entity_ids):
    manager.execute_write(
        "MATCH ()-[r]->() WHERE r.paper_id = $paper_id DELETE r",
        {"paper_id": paper_id},
    )
    manager.execute_write(
        "MATCH (p:Paper {paper_id: $paper_id}) DETACH DELETE p",
        {"paper_id": paper_id},
    )
    manager.execute_write(
        """
        MATCH (e)
        WHERE e.entity_id IN $entity_ids
          AND $paper_id IN coalesce(e.source_paper_ids, [])
          AND size(coalesce(e.source_paper_ids, [])) = 1
          AND NOT (e)--()
        DELETE e
        """,
        {"paper_id": paper_id, "entity_ids": list(entity_ids)},
    )


def _wait_for_database(manager, timeout=60):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if manager.connect():
            return
        time.sleep(2)
    pytest.fail("Neo4j did not become available within 60 seconds")


def test_phase3_real_pdf_to_neo4j_integration(tmp_path: Path):
    manager = get_neo4j_manager()
    _wait_for_database(manager)
    health = manager.health_check()
    assert health["status"] == "healthy", health

    token = uuid.uuid4().hex[:12]
    paper_id = int.from_bytes(uuid.uuid4().bytes[:6], "big")
    title = f"KnowledgeGraphAI Scientific Integration Study {token}"
    pdf_text = (
        f"BERT was evaluated on the SQuAD dataset, and BERT achieved an "
        f"F1-score of 91 percent (study {token})."
    )
    pdf_path = tmp_path / f"kgai_scientific_integration_{token}.pdf"
    document = pymupdf.open()
    page = document.new_page(width=800, height=200)
    page.insert_text((28, 50), pdf_text, fontsize=11)
    document.set_metadata({"title": title, "author": ""})
    document.save(str(pdf_path))
    document.close()

    pdf_data = PDFIngestionService.extract_pdf_data(str(pdf_path), paper_id=paper_id)
    assert pdf_data["has_extractable_text"] is True
    assert pdf_data["page_count"] == 1
    preprocessing = NLPProcessingPipeline(paper_id, str(pdf_path)).process()
    sentences = [
        ExtractedSentence(**sentence)
        for paragraph in preprocessing["paragraphs"]
        for sentence in paragraph["sentences"]
    ]
    assert sentences

    entity_batch = NERPipeline().extract_paper(sentences)
    entities = entity_batch.entities
    assert entities, "Scientific NER produced no entities from the extracted PDF text"
    assert {entity.entity_type for entity in entities} >= {"MODEL", "DATASET", "METRIC"}
    assert all(
        entity.paper_id == paper_id
        and entity.page_number == 1
        and entity.original_text
        and entity.cleaned_text
        and 0 <= entity.start_char < entity.end_char <= len(entity.cleaned_text)
        for entity in entities
    )

    cleaned_text = " ".join(sentence.cleaned_text for sentence in sentences)
    extracted_relations = ScientificRelationExtractionService(
        use_relabel=False, use_classifier=False
    ).extract_relations(cleaned_text, entities, sentences, paper_id)
    relations = [relation.to_dict() for relation in extracted_relations]
    assert relations, "Rule-based relation extraction produced no relations"
    assert "ACHIEVES" in {relation["relation"] for relation in relations}
    assert all(
        relation["paper_id"] == paper_id
        and relation["original_text"]
        and relation["cleaned_text"]
        for relation in relations
    )

    construction = GraphConstructionService()
    construction._generate_entity_id = lambda text, entity_type: hashlib.sha256(
        f"{token}:{entity_type}:{text.strip().lower()}".encode("utf-8")
    ).hexdigest()[:16]
    entity_ids = {
        construction._generate_entity_id(entity.text, entity.entity_type)
        for entity in entities
    }
    content_hash = PDFIngestionService.compute_content_hash(str(pdf_path))
    file_hash = PDFIngestionService.compute_sha256(str(pdf_path))
    conflicts = manager.execute_query(
        """
        MATCH (n)
        WHERE n.entity_id IN $entity_ids
           OR (n:Paper AND (n.paper_id = $paper_id
               OR n.file_hash = $file_hash OR n.content_hash = $content_hash))
        RETURN labels(n) AS labels, n.entity_id AS entity_id, n.paper_id AS paper_id
        """,
        {
            "entity_ids": list(entity_ids),
            "paper_id": paper_id,
            "file_hash": file_hash,
            "content_hash": content_hash,
        },
    )
    assert not conflicts, f"Refusing to modify pre-existing graph records: {conflicts}"

    paper_metadata = {
        "paper_id": paper_id,
        "title": pdf_data["title"],
        "author": "" if pdf_data["author"] == "Unknown" else pdf_data["author"],
        "file_path": str(pdf_path),
        "file_hash": file_hash,
        "content_hash": content_hash,
        "page_count": pdf_data["page_count"],
        "status": "processed",
    }
    before = _counts(manager)
    try:
        first = construction.build_graph_for_paper(paper_metadata, entities, relations)
        assert first["errors"] == []

        model = next(entity for entity in entities if entity.entity_type == "MODEL")
        dataset = next(entity for entity in entities if entity.entity_type == "DATASET")
        metric = next(entity for entity in entities if entity.entity_type == "METRIC")
        model_id = construction._generate_entity_id(model.text, model.entity_type)
        dataset_id = construction._generate_entity_id(dataset.text, dataset.entity_type)
        metric_id = construction._generate_entity_id(metric.text, metric.entity_type)

        paper_records = manager.execute_query(
            "MATCH (p:Paper {paper_id: $paper_id}) "
            "RETURN p.title AS title, p.page_count AS page_count, "
            "p.file_hash AS file_hash, p.content_hash AS content_hash",
            {"paper_id": paper_id},
        )
        assert paper_records == [{
            "title": title,
            "page_count": 1,
            "file_hash": file_hash,
            "content_hash": content_hash,
        }]

        persisted_entities = manager.execute_query(
            """
            MATCH (p:Paper {paper_id: $paper_id})-[r:CONTAINS_ENTITY]->(e)
            RETURN e.entity_id AS entity_id, e.canonical_name AS canonical_name,
                   e.occurrence_count AS occurrence_count, labels(e)[0] AS label,
                   r.paper_id AS paper_id, r.page_number AS page_number,
                   r.sentence_id AS sentence_index, r.start_char AS start_char,
                   r.end_char AS end_char, r.original_text AS original_text,
                   r.cleaned_text AS cleaned_text
            """,
            {"paper_id": paper_id},
        )
        assert {row["entity_id"] for row in persisted_entities} == entity_ids
        bert_record = next(row for row in persisted_entities if row["entity_id"] == model_id)
        assert bert_record["occurrence_count"] == 2
        assert bert_record["label"] == "Model"
        for row in persisted_entities:
            expected_entity = next(
                entity
                for entity in entities
                if construction._generate_entity_id(
                    entity.text, entity.entity_type
                ) == row["entity_id"]
            )
            assert row["paper_id"] == expected_entity.paper_id == paper_id
            assert row["page_number"] == expected_entity.page_number == 1
            assert row["sentence_index"] == expected_entity.sentence_index == 0
            assert row["start_char"] == expected_entity.start_char
            assert row["end_char"] == expected_entity.end_char
            assert row["original_text"] == expected_entity.original_text
            assert row["cleaned_text"] == expected_entity.cleaned_text
            assert (
                row["cleaned_text"][row["start_char"]:row["end_char"]]
                == expected_entity.text
            )

        query_service = GraphQueryService()
        paper_entities = query_service.get_paper_entities(paper_id)
        paper_relationships = query_service.get_paper_relationships(paper_id)
        assert len(paper_entities) == len(entity_ids)
        assert len(paper_relationships) == len(relations)
        assert {row["relationship_type"] for row in paper_relationships} == {
            relation["relation"] for relation in relations
        }
        for row in paper_relationships:
            expected_relation = next(
                relation
                for relation in relations
                if relation["relation"] == row["relationship_type"]
                and relation["subject"]["text"] == row["subject"]
                and relation["object"]["text"] == row["object"]
            )
            assert row["paper_id"] == paper_id
            assert row["original_text"] == expected_relation["original_text"]
            assert row["cleaned_text"] == expected_relation["cleaned_text"]
            assert row["page_number"] == expected_relation["page_number"]
            assert row["sentence_id"] == expected_relation["sentence_id"]
            assert row["start_char"] == min(
                expected_relation["subject"]["start"],
                expected_relation["object"]["start"],
            )
            assert row["end_char"] == max(
                expected_relation["subject"]["end"],
                expected_relation["object"]["end"],
            )

        models = query_service.find_models_for_dataset(dataset_id)
        metrics = query_service.find_metrics_for_model(model_id)
        neighborhood = query_service.get_entity_neighborhood(
            model_id, "Model", depth=2, limit=20
        )
        assert any(row["entity_id"] == model_id for row in models)
        assert any(row["entity_id"] == metric_id for row in metrics)
        assert neighborhood["nodes"]
        assert neighborhood["relationships"]

        after_first = _counts(manager)
        assert after_first == {
            "nodes": before["nodes"] + 1 + len(entity_ids),
            "relationships": before["relationships"] + len(entity_ids) + len(relations),
        }

        second = construction.build_graph_for_paper(paper_metadata, entities, relations)
        assert second["errors"] == []
        assert _counts(manager) == after_first
        occurrence_counts = manager.execute_query(
            "MATCH (e) WHERE e.entity_id IN $entity_ids "
            "RETURN e.entity_id AS entity_id, e.occurrence_count AS occurrence_count",
            {"entity_ids": list(entity_ids)},
        )
        assert {row["entity_id"]: row["occurrence_count"] for row in occurrence_counts}[
            model_id
        ] == 2

        print({
            "pdf_pages": pdf_data["page_count"],
            "preprocessed_sentences": len(sentences),
            "entities_extracted": len(entities),
            "unique_entity_nodes": len(entity_ids),
            "relations_extracted_and_persisted": len(relations),
            "nodes_before": before["nodes"],
            "relationships_before": before["relationships"],
            "nodes_after": after_first["nodes"],
            "relationships_after": after_first["relationships"],
            "provenance": "verified",
            "duplicate_BERT_resolution": "two mentions, one entity node",
            "repeated_ingestion": "node, relationship, and occurrence counts unchanged",
            "paper_query_entities": len(paper_entities),
            "paper_query_relationships": len(paper_relationships),
            "models_for_dataset": len(models),
            "metrics_for_model": len(metrics),
        })
    finally:
        _delete_pdf_fixture(manager, paper_id, entity_ids)
        print("Scoped PDF integration fixture cleanup: complete")


def test_phase3_real_neo4j_integration():
    manager = get_neo4j_manager()
    _wait_for_database(manager)
    health = manager.health_check()
    assert health["connected"] is True
    assert health["status"] == "healthy", health

    token = _test_token()
    (
        paper_id,
        names,
        original_text,
        cleaned_text,
        entities,
        relations,
        metadata,
        entity_ids,
    ) = _fixture(token)
    query_service = GraphQueryService()
    analytics = GraphAnalytics()
    verify_after_restart = os.environ.get("KGAI_NEO4J_VERIFY_AFTER_RESTART") == "1"
    keep_data = os.environ.get("KGAI_NEO4J_KEEP_TEST_DATA") == "1"

    if verify_after_restart:
        try:
            _wait_for_database(manager)
            paper = manager.execute_query(
                "MATCH (p:Paper {paper_id: $paper_id}) RETURN p.title AS title",
                {"paper_id": paper_id},
            )
            assert paper and paper[0]["title"] == metadata["title"]
            actual_entities = manager.execute_query(
                "MATCH (p:Paper {paper_id: $paper_id})-[:CONTAINS_ENTITY]->(e) "
                "RETURN e.entity_id AS entity_id",
                {"paper_id": paper_id},
            )
            assert {row["entity_id"] for row in actual_entities} == set(entity_ids.values())
            stored_relations = manager.execute_query(
                """
                MATCH (subject)-[rel]->(object)
                WHERE rel.paper_id = $paper_id AND type(rel) <> 'CONTAINS_ENTITY'
                RETURN labels(subject)[0] AS subject_type, type(rel) AS relationship,
                       labels(object)[0] AS object_type, rel.paper_id AS paper_id,
                       rel.page_number AS page_number, rel.sentence_id AS sentence_id,
                       rel.start_char AS start_char, rel.end_char AS end_char,
                       rel.original_text AS original_text, rel.cleaned_text AS cleaned_text
                """,
                {"paper_id": paper_id},
            )
            assert {
                (row["subject_type"], row["relationship"], row["object_type"])
                for row in stored_relations
            } == {
                ("Model", "EVALUATED_ON", "Dataset"),
                ("Model", "USES", "Algorithm"),
                ("Model", "ACHIEVES", "Metric"),
            }
            assert all(
                row["paper_id"] == paper_id
                and row["page_number"] == 2
                and row["sentence_id"] == 3
                and row["start_char"] == 0
                and row["end_char"] == len(original_text)
                and row["original_text"] == original_text
                and row["cleaned_text"] == cleaned_text
                for row in stored_relations
            )
            model_id = entity_ids["MODEL"]
            models = query_service.find_models_for_dataset(entity_ids["DATASET"])
            algorithms = query_service.find_algorithms_for_model(model_id)
            metrics = query_service.find_metrics_for_model(model_id)
            assert [row["canonical_name"] for row in models] == [names["MODEL"]]
            assert [row["canonical_name"] for row in algorithms] == [names["ALGORITHM"]]
            assert [row["canonical_name"] for row in metrics] == [names["METRIC"]]
            neighborhood = query_service.get_entity_neighborhood(
                model_id, "Model", depth=2, limit=20
            )
            neighborhood_analytics = analytics.get_entity_neighborhood(
                model_id, "Model", max_depth=2, limit=20
            )
            assert neighborhood["nodes"]
            assert neighborhood["relationships"]
            assert neighborhood_analytics["nodes"]
            assert neighborhood_analytics["relationships"]
            paper_entities = query_service.get_paper_entities(paper_id)
            paper_relationships = query_service.get_paper_relationships(paper_id)
            assert len(paper_entities) == 4
            assert len(paper_relationships) == 3
            assert all(
                row["paper_id"] == paper_id
                and row["page_number"] == 2
                and row["sentence_id"] == 3
                and row["start_char"] >= 0
                and row["end_char"] > row["start_char"]
                and row["original_text"] == original_text
                and row["cleaned_text"] == cleaned_text
                for row in paper_entities
            )
            persisted_counts = _counts(manager)
            print(
                {
                    "persistence_after_container_restart": "verified",
                    "nodes": persisted_counts["nodes"],
                    "relationships": persisted_counts["relationships"],
                    "provenance": "verified",
                    "query_results": {
                        "models_for_dataset": len(models),
                        "algorithms_for_model": len(algorithms),
                        "metrics_for_model": len(metrics),
                        "neighborhood_nodes": len(neighborhood["nodes"]),
                        "paper_entities": len(paper_entities),
                        "paper_relationships": len(paper_relationships),
                    },
                }
            )
        finally:
            _delete_fixture(manager, paper_id, entity_ids)
            print("Post-restart scoped integration fixture cleanup: complete")
        return

    existing = manager.execute_query(
        """
        OPTIONAL MATCH (p:Paper {paper_id: $paper_id})
        WITH p
        OPTIONAL MATCH (e {entity_id: $entity_id})
        RETURN p IS NOT NULL AS paper_exists, count(e) AS entity_count
        """,
        {"paper_id": paper_id, "entity_id": next(iter(entity_ids.values()))},
    )[0]
    assert existing == {"paper_exists": False, "entity_count": 0}
    before = _counts(manager)
    seed_succeeded = False
    try:
        construction = GraphConstructionService()
        first = construction.build_graph_for_paper(metadata, entities, relations)
        assert first["errors"] == []
        assert first["papers_created"] == 1
        assert first["entities_created"] == 4
        assert first["relationships_created"] == 7

        paper = manager.execute_query(
            "MATCH (p:Paper {paper_id: $paper_id}) RETURN p.paper_id AS paper_id, p.title AS title",
            {"paper_id": paper_id},
        )
        assert paper == [{"paper_id": paper_id, "title": metadata["title"]}]
        stored_entities = manager.execute_query(
            """
            MATCH (p:Paper {paper_id: $paper_id})-[r:CONTAINS_ENTITY]->(e)
            RETURN e.entity_id AS entity_id, e.canonical_name AS canonical_name,
                   e.occurrence_count AS occurrence_count, labels(e)[0] AS label,
                   r.paper_id AS paper_id, r.page_number AS page_number,
                   r.sentence_id AS sentence_id, r.start_char AS start_char,
                   r.end_char AS end_char, r.original_text AS original_text,
                   r.cleaned_text AS cleaned_text, r.evidence AS evidence
            """,
            {"paper_id": paper_id},
        )
        assert len(stored_entities) == 4
        for row in stored_entities:
            assert row["entity_id"] in entity_ids.values()
            assert row["canonical_name"] in names.values()
            assert row["label"] == next(
                label for label, name in (
                    ("Model", names["MODEL"]),
                    ("Dataset", names["DATASET"]),
                    ("Algorithm", names["ALGORITHM"]),
                    ("Metric", names["METRIC"]),
                ) if name == row["canonical_name"]
            )
            assert row["paper_id"] == paper_id
            assert row["page_number"] == 2
            assert row["sentence_id"] == 3
            assert row["start_char"] >= 0
            assert row["end_char"] > row["start_char"]
            assert row["original_text"] == original_text
            assert row["cleaned_text"] == cleaned_text
            assert row["evidence"] == original_text

        directions = manager.execute_query(
            """
            MATCH (s:Model)-[r]->(o)
            WHERE r.paper_id = $paper_id
            RETURN labels(s)[0] AS subject_label, type(r) AS relationship,
                   labels(o)[0] AS object_label, r.paper_id AS paper_id
            ORDER BY relationship
            """,
            {"paper_id": paper_id},
        )
        assert {
            (row["subject_label"], row["relationship"], row["object_label"])
            for row in directions
        } == {
            ("Model", "EVALUATED_ON", "Dataset"),
            ("Model", "USES", "Algorithm"),
            ("Model", "ACHIEVES", "Metric"),
        }
        assert all(row["paper_id"] == paper_id for row in directions)

        model_id = entity_ids["MODEL"]
        dataset_id = entity_ids["DATASET"]
        algorithms = query_service.find_algorithms_for_model(model_id)
        metrics = query_service.find_metrics_for_model(model_id)
        models = query_service.find_models_for_dataset(dataset_id)
        assert [row["canonical_name"] for row in algorithms] == [names["ALGORITHM"]]
        assert [row["canonical_name"] for row in metrics] == [names["METRIC"]]
        assert [row["canonical_name"] for row in models] == [names["MODEL"]]
        assert algorithms[0]["entity_id"] == entity_ids["ALGORITHM"]
        assert metrics[0]["entity_id"] == entity_ids["METRIC"]
        assert models[0]["entity_id"] == model_id

        neighborhood = query_service.get_entity_neighborhood(
            model_id, "Model", depth=2, limit=20
        )
        neighborhood_nodes = [dict(node.items()) for node in neighborhood["nodes"]]
        neighborhood_relations = neighborhood["relationships"]
        assert {node.get("entity_id") for node in neighborhood_nodes} >= {
            entity_ids["MODEL"],
            entity_ids["DATASET"],
            entity_ids["ALGORITHM"],
            entity_ids["METRIC"],
        }
        assert {rel["type"] for rel in neighborhood_relations} >= {
            "EVALUATED_ON",
            "USES",
            "ACHIEVES",
        }

        paper_entities = query_service.get_paper_entities(paper_id)
        paper_relationships = query_service.get_paper_relationships(paper_id)
        assert len(paper_entities) == 4
        assert len(paper_relationships) == 3
        assert {row["relationship_type"] for row in paper_relationships} == {
            "EVALUATED_ON",
            "USES",
            "ACHIEVES",
        }
        assert all(row["paper_id"] == paper_id for row in paper_relationships)
        assert all(
            row["original_text"] == original_text
            and row["cleaned_text"] == cleaned_text
            and row["start_char"] == 0
            and row["end_char"] == len(original_text)
            for row in paper_relationships
        )
        assert all(
            row["original_text"] == original_text
            and row["cleaned_text"] == cleaned_text
            and row["start_char"] >= 0
            and row["end_char"] > row["start_char"]
            for row in paper_entities
        )

        second = construction.build_graph_for_paper(metadata, entities, relations)
        assert second["errors"] == []
        repeated_counts = _counts(manager)
        assert repeated_counts == {
            "nodes": before["nodes"] + 5,
            "relationships": before["relationships"] + 7,
        }
        assert construction.stats.entities_merged == 4

        case_variant = list(entities)
        model_entity = entities[0]
        case_variant[0] = ExtractedEntity(
            text=model_entity.text.swapcase(),
            entity_type=model_entity.entity_type,
            start_char=model_entity.start_char,
            end_char=model_entity.end_char,
            confidence=model_entity.confidence,
            paper_id=model_entity.paper_id,
            page_number=model_entity.page_number,
            sentence_index=model_entity.sentence_index,
            source_text=model_entity.source_text,
            original_text=model_entity.original_text,
            cleaned_text=model_entity.cleaned_text,
        )
        third = construction.build_graph_for_paper(metadata, case_variant, relations)
        assert third["errors"] == []
        assert _counts(manager) == repeated_counts
        canonical = manager.execute_query(
            "MATCH (m:Model {entity_id: $entity_id}) "
            "RETURN m.canonical_name AS name, m.occurrence_count AS count",
            {"entity_id": model_id},
        )
        assert canonical == [{"name": names["MODEL"], "count": 1}]

        after = _counts(manager)
        assert after == repeated_counts
        seed_succeeded = True
        print(
            {
                "nodes_before": before["nodes"],
                "relationships_before": before["relationships"],
                "nodes_after_ingestion": after["nodes"],
                "relationships_after_ingestion": after["relationships"],
                "created_nodes": 5,
                "created_relationships": 7,
                "provenance": "verified",
                "idempotency": "verified",
                "queries": {
                    "models_for_dataset": models,
                    "algorithms_for_model": algorithms,
                    "metrics_for_model": metrics,
                    "neighborhood_node_count": len(neighborhood_nodes),
                    "paper_entity_count": len(paper_entities),
                    "paper_relationship_count": len(paper_relationships),
                },
            }
        )
    finally:
        if not keep_data or not seed_succeeded:
            _delete_fixture(manager, paper_id, entity_ids)
            print("Scoped integration fixture cleanup: complete")


def test_phase3_data_persists_after_container_restart():
    if os.environ.get("KGAI_NEO4J_VERIFY_AFTER_RESTART") != "1":
        pytest.skip("Run after seeding the dedicated test graph and restarting Neo4j")
    test_phase3_real_neo4j_integration()
