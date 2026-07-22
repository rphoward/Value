#!/usr/bin/env python3
"""Shared forwarder to .cursor/skills/scripted-skill-from-doc/scripts/."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

SKILL_SCRIPTS = (
    Path(__file__).resolve().parents[2]
    / ".cursor"
    / "skills"
    / "scripted-skill-from-doc"
    / "scripts"
)


def forward(script_name: str) -> None:
    target = SKILL_SCRIPTS / script_name
    if not target.is_file():
        raise SystemExit(f"Missing skill pack script: {target}")
    scripts_dir = str(SKILL_SCRIPTS)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    sys.argv[0] = str(target)
    runpy.run_path(str(target), run_name="__main__")
