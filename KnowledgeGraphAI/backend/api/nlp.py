import os
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from KnowledgeGraphAI.backend.database import get_db
from KnowledgeGraphAI.models.paper import Paper
from KnowledgeGraphAI.backend.nlp.preprocessing.pipeline import NLPProcessingPipeline

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/nlp", tags=["nlp"])

@router.post("/preprocess/{paper_id}", status_code=status.HTTP_200_OK)
async def preprocess_paper(paper_id: int, db: Session = Depends(get_db)):
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found.")

    if not os.path.exists(paper.file_path):
        raise HTTPException(status_code=404, detail="Source PDF file not found.")

    try:
        pipeline = NLPProcessingPipeline(paper_id=paper.id, file_path=paper.file_path)
        result = pipeline.process()

        # Preserve full-pipeline state semantics: a diagnostic preprocessing
        # call does not imply graph/index completion.
        metadata = dict(paper.metadata_json or {})
        metadata["preprocessing_statistics"] = result.get("statistics", {})
        metadata["preprocessing_warnings"] = result.get("warnings", [])
        paper.metadata_json = metadata
        db.commit()

        return result
    except Exception as e:
        logger.exception(f"Preprocessing failed for paper {paper_id}")
        raise HTTPException(status_code=500, detail=str(e))
