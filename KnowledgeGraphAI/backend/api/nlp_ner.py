import os
import json
import logging
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from KnowledgeGraphAI.backend.nlp.ner.entity_schema import EntityTaxonomy
from KnowledgeGraphAI.backend.nlp.ner.ner_pipeline import (
    extract_entities_from_paper as extract_ner_entities,
)
from KnowledgeGraphAI.backend.nlp.preprocessing.pipeline import NLPProcessingPipeline
from KnowledgeGraphAI.backend.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/nlp/ner", tags=["ner"])

# Request/Response schemas
class ExtractEntityRequest(BaseModel):
    paper_id: int
    extraction_method: str = "rule_based"


class EntitySchema(BaseModel):
    entity_id: str
    text: str
    entity_type: str
    start_char: int
    end_char: int
    confidence: float
    paper_id: int
    page_number: int
    sentence_index: int
    source_text: str
    extraction_method: str
    original_text: str = ""
    cleaned_text: str = ""


class EntityBatchResponse(BaseModel):
    paper_id: int
    processing_status: str
    total_sentences_processed: int
    total_entities: int
    entity_distribution: Dict[str, int]
    entities: List[EntitySchema]
    model_metadata: Dict[str, Any]


@router.post("/extract/{paper_id}", response_model=EntityBatchResponse, status_code=200)
async def extract_entities_from_paper(paper_id: int, db: Session = Depends(get_db)):
    """Extract entities from a paper using the configured NER pipeline."""
    from KnowledgeGraphAI.models.paper import Paper
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    if not os.path.exists(paper.file_path):
        raise HTTPException(status_code=404, detail="Source PDF file not found")

    try:
        preprocessing_result = NLPProcessingPipeline(
            paper_id=paper_id, file_path=paper.file_path
        ).process()
        sentences = [
            sentence
            for paragraph in preprocessing_result["paragraphs"]
            for sentence in paragraph["sentences"]
        ]
        result = extract_ner_entities(sentences)
        entity_schemas = [
            EntitySchema(
                entity_id=f"{paper_id}_{index}",
                text=entity["text"],
                entity_type=entity["entity_type"],
                start_char=entity["start"],
                end_char=entity["end"],
                confidence=entity["confidence"],
                paper_id=entity["paper_id"],
                page_number=entity["page_number"],
                sentence_index=entity["sentence_index"],
                source_text=entity["source_text"],
                extraction_method=entity["extraction_method"],
                original_text=entity.get("original_text") or "",
                cleaned_text=entity.get("cleaned_text") or "",
            )
            for index, entity in enumerate(result["entities"])
        ]

        # This is a standalone diagnostic endpoint, not the end-to-end
        # processing workflow.  It must not claim that the paper completed an
        # undocumented processing state or overwrite a completed state.
        metadata = dict(paper.metadata_json or {})
        metadata.update({
            "entities": result["entities"],
            "entity_count": result["total_entities"],
            "entity_distribution": result["entity_distribution"],
            "ner_extraction_method": result["model_metadata"]["model_name"],
        })
        paper.metadata_json = metadata
        db.commit()

        return {
            "paper_id": paper_id,
            "processing_status": "completed",
            "total_sentences_processed": result["total_sentences_processed"],
            "total_entities": result["total_entities"],
            "entity_distribution": result["entity_distribution"],
            "entities": entity_schemas,
            "model_metadata": {
                **result["model_metadata"],
                "extraction_method": "rule_based",
            }
        }

    except Exception as e:
        logger.exception(f"NER extraction failed for paper {paper_id}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/entities/{paper_id}", response_model=Dict[str, Any])
async def get_entities_for_paper(paper_id: int, db: Session = Depends(get_db)):
    """Get all entities extracted for a paper."""
    # Try to get from database
    from KnowledgeGraphAI.models.paper import Paper
    paper = db.query(Paper).filter(Paper.id == paper_id).first()

    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    metadata = paper.metadata_json if paper.metadata_json else {}

    entities = metadata.get("entities", [])
    if isinstance(entities, str):
        entities = json.loads(entities)

    return {
        "paper_id": paper_id,
        "entity_count": metadata.get("entity_count", 0),
        "entity_distribution": metadata.get("entity_distribution", {}),
        "entities": entities,
    }


@router.get("/model-info")
async def get_ner_model_info():
    """Get NER model information."""
    return {
        "model_name": "rule_based",
        "model_type": "baseline",
        "extraction_method": "rule_based",
        "confidence_threshold": 0.55,
        "entity_categories": EntityTaxonomy.valid_names(),
    }
