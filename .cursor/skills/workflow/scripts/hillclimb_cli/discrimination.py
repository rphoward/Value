"""Legacy indistinguishability job-board subcommands (job-open, job-trial, …)."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from eliotapp.core.evaluator.discrimination import (
    DiscriminationTrial,
    aggregate,
    build_trials,
    parse_verdicts,
)
from eliotapp.application.workflow.job_board import (
    atomic_write_text,
    job_path,
    list_active_jobs,
    load_job,
    mark_recorded,
    mark_scored,
    mark_trial,
    open_job,
    unfinished_seed_jobs,
)
from eliotapp.application.workflow.climb_recording import record_discrimination
from eliotapp.application.workflow.scores_io import require_tuning_allowed

from hillclimb_cli.common import rel_under_run


def cmd_job_open(args: argparse.Namespace) -> int:
    run_dir = args.run_dir
    try:
        require_tuning_allowed(run_dir)
        genuine_text = args.genuine.read_text(encoding="utf-8")
        draft_text = args.draft.read_text(encoding="utf-8")
        trials = build_trials(
            genuine_text,
            draft_text,
            n_trials=args.n,
            seed=args.seed,
        )
        job = open_job(
            run_dir,
            iteration=args.iteration,
            draft=rel_under_run(run_dir, args.draft),
            genuine=rel_under_run(run_dir, args.genuine),
            n=args.n,
            seed=args.seed,
            seed_suffix=args.seed_suffix,
        )
        trials_out = (
            args.trials_out
            if args.trials_out is not None
            else run_dir / job.trials_path
        )
        trials_out.parent.mkdir(parents=True, exist_ok=True)
        trials_body = json.dumps([asdict(trial) for trial in trials], indent=2) + "\n"
        atomic_write_text(trials_out, trials_body)
        if args.trials_out is not None:
            default_trials = run_dir / job.trials_path
            if trials_out.resolve() != default_trials.resolve():
                atomic_write_text(default_trials, trials_body)
    except (OSError, ValueError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(job.to_dict(), indent=2))
    return 0


def cmd_job_trial(args: argparse.Namespace) -> int:
    run_dir = args.run_dir
    path = job_path(run_dir, args.iteration, args.seed_suffix)
    try:
        require_tuning_allowed(run_dir)
        job = load_job(path)
        verdict_payload = json.loads(args.verdict.read_text(encoding="utf-8"))
        if not isinstance(verdict_payload, dict):
            raise ValueError("verdict must be a JSON object")
        trial_id = args.trial_id or verdict_payload.get("trial_id")
        if not trial_id:
            raise ValueError("trial_id required via --trial-id or verdict JSON")
        if verdict_payload.get("trial_id") not in (None, trial_id):
            raise ValueError(
                f"verdict trial_id {verdict_payload.get('trial_id')!r} "
                f"does not match --trial-id {trial_id!r}"
            )
        verdict_payload = {
            "trial_id": trial_id,
            "genuine": verdict_payload["genuine"],
            "tell": verdict_payload["tell"],
        }
        verdicts_file = run_dir / job.verdicts_path
        if verdicts_file.is_file():
            existing = json.loads(verdicts_file.read_text(encoding="utf-8"))
            if not isinstance(existing, list):
                raise ValueError(f"verdicts must be a JSON array: {verdicts_file}")
        else:
            existing = []
        replaced = False
        for index, item in enumerate(existing):
            if isinstance(item, dict) and item.get("trial_id") == trial_id:
                existing[index] = verdict_payload
                replaced = True
                break
        if not replaced:
            existing.append(verdict_payload)
        verdicts_file.parent.mkdir(parents=True, exist_ok=True)
        atomic_write_text(
            verdicts_file,
            json.dumps(existing, indent=2) + "\n",
        )
        updated = mark_trial(path, trial_id)
    except (OSError, ValueError, json.JSONDecodeError, TypeError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(updated.to_dict(), indent=2))
    return 0


def cmd_job_score(args: argparse.Namespace) -> int:
    run_dir = args.run_dir
    path = job_path(run_dir, args.iteration, args.seed_suffix)
    try:
        require_tuning_allowed(run_dir)
        job = load_job(path)
        if job.pending_trial_ids:
            raise ValueError(
                "cannot score while pending_trial_ids is nonempty: "
                f"{job.pending_trial_ids!r}"
            )
        trials = tuple(
            DiscriminationTrial(**item)
            for item in json.loads((run_dir / job.trials_path).read_text(encoding="utf-8"))
        )
        verdicts = parse_verdicts((run_dir / job.verdicts_path).read_text(encoding="utf-8"))
        result = aggregate(trials, verdicts)
        result_path = run_dir / job.result_path
        atomic_write_text(
            result_path,
            json.dumps(result.to_dict(), indent=2) + "\n",
        )
        mark_scored(path)
    except (OSError, ValueError, json.JSONDecodeError, TypeError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result.to_dict(), indent=2))
    return 0


def cmd_job_record(args: argparse.Namespace) -> int:
    run_dir = args.run_dir
    if not (run_dir / "scores.json").is_file():
        print(f"run not initialized: {run_dir}", file=sys.stderr)
        return 1
    path = job_path(run_dir, args.iteration, args.seed_suffix)
    try:
        require_tuning_allowed(run_dir)
        job = load_job(path)
        siblings = unfinished_seed_jobs(
            run_dir,
            iteration=args.iteration,
            exclude_suffix=job.seed_suffix,
        )
        if siblings:
            print(
                "cannot job-record while sibling seed jobs are unfinished; "
                "complete discrimination for all seeds first",
                file=sys.stderr,
            )
            return 1
        if job.seed_suffix:
            if job.status != "scored":
                print(
                    f"cannot job-record seed job in status {job.status!r}; "
                    "job-score first",
                    file=sys.stderr,
                )
                return 1
            mark_recorded(path)
            out = {
                "seed_suffix": job.seed_suffix,
                "status": "recorded",
                "result_path": job.result_path,
                "note": "seed sidecar only; run seed-promote --record to enter scores.json",
            }
        else:
            result = json.loads((run_dir / job.result_path).read_text(encoding="utf-8"))
            out = record_discrimination(run_dir, result)
            mark_recorded(path)
    except (OSError, ValueError, json.JSONDecodeError, TypeError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0


def cmd_job_status(args: argparse.Namespace) -> int:
    active = list_active_jobs(args.run_dir)
    print(json.dumps([job.to_dict() for job in active], indent=2))
    return 0
