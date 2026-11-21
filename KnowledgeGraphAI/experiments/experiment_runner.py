"""Reproducible, baseline-first experiment bookkeeping.

This utility records configurations and actual outcomes only.  It never
creates placeholder scores: an experiment remains ``not_run`` until a supplied
runner produces measured metrics from an explicitly identified dataset.
"""

from __future__ import annotations

import json
import random
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Optional


ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"


@dataclass(frozen=True)
class ExperimentSpec:
    name: str
    research_question: str
    dataset_description: str
    seed: int
    strategy: str
    metrics: list[str]
    parameters: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_file(cls, path: Path) -> "ExperimentSpec":
        payload = json.loads(path.read_text(encoding="utf-8"))
        required = ("name", "research_question", "dataset_description", "seed", "strategy", "metrics")
        missing = [key for key in required if key not in payload]
        if missing:
            raise ValueError(f"Experiment configuration missing: {', '.join(missing)}")
        if not isinstance(payload["metrics"], list) or not payload["metrics"]:
            raise ValueError("Experiment metrics must be a non-empty list")
        return cls(**payload)


def result_path(spec: ExperimentSpec) -> Path:
    safe_name = "".join(char if char.isalnum() or char in "-_" else "_" for char in spec.name)
    return RESULTS_DIR / f"{safe_name}.json"


def record_not_run(spec: ExperimentSpec, reason: str) -> Path:
    """Persist an honest pending result without inventing measurements."""

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output = {
        "schema_version": 1,
        "status": "not_run",
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "spec": asdict(spec),
        "reason": reason,
        "metrics": {},
    }
    target = result_path(spec)
    target.write_text(json.dumps(output, indent=2), encoding="utf-8")
    return target


def run_measured(
    spec: ExperimentSpec,
    runner: Callable[[ExperimentSpec], Dict[str, Any]],
) -> Path:
    """Run a caller-provided measurement and persist its raw returned metrics."""

    random.seed(spec.seed)
    metrics = runner(spec)
    if not isinstance(metrics, dict) or not metrics:
        raise ValueError("Runner returned no measured metrics; no result was recorded")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output = {
        "schema_version": 1,
        "status": "complete",
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "spec": asdict(spec),
        "metrics": metrics,
    }
    target = result_path(spec)
    target.write_text(json.dumps(output, indent=2), encoding="utf-8")
    return target
