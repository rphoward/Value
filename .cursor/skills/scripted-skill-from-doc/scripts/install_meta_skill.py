#!/usr/bin/env python3
"""This skill folder IS the pack. install_meta_skill is a no-op."""

from __future__ import annotations

import sys

from _paths import SCRIPTS_DIR, SKILL_ROOT


def main() -> int:
    print(
        f"Pack already lives at {SKILL_ROOT} "
        "(transports with .cursor). Nothing to install."
    )
    if not (SCRIPTS_DIR / "compile.py").is_file():
        print("Missing scripts/compile.py — skill pack is incomplete.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
