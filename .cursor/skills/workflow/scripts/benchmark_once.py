#!/usr/bin/env python3
"""Thin CLI for benchmark runner mechanics (phase 10). No live calls."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from eliotapp.application.workflow.benchmark import (
    BenchmarkError,
    aggregate_experiment_outcome,
    freeze_generation,
    init_generation,
    load_benchmark_manifest,
    open_validation,
    reserved_consumption_state,
    run_status,
    write_report,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_RUNS_BASE = REPO_ROOT / "tools" / "runs"


def _print_json(payload: object) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def _cmd_validate_manifest(args: argparse.Namespace) -> int:
    loaded = load_benchmark_manifest(
        args.manifest,
        benchmark_root=args.benchmark_root,
        repo_root=args.repo_root,
    )
    _print_json(
        {
            "ok": True,
            "benchmark_id": loaded.benchmark_id,
            "item_count": len(loaded.items),
            "manifest_sha256": loaded.manifest_sha256,
            "parent_sha256": loaded.parent_experiment_manifest.sha256,
        }
    )
    return 0


def _cmd_init(args: argparse.Namespace) -> int:
    loaded = load_benchmark_manifest(
        args.manifest,
        benchmark_root=args.benchmark_root,
        repo_root=args.repo_root,
    )
    result = init_generation(
        args.generations_base,
        loaded,
        generation_slug=args.slug,
    )
    _print_json(
        {
            "run_dir": str(result.run_dir),
            "generation_id": result.generation_id,
            "generation_state": result.generation_state,
        }
    )
    return 0


def _cmd_status(args: argparse.Namespace) -> int:
    _print_json(run_status(args.run_dir))
    return 0


def _cmd_freeze(args: argparse.Namespace) -> int:
    payload = freeze_generation(args.run_dir)
    _print_json(
        {
            "generation_state": payload["generation_state"],
            "freeze": payload.get("freeze"),
        }
    )
    return 0


def _cmd_validation_open(args: argparse.Namespace) -> int:
    _print_json(open_validation(args.run_dir))
    return 0


def _cmd_reserved_state(args: argparse.Namespace) -> int:
    _print_json(reserved_consumption_state(args.run_dir))
    return 0


def _cmd_aggregate(args: argparse.Namespace) -> int:
    report = json.loads(args.report.read_text(encoding="utf-8"))
    _print_json(aggregate_experiment_outcome(report))
    return 0


def _cmd_write_report(args: argparse.Namespace) -> int:
    report = json.loads(args.report.read_text(encoding="utf-8"))
    path = write_report(args.run_dir, report)
    _print_json({"path": str(path)})
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Benchmark runner mechanics")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root for parent-manifest path containment",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate-manifest", help="Strict-load a benchmark manifest")
    validate.add_argument("--manifest", type=Path, required=True)
    validate.add_argument("--benchmark-root", type=Path, default=None)
    validate.set_defaults(func=_cmd_validate_manifest)

    init_cmd = sub.add_parser("init", help="Initialize a generation folder")
    init_cmd.add_argument("--manifest", type=Path, required=True)
    init_cmd.add_argument("--benchmark-root", type=Path, default=None)
    init_cmd.add_argument("--slug", required=True)
    init_cmd.add_argument(
        "--generations-base",
        type=Path,
        default=DEFAULT_RUNS_BASE / "reverse-engineering-quality",
    )
    init_cmd.set_defaults(func=_cmd_init)

    status = sub.add_parser("status", help="Show generation status")
    status.add_argument("--run-dir", type=Path, required=True)
    status.set_defaults(func=_cmd_status)

    freeze = sub.add_parser("freeze", help="Freeze a complete development generation")
    freeze.add_argument("--run-dir", type=Path, required=True)
    freeze.set_defaults(func=_cmd_freeze)

    open_cmd = sub.add_parser("validation-open", help="Open reserved validation once")
    open_cmd.add_argument("--run-dir", type=Path, required=True)
    open_cmd.set_defaults(func=_cmd_validation_open)

    reserved = sub.add_parser("reserved-state", help="Show reserved-consumption state")
    reserved.add_argument("--run-dir", type=Path, required=True)
    reserved.set_defaults(func=_cmd_reserved_state)

    aggregate = sub.add_parser("aggregate", help="Aggregate item-clustered outcomes")
    aggregate.add_argument("--report", type=Path, required=True)
    aggregate.set_defaults(func=_cmd_aggregate)

    write = sub.add_parser("write-report", help="Write deterministic benchmark report")
    write.add_argument("--run-dir", type=Path, required=True)
    write.add_argument("--report", type=Path, required=True)
    write.set_defaults(func=_cmd_write_report)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (BenchmarkError, FileExistsError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
