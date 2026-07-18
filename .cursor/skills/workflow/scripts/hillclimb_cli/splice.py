"""Span-splice crossover subcommand."""

from __future__ import annotations

import argparse
import json
import sys

from eliotapp.application.workflow.crossover_splice import (
    load_span_map_arg,
    run_crossover_splice,
)
from eliotapp.application.workflow.scores_io import require_tuning_allowed


def cmd_splice(args: argparse.Namespace) -> int:
    run_dir = args.run_dir
    if not (run_dir / "scores.json").is_file():
        print(f"run not initialized: {run_dir}", file=sys.stderr)
        return 1
    try:
        require_tuning_allowed(run_dir)
        span_map = load_span_map_arg(args.span_map)
        qualitative_json = None
        if args.qualitative is not None:
            qualitative_json = args.qualitative.read_text(encoding="utf-8")
        out = run_crossover_splice(
            run_dir,
            parent_a=args.parent_a,
            parent_b=args.parent_b,
            span_map=span_map,
            record=args.record,
            qualitative_json=qualitative_json,
        )
    except (OSError, ValueError, json.JSONDecodeError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0
