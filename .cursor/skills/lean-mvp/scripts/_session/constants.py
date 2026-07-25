"""Constants and compiled patterns for the lean-mvp session package."""

from __future__ import annotations

import re
from typing import Any

MODULE_ORDER = (
    "customer-context",
    "underserved-needs",
    "mvp-scope",
    "ux-prototype",
    "metrics",
)
MODULE_PHASE = {
    "customer-context": "Step 1: Target Customer",
    "underserved-needs": "Step 2: Underserved Needs",
    "mvp-scope": "Steps 3–4: Value Prop & MVP Features",
    "ux-prototype": "Steps 5–6: Prototype & Customer Test",
    "metrics": "Post-Launch Optimization",
}
GATE_ARTIFACTS = {
    "customer-context": "customer-context.md",
    "underserved-needs": "underserved-needs.md",
    "mvp-scope": "mvp-scope.md",
    "ux-prototype": "ux-prototype.md",
    "metrics": "metrics.md",
}
MILESTONE_TEMPLATES = {
    "customer-context": "customer-context.template.md",
    "underserved-needs": "underserved-needs.template.md",
    "mvp-scope": "mvp-scope.template.md",
    "ux-prototype": "ux-prototype.template.md",
    "metrics": "metrics.template.md",
}
DESIGN_BRIEFS: tuple[tuple[str, str], ...] = ()
BUILD_PACK_FILES: tuple[tuple[str, str], ...] = ()
VALUE_TRAIL_CRUMBS: tuple[dict[str, Any], ...] = ()
_NUMBERED_ITEM_RE = re.compile(r"\((\d+)\)\s*")
_LINE_ITEM_RE = re.compile(
    r"(?:^|\n)\s*(?:[-*•]|\(?\d+[\)\].:])\s+",
    flags=re.MULTILINE,
)
_EXTREME_PAIN_RE = re.compile(r"\b(extreme|severe)\b", flags=re.IGNORECASE)
HARD_DECISION_MARKERS = (
    "bypass",
    "reopen",
    "segment boundary",
    "excluded",
    "park",
    "non-goal",
    "out of scope",
    "defer delighter",
)
CANONICAL_GATE_PASS = {
    "customer-context": "pass customer-context gate",
    "underserved-needs": "pass underserved-needs gate",
    "mvp-scope": "pass mvp-scope gate",
    "ux-prototype": "pass ux-prototype gate",
    "metrics": "pass metrics gate",
}
EXPRESS_SPINE: dict[str, tuple[str, ...]] = {
    "customer-context": ("C01", "C05", "C12"),
    "underserved-needs": ("U01", "U05", "U12"),
    "mvp-scope": ("MS01", "MS05", "MS12"),
    "ux-prototype": ("UX01", "UX04", "UX12"),
    "metrics": ("MT01", "MT04", "MT12"),
}
EXPRESS_REQUIRES: dict[str, tuple[str, ...]] = {
    "C05": ("C01",),
    "C12": ("C05",),
    "U05": ("U01",),
    "U12": ("U05",),
    "MS05": ("MS01",),
    "MS12": ("MS05",),
    "UX04": ("UX01",),
    "UX12": ("UX04",),
    "MT04": ("MT01",),
    "MT12": ("MT04",),
}
PACING_MODES = ("standard", "express")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MODULE_BRIEF_LABEL = {
    "customer-context": "Target customer",
    "underserved-needs": "Underserved needs",
    "mvp-scope": "MVP scope",
    "ux-prototype": "UX prototype",
    "metrics": "Metrics",
}
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
UNKNOWN_FIELDS = ("question", "blocking")
ARTIFACT_FIELDS = ("path", "status")
