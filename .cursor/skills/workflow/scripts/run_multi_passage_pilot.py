#!/usr/bin/env python3
"""Thin CLI for the phase-15 report-only multi-passage pilot."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from eliotapp.application.workflow.multi_passage_pilot import (
    PilotError,
    build_blind_jobs,
    finalize_report,
    load_passage_manifest,
    write_report,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_RUN_DIR = REPO_ROOT / "tools" / "runs" / "reverse-engineering-quality" / "phase-15"


def _print_json(payload: object) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def _read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _cmd_validate(args: argparse.Namespace) -> int:
    manifest = load_passage_manifest(args.manifest, repo_root=args.repo_root)
    _print_json(
        {
            "ok": True,
            "target_id": manifest.target_id,
            "passage_count": len(manifest.passages),
            "manifest_sha256": manifest.manifest_sha256,
        }
    )
    return 0


def _cmd_build_jobs(args: argparse.Namespace) -> int:
    manifest = load_passage_manifest(args.manifest, repo_root=args.repo_root)
    finalists = _read_json(args.finalists)
    if not isinstance(finalists, list):
        raise PilotError("finalists: array required")
    jobs = build_blind_jobs(
        manifest,
        finalists,
        args.output_dir,
        n_trials=args.n_trials,
        seed=args.seed,
        repo_root=args.repo_root,
    )
    _print_json({"ok": True, "job_count": len(jobs), "output_dir": str(args.output_dir)})
    return 0


def _cmd_write_report(args: argparse.Namespace) -> int:
    manifest = load_passage_manifest(args.manifest, repo_root=args.repo_root)
    finalists = _read_json(args.finalists)
    jobs_raw = _read_json(args.jobs)
    verdicts = _read_json(args.verdicts)
    clean_winners = _read_json(args.clean_winners)
    frozen_hashes = _read_json(args.frozen_hashes_unchanged)
    if not isinstance(finalists, list):
        raise PilotError("finalists: array required")
    if not isinstance(jobs_raw, list):
        raise PilotError("jobs: array required")
    if not isinstance(verdicts, dict):
        raise PilotError("verdicts: object required")
    if not isinstance(clean_winners, dict):
        raise PilotError("clean_winners: object required")
    if not isinstance(frozen_hashes, dict):
        raise PilotError("frozen_hashes_unchanged: object required")
    jobs = build_blind_jobs(
        manifest,
        finalists,
        args.output_dir,
        n_trials=args.n_trials,
        seed=args.seed,
        repo_root=args.repo_root,
    )
    if len(jobs_raw) != len(jobs):
        raise PilotError("jobs file does not match rebuilt job count")
    report = finalize_report(
        manifest,
        finalists,
        jobs,
        verdicts,
        clean_winner_by_item=clean_winners,
        frozen_hashes_unchanged={str(key): bool(value) for key, value in frozen_hashes.items()},
        started_at=args.started_at,
        completed_at=args.completed_at,
    )
    path = write_report(args.run_dir, report)
    _print_json({"ok": True, "path": str(path), "outcome": report["outcome"]})
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Phase-15 multi-passage pilot")
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="Validate the passage manifest")
    validate.add_argument("--manifest", type=Path, required=True)
    validate.set_defaults(func=_cmd_validate)

    build_jobs = sub.add_parser("build-jobs", help="Build blind discrimination jobs")
    build_jobs.add_argument("--manifest", type=Path, required=True)
    build_jobs.add_argument("--finalists", type=Path, required=True)
    build_jobs.add_argument("--output-dir", type=Path, default=DEFAULT_RUN_DIR / "jobs")
    build_jobs.add_argument("--n-trials", type=int, default=10)
    build_jobs.add_argument("--seed", type=int, default=7)
    build_jobs.set_defaults(func=_cmd_build_jobs)

    report = sub.add_parser("write-report", help="Write the deterministic pilot report")
    report.add_argument("--manifest", type=Path, required=True)
    report.add_argument("--finalists", type=Path, required=True)
    report.add_argument("--jobs", type=Path, required=True)
    report.add_argument("--verdicts", type=Path, required=True)
    report.add_argument("--clean-winners", type=Path, required=True)
    report.add_argument("--frozen-hashes-unchanged", type=Path, required=True)
    report.add_argument("--output-dir", type=Path, default=DEFAULT_RUN_DIR / "jobs")
    report.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    report.add_argument("--n-trials", type=int, default=10)
    report.add_argument("--seed", type=int, default=7)
    report.add_argument("--started-at", required=True)
    report.add_argument("--completed-at", required=True)
    report.set_defaults(func=_cmd_write_report)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (PilotError, FileExistsError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
