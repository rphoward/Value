"""Shared helpers for hillclimb CLI subcommands."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from eliotapp.core.eliot.scorecard import extract_style_block

REPO_ROOT = Path(__file__).resolve().parents[5]
DEFAULT_RUNS_BASE = REPO_ROOT / "tools" / "runs"
DEFAULT_PREFERENCE_AGENT = "reference-preference"


def resolve_run_dir_arg(value: str) -> Path:
    return Path(value).resolve()


def agent_prompt_hash(agent: str = DEFAULT_PREFERENCE_AGENT) -> str:
    agent_path = REPO_ROOT / ".cursor" / "agents" / f"{agent}.md"
    if not agent_path.is_file():
        raise ValueError(f"agent prompt not found: {agent_path}")
    return hashlib.sha256(agent_path.read_bytes()).hexdigest()


def rel_under_run(run_dir: Path, path: Path) -> str:
    resolved = path.resolve()
    run_resolved = run_dir.resolve()
    try:
        return str(resolved.relative_to(run_resolved)).replace("\\", "/")
    except ValueError as exc:
        raise ValueError(
            f"path must be relative to run folder {run_resolved}: {path}"
        ) from exc


def resolve_block(raw: str) -> str:
    extracted = extract_style_block(raw)
    return extracted if extracted else raw.strip()


def latest_iteration(run_dir: Path) -> int | None:
    payload = json.loads((run_dir / "scores.json").read_text(encoding="utf-8"))
    iterations = payload.get("iterations") if isinstance(payload, dict) else None
    if not isinstance(iterations, list) or not iterations:
        return None
    return int(iterations[-1]["iteration"])


def read_scores_payload(run_dir: Path) -> dict:
    return json.loads((run_dir / "scores.json").read_text(encoding="utf-8"))


def preference_judge_model(run_dir: Path) -> str:
    payload = read_scores_payload(run_dir)
    model = payload.get("preference_judge_model")
    if not model or str(model).strip().lower() == "inherit":
        raise ValueError(
            "preference_judge_model missing on scores.json; "
            "set it at init (required for reference_preference_v1) "
            "or pass --judge-model on pref-job-open"
        )
    return str(model).strip()
