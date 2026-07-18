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

    progress_path = root / "tools" / "runs" / ".sdk-climb-last.json"
    if progress_path.is_file():
        try:
            payload = json.loads(progress_path.read_text(encoding="utf-8"))
            if isinstance(payload, dict) and payload.get("slug"):
                iteration = payload.get("iteration_count", "?")
                action = payload.get("next_action", "?")
                print(
                    f"observe: sdk-climb run {payload['slug']!r} "
                    f"iteration {iteration}; next_action={action!r}",
                    file=sys.stderr,
                )
        except (OSError, json.JSONDecodeError):
            pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
