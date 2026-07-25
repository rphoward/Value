"""Resolve atom-coaching assets into the teaching half of a turn payload."""

from __future__ import annotations

import json
from typing import Any

from .catalog import ASSETS_DIR, atom_provenance_label, load_json
from .runtime import current_answer, is_ceremony_answer

_ATOM_COACHING_FILE = "atom-coaching.json"
_KNOWLEDGE_BASE_FILE = "knowledge-base.json"


def _load_asset(name: str) -> dict[str, Any]:
    """A damaged or absent coaching asset costs the teaching, never the interview."""
    path = ASSETS_DIR / name
    if not path.is_file():
        return {}
    try:
        payload = load_json(path)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def load_atom_coaching() -> dict[str, dict[str, Any]]:
    """Load assets/atom-coaching.json; empty dict when the file is absent."""
    return _load_asset(_ATOM_COACHING_FILE)


def _humanize(key: str) -> str:
    if len(key) <= 2 and key.isupper():
        return key
    return key.replace("_", " ")


def flatten_kb_value(value: Any) -> str:
    """Collapse any knowledge-base value shape into one teaching string."""
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "; ".join(part for part in map(flatten_kb_value, value) if part)
    if isinstance(value, dict):
        clauses = (
            f"{_humanize(key)}: {flatten_kb_value(child)}"
            for key, child in value.items()
            if flatten_kb_value(child)
        )
        return " | ".join(clauses)
    return str(value).strip()


def resolve_kb_ref(knowledge_base: dict[str, Any], ref: str) -> str:
    """Walk a dotted path such as visual_grounding_analogies.follow_me_home."""
    node: Any = knowledge_base
    for segment in ref.split("."):
        if not isinstance(node, dict) or segment not in node:
            return ""
        node = node[segment]
    return flatten_kb_value(node)


def _prior_for(session: dict[str, Any], read: Any) -> dict[str, Any] | None:
    atom_id = read.get("atom") if isinstance(read, dict) else read
    if not isinstance(atom_id, str):
        return None
    prior = {
        "atom_id": atom_id,
        "label": atom_provenance_label(atom_id),
        "why": read.get("why", "") if isinstance(read, dict) else "",
        "status": "missing",
        "answer": None,
    }
    record = current_answer(session, atom_id)
    if record is None:
        return prior
    if is_ceremony_answer(record):
        prior["status"] = "ceremony"
        return prior
    answer = record.get("answer")
    prior["status"] = "ok"
    prior["answer"] = answer if isinstance(answer, str) else None
    return prior


def coaching_for_atom(session: dict[str, Any], atom_id: str) -> dict[str, Any] | None:
    """Resolved coaching block for a turn, or None when the atom has no entry."""
    entry = load_atom_coaching().get(atom_id)
    if not isinstance(entry, dict):
        return None

    knowledge_base = _load_asset(_KNOWLEDGE_BASE_FILE)
    definitions = [
        {"ref": ref, "text": text}
        for ref in entry.get("kb_refs") or []
        if isinstance(ref, str) and (text := resolve_kb_ref(knowledge_base, ref))
    ]
    priors = [
        prior
        for prior in (_prior_for(session, read) for read in entry.get("reads") or [])
        if prior is not None
    ]
    block = {
        "why_it_matters": entry.get("why_it_matters", ""),
        "definitions": definitions,
        "complete_when": list(entry.get("complete_when") or []),
        "worked_example": entry.get("worked_example", ""),
        "common_miss": entry.get("common_miss", ""),
        "priors": priors,
    }
    story_assist = entry.get("story_assist")
    if isinstance(story_assist, str) and story_assist.strip():
        block["story_assist"] = story_assist
    return block
