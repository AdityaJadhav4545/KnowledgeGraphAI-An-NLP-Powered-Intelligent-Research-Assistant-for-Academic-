"""Small deployment-safe authorization dependency.

Local development remains frictionless by default.  Production must opt into a
non-empty API key through centralized settings; the key itself is never
returned, logged, or embedded in generated documentation.
"""

from __future__ import annotations

import secrets
from typing import Optional

from fastapi import Header, HTTPException, status

from KnowledgeGraphAI.backend.config import get_settings


def require_write_access(x_api_key: Optional[str] = Header(default=None)) -> None:
    settings = get_settings()
    if not settings.require_authentication:
        return
    if not settings.api_key or not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication is required for this operation.",
        )
    if not secrets.compare_digest(x_api_key, settings.api_key):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials.",
        )
