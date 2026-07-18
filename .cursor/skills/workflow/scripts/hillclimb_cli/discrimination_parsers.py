"""Argparse registration for legacy discrimination job-board subcommands."""

from __future__ import annotations

import argparse
from pathlib import Path

from hillclimb_cli.common import resolve_run_dir_arg
from hillclimb_cli.discrimination import (
    cmd_job_open,
    cmd_job_record,
    cmd_job_score,
    cmd_job_status,
    cmd_job_trial,
)


def register_discrimination_parsers(sub: argparse._SubParsersAction) -> None:
    job_open = sub.add_parser(
        "job-open",
        help="Prepare discrimination trials and open a mid-batch job file",
    )
    job_open.add_argument(
        "--run-dir", type=resolve_run_dir_arg, required=True, help="Existing run folder"
    )
    job_open.add_argument("--iteration", type=int, required=True)
    job_open.add_argument("--draft", type=Path, required=True, help="Imitation draft path")
    job_open.add_argument("--genuine", type=Path, required=True, help="Genuine passage path")
    job_open.add_argument("--n", type=int, default=10, help="Trial count")
    job_open.add_argument("--seed", type=int, default=0, help="Side-randomization seed")
    job_open.add_argument(
        "--seed-suffix",
        default=None,
        help="Best-of-n seed suffix (e.g. a for trials-v1a.json)",
    )
    job_open.add_argument(
        "--trials-out",
        type=Path,
        default=None,
        help="Optional override path for the trials answer key",
    )
    job_open.set_defaults(func=cmd_job_open)

    job_trial = sub.add_parser(
        "job-trial",
        help="Append one discrimination verdict and update the job board",
    )
    job_trial.add_argument(
        "--run-dir", type=resolve_run_dir_arg, required=True, help="Existing run folder"
    )
    job_trial.add_argument("--iteration", type=int, required=True)
    job_trial.add_argument("--seed-suffix", default=None)
    job_trial.add_argument(
        "--trial-id",
        default=None,
        help="Trial id (default: trial_id from --verdict JSON)",
    )
    job_trial.add_argument(
        "--verdict",
        type=Path,
        required=True,
        help="JSON object with trial_id, genuine (A|B), tell",
    )
    job_trial.set_defaults(func=cmd_job_trial)

    job_score = sub.add_parser(
        "job-score",
        help="Score completed verdicts via discrimination aggregate; mark job scored",
    )
    job_score.add_argument(
        "--run-dir", type=resolve_run_dir_arg, required=True, help="Existing run folder"
    )
    job_score.add_argument("--iteration", type=int, required=True)
    job_score.add_argument("--seed-suffix", default=None)
    job_score.set_defaults(func=cmd_job_score)

    job_record = sub.add_parser(
        "job-record",
        help="Attach scored discrimination result to scores.json; mark job recorded",
    )
    job_record.add_argument(
        "--run-dir", type=resolve_run_dir_arg, required=True, help="Existing run folder"
    )
    job_record.add_argument("--iteration", type=int, required=True)
    job_record.add_argument("--seed-suffix", default=None)
    job_record.set_defaults(func=cmd_job_record)

    job_status = sub.add_parser(
        "job-status",
        help="List active (non-terminal) discrimination jobs for resume",
    )
    job_status.add_argument(
        "--run-dir", type=resolve_run_dir_arg, required=True, help="Existing run folder"
    )
    job_status.set_defaults(func=cmd_job_status)
