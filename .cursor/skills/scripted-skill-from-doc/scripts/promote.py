#!/usr/bin/env python3
"""Promote a draft skill to .cursor/skills/<slug>/ after audit passes."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from _paths import SCRIPTS_DIR, find_repo_root

# Never install or overwrite these live skills via promote.
ALWAYS_FORBIDDEN = frozenset({"value", "scripted-skill-from-doc"})

STUB_ASK_RE = re.compile(r"^What is the first concrete fact for\b", re.IGNORECASE)

IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", "ir.json")


def _refuse(msg: str) -> int:
    print(msg, file=sys.stderr)
    return 1


def _copy_skill(draft: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(draft, dest, ignore=IGNORE)


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote draft paced skill")
    parser.add_argument("draft", type=Path, help="Path to draft skill folder")
    parser.add_argument(
        "--repo",
        type=Path,
        default=None,
        help="Target repo root (default: find .git/.cursor from cwd)",
    )
    parser.add_argument(
        "--also-skills",
        action="store_true",
        help="Also copy to skills/<slug>/ (ship surface)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow overwrite when destination exists (still needs --overwrite-slug)",
    )
    parser.add_argument(
        "--overwrite-slug",
        default=None,
        help="Must equal the draft slug when overwriting an existing skill",
    )
    args = parser.parse_args()
    draft = args.draft.resolve()
    if not (draft / "SKILL.md").is_file():
        return _refuse(f"Not a skill draft: {draft}")
    slug = draft.name
    if slug in ALWAYS_FORBIDDEN:
        return _refuse(
            f"Refusing to promote slug {slug!r} — protected skill name."
        )

    audit = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS_DIR / "audit_dag.py"),
            str(draft),
            "--mode",
            "standard",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    print(audit.stdout)
    if audit.returncode != 0:
        return _refuse("Promote blocked: audit_dag failed")

    atoms_path = draft / "assets" / "atoms.json"
    if atoms_path.is_file():
        data = json.loads(atoms_path.read_text(encoding="utf-8"))
        for atom in data.get("atoms") or []:
            asks = atom.get("asks") or ""
            if STUB_ASK_RE.match(asks.strip()):
                return _refuse(
                    "Promote blocked: atoms.json still contains stub-ask placeholders. "
                    "Expand curriculum per references/curriculum-synthesis.md."
                )

    repo = (args.repo or find_repo_root()).resolve()
    dest = repo / ".cursor" / "skills" / slug
    ship = repo / "skills" / slug if args.also_skills else None

    targets: list[Path] = [dest]
    if ship is not None:
        targets.append(ship)

    for target in targets:
        if not target.exists():
            continue
        if not args.force:
            return _refuse(
                f"Destination exists: {target} (pass --force and "
                f"--overwrite-slug {slug})"
            )
        if args.overwrite_slug != slug:
            return _refuse(
                f"Overwrite of {target} requires --overwrite-slug {slug} "
                f"(got {args.overwrite_slug!r})"
            )

    # Preflight passed — only now mutate.
    _copy_skill(draft, dest)
    print(f"Promoted to {dest}")
    if ship is not None:
        _copy_skill(draft, ship)
        print(f"Also copied to {ship}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
