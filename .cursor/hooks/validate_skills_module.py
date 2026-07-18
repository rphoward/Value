#!/usr/bin/env python3
# hook-class: observe
"""Lightweight import smoke after edits under eliotapp/."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    if sys.stdin.isatty():
        return 0
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    file_path = str(payload.get("file_path") or payload.get("path") or "").replace(
        "\\", "/"
    )
    if "/eliotapp/" not in f"/{file_path}" and not file_path.startswith("eliotapp/"):
        return 0

    root = Path(__file__).resolve().parents[2]
    shapes = root / "eliotapp" / "core" / "shapes" / "score.py"
    if not shapes.is_file():
        return 0

    sys.path.insert(0, str(root))
    try:
        import eliotapp.core.shapes.score  # noqa: F401
        import eliotapp.application.workflow.scores_io  # noqa: F401
    except ImportError as exc:
        print(f"observe: eliotapp import failed: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
