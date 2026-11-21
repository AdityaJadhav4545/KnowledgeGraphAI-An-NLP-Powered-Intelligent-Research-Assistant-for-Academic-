import time
import logging
from dataclasses import asdict
from typing import Dict, Any, List

from KnowledgeGraphAI.backend.services.pdf_ingestion import PDFIngestionService
from KnowledgeGraphAI.backend.nlp.preprocessing.text_cleaner import TextCleaner
from KnowledgeGraphAI.backend.nlp.preprocessing.sentence_segmenter import SentenceSegmenter
from KnowledgeGraphAI.backend.nlp.preprocessing.section_extractor import SectionExtractor
from KnowledgeGraphAI.backend.nlp.preprocessing.schemas import PreprocessingResult, ExtractedParagraph, ExtractedSentence

logger = logging.getLogger(__name__)

class NLPProcessingPipeline:
    """
    Unified Preprocessing Pipeline for KnowledgeGraphAI Phase 2.1.
    Executes PDF Extraction -> Cleaning -> Paragraph Segmentation -> Section Detection -> Sentence Segmentation.
    """

    def __init__(self, paper_id: int, file_path: str):
        self.paper_id = paper_id
        self.file_path = file_path

    def process(self) -> Dict[str, Any]:
        """
        Execute the complete preprocessing pipeline on a PDF file.
        """
        start_time = time.time()
        warnings = []

        try:
            # 1. PDF Extraction
            pdf_data = PDFIngestionService.extract_pdf_data(self.file_path, paper_id=self.paper_id)
            warnings.extend(pdf_data.get("warnings", []))

            if not pdf_data.get("has_extractable_text"):
                raise ValueError("PDF contains no extractable text. OCR may be required.")

            total_paragraphs = 0
            total_sentences = 0
            extracted_paragraphs = []

            # 2. Page-wise Processing
            for page in pdf_data.get("pages", []):
                page_num = page["page_number"]
                raw_text = page["text"]

                # 3. Text Cleaning
                cleaned_page_text = TextCleaner.clean_scientific_text(raw_text)
                if not cleaned_page_text:
                    continue

                # 4. Section Detection.  A page may contain more than one
                # section, so resolve the section for each paragraph rather
                # than applying the first heading to its entire page.
                sections = SectionExtractor.extract_sections(cleaned_page_text)

                # 5. Paragraph Segmentation (by double newline)
                raw_paragraphs = cleaned_page_text.split('\n\n')
                paragraph_cursor = 0

                for p_idx, para in enumerate(raw_paragraphs):
                    para_cleaned = para.strip()
                    if not para_cleaned:
                        continue

                    line_offset = cleaned_page_text[:paragraph_cursor].count("\n")
                    paragraph_cursor += len(para) + 2
                    current_section = next(
                        (
                            section["section_name"]
                            for section in sections
                            if section["start_line"] <= line_offset < section["end_line"]
                        ),
                        "UNKNOWN",
                    )

                    # 6. Sentence Segmentation
                    sentences_data = SentenceSegmenter.segment_sentences(
                        cleaned_text=para_cleaned,
                        paper_id=self.paper_id,
                        page_number=page_num,
                        section_name=current_section
                    )

                    extracted_sentences = []
                    for s_data in sentences_data:
                        extracted_sentences.append(ExtractedSentence(
                            paper_id=self.paper_id,
                            page_number=page_num,
                            section_name=current_section,
                            paragraph_index=total_paragraphs,
                            sentence_index=total_sentences,
                            original_text=s_data["original_text"],
                            cleaned_text=s_data["cleaned_text"]
                        ))
                        total_sentences += 1

                    extracted_paragraphs.append(ExtractedParagraph(
                        paper_id=self.paper_id,
                        page_number=page_num,
                        paragraph_index=total_paragraphs,
                        section_name=current_section,
                        original_text=para,
                        cleaned_text=para_cleaned,
                        sentence_count=len(extracted_sentences),
                        sentences=extracted_sentences
                    ))
                    total_paragraphs += 1

            processing_time = round(time.time() - start_time, 3)

            statistics = {
                "total_pages": pdf_data.get("page_count", 0),
                "total_paragraphs": total_paragraphs,
                "total_sentences": total_sentences,
                "total_text_length": pdf_data.get("total_text_length", 0)
            }

            processing_metadata = {
                "processing_time_seconds": processing_time,
                "pipeline_version": "2.1",
                "title": pdf_data.get("title"),
                "author": pdf_data.get("author")
            }

            result = PreprocessingResult(
                paper_id=self.paper_id,
                processing_status="completed",
                statistics=statistics,
                paragraphs=extracted_paragraphs,
                processing_metadata=processing_metadata,
                warnings=warnings
            )

            return asdict(result)

        except Exception as e:
            logger.exception(f"Preprocessing failed for paper {self.paper_id}")
            raise
