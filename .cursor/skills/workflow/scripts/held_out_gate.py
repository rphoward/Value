#!/usr/bin/env python3
"""CLI: register-matched held-out gate for /hillclimb sibling pull."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from eliotapp.application.workflow.held_out_gate import gate_held_out, write_gate_artifact


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gate a held-out candidate against source (POV/mode/overlap/words)."
    )
    parser.add_argument("--source", type=Path, required=True, help="Path to source.txt")
    parser.add_argument(
        "--candidate", type=Path, required=True, help="Path to held-out candidate text"
    )
    parser.add_argument(
        "--run-dir",
        type=Path,
        default=None,
        help="Write held-out-gate.json here (default: parent of source.txt)",
    )
    args = parser.parse_args()

    try:
        source = args.source.read_text(encoding="utf-8")
        candidate = args.candidate.read_text(encoding="utf-8")
    except OSError as exc:
        print(json.dumps({"pass": False, "reasons": [str(exc)]}), file=sys.stderr)
        return 1

    result = gate_held_out(source, candidate)
    run_dir = args.run_dir
    if run_dir is None and args.source.name == "source.txt":
        run_dir = args.source.parent
    if run_dir is not None:
        write_gate_artifact(
            run_dir, result, candidate=str(args.candidate.resolve())
        )

    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
