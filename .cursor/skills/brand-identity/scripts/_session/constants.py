"""Constants loaded from assets/skill-config.json (portable session runtime)."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = SKILL_ROOT / "assets"
_CONFIG_PATH = ASSETS_DIR / "skill-config.json"


def _load_config() -> dict[str, Any]:
    if not _CONFIG_PATH.is_file():
        return {}
    return json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))


_CFG = _load_config()

MODULE_ORDER: tuple[str, ...] = tuple(
    _CFG.get("module_order")
    or ("module-1",)
)
MODULE_PHASE: dict[str, str] = dict(
    _CFG.get("module_phase")
    or {MODULE_ORDER[0]: "Phase 1"}
)
GATE_ARTIFACTS: dict[str, str] = dict(
    _CFG.get("gate_artifacts")
    or {m: f"{m}.md" for m in MODULE_ORDER}
)
MILESTONE_TEMPLATES: dict[str, str] = dict(
    _CFG.get("milestone_templates")
    or {m: f"{m}.template.md" for m in MODULE_ORDER}
)
DESIGN_BRIEFS: tuple[tuple[str, str], ...] = ()
BUILD_PACK_FILES: tuple[tuple[str, str], ...] = ()
VALUE_TRAIL_CRUMBS: tuple[dict[str, Any], ...] = ()
MATCH_BOARD_ATOMS: dict[str, tuple[str, str, str]] = {}
_NUMBERED_ITEM_RE = re.compile(r"\((\d+)\)\s*")
_LINE_ITEM_RE = re.compile(
    r"(?:^|\n)\s*(?:[-*•]|\(?\d+[\)\].:])\s+",
    flags=re.MULTILINE,
)
_EXTREME_PAIN_RE = re.compile(r"\b(extreme|severe)\b", flags=re.IGNORECASE)
HARD_DECISION_MARKERS = tuple(
    _CFG.get("hard_decision_markers")
    or ("bypass", "reopen", "excluded", "park", "non-goal", "out of scope")
)
CANONICAL_GATE_PASS: dict[str, str] = dict(
    _CFG.get("canonical_gate_pass")
    or {m: f"pass {m} gate" for m in MODULE_ORDER}
)
EXPRESS_SPINE: dict[str, tuple[str, ...]] = {
    k: tuple(v) for k, v in (_CFG.get("express_spine") or {}).items()
}
EXPRESS_REQUIRES: dict[str, tuple[str, ...]] = {
    k: tuple(v) for k, v in (_CFG.get("express_requires") or {}).items()
}
PACING_MODES = ("standard", "express")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MODULE_BRIEF_LABEL: dict[str, str] = dict(
    _CFG.get("module_brief_labels")
    or {m: m.replace("-", " ").title() for m in MODULE_ORDER}
)
SECTION_STATE_BRIEF = {
    "partial": "in progress",
    "satisfied": "locked",
    "unknown_ok": "locked",
}
SECTION_STRIP_SYMBOLS = {
    "empty": "·",
    "partial": "◐",
    "satisfied": "✓",
    "unknown_ok": "✓?",
}
EVIDENCE_FIELDS = ("claim", "kind", "source", "strength")
ASSUMPTION_FIELDS = ("claim", "criticality", "evidence_status", "source_atom")
DECISION_FIELDS = (
    "decision",
    "reason",
    "source_atom",
    "resulting_module",
    "resulting_atom",
    "resulting_status",
)
UNKNOWN_FIELDS = ("question", "blocking", "source_atom")
ARTIFACT_FIELDS = ("path", "status")
WORKPRODUCT_ROOT = str(_CFG.get("workproduct_root") or f"workproduct/{SKILL_ROOT.name}")
ENTRY_MODULE = MODULE_ORDER[0]
ENTRY_ATOM = str(_CFG.get("entry_atom") or "M01")
