"""Opt-in LLM relevance suggestions for the local annotation workflow."""

import json
import math
import os
import re
import time
from typing import Any, Dict, Optional

import requests


AUTOMATED_LABELS = {"relevant", "not_relevant", "uncertain"}


def _decode_suggestion_json(content: Any) -> Any:
    if isinstance(content, dict):
        return content
    if not isinstance(content, str):
        raise ValueError("LLM response content must be JSON text or an object")
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        decoder = json.JSONDecoder()
        for match in re.finditer(r"\{", content):
            try:
                decoded, _end = decoder.raw_decode(content[match.start():])
                return decoded
            except json.JSONDecodeError:
                continue
    raise ValueError("LLM returned an invalid JSON suggestion response")


def _validate_suggestion(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("LLM response must be a JSON object")
    label = payload.get("label")
    explanation = payload.get("explanation")
    confidence = payload.get("confidence")
    if not isinstance(label, str) or label not in AUTOMATED_LABELS:
        raise ValueError("LLM label must be relevant, not_relevant, or uncertain")
    if (
        isinstance(confidence, bool)
        or not isinstance(confidence, (int, float))
        or not math.isfinite(float(confidence))
        or not 0.0 <= float(confidence) <= 1.0
    ):
        raise ValueError("LLM confidence must be a finite number from 0 to 1")
    if not isinstance(explanation, str) or not explanation.strip():
        raise ValueError("LLM explanation must be a non-empty string")
    return {
        "label": label,
        "confidence": float(confidence),
        "explanation": explanation.strip()[:1000],
    }


def suggest_relevance(
    query: str,
    title: str,
    abstract: str,
    passage: Optional[str] = None,
    *,
    base_url: Optional[str] = None,
    model: Optional[str] = None,
    timeout_seconds: float = 120.0,
    max_retries: int = 2,
    retry_backoff_seconds: float = 0.5,
) -> Dict[str, Any]:
    """Request a strict JSON relevance suggestion from an Ollama-compatible API.

    The default endpoint is local. No request is made unless this function is
    explicitly invoked by the reviewer.
    """
    endpoint = (base_url or os.getenv(
        "ANNOTATION_LLM_BASE_URL", "http://localhost:11434"
    )).rstrip("/")
    model_name = (model or os.getenv("ANNOTATION_LLM_MODEL", "llama3.1")).strip()
    if not model_name:
        raise ValueError("ANNOTATION_LLM_MODEL cannot be empty")
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")
    if isinstance(max_retries, bool) or max_retries < 0:
        raise ValueError("max_retries must be a non-negative integer")
    if retry_backoff_seconds < 0:
        raise ValueError("retry_backoff_seconds must be non-negative")
    if not query.strip() or not title.strip() or not abstract.strip():
        raise ValueError("query, title, and abstract are required")
    candidate_text = (
        f"Retrieved passage:\n{passage.strip()}"
        if passage and passage.strip()
        else "No retrieved passage was supplied; assess the paper using its title and abstract."
    )
    prompt = (
        "Assess whether the candidate is relevant to the research query. "
        "Use only the supplied evidence. Return exactly one JSON object with "
        'keys "label" (relevant, not_relevant, or uncertain), "confidence" '
        "(number from 0 to 1), and \"explanation\" (brief evidence-based reason). "
        "Use uncertain when evidence is insufficient. This is only a suggestion; "
        "do not claim a human reviewed it.\n\n"
        f"Query:\n{query}\n\nPaper title:\n{title}\n\n"
        f"Abstract:\n{abstract}\n\n{candidate_text}"
    )
    payload = {
        "model": model_name,
        "stream": False,
        "format": "json",
        "messages": [{"role": "user", "content": prompt}],
    }
    last_error: Optional[Exception] = None
    for attempt in range(max_retries + 1):
        try:
            response = requests.post(
                f"{endpoint}/api/chat",
                json=payload,
                timeout=timeout_seconds,
            )
            response.raise_for_status()
            body = response.json()
            content = body["message"]["content"]
            suggestion = _validate_suggestion(_decode_suggestion_json(content))
            suggestion["model"] = model_name
            return suggestion
        except (requests.RequestException, KeyError, TypeError, ValueError) as exc:
            last_error = exc
            if attempt >= max_retries:
                break
            time.sleep(retry_backoff_seconds * (2 ** attempt))
    if isinstance(last_error, requests.RequestException):
        raise last_error
    raise ValueError(
        f"LLM failed to produce a valid suggestion after {max_retries + 1} attempts: "
        f"{last_error}"
    ) from last_error
