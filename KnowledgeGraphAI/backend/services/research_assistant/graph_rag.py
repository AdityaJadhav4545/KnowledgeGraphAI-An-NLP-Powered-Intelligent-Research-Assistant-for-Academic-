"""Evidence-first GraphRAG orchestration for the research assistant.

The service intentionally separates retrieval from generation: citations are
constructed from real indexed passages before an LLM is asked to write, and an
unavailable/mis-grounded LLM degrades to an evidence-only response.
"""

from __future__ import annotations

import logging
import re
from dataclasses import asdict, dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence

import requests

from KnowledgeGraphAI.backend.config import Settings, get_settings


logger = logging.getLogger(__name__)
_CITATION_RE = re.compile(r"\[(S\d+)\]")


class ResearchAssistantError(RuntimeError):
    pass


@dataclass(frozen=True)
class QueryUnderstanding:
    intent: str
    mentioned_terms: List[str]
    comparison_requested: bool
    gap_analysis_requested: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _json_value(value: Any) -> Any:
    """Convert Neo4j/driver values to response-safe basic Python objects."""

    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_value(item) for item in value]
    items = getattr(value, "items", None)
    if callable(items):
        try:
            return {str(key): _json_value(item) for key, item in value.items()}
        except (TypeError, ValueError):
            pass
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


class GraphRAGService:
    MAX_QUERY_LENGTH = 20_000

    def __init__(
        self,
        *,
        settings: Optional[Settings] = None,
        semantic_service: Any = None,
        graph_query_service: Any = None,
        http_session: Any = requests,
    ) -> None:
        self.settings = settings or get_settings()
        self._semantic_service = semantic_service
        self._graph_query_service = graph_query_service
        self.http = http_session

    @staticmethod
    def understand_query(query: str) -> QueryUnderstanding:
        normalized = query.casefold()
        comparison = any(token in normalized for token in ("compare", "versus", " vs ", "difference"))
        gaps = any(token in normalized for token in ("research gap", "research gaps", "underexplored", "future work"))
        if gaps:
            intent = "research_gap_analysis"
        elif comparison:
            intent = "comparison"
        elif any(token in normalized for token in ("which papers", "find papers", "papers using")):
            intent = "paper_discovery"
        else:
            intent = "evidence_question"
        terms = list(
            dict.fromkeys(
                token
                for token in re.findall(r"\b[A-Za-z][A-Za-z0-9+_.-]{2,}\b", query)
                if token.casefold() not in {"what", "which", "does", "with", "that", "from", "about", "research"}
            )
        )[:20]
        return QueryUnderstanding(intent, terms, comparison, gaps)

    def _semantic(self) -> Any:
        if self._semantic_service is None:
            from KnowledgeGraphAI.backend.services.semantic_retrieval.retrieval_service import (
                SemanticRetrievalService,
            )

            self._semantic_service = SemanticRetrievalService()
        return self._semantic_service

    def _graph(self) -> Any:
        if self._graph_query_service is None:
            from KnowledgeGraphAI.backend.services.knowledge_graph.graph_query import (
                GraphQueryService,
            )

            self._graph_query_service = GraphQueryService()
        return self._graph_query_service

    @staticmethod
    def _sources(results: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
        sources: List[Dict[str, Any]] = []
        for index, result in enumerate(results, start=1):
            text = str(result.get("text") or "").strip()
            if not text:
                continue
            sources.append(
                {
                    "citation_id": f"S{index}",
                    "paper_id": result.get("paper_id"),
                    "title": result.get("title") or "Untitled paper",
                    "source_identifier": result.get("source_identifier"),
                    "page_number": result.get("page_number"),
                    "section_title": result.get("section_title"),
                    "chunk_id": result.get("chunk_id"),
                    "similarity_score": result.get("similarity_score"),
                    "reranking_score": result.get("reranking_score"),
                    "passage": text,
                }
            )
        return sources

    def _graph_context(
        self,
        sources: Sequence[Dict[str, Any]],
        understanding: Optional[QueryUnderstanding] = None,
    ) -> Dict[str, Any]:
        paper_ids = list(
            dict.fromkeys(
                int(source["paper_id"])
                for source in sources
                if isinstance(source.get("paper_id"), int)
            )
        )[:5]
        if not paper_ids:
            return {"available": False, "papers": [], "subgraph": [], "error": "No paper identifiers were retrieved."}
        contexts: List[Dict[str, Any]] = []
        subgraph: List[Dict[str, Any]] = []
        seen_edges: set[tuple[str, str, str]] = set()
        try:
            graph = self._graph()
            for paper_id in paper_ids:
                entities = _json_value(graph.get_paper_entities(paper_id))
                relationships = _json_value(graph.get_paper_relationships(paper_id))
                contexts.append(
                    {
                        "paper_id": paper_id,
                        "entities": entities,
                        "relationships": relationships,
                    }
                )
            search_fn = getattr(graph, "search_entities", None)
            neighbors_fn = getattr(graph, "get_entity_neighbors", None)
            if callable(search_fn) and callable(neighbors_fn) and understanding and understanding.mentioned_terms:
                for term in understanding.mentioned_terms[:5]:
                    for match in search_fn(term, limit=2) or []:
                        eid = match.get("entity_id")
                        labels = match.get("labels") or []
                        etype = match.get("type") or (labels[0] if labels else "Model")
                        if not eid:
                            continue
                        for nb in _json_value(neighbors_fn(eid, etype, limit=8) or []):
                            nb_node = nb.get("neighbor") if isinstance(nb.get("neighbor"), dict) else nb
                            src = str(match.get("canonical_name") or term)
                            rel = str(nb.get("relationship_type") or nb.get("relation") or "RELATED_TO")
                            tgt = str(
                                nb_node.get("canonical_name")
                                or nb_node.get("title")
                                or nb_node.get("name")
                                or nb_node.get("entity_id")
                                or ""
                            )
                            if tgt and (src, rel, tgt) not in seen_edges:
                                seen_edges.add((src, rel, tgt))
                                subgraph.append({
                                    "source": src,
                                    "relation": rel,
                                    "target": tgt,
                                    "target_labels": nb.get("labels", []),
                                })
            return {"available": True, "papers": contexts, "subgraph": subgraph[:25]}
        except Exception as exc:
            logger.info("Graph context unavailable: %s", exc)
            return {
                "available": False,
                "papers": [],
                "subgraph": [],
                "error": "Graph context is currently unavailable.",
            }

    @staticmethod
    def _evidence_only_answer(sources: Sequence[Dict[str, Any]]) -> str:
        if not sources:
            return (
                "I could not find indexed evidence sufficient to answer this question. "
                "Try broadening the query or process additional papers."
            )
        lines = ["The local language model is unavailable, so this is an evidence-only response:"]
        for source in sources[:5]:
            title = source["title"]
            page = f", p. {source['page_number']}" if source.get("page_number") else ""
            excerpt = source["passage"].replace("\n", " ").strip()
            if len(excerpt) > 400:
                excerpt = excerpt[:397].rstrip() + "..."
            lines.append(f"- {title}{page}: {excerpt} [{source['citation_id']}]")
        return "\n".join(lines)

    @staticmethod
    def _prompt(query: str, understanding: QueryUnderstanding, sources: Sequence[Dict[str, Any]], graph_context: Dict[str, Any]) -> str:
        evidence = []
        for source in sources:
            location = []
            if source.get("page_number") is not None:
                location.append(f"page {source['page_number']}")
            if source.get("section_title"):
                location.append(str(source["section_title"]))
            evidence.append(
                f"[{source['citation_id']}] Title: {source['title']}"
                f" ({', '.join(location) or 'location unavailable'})\n"
                f"Passage: {source['passage']}"
            )
        paper_to_citations: Dict[int, List[str]] = {}
        for source in sources:
            pid = source.get("paper_id")
            if isinstance(pid, int):
                paper_to_citations.setdefault(pid, []).append(source["citation_id"])

        graph_summary = "No graph context is available."
        if graph_context.get("available"):
            graph_lines = [
                "Knowledge graph facts retrieved from Neo4j for the cited papers (cite the matching [S#] passage when referencing these):"
            ]
            for paper_entry in graph_context.get("papers", [])[:5]:
                pid = paper_entry.get("paper_id")
                cits = ", ".join(f"[{c}]" for c in paper_to_citations.get(pid, [])[:3])
                entity_names = []
                for ent in paper_entry.get("entities", [])[:15]:
                    if isinstance(ent, dict):
                        node = ent.get("e") if isinstance(ent.get("e"), dict) else ent
                        name = node.get("canonical_name") or node.get("name")
                        labels = ent.get("labels") or []
                        if name:
                            entity_names.append(f"{name} ({labels[0]})" if labels else str(name))
                entity_names = list(dict.fromkeys(entity_names))
                if entity_names:
                    graph_lines.append(f"- Paper {pid} {cits} entities: {', '.join(entity_names[:12])}")
                rel_items = []
                for rel in paper_entry.get("relationships", [])[:15]:
                    if isinstance(rel, dict):
                        subj = rel.get("subject") or ""
                        rtype = rel.get("relation") or rel.get("relationship_type") or ""
                        obj = rel.get("object") or ""
                        if subj and rtype and obj:
                            rel_items.append(f"{subj} -[{rtype}]-> {obj}")
                        elif rtype:
                            rel_items.append(str(rtype))
                rel_items = list(dict.fromkeys(rel_items))
                if rel_items:
                    graph_lines.append(f"- Paper {pid} {cits} relationships: {'; '.join(rel_items[:12])}")
            subgraph_triples = [
                f"{edge['source']} -[{edge['relation']}]-> {edge['target']}"
                for edge in graph_context.get("subgraph", [])[:12]
                if isinstance(edge, dict) and edge.get("source") and edge.get("target")
            ]
            if subgraph_triples:
                graph_lines.append(f"- Subgraph neighbors: {'; '.join(subgraph_triples)}")
            graph_summary = "\n".join(graph_lines)
        gap_instruction = (
            "If discussing gaps, label each as a hypothesis requiring validation; do not present it as an established fact."
            if understanding.gap_analysis_requested
            else ""
        )
        return (
            "You are an evidence-grounded academic research assistant. Answer only from the supplied "
            "evidence. Every factual sentence and every performance comparison must end with one or "
            "more citations in the exact form [S1]. Do not invent papers, authors, results, metrics, "
            "or citations. If the evidence is insufficient, say so plainly. "
            "Use concise sections: Direct answer, Technical explanation, Limitations, Further reading. "
            f"{gap_instruction}\n\nQuestion: {query}\nIntent: {understanding.intent}\n\n"
            f"{graph_summary}\n\nEvidence:\n" + "\n\n".join(evidence)
        )

    @staticmethod
    def _grounded_text(answer: str, allowed_ids: set[str]) -> Optional[str]:
        """Keep only answer blocks with at least one valid evidence citation."""

        if not isinstance(answer, str) or not answer.strip():
            return None
        blocks: List[str] = []
        for block in re.split(r"\n\s*\n", answer.strip()):
            citations = set(_CITATION_RE.findall(block))
            invalid = citations.difference(allowed_ids)
            if invalid:
                block = _CITATION_RE.sub(lambda match: "" if match.group(1) in invalid else match.group(0), block)
                citations = set(_CITATION_RE.findall(block))
            # Headings contain no factual claim and make the rendered response
            # easier to read; all other retained blocks need evidence.
            if citations or re.fullmatch(r"[A-Za-z ][A-Za-z :&-]{1,80}", block.strip()):
                blocks.append(block.strip())
        result = "\n\n".join(blocks).strip()
        return result if set(_CITATION_RE.findall(result)).intersection(allowed_ids) else None

    def _generate(self, query: str, understanding: QueryUnderstanding, sources: Sequence[Dict[str, Any]], graph_context: Dict[str, Any]) -> Optional[str]:
        payload = {
            "model": self.settings.ollama_model,
            "stream": False,
            "messages": [{"role": "user", "content": self._prompt(query, understanding, sources, graph_context)}],
            "options": {"temperature": 0.1},
        }
        try:
            response = self.http.post(
                f"{self.settings.ollama_base_url}/api/chat",
                json=payload,
                timeout=self.settings.ollama_timeout_seconds,
            )
            response.raise_for_status()
            body = response.json()
            return self._grounded_text(
                body.get("message", {}).get("content", ""),
                {source["citation_id"] for source in sources},
            )
        except (requests.RequestException, ValueError, KeyError, TypeError) as exc:
            logger.info("Ollama answer generation unavailable: %s", exc)
            return None

    @staticmethod
    def _gap_hypotheses(sources: Sequence[Dict[str, Any]]) -> List[Dict[str, str]]:
        hypotheses: List[Dict[str, str]] = []
        for source in sources:
            passage = source["passage"]
            if re.search(r"\b(limitations?|future work|remains? (?:unclear|limited)|challenge)\b", passage, re.I):
                hypotheses.append(
                    {
                        "hypothesis": "This passage signals a possible research gap that needs independent validation.",
                        "evidence_citation": source["citation_id"],
                        "status": "hypothesis",
                    }
                )
            if len(hypotheses) >= 5:
                break
        if not hypotheses and sources:
            hypotheses.append(
                {
                    "hypothesis": "The retrieved evidence does not establish a research gap; additional corpus coverage and human review are needed.",
                    "evidence_citation": sources[0]["citation_id"],
                    "status": "insufficient_evidence",
                }
            )
        return hypotheses

    def ask(self, query: str, *, top_k: int = 8) -> Dict[str, Any]:
        if not isinstance(query, str) or not query.strip():
            raise ResearchAssistantError("A non-empty question is required.")
        if len(query) > self.MAX_QUERY_LENGTH:
            raise ResearchAssistantError(f"Question cannot exceed {self.MAX_QUERY_LENGTH} characters.")
        if isinstance(top_k, bool) or not isinstance(top_k, int) or not 1 <= top_k <= 20:
            raise ResearchAssistantError("top_k must be between 1 and 20.")
        understanding = self.understand_query(query)
        try:
            results = self._semantic().search(
                query,
                top_k=top_k,
                diversity=True,
                diversity_lambda=0.7,
            )
        except Exception as exc:
            raise ResearchAssistantError("Semantic retrieval is unavailable; no answer was generated.") from exc
        sources = self._sources(results)
        graph_context = self._graph_context(sources, understanding=understanding)
        answer = self._generate(query, understanding, sources, graph_context)
        generation_mode = "ollama_grounded" if answer else "evidence_only"
        if not answer:
            answer = self._evidence_only_answer(sources)
        response: Dict[str, Any] = {
            "question": query,
            "query_understanding": understanding.to_dict(),
            "answer": answer,
            "generation_mode": generation_mode,
            "citations": sources,
            "retrieved_passages": sources,
            "graph_context": graph_context,
            "limitations": [
                "Answers are limited to the locally indexed corpus and retrieved passages.",
                "Graph-derived context is omitted when Neo4j is unavailable.",
            ],
        }
        if understanding.gap_analysis_requested:
            response["research_gap_hypotheses"] = self._gap_hypotheses(sources)
        return response
