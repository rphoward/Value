#!/usr/bin/env python3
# hook-class: observe
"""Run pytest on every agent stop; observe-only (exit 0 always)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main() -> int:
    if not sys.stdin.isatty():
        try:
            json.load(sys.stdin)
        except json.JSONDecodeError:
            pass

    root = _repo_root()
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root)
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q", "--tb=no"],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stdout, file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        print(f"observe: pytest failed (exit {result.returncode})", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
