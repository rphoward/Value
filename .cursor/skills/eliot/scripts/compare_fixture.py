#!/usr/bin/env python3
"""Thin CLI: score three-way ELIOT compare runs in tools/runs/eliot-compare/<date>/."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from eliotapp.infrastructure.scorecard_store import scorecard_from_files


def main() -> int:
    parser = argparse.ArgumentParser(description="Score ELIOT three-way compare runs")
    parser.add_argument(
        "run_dir",
        type=Path,
        help="Directory with run-a-5.7-monolith.md, run-b-5.3-monolith.md, run-c-split-skill.md",
    )
    args = parser.parse_args()
    if not args.run_dir.is_dir():
        print(f"not a directory: {args.run_dir}", file=sys.stderr)
        return 1
    card = scorecard_from_files(args.run_dir)
    summary = card["summary"]
    print(json.dumps(summary, indent=2))
    return 0 if summary["run_c_passes"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
