#!/usr/bin/env python3
"""Thin CLI for phase-16 offline staged-evaluation replay."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from eliotapp.application.workflow.staged_replay import (
    ReplayError,
    build_report,
    load_evaluation_traces,
    load_staged_policy,
    replay_full_policy,
    replay_staged_policy,
    write_report,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_RUN_DIR = (
    REPO_ROOT / "tools" / "runs" / "reverse-engineering-quality" / "development-001"
)
DEFAULT_MANIFEST = (
    REPO_ROOT / "tools" / "runs" / "reverse-engineering-quality" / "experiment-manifest.json"
)
DEFAULT_REPORT = (
    REPO_ROOT
    / "tools"
    / "runs"
    / "reverse-engineering-quality"
    / "phase-16"
    / "staged-replay-report.json"
)


def _print_json(payload: object) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def _cmd_replay(args: argparse.Namespace) -> int:
    policy = load_staged_policy(args.manifest)
    traces = load_evaluation_traces(args.run_dir)
    staged = replay_staged_policy(traces, policy)
    full = replay_full_policy(traces, policy)
    report = build_report(traces, policy, staged=staged, full=full)
    path = write_report(args.report, report)
    _print_json(
        {
            "ok": True,
            "path": str(path),
            "outcome": report["outcome"],
            "selected_policy": report["selected_policy"],
            "phase_17": report["phase_17"],
            "cost_reduction": report["cost_reduction"],
            "wall_time_ratio": report["wall_time_ratio"],
            "live_calls": report["live_calls"],
        }
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Phase-16 staged evaluation replay")
    sub = parser.add_subparsers(dest="command", required=True)
    replay = sub.add_parser("replay", help="Replay frozen traces and write the report")
    replay.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    replay.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    replay.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    replay.set_defaults(func=_cmd_replay)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (ReplayError, FileExistsError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
