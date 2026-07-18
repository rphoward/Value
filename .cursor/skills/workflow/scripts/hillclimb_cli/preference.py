"""Reference-preference job-board subcommands (pref-job-open, pref-job-order, …)."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from eliotapp.core.evaluator.reference_preference import (
    build_manifest,
    build_reference_windows,
    check_candidate_overlap,
    parse_order_key,
)
from eliotapp.application.workflow.job_board import (
    _preference_artifact_names,
    atomic_write_text,
    list_active_preference_jobs,
    load_preference_job,
    mark_preference_order,
    open_preference_job,
    preference_job_path,
    preference_pair_key,
    unfinished_preference_seed_jobs,
)
from eliotapp.application.workflow.preference_jobs import (
    record_preference_job,
    score_preference_job,
)
from eliotapp.application.workflow.scores_io import require_tuning_allowed

from hillclimb_cli.common import (
    agent_prompt_hash,
    preference_judge_model,
    rel_under_run,
)


def cmd_pref_job_open(args: argparse.Namespace) -> int:
    run_dir = args.run_dir
    try:
        require_tuning_allowed(run_dir)
        prompt_hash = args.prompt_hash or agent_prompt_hash()
        reference_text = args.reference.read_text(encoding="utf-8")
        candidate_a_text = args.candidate_a.read_text(encoding="utf-8")
        candidate_b_text = args.candidate_b.read_text(encoding="utf-8")
        judge_model = args.judge_model or preference_judge_model(run_dir)
        manifest = build_manifest(
            judge_model=judge_model,
            prompt_hash=prompt_hash,
            reference=reference_text,
            candidate_a=candidate_a_text,
            candidate_b=candidate_b_text,
        )
        rejections = check_candidate_overlap(
            reference_text,
            candidate_a_text,
            candidate_b_text,
        )
        windows = build_reference_windows(
            reference_text,
            candidate_a_text,
            candidate_b_text,
        )
        seed_pair = args.seed_pair
        if seed_pair is None and args.left_suffix and args.right_suffix:
            seed_pair = preference_pair_key(args.left_suffix, args.right_suffix)
        _, windows_name, manifest_name, _, _ = _preference_artifact_names(
            args.iteration,
            seed_pair,
        )
        windows_path = run_dir / windows_name
        manifest_path = run_dir / manifest_name
        atomic_write_text(
            windows_path,
            json.dumps([asdict(window) for window in windows], indent=2) + "\n",
        )
        atomic_write_text(
            manifest_path,
            json.dumps(manifest.to_dict(), indent=2) + "\n",
        )
        job = open_preference_job(
            run_dir,
            iteration=args.iteration,
            candidate_a=rel_under_run(run_dir, args.candidate_a),
            candidate_b=rel_under_run(run_dir, args.candidate_b),
            reference=rel_under_run(run_dir, args.reference),
            judge_model=judge_model,
            prompt_hash=prompt_hash,
            seed_pair=seed_pair,
        )
    except (OSError, ValueError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    out = job.to_dict()
    out["rejections"] = [item.to_dict() for item in rejections]
    print(json.dumps(out, indent=2))
    return 0


def cmd_pref_job_order(args: argparse.Namespace) -> int:
    run_dir = args.run_dir
    path = preference_job_path(run_dir, args.iteration, args.seed_pair)
    try:
        require_tuning_allowed(run_dir)
        job = load_preference_job(path)
        verdict_payload = json.loads(args.verdict.read_text(encoding="utf-8"))
        if not isinstance(verdict_payload, dict):
            raise ValueError("verdict must be a JSON object")
        order_key = args.order_key or verdict_payload.get("order_key")
        if not order_key:
            window_id = verdict_payload.get("window_id")
            order = verdict_payload.get("order")
            if window_id and order:
                order_key = f"{window_id}-{order}"
        if not order_key:
            raise ValueError("order_key required via --order-key or verdict JSON")
        window_id, order = parse_order_key(order_key)
        verdict_payload = {
            "window_id": window_id,
            "order": order,
            "winner": verdict_payload["winner"],
            "evidence": verdict_payload["evidence"],
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
            if (
                isinstance(item, dict)
                and item.get("window_id") == window_id
                and item.get("order") == order
            ):
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
        updated = mark_preference_order(path, order_key)
    except (OSError, ValueError, json.JSONDecodeError, TypeError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(updated.to_dict(), indent=2))
    return 0


def cmd_pref_job_score(args: argparse.Namespace) -> int:
    run_dir = args.run_dir
    path = preference_job_path(run_dir, args.iteration, args.seed_pair)
    try:
        require_tuning_allowed(run_dir)
        result = score_preference_job(run_dir, path)
    except (OSError, ValueError, json.JSONDecodeError, TypeError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


def cmd_pref_job_record(args: argparse.Namespace) -> int:
    run_dir = args.run_dir
    if not (run_dir / "scores.json").is_file():
        print(f"run not initialized: {run_dir}", file=sys.stderr)
        return 1
    path = preference_job_path(run_dir, args.iteration, args.seed_pair)
    try:
        require_tuning_allowed(run_dir)
        job = load_preference_job(path)
        siblings = unfinished_preference_seed_jobs(
            run_dir,
            iteration=args.iteration,
            exclude_pair=job.seed_pair,
        )
        if siblings:
            print(
                "cannot pref-job-record while sibling seed jobs are unfinished; "
                "complete preference for all seeds first",
                file=sys.stderr,
            )
            return 1
        out = record_preference_job(run_dir, path, held_out=args.held_out)
    except (OSError, ValueError, json.JSONDecodeError, TypeError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0


def cmd_pref_job_status(args: argparse.Namespace) -> int:
    active = list_active_preference_jobs(args.run_dir)
    print(json.dumps([job.to_dict() for job in active], indent=2))
    return 0
