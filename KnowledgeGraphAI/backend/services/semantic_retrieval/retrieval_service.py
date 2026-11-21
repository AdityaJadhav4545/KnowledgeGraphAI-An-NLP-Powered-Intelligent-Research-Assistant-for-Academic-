"""End-to-end semantic indexing and retrieval for scientific PDF passages."""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import numpy as np

from KnowledgeGraphAI.backend.nlp.preprocessing.pipeline import NLPProcessingPipeline
from KnowledgeGraphAI.backend.services.pdf_ingestion import PDFIngestionService
from KnowledgeGraphAI.backend.services.knowledge_graph.graph_query import GraphQueryService
from KnowledgeGraphAI.backend.services.knowledge_graph.neo4j_connection import (
    get_neo4j_manager,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.chunking_service import (
    ScientificChunkingService,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.config import (
    SemanticRetrievalConfig,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.embedding_service import (
    Specter2EmbeddingService,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.schemas import (
    ScientificChunk,
    SearchResult,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.vector_store import (
    FaissVectorStore,
)

logger = logging.getLogger(__name__)


class SemanticRetrievalService:
    """Chunk, embed, persist, and search passages linked to Neo4j paper IDs."""

    MAX_QUERY_LENGTH = 20_000
    MAX_TOP_K = 1_000

    def __init__(
        self,
        config: Optional[SemanticRetrievalConfig] = None,
        chunker: Optional[ScientificChunkingService] = None,
        embedding_service: Optional[Specter2EmbeddingService] = None,
        vector_store: Optional[FaissVectorStore] = None,
        neo4j_manager: Any = None,
    ) -> None:
        self.config = config or SemanticRetrievalConfig.from_env()
        self.chunker = chunker or ScientificChunkingService(
            self.config.chunk_size, self.config.chunk_overlap
        )
        self.embedding_service = embedding_service or Specter2EmbeddingService(self.config)
        if vector_store is None:
            from KnowledgeGraphAI.backend.services.semantic_retrieval.metadata_store import (
                ChunkMetadataStore,
            )

            index_path = self.config.index_dir / self.config.index_name
            vector_store = FaissVectorStore(
                self.config.embedding_dimension,
                index_path,
                metadata_store=ChunkMetadataStore(),
            )
        self.vector_store = vector_store
        self.neo4j = neo4j_manager or get_neo4j_manager()

    @staticmethod
    def _paper_exists(manager: Any, paper_id: int) -> bool:
        try:
            records = manager.execute_query(
                "MATCH (p:Paper {paper_id: $paper_id}) RETURN p.paper_id AS paper_id LIMIT 1",
                {"paper_id": paper_id},
            )
            return bool(records)
        except Exception:
            return False

    def index_pdf(
        self,
        pdf_path: str,
        paper_id: int,
        *,
        validate_graph: bool = True,
        paper_title: Optional[str] = None,
        source_identifier: Optional[str] = None,
    ) -> List[ScientificChunk]:
        """Run existing PDF extraction/preprocessing and index the resulting chunks.

        ``paper_id`` must already identify a Neo4j Paper node; this keeps the
        graph's canonical paper ID as the retrieval metadata reference.
        """
        if isinstance(paper_id, bool) or not isinstance(paper_id, int) or paper_id < 0:
            raise ValueError("paper_id must be a non-negative integer")
        path = Path(pdf_path)
        if not path.is_file():
            raise FileNotFoundError(f"PDF not found: {path}")
        if validate_graph and not self._paper_exists(self.neo4j, paper_id):
            raise ValueError(f"Neo4j Paper node does not exist for paper_id={paper_id}")

        pdf_data = PDFIngestionService.extract_pdf_data(str(path), paper_id=paper_id)
        preprocessing = NLPProcessingPipeline(paper_id, str(path)).process()
        page_texts = {
            page["page_number"]: page["text"] for page in pdf_data.get("pages", [])
        }
        chunks = self.chunker.chunk(preprocessing, path.name, page_texts=page_texts)
        if not chunks:
            raise ValueError(f"No non-empty text chunks were produced for paper_id={paper_id}")

        title = paper_title or pdf_data.get("title") or ""
        vectors = self.embedding_service.embed_documents(
            [chunk.text for chunk in chunks],
            titles=[title] * len(chunks),
        )
        chunk_records = [
            {
                **chunk.to_dict(),
                "title": title,
                "source_identifier": source_identifier,
            }
            for chunk in chunks
        ]
        self.vector_store.add(chunk_records, vectors)
        logger.info(
            "Indexed %s semantic chunks for paper_id=%s.",
            len(chunks),
            paper_id,
        )
        return chunks

    def index_preprocessed(
        self,
        preprocessing_result: Dict[str, Any],
        source_document: str,
        page_texts: Optional[Dict[int, str]] = None,
        paper_title: Optional[str] = None,
        *,
        validate_graph: bool = True,
        source_identifier: Optional[str] = None,
    ) -> List[ScientificChunk]:
        """Index existing preprocessing output for controlled integrations."""
        paper_id = preprocessing_result.get("paper_id")
        if (
            isinstance(paper_id, bool)
            or not isinstance(paper_id, int)
            or paper_id < 0
        ):
            raise ValueError("preprocessing_result must contain a non-negative integer paper_id")
        if validate_graph and not self._paper_exists(self.neo4j, paper_id):
            raise ValueError(f"Neo4j Paper node does not exist for paper_id={paper_id}")
        chunks = self.chunker.chunk(
            preprocessing_result,
            source_document,
            page_texts=page_texts,
        )
        if not chunks:
            return []
        vectors = self.embedding_service.embed_documents(
            [chunk.text for chunk in chunks],
            titles=[paper_title] * len(chunks),
        )
        chunk_records = [
            {
                **chunk.to_dict(),
                "title": paper_title,
                "source_identifier": source_identifier,
            }
            for chunk in chunks
        ]
        self.vector_store.add(chunk_records, vectors)
        logger.info("Indexed %s chunks for paper_id=%s.", len(chunks), paper_id)
        return chunks

    def search(
        self,
        query: str,
        top_k: int = 5,
        *,
        paper_id: Optional[int] = None,
        paper_ids: Optional[Sequence[int]] = None,
        page_number: Optional[int] = None,
        section_title: Optional[str] = None,
        min_similarity: Optional[float] = None,
        aggregate_by_paper: bool = False,
        diversity: bool = False,
        diversity_lambda: float = 0.7,
    ) -> List[Dict[str, Any]]:
        """Search chunks with exact metadata filters and optional MMR diversity.

        ``similarity_score`` always remains the original FAISS cosine score.
        When ``diversity`` is enabled, ``reranking_score`` is standard MMR:
        lambda times query relevance minus (1-lambda) times maximum redundancy.
        The selector first covers unrepresented papers when available, then
        applies the same-paper redundancy penalty; neither step changes or
        conflates the original similarity score.
        """
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")
        if len(query) > self.MAX_QUERY_LENGTH:
            raise ValueError(f"query cannot exceed {self.MAX_QUERY_LENGTH} characters")
        if (
            isinstance(top_k, bool)
            or not isinstance(top_k, int)
            or not 1 <= top_k <= self.MAX_TOP_K
        ):
            raise ValueError(f"top_k must be between 1 and {self.MAX_TOP_K}")
        if paper_id is not None and (
            isinstance(paper_id, bool) or not isinstance(paper_id, int) or paper_id < 0
        ):
            raise ValueError("paper_id must be a non-negative integer")
        if paper_ids is not None:
            if isinstance(paper_ids, (str, bytes)) or not isinstance(paper_ids, Sequence):
                raise ValueError("paper_ids must be a sequence of non-negative integers")
            if any(
                isinstance(value, bool) or not isinstance(value, int) or value < 0
                for value in paper_ids
            ):
                raise ValueError("paper_ids must contain non-negative integers")
            paper_ids = tuple(dict.fromkeys(paper_ids))
        if page_number is not None and (
            isinstance(page_number, bool)
            or not isinstance(page_number, int)
            or page_number < 1
        ):
            raise ValueError("page_number must be a positive integer")
        if section_title is not None and (
            not isinstance(section_title, str) or not section_title.strip()
        ):
            raise ValueError("section_title must be a non-empty string")
        if min_similarity is not None and (
            isinstance(min_similarity, bool)
            or not isinstance(min_similarity, (int, float))
            or not -1.0 <= min_similarity <= 1.0
        ):
            raise ValueError("min_similarity must be between -1 and 1")
        if not isinstance(aggregate_by_paper, bool) or not isinstance(diversity, bool):
            raise ValueError("aggregate_by_paper and diversity must be booleans")
        if (
            isinstance(diversity_lambda, bool)
            or not isinstance(diversity_lambda, (int, float))
            or not 0.0 <= diversity_lambda <= 1.0
        ):
            raise ValueError("diversity_lambda must be between 0 and 1")
        if self.vector_store.count == 0:
            return []

        query_vector = self.embedding_service.embed_queries([query])[0]
        total_vectors = self.vector_store.count
        candidate_count = (
            total_vectors
            if aggregate_by_paper
            else min(total_vectors, max(top_k * 4, 32))
        )
        candidates: List[Dict[str, Any]] = []
        seen_chunks = set()

        while True:
            matches = self.vector_store.search(query_vector, candidate_count)
            metadata = self.vector_store.get_metadata(
                [vector_id for vector_id, _ in matches]
            )
            candidates = []
            seen_chunks.clear()
            for vector_id, score in matches:
                record = metadata.get(vector_id)
                if (
                    not record
                    or not isinstance(record.get("chunk_id"), str)
                    or not record["chunk_id"]
                    or not isinstance(record.get("text"), str)
                    or not record["text"].strip()
                ):
                    continue
                try:
                    record_paper_id = int(record["paper_id"])
                    record_page = record.get("page_number")
                    similarity = max(-1.0, min(1.0, float(score)))
                    if record_page is not None:
                        record_page = int(record_page)
                except (KeyError, TypeError, ValueError) as exc:
                    logger.warning(
                        "Skipping malformed semantic metadata for vector_id=%s: %s",
                        vector_id,
                        exc,
                    )
                    continue
                if paper_id is not None and record_paper_id != paper_id:
                    continue
                if paper_ids is not None and record_paper_id not in paper_ids:
                    continue
                if page_number is not None and record_page != page_number:
                    continue
                if section_title is not None and (
                    not isinstance(record.get("section_title"), str)
                    or record["section_title"].strip().casefold()
                    != section_title.strip().casefold()
                ):
                    continue
                if min_similarity is not None and similarity < min_similarity:
                    continue
                if record["chunk_id"] in seen_chunks:
                    continue
                seen_chunks.add(record["chunk_id"])
                candidates.append({
                    "vector_id": vector_id,
                    "paper_id": record_paper_id,
                    "page_number": record_page,
                    "section_title": record.get("section_title"),
                    "similarity_score": similarity,
                    "metadata": record,
                })

            distinct_count = (
                len({candidate["paper_id"] for candidate in candidates})
                if aggregate_by_paper
                else len(candidates)
            )
            if (
                aggregate_by_paper
                or distinct_count >= top_k
                or candidate_count >= total_vectors
            ):
                break
            candidate_count = min(total_vectors, candidate_count * 2)

        candidates.sort(key=lambda item: item["similarity_score"], reverse=True)
        if diversity and candidates:
            vector_records = self.vector_store.get_vectors(
                [candidate["vector_id"] for candidate in candidates]
            )
            selected: List[Dict[str, Any]] = []
            remaining = list(candidates)
            while remaining and len(selected) < len(candidates):
                best_candidate = None
                best_score = float("-inf")
                represented_papers = {
                    previous["paper_id"] for previous in selected
                }
                unrepresented = [
                    candidate
                    for candidate in remaining
                    if candidate["paper_id"] not in represented_papers
                ]
                eligible = unrepresented or remaining
                for candidate in eligible:
                    vector = vector_records.get(candidate["vector_id"])
                    if vector is None or vector.size != query_vector.size:
                        raise RuntimeError(
                            "Missing or incompatible stored vector required for MMR reranking"
                        )
                    redundancy = 0.0
                    if selected:
                        redundancy = max(
                            1.0
                            if candidate["paper_id"] == previous["paper_id"]
                            else float(np.dot(vector, vector_records[previous["vector_id"]]))
                            for previous in selected
                        )
                    reranking_score = (
                        float(diversity_lambda) * candidate["similarity_score"]
                        - (1.0 - float(diversity_lambda)) * redundancy
                    )
                    if reranking_score > best_score:
                        best_candidate = candidate
                        best_score = reranking_score
                assert best_candidate is not None
                best_candidate["reranking_score"] = best_score
                selected.append(best_candidate)
                remaining.remove(best_candidate)
            candidates = selected

        if aggregate_by_paper:
            grouped: Dict[int, List[Dict[str, Any]]] = {}
            for candidate in candidates:
                grouped.setdefault(candidate["paper_id"], []).append(candidate)
            candidates = []
            for paper_candidates in grouped.values():
                representative = dict(paper_candidates[0])
                representative["matched_chunk_count"] = len(paper_candidates)
                candidates.append(representative)
            candidates.sort(
                key=lambda item: item.get(
                    "reranking_score", item["similarity_score"]
                ),
                reverse=True,
            )

        results: List[Dict[str, Any]] = []
        for candidate in candidates[:top_k]:
            record = candidate["metadata"]
            results.append(SearchResult(
                rank=len(results) + 1,
                paper_id=candidate["paper_id"],
                chunk_id=record["chunk_id"],
                text=record["text"],
                similarity_score=candidate["similarity_score"],
                page_number=candidate["page_number"],
                section_title=candidate["section_title"],
                chunk_index=int(record["chunk_index"]),
                start_char=record.get("start_char"),
                end_char=record.get("end_char"),
                source_document=record.get("source_document"),
                title=record.get("title"),
                source_identifier=record.get("source_identifier"),
                reranking_score=candidate.get("reranking_score"),
            ).to_dict())
            if aggregate_by_paper:
                results[-1]["matched_chunk_count"] = candidate["matched_chunk_count"]
        return results

    def get_paper_context(self, paper_id: int) -> Dict[str, Any]:
        """Retrieve the existing graph entities and relationships for a paper."""
        graph = GraphQueryService()
        return {
            "paper_id": paper_id,
            "entities": graph.get_paper_entities(paper_id),
            "relationships": graph.get_paper_relationships(paper_id),
        }

    def delete_paper(self, paper_id: int) -> int:
        """Remove vector records for a paper and rebuild the FAISS index."""
        return self.vector_store.delete_paper(paper_id)
