"""Shared helpers and constants for value skill package tests."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


def repo_root() -> Path:
    """Locate the repository root from this test module."""
    here = Path(__file__).resolve()
    for candidate in (here.parent, *here.parents):
        if (candidate / "pyproject.toml").is_file():
            return candidate
    raise RuntimeError(
        "Could not locate repository root from tests/value_skill_support.py"
    )


ROOT = repo_root()
CANONICAL_SKILL_ROOT = ROOT / "skills" / "value"
SKILL_ROOT = ROOT / ".cursor" / "skills" / "value"
SKILL_MD = SKILL_ROOT / "SKILL.md"
REFERENCES_DIR = SKILL_ROOT / "references"
ASSETS_DIR = SKILL_ROOT / "assets"
SCRIPTS_DIR = SKILL_ROOT / "scripts"

REFERENCE_FILES = (
    "profile.md",
    "value-map.md",
    "business-model.md",
    "experiments.md",
    "session-contract.md",
    "export-lenses.md",
)

MODULE_FILES = (
    "profile.md",
    "value-map.md",
    "business-model.md",
    "experiments.md",
)

MODULE_NAMES = {
    "profile.md": "profile",
    "value-map.md": "value-map",
    "business-model.md": "business-model",
    "experiments.md": "experiments",
}

TEMPLATE_FILES = (
    "customer-profile.template.md",
    "value-map.template.md",
    "business-model.template.md",
    "experiment-plan.template.md",
    "product-design-brief.template.md",
    "ux-brief.template.md",
    "app-design-brief.template.md",
    "test-card.template.md",
    "learning-card.template.md",
    "CONTEXT.product.template.md",
    "AGENTS.product.template.md",
    "ui-copy.template.md",
    "states-and-flows.template.md",
    "first-value.template.md",
    "north-star-blurb.template.md",
    "value-trail.template.md",
)

SYNC_IGNORE_NAMES = {".DS_Store", "Thumbs.db"}


def iter_skill_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.name not in SYNC_IGNORE_NAMES
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    )

REQUIRED_KB_KEYS = (
    "visual_grounding_analogies",
    "customer_profile_triggers",
    "high_value_job_rubric",
    "value_map_categories",
    "osterwalder_7_bm_questions",
    "experiment_library",
    "data_traps",
    "validation_funnel",
    "phase_module_map",
)

REQUIRED_SCHEMA_PROPERTIES = (
    "schema_version",
    "project",
    "position",
    "ledger",
    "answers",
    "evidence",
    "assumptions",
    "decisions",
    "unknowns",
    "artifacts",
)

ATOM_FIELDS = ("id", "teaches", "asks", "accepts", "writes", "unlocks")

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
REFERENCE_LINK_RE = re.compile(r"references/([^\s\"')\]]+)")
ATOM_ID_RE = re.compile(r"\(id\s+([^)\s]+)\)")
BRACKET_TOKEN_RE = re.compile(r"\[[^\]\r\n]+\](?!\s*\()")


def read_skill_md() -> str:
    if not SKILL_MD.is_file():
        raise FileNotFoundError(f"Missing skill entrypoint: {SKILL_MD}")
    return SKILL_MD.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> str:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return ""
    return match.group(1)


def frontmatter_field(block: str, field: str) -> str:
    folded = re.search(rf"^{field}:\s*>\s*\n((?:  .+\n?)+)", block, re.MULTILINE)
    if folded:
        lines = folded.group(1).splitlines()
        return " ".join(
            line[2:] if line.startswith("  ") else line.strip() for line in lines
        ).strip()

    inline = re.search(rf"^{field}:\s*(.+)$", block, re.MULTILINE)
    if not inline:
        return ""

    value = inline.group(1).strip()
    if value == ">":
        return ""
    return value.strip("\"'")


def extract_reference_links(text: str) -> list[str]:
    return REFERENCE_LINK_RE.findall(text)


def split_atoms(text: str) -> list[str]:
    matches = list(ATOM_ID_RE.finditer(text))
    if not matches:
        return []

    atoms: list[str] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        atoms.append(text[start:end])
    return atoms


def atom_field(atom_text: str, field: str) -> str:
    match = re.search(rf'\({field}\s+"([^"]*)"\)', atom_text)
    return match.group(1) if match else ""


def record_operations(writes: str) -> list[tuple[str, str, str]]:
    return re.findall(
        r"\b(append|upsert)\s+([a-z]+)\s+record\s+\{([^}]*)\}",
        writes,
    )


def module_atom_ids() -> dict[str, list[str]]:
    return {
        MODULE_NAMES[module_name]: ATOM_ID_RE.findall(
            (REFERENCES_DIR / module_name).read_text(encoding="utf-8")
        )
        for module_name in MODULE_FILES
    }


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_script(script_name: str, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    script_path = SCRIPTS_DIR / script_name
    return subprocess.run(
        [sys.executable, str(script_path), *args],
        cwd=cwd or ROOT,
        capture_output=True,
        text=True,
        check=False,
    )



def import_session_helper():
    from tests.skill_session_loader import load_skill_session

    return load_skill_session(SCRIPTS_DIR)

