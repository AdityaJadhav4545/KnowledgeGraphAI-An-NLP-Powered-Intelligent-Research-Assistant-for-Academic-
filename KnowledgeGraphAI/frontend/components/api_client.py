"""Shared HTTP client for Streamlit-to-FastAPI requests."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterator, Mapping, Optional
from urllib.parse import urljoin

import requests

_SHARED_CLIENT_SESSION = requests.Session()


@dataclass(frozen=True)
class APIResult:
    status_code: Optional[int]
    data: Any = None
    error: Optional[str] = None
    content_type: str = ""

    @property
    def ok(self) -> bool:
        return self.status_code is not None and 200 <= self.status_code < 300

    @property
    def available(self) -> bool:
        return self.status_code is not None


class APIClient:
    """Keep base URL, auth headers, timeouts, and response parsing in one place."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        session: Any = None,
    ) -> None:
        self.base_url = (base_url or os.getenv(
            "API_BASE_URL", "http://localhost:8000"
        )).rstrip("/") + "/"
        self.api_key = api_key if api_key is not None else os.getenv("API_KEY", "")
        self.session = session if session is not None else _SHARED_CLIENT_SESSION

    @property
    def headers(self) -> dict[str, str]:
        return {"X-API-Key": self.api_key} if self.api_key else {}

    def request(
        self,
        method: str,
        path: str,
        *,
        timeout: int = 10,
        params: Optional[Mapping[str, Any]] = None,
        files: Any = None,
        data: Any = None,
        json_body: Any = None,
    ) -> APIResult:
        try:
            response = self.session.request(
                method,
                urljoin(self.base_url, path.lstrip("/")),
                headers=self.headers,
                timeout=timeout,
                params=params,
                files=files,
                data=data,
                json=json_body,
            )
        except requests.RequestException as exc:
            return APIResult(None, error=f"Could not reach the backend: {exc}")

        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type.lower():
            try:
                body = response.json()
            except ValueError:
                body = None
                error = "The backend returned invalid JSON."
            else:
                detail = body.get("detail") if isinstance(body, dict) else None
                error = self._format_error(detail) if detail else None
        else:
            body = response.content
            error = None

        if not response.ok and not error:
            error = f"Backend request failed with HTTP {response.status_code}."
        return APIResult(response.status_code, body, error, content_type)

    @staticmethod
    def _format_error(detail: Any) -> str:
        if isinstance(detail, dict):
            stage = detail.get("stage")
            message = detail.get("message") or detail.get("detail")
            if stage and message:
                return f"{stage}: {message}"
            return str(message or detail)
        if isinstance(detail, list):
            messages = [
                str(item.get("msg", item)) if isinstance(item, dict) else str(item)
                for item in detail
            ]
            return "; ".join(messages)
        return str(detail)

    def get(self, path: str, *, timeout: int = 10, params=None) -> APIResult:
        return self.request("GET", path, timeout=timeout, params=params)

    def post(
        self,
        path: str,
        *,
        timeout: int = 30,
        files=None,
        data=None,
        json_body=None,
    ) -> APIResult:
        return self.request(
            "POST",
            path,
            timeout=timeout,
            files=files,
            data=data,
            json_body=json_body,
        )

    def stream_post(
        self,
        path: str,
        *,
        timeout: int = 180,
        json_body: Any = None,
    ) -> Iterator[Dict[str, Any]]:
        """Stream SSE JSON events from a FastAPI POST endpoint."""
        url = urljoin(self.base_url, path.lstrip("/"))
        headers = {**self.headers, "Accept": "text/event-stream"}
        try:
            with self.session.request(
                "POST",
                url,
                headers=headers,
                timeout=timeout,
                json=json_body,
                stream=True,
            ) as response:
                if not response.ok:
                    err_msg = f"Backend request failed with HTTP {response.status_code}."
                    content_type = response.headers.get("content-type", "")
                    if "application/json" in content_type.lower():
                        try:
                            body = response.json()
                            detail = body.get("detail") if isinstance(body, dict) else None
                            if detail:
                                err_msg = self._format_error(detail)
                        except ValueError:
                            pass
                    yield {
                        "type": "error",
                        "status_code": response.status_code,
                        "detail": err_msg,
                    }
                    return

                for raw_line in response.iter_lines(decode_unicode=True):
                    if not raw_line:
                        continue
                    line = raw_line.strip()
                    if not line.startswith("data:"):
                        continue
                    payload_str = line[5:].strip()
                    if not payload_str:
                        continue
                    try:
                        event = json.loads(payload_str)
                    except ValueError:
                        continue
                    if isinstance(event, dict):
                        yield event
        except requests.RequestException as exc:
            yield {
                "type": "error",
                "status_code": None,
                "detail": f"Could not reach the backend: {exc}",
            }

    def delete(self, path: str, *, timeout: int = 10) -> APIResult:
        return self.request("DELETE", path, timeout=timeout)
