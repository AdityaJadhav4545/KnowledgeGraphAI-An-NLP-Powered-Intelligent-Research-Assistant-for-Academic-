"""Read-only experiment registry; values originate from saved measured runs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from fastapi import APIRouter

from KnowledgeGraphAI.backend.config import PROJECT_ROOT


router = APIRouter(prefix="/api/experiments", tags=["experiments"])
_EXPERIMENTS = PROJECT_ROOT / "experiments"


def _json_files(directory: Path) -> List[Dict[str, Any]]:
    if not directory.is_dir():
        return []
    items: List[Dict[str, Any]] = []
    for path in sorted(directory.glob("*.json")):
        try:
            items.append({"file": path.name, "data": json.loads(path.read_text(encoding="utf-8"))})
        except (OSError, json.JSONDecodeError):
            items.append({"file": path.name, "data": {"status": "unreadable"}})
    return items


@router.get("")
async def experiment_registry() -> Dict[str, Any]:
    return {
        "configurations": _json_files(_EXPERIMENTS / "configs"),
        "results": _json_files(_EXPERIMENTS / "results"),
    }
