"""Document-isolated AI Research Assistant for uploaded PDFs and pasted text."""

from __future__ import annotations

import json
import logging
import math
import os
import re
import threading
import time
from typing import Any, Dict, Iterator, List, Optional, Sequence, Tuple

import requests
from sqlalchemy.orm import Session

from KnowledgeGraphAI.backend.config import Settings, get_settings
from KnowledgeGraphAI.backend.services.research_assistant.graph_rag import (
    _CITATION_RE,
    GraphRAGService,
)
from KnowledgeGraphAI.models.analysis import AnalysisRecord

logger = logging.getLogger(__name__)

_SHARED_HTTP_SESSION = requests.Session()
_SEMANTIC_SERVICE_LOCK = threading.Lock()
_SEMANTIC_SERVICE_CACHE: Dict[Tuple[str, str, str], Tuple[Any, float]] = {}


def _default_http_client() -> Any:
    """Use pooled HTTP connections unless ``requests.post`` is patched in tests."""
    if getattr(requests.post, "__module__", "") != "requests.api":
        return requests
    return _SHARED_HTTP_SESSION


def _index_mtime(service: Any) -> float:
    try:
        idx_file = Path_from_service(service)
        return os.path.getmtime(idx_file) if idx_file and os.path.exists(idx_file) else 0.0
    except OSError:
        return 0.0


def Path_from_service(service: Any) -> Optional[str]:
    vs = getattr(service, "vector_store", None)
    path = getattr(vs, "index_path", None)
    if path is None:
        return None
    return f"{path}.faiss"


def get_shared_semantic_service() -> Any:
    """Return a cached ``SemanticRetrievalService`` keyed by active index configuration."""
    from KnowledgeGraphAI.backend.services.semantic_retrieval.config import (
        SemanticRetrievalConfig,
    )
    from KnowledgeGraphAI.backend.services.semantic_retrieval.retrieval_service import (
        SemanticRetrievalService,
    )

    cfg = SemanticRetrievalConfig.from_env()
    key = (str(cfg.index_dir), str(cfg.index_name), str(cfg.model_name))
    with _SEMANTIC_SERVICE_LOCK:
        cached = _SEMANTIC_SERVICE_CACHE.get(key)
        if cached is not None:
            service, cached_mtime = cached
            current_mtime = _index_mtime(service)
            if current_mtime != cached_mtime:
                try:
                    service.vector_store.load()
                except Exception as exc:
                    logger.debug("FAISS index refresh skipped: %s", exc)
                _SEMANTIC_SERVICE_CACHE[key] = (service, current_mtime)
            return service

        service = SemanticRetrievalService(config=cfg)
        _SEMANTIC_SERVICE_CACHE[key] = (service, _index_mtime(service))
        return service

_STOPWORDS = frozenset(
    {
        "the", "and", "for", "with", "that", "this", "from", "are", "was", "were",
        "what", "which", "how", "does", "used", "using", "about", "into", "between",
        "paper", "document", "text", "explain", "describe", "identify", "list",
    }
)


class AnalysisAssistantError(RuntimeError):
    """Raised when an assistant request fails validation."""


def _tokens(text: str) -> List[str]:
    return [
        tok
        for tok in re.findall(r"[A-Za-z0-9][A-Za-z0-9_+.-]{1,}", text.casefold())
        if tok not in _STOPWORDS
    ]


class AnalysisAssistantService:
    """Answer questions strictly scoped to one ``AnalysisRecord``."""

    MAX_QUESTION_LENGTH = 10_000

    def __init__(
        self,
        db: Session,
        *,
        settings: Optional[Settings] = None,
        http_session: Any = None,
        semantic_service: Any = None,
    ) -> None:
        self.db = db
        self.settings = settings or get_settings()
        self.http = http_session if http_session is not None else _default_http_client()
        self._semantic_service = semantic_service

    # ------------------------------------------------------------------
    # Retrieval scoped to the current analysis
    # ------------------------------------------------------------------
    @staticmethod
    def _rank_local_passages(
        question: str,
        passages: Sequence[Dict[str, Any]],
        *,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        if not passages:
            return []
        q_tokens = _tokens(question)
        q_lower = question.casefold()
        is_summary = any(
            kw in q_lower
            for kw in ("summarize", "summary", "overview", "main objective", "conclusion", "findings", "limitation")
        )

        # Compute simple IDF over document passages
        n_docs = len(passages)
        df: Dict[str, int] = {}
        doc_tokens: List[List[str]] = []
        for passage in passages:
            toks = _tokens(str(passage.get("text") or ""))
            doc_tokens.append(toks)
            for t in set(toks):
                df[t] = df.get(t, 0) + 1

        scored: List[Tuple[float, int, Dict[str, Any]]] = []
        for idx, (passage, toks) in enumerate(zip(passages, doc_tokens)):
            tf: Dict[str, int] = {}
            for t in toks:
                tf[t] = tf.get(t, 0) + 1
            score = 0.0
            for qt in q_tokens:
                if qt in tf:
                    idf = math.log(1.0 + (n_docs / (1.0 + df.get(qt, 0))))
                    score += (1.0 + math.log(tf[qt])) * idf
            sec = str(passage.get("section_title") or "").casefold()
            if is_summary and sec in {"abstract", "introduction", "conclusion", "results", "discussion"}:
                score += 1.5
            if "limitation" in q_lower and re.search(
                r"\b(limit|limitation|future work|drawback|challenge|constraint|shortcoming)\b",
                str(passage.get("text") or ""),
                re.I,
            ):
                score += 2.0
            scored.append((score, idx, dict(passage)))

        scored.sort(key=lambda item: (-item[0], item[1]))
        selected = [item[2] for item in scored[:top_k]]
        # Always include the opening passage for summary questions if not already selected
        if is_summary and passages and all(
            p.get("passage_id") != passages[0].get("passage_id") for p in selected
        ):
            selected = [dict(passages[0]), *selected[: max(0, top_k - 1)]]
        return selected

    def _retrieve_passages(
        self,
        record: AnalysisRecord,
        question: str,
        *,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        local_passages = list(record.passages_json or [])
        ranked_local = self._rank_local_passages(question, local_passages, top_k=top_k)

        merged: List[Dict[str, Any]] = []
        seen_texts: set[str] = set()

        # When PDF has indexed FAISS chunks, retrieve strictly scoped to record.paper_id
        if record.source_type == "pdf" and record.paper_id is not None:
            try:
                if self._semantic_service is None:
                    self._semantic_service = get_shared_semantic_service()
                if self._semantic_service.vector_store.count > 0:
                    hits = self._semantic_service.search(
                        question,
                        top_k=top_k,
                        paper_id=int(record.paper_id),
                        diversity=True,
                    )
                    for hit in hits:
                        txt = str(hit.get("text") or "").strip()
                        norm = txt[:160].casefold()
                        if txt and norm not in seen_texts:
                            seen_texts.add(norm)
                            page = hit.get("page_number")
                            sec = hit.get("section_title") or "Document"
                            merged.append(
                                {
                                    "source_ref": f"Page {page}" if page else sec,
                                    "page_number": page,
                                    "section_title": sec,
                                    "text": txt,
                                    "similarity_score": hit.get("similarity_score"),
                                }
                            )
            except Exception as exc:
                logger.info("Scoped semantic retrieval fallback to local passages: %s", exc)

        for passage in ranked_local:
            txt = str(passage.get("text") or "").strip()
            norm = txt[:160].casefold()
            if txt and norm not in seen_texts:
                seen_texts.add(norm)
                merged.append(passage)
            if len(merged) >= top_k:
                break

        citations: List[Dict[str, Any]] = []
        for idx, item in enumerate(merged[:top_k], start=1):
            citations.append(
                {
                    "citation_id": f"S{idx}",
                    "title": record.title,
                    "source_type": record.source_type,
                    "page_number": item.get("page_number"),
                    "section_title": item.get("section_title"),
                    "source_ref": item.get("source_ref")
                    or (f"Page {item['page_number']}" if item.get("page_number") else "Document"),
                    "passage": str(item.get("text") or "").strip(),
                    "similarity_score": item.get("similarity_score"),
                }
            )
        return citations

    @staticmethod
    def _extract_graph_context(record: AnalysisRecord, question: str) -> Dict[str, Any]:
        graph = record.graph_json or {}
        nodes = list(graph.get("nodes") or [])
        edges = list(graph.get("edges") or [])
        q_tokens = set(_tokens(question))

        matched_nodes = [
            n
            for n in nodes
            if any(tok in str(n.get("label") or "").casefold() for tok in q_tokens)
            or any(tok in str(n.get("category") or "").casefold() for tok in q_tokens)
        ]
        if not matched_nodes:
            matched_nodes = nodes[:8]

        matched_ids = {n["id"] for n in matched_nodes if "id" in n}
        connected_edges = [
            e
            for e in edges
            if e.get("source") in matched_ids or e.get("target") in matched_ids
        ]
        if not connected_edges:
            connected_edges = edges[:10]

        return {
            "available": bool(nodes or edges),
            "entity_count": len(nodes),
            "relationship_count": len(edges),
            "entities": [
                {
                    "label": n.get("label"),
                    "category": n.get("category"),
                    "occurrences": n.get("occurrences", 1),
                    "source_refs": n.get("source_refs", []),
                }
                for n in matched_nodes[:12]
            ],
            "relationships": [
                {
                    "subject": e.get("source_label"),
                    "relation": e.get("relation"),
                    "object": e.get("target_label"),
                    "source_ref": e.get("source_ref"),
                    "evidence": e.get("evidence"),
                }
                for e in connected_edges[:12]
            ],
        }

    # ------------------------------------------------------------------
    # Prompting & Grounded Generation
    # ------------------------------------------------------------------
    @staticmethod
    def _compact_passage(text: str, max_chars: int = 750) -> str:
        clean = " ".join(str(text or "").split())
        if len(clean) <= max_chars:
            return clean
        clipped = clean[: max_chars - 3].rsplit(" ", 1)[0].rstrip(" ,;:")
        return (clipped or clean[: max_chars - 3]).strip() + "..."

    @classmethod
    def _build_prompt(
        cls,
        record: AnalysisRecord,
        question: str,
        citations: Sequence[Dict[str, Any]],
        graph_context: Dict[str, Any],
    ) -> str:
        evidence_blocks: List[str] = []
        used_chars = 0
        budget_chars = 2600
        for c in citations:
            loc = c.get("source_ref") or "Document"
            excerpt = cls._compact_passage(str(c.get("passage") or ""), max_chars=750)
            block = f"[{c['citation_id']}] ({loc}) {excerpt}"
            if evidence_blocks and used_chars + len(block) > budget_chars:
                break
            evidence_blocks.append(block)
            used_chars += len(block)

        graph_line = "None."
        if graph_context.get("available"):
            seen_rels: set[Tuple[str, str, str]] = set()
            compact_rels: List[str] = []
            for r in graph_context.get("relationships", []):
                subj = str(r.get("subject") or "").strip()
                rel = str(r.get("relation") or "").strip()
                obj = str(r.get("object") or "").strip()
                if not (subj and rel and obj):
                    continue
                sig = (subj.casefold(), rel.casefold(), obj.casefold())
                if sig in seen_rels:
                    continue
                seen_rels.add(sig)
                compact_rels.append(f"{subj} -[{rel}]-> {obj}")
                if len(compact_rels) >= 8:
                    break

            seen_ents: set[str] = set()
            compact_ents: List[str] = []
            for e in graph_context.get("entities", []):
                lbl = str(e.get("label") or "").strip()
                if not lbl or lbl.casefold() in seen_ents:
                    continue
                seen_ents.add(lbl.casefold())
                cat = str(e.get("category") or "").strip()
                compact_ents.append(f"{lbl} ({cat})" if cat else lbl)
                if len(compact_ents) >= 8:
                    break

            parts: List[str] = []
            if compact_ents:
                parts.append("Entities: " + ", ".join(compact_ents))
            if compact_rels:
                parts.append("Relations: " + "; ".join(compact_rels))
            if parts:
                graph_line = " | ".join(parts)

        return (
            f"Answer concisely using ONLY the evidence below for \"{record.title}\". "
            "End every factual sentence with citation(s) like [S1]. "
            "Note if a connection is graph-inferred, and say clearly if the document does not state the answer.\n\n"
            f"Graph: {graph_line}\n\n"
            "Passages:\n"
            + ("\n".join(evidence_blocks) or "No passages available.")
            + f"\n\nQuestion: {question}"
        )

    @staticmethod
    def _evidence_fallback(
        question: str,
        citations: Sequence[Dict[str, Any]],
        graph_context: Dict[str, Any],
    ) -> str:
        if not citations:
            return (
                "The analyzed document does not contain enough extractable text to answer "
                "this question."
            )
        lines = [
            "Here is the grounded evidence retrieved from the analyzed document "
            "(local language model unavailable or timed out):"
        ]
        for c in citations[:4]:
            excerpt = c["passage"].replace("\n", " ").strip()
            if len(excerpt) > 360:
                excerpt = excerpt[:357].rstrip() + "..."
            lines.append(f"- ({c.get('source_ref', 'Source')}) {excerpt} [{c['citation_id']}]")
        rels = graph_context.get("relationships", [])[:5]
        if rels:
            rel_txt = "; ".join(
                f"{r['subject']} {r['relation']} {r['object']}" for r in rels
            )
            lines.append(f"\nConnected knowledge graph relationships: {rel_txt}.")
        return "\n".join(lines)

    @staticmethod
    def _finalize_grounded_answer(
        raw_answer: str,
        allowed_ids: set[str],
        primary_citation_id: Optional[str] = None,
    ) -> Optional[str]:
        grounded = GraphRAGService._grounded_text(raw_answer, allowed_ids)
        if grounded:
            return grounded
        if not isinstance(raw_answer, str) or not raw_answer.strip() or not allowed_ids:
            return None
        found_cites = set(_CITATION_RE.findall(raw_answer))
        # Reject responses that cited non-existent sources.
        if found_cites - allowed_ids:
            return None
        cleaned = raw_answer.strip()
        if primary_citation_id and primary_citation_id in allowed_ids:
            if cleaned.endswith((".", "!", "?")):
                return f"{cleaned[:-1]} [{primary_citation_id}]{cleaned[-1]}"
            return f"{cleaned} [{primary_citation_id}]"
        return None

    def _ollama_payload(self, prompt: str, *, stream: bool) -> Dict[str, Any]:
        return {
            "model": self.settings.ollama_model,
            "stream": stream,
            "keep_alive": self.settings.ollama_keep_alive,
            "messages": [{"role": "user", "content": prompt}],
            "options": {
                "temperature": 0.1,
                "num_ctx": self.settings.ollama_num_ctx,
                "num_predict": self.settings.ollama_num_predict,
                "num_thread": self.settings.ollama_num_thread,
            },
        }

    @staticmethod
    def _extract_ollama_metrics(data: Dict[str, Any]) -> Dict[str, Any]:
        load_ms = round(float(data.get("load_duration") or 0) / 1e6, 2)
        pe_ms = round(float(data.get("prompt_eval_duration") or 0) / 1e6, 2)
        ev_ms = round(float(data.get("eval_duration") or 0) / 1e6, 2)
        pe_tok = int(data.get("prompt_eval_count") or 0)
        ev_tok = int(data.get("eval_count") or 0)
        tok_s = round(ev_tok / (ev_ms / 1000.0), 2) if ev_ms > 0 and ev_tok > 0 else 0.0
        return {
            "ollama_load_ms": load_ms,
            "ollama_prompt_eval_ms": pe_ms,
            "ollama_eval_ms": ev_ms,
            "prompt_tokens": pe_tok,
            "generated_tokens": ev_tok,
            "tokens_per_second": tok_s,
            "model_reloaded": load_ms > 500.0,
        }

    def _call_ollama_with_metrics(
        self,
        prompt: str,
        allowed_ids: set[str],
        primary_citation_id: Optional[str] = None,
    ) -> Tuple[Optional[str], Dict[str, Any]]:
        payload = self._ollama_payload(prompt, stream=False)
        try:
            resp = self.http.post(
                f"{self.settings.ollama_base_url}/api/chat",
                json=payload,
                timeout=self.settings.ollama_timeout_seconds,
            )
            resp.raise_for_status()
            body = resp.json()
            raw = (body.get("message") or {}).get("content", "")
            metrics = self._extract_ollama_metrics(body)
            answer = self._finalize_grounded_answer(
                raw, allowed_ids, primary_citation_id=primary_citation_id
            )
            return answer, metrics
        except (requests.RequestException, OSError, ValueError, KeyError, TypeError) as exc:
            logger.info("Ollama generation fallback triggered: %s", exc)
            return None, {}

    def _call_ollama(self, prompt: str, allowed_ids: set[str]) -> Optional[str]:
        primary_id = sorted(allowed_ids)[0] if allowed_ids else None
        answer, _ = self._call_ollama_with_metrics(
            prompt, allowed_ids, primary_citation_id=primary_id
        )
        return answer

    # ------------------------------------------------------------------
    # Public chat entrypoint (sync + real SSE streaming)
    # ------------------------------------------------------------------
    def _prepare_turn_inputs(
        self,
        analysis_id: str,
        question: str,
        *,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        req_t0 = time.perf_counter()
        if not isinstance(question, str) or not question.strip():
            raise AnalysisAssistantError("Please enter a question.")
        clean_q = question.strip()
        if len(clean_q) > self.MAX_QUESTION_LENGTH:
            raise AnalysisAssistantError(
                f"Question cannot exceed {self.MAX_QUESTION_LENGTH:,} characters."
            )

        t_db0 = time.perf_counter()
        record = (
            self.db.query(AnalysisRecord)
            .filter(AnalysisRecord.id == analysis_id)
            .first()
        )
        db_lookup_ms = round((time.perf_counter() - t_db0) * 1000.0, 2)
        if record is None:
            raise KeyError(f"Analysis {analysis_id} not found")
        if record.status != "completed":
            raise AnalysisAssistantError("Analysis must complete before asking questions.")

        t_ret0 = time.perf_counter()
        citations = self._retrieve_passages(record, clean_q, top_k=top_k)
        retrieval_ms = round((time.perf_counter() - t_ret0) * 1000.0, 2)

        t_graph0 = time.perf_counter()
        graph_context = self._extract_graph_context(record, clean_q)
        graph_ms = round((time.perf_counter() - t_graph0) * 1000.0, 2)

        t_prompt0 = time.perf_counter()
        prompt = self._build_prompt(record, clean_q, citations, graph_context)
        prompt_ms = round((time.perf_counter() - t_prompt0) * 1000.0, 2)

        allowed_ids = {c["citation_id"] for c in citations}
        primary_citation_id = citations[0]["citation_id"] if citations else None

        return {
            "req_t0": req_t0,
            "record": record,
            "analysis_id": analysis_id,
            "question": clean_q,
            "citations": citations,
            "graph_context": graph_context,
            "prompt": prompt,
            "allowed_ids": allowed_ids,
            "primary_citation_id": primary_citation_id,
            "prep_timing": {
                "db_lookup_ms": db_lookup_ms,
                "retrieval_ms": retrieval_ms,
                "graph_ms": graph_ms,
                "prompt_ms": prompt_ms,
                "passages_retrieved": len(citations),
                "prompt_chars": len(prompt),
            },
        }

    def _commit_turn(
        self,
        prepared: Dict[str, Any],
        *,
        answer: str,
        mode: str,
        ollama_metrics: Dict[str, Any],
        ttft_ms: Optional[float] = None,
    ) -> Dict[str, Any]:
        t_post0 = time.perf_counter()
        record: AnalysisRecord = prepared["record"]
        timing: Dict[str, Any] = {
            **prepared["prep_timing"],
            "ollama_load_ms": ollama_metrics.get("ollama_load_ms", 0.0),
            "ollama_prompt_eval_ms": ollama_metrics.get("ollama_prompt_eval_ms", 0.0),
            "ollama_eval_ms": ollama_metrics.get("ollama_eval_ms", 0.0),
            "prompt_tokens": ollama_metrics.get("prompt_tokens", 0),
            "generated_tokens": ollama_metrics.get("generated_tokens", 0),
            "tokens_per_second": ollama_metrics.get("tokens_per_second", 0.0),
            "model_reloaded": ollama_metrics.get("model_reloaded", False),
            "ttft_ms": round(ttft_ms, 2) if ttft_ms is not None else None,
        }
        turn_base = {
            "question": prepared["question"],
            "answer": answer,
            "generation_mode": mode,
            "citations": prepared["citations"],
            "graph_context": prepared["graph_context"],
        }
        history = list(record.chat_history_json or [])
        postprocess_ms = round((time.perf_counter() - t_post0) * 1000.0, 2)
        total_ms = round((time.perf_counter() - prepared["req_t0"]) * 1000.0, 2)
        timing["postprocess_ms"] = postprocess_ms
        timing["total_ms"] = total_ms
        turn = {**turn_base, "timing": timing}
        history.append(turn)
        record.chat_history_json = history[-30:]
        self.db.commit()

        logger.info(
            "assistant_ask analysis_id=%s mode=%s retrieval_ms=%.2f graph_ms=%.2f "
            "prompt_ms=%.2f load_ms=%.2f prompt_eval_ms=%.2f eval_ms=%.2f ttft_ms=%s "
            "total_ms=%.2f passages=%d prompt_tokens=%d generated_tokens=%d tok_s=%.2f",
            prepared["analysis_id"],
            mode,
            timing["retrieval_ms"],
            timing["graph_ms"],
            timing["prompt_ms"],
            timing["ollama_load_ms"],
            timing["ollama_prompt_eval_ms"],
            timing["ollama_eval_ms"],
            f"{timing['ttft_ms']:.2f}" if timing["ttft_ms"] is not None else "n/a",
            timing["total_ms"],
            timing["passages_retrieved"],
            timing["prompt_tokens"],
            timing["generated_tokens"],
            timing["tokens_per_second"],
        )
        return turn

    def ask(self, analysis_id: str, question: str, *, top_k: int = 5) -> Dict[str, Any]:
        prepared = self._prepare_turn_inputs(analysis_id, question, top_k=top_k)
        citations = prepared["citations"]
        ollama_metrics: Dict[str, Any] = {}
        answer: Optional[str] = None
        if citations:
            answer, ollama_metrics = self._call_ollama_with_metrics(
                prepared["prompt"],
                prepared["allowed_ids"],
                primary_citation_id=prepared["primary_citation_id"],
            )
        mode = "ollama_grounded" if answer else "evidence_only"
        if not answer:
            answer = self._evidence_fallback(
                prepared["question"], citations, prepared["graph_context"]
            )
        return self._commit_turn(
            prepared,
            answer=answer,
            mode=mode,
            ollama_metrics=ollama_metrics,
        )

    def prepare_stream(
        self, analysis_id: str, question: str, *, top_k: int = 5
    ) -> Dict[str, Any]:
        """Validate inputs and compute retrieval/graph/prompt context prior to SSE headers."""
        return self._prepare_turn_inputs(analysis_id, question, top_k=top_k)

    def stream_events(self, prepared: Dict[str, Any]) -> Iterator[Dict[str, Any]]:
        """Yield incremental ``meta``, ``token``, ``done`` (or ``error``) events for SSE."""
        citations = prepared["citations"]
        graph_context = prepared["graph_context"]
        yield {
            "type": "meta",
            "question": prepared["question"],
            "citations": citations,
            "graph_context": graph_context,
            "timing": dict(prepared["prep_timing"]),
        }

        if not citations:
            fallback = self._evidence_fallback(prepared["question"], citations, graph_context)
            turn = self._commit_turn(
                prepared, answer=fallback, mode="evidence_only", ollama_metrics={}
            )
            yield {"type": "done", "turn": turn}
            return

        payload = self._ollama_payload(prepared["prompt"], stream=True)
        chunks: List[str] = []
        final_metrics: Dict[str, Any] = {}
        ttft_ms: Optional[float] = None
        stream_failed = False

        try:
            with self.http.post(
                f"{self.settings.ollama_base_url}/api/chat",
                json=payload,
                stream=True,
                timeout=self.settings.ollama_timeout_seconds,
            ) as resp:
                resp.raise_for_status()
                for raw_line in resp.iter_lines(decode_unicode=True):
                    if not raw_line:
                        continue
                    try:
                        chunk = json.loads(raw_line)
                    except ValueError:
                        continue
                    tok = (chunk.get("message") or {}).get("content", "")
                    if tok:
                        if ttft_ms is None:
                            ttft_ms = (time.perf_counter() - prepared["req_t0"]) * 1000.0
                        chunks.append(tok)
                        yield {"type": "token", "content": tok}
                    if chunk.get("done"):
                        final_metrics = self._extract_ollama_metrics(chunk)
                        break
        except (requests.RequestException, OSError, ValueError, KeyError, TypeError) as exc:
            logger.info("Ollama streaming fallback triggered: %s", exc)
            stream_failed = True

        raw_answer = "".join(chunks)
        answer = None if (stream_failed and not raw_answer.strip()) else self._finalize_grounded_answer(
            raw_answer,
            prepared["allowed_ids"],
            primary_citation_id=prepared["primary_citation_id"],
        )
        mode = "ollama_grounded" if answer else "evidence_only"
        if not answer:
            answer = self._evidence_fallback(prepared["question"], citations, graph_context)

        try:
            turn = self._commit_turn(
                prepared,
                answer=answer,
                mode=mode,
                ollama_metrics=final_metrics,
                ttft_ms=ttft_ms,
            )
        except Exception as exc:
            logger.exception("Failed persisting streamed assistant turn")
            yield {"type": "error", "detail": f"Unable to save assistant response: {exc}"}
            return

        yield {"type": "done", "turn": turn}

    def ask_stream(
        self, analysis_id: str, question: str, *, top_k: int = 5
    ) -> Iterator[Dict[str, Any]]:
        prepared = self.prepare_stream(analysis_id, question, top_k=top_k)
        return self.stream_events(prepared)

    def clear_chat(self, analysis_id: str) -> None:
        record = (
            self.db.query(AnalysisRecord)
            .filter(AnalysisRecord.id == analysis_id)
            .first()
        )
        if record is None:
            raise KeyError(f"Analysis {analysis_id} not found")
        record.chat_history_json = []
        self.db.commit()
