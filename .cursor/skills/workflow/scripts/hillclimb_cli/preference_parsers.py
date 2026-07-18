"""Argparse registration for reference-preference job-board subcommands."""

from __future__ import annotations

import argparse
from pathlib import Path

from hillclimb_cli.common import resolve_run_dir_arg
from hillclimb_cli.preference import (
    cmd_pref_job_open,
    cmd_pref_job_order,
    cmd_pref_job_record,
    cmd_pref_job_score,
    cmd_pref_job_status,
)


def register_preference_parsers(sub: argparse._SubParsersAction) -> None:
    pref_open = sub.add_parser(
        "pref-job-open",
        help="Prepare reference preference windows and open a preference job",
    )
    pref_open.add_argument("--run-dir", type=resolve_run_dir_arg, required=True)
    pref_open.add_argument("--iteration", type=int, required=True)
    pref_open.add_argument("--reference", type=Path, required=True)
    pref_open.add_argument("--candidate-a", type=Path, required=True)
    pref_open.add_argument("--candidate-b", type=Path, required=True)
    pref_open.add_argument(
        "--prompt-hash",
        default=None,
        help="SHA-256 of judge agent prompt (default: reference-preference.md)",
    )
    pref_open.add_argument("--judge-model", default=None)
    pref_open.add_argument(
        "--seed-pair",
        default=None,
        help="Seed pair key (e.g. a-vs-b); default from --left-suffix and --right-suffix",
    )
    pref_open.add_argument("--left-suffix", default=None)
    pref_open.add_argument("--right-suffix", default=None)
    pref_open.set_defaults(func=cmd_pref_job_open)

    pref_order = sub.add_parser(
        "pref-job-order",
        help="Append one preference window verdict and update the job board",
    )
    pref_order.add_argument("--run-dir", type=resolve_run_dir_arg, required=True)
    pref_order.add_argument("--iteration", type=int, required=True)
    pref_order.add_argument("--seed-pair", default=None)
    pref_order.add_argument("--order-key", default=None)
    pref_order.add_argument("--verdict", type=Path, required=True)
    pref_order.set_defaults(func=cmd_pref_job_order)

    pref_score = sub.add_parser(
        "pref-job-score",
        help="Score completed preference verdicts; mark job scored",
    )
    pref_score.add_argument("--run-dir", type=resolve_run_dir_arg, required=True)
    pref_score.add_argument("--iteration", type=int, required=True)
    pref_score.add_argument("--seed-pair", default=None)
    pref_score.set_defaults(func=cmd_pref_job_score)

    pref_record = sub.add_parser(
        "pref-job-record",
        help="Attach scored preference result; mark job recorded",
    )
    pref_record.add_argument("--run-dir", type=resolve_run_dir_arg, required=True)
    pref_record.add_argument("--iteration", type=int, required=True)
    pref_record.add_argument("--seed-pair", default=None)
    pref_record.add_argument(
        "--held-out",
        action="store_true",
        help="Apply prefer-vs-held-out anti-cheat overlay (explicit; not inferred from --reference)",
    )
    pref_record.set_defaults(func=cmd_pref_job_record)

    pref_status = sub.add_parser(
        "pref-job-status",
        help="List active (non-terminal) preference jobs for resume",
    )
    pref_status.add_argument("--run-dir", type=resolve_run_dir_arg, required=True)
    pref_status.set_defaults(func=cmd_pref_job_status)
