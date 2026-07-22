"""Shared path helpers for the scripted-skill-from-doc pack."""

from __future__ import annotations

from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPTS_DIR.parent
# Alias: pack root is the skill folder (SKILL.md lives here).
PACK_ROOT = SKILL_ROOT
ASSETS_DIR = SKILL_ROOT / "assets"
TEMPLATE_RUNTIME = ASSETS_DIR / "session-runtime"
SAMPLE_FIXTURE = ASSETS_DIR / "fixtures" / "sample-prompt-suite.md"


def find_repo_root(start: Path | None = None) -> Path:
    """Prefer an ancestor with .git or .cursor. Else use current working directory."""
    cur = (start or Path.cwd()).resolve()
    for candidate in (cur, *cur.parents):
        if (candidate / ".git").exists() or (candidate / ".cursor").is_dir():
            return candidate
    return cur
