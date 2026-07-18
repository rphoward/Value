"""Core hillclimb run-folder subcommands (prepare, init, record, status, …)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from eliotapp.infrastructure.cast_aliases_store import load_aliases_file
from eliotapp.application.workflow.job_board import unfinished_seed_jobs
from eliotapp.core.evaluator.reference_preference import require_preference_outcome
from eliotapp.application.workflow.climb_metrics import (
    HillclimbConfig,
    uses_pairwise_style,
    uses_reference_preference,
    uses_style_fidelity,
)
from eliotapp.application.workflow.climb_recording import (
    append_decision,
    record_discrimination,
    record_iteration,
    record_preference,
)
from eliotapp.application.workflow.generation_lifecycle import freeze_finalist, open_validation
from eliotapp.application.workflow.scores_io import init_run, require_tuning_allowed, run_status
from eliotapp.application.workflow.seed_round import (
    finalize_seed_winner,
    promote_seed_winner,
    seed_round_blocks_record_for_run,
    seed_round_status,
)
from eliotapp.application.workflow.prepare import (
    HELD_OUT_MIN_WORDS,
    derive_slug_from_path,
    prepare_run,
    read_source_text,
    validate_source_text,
)
from eliotapp.application.workflow.run_state import inspect_run_dir

from hillclimb_cli.common import (
    agent_prompt_hash,
    latest_iteration,
    resolve_block,
)


def pending_seed_promotion(run_dir: Path, iteration: int = 1) -> bool:
    """Seed jobs are scored and compared; winner must enter scores via seed-promote."""
    status = seed_round_status(run_dir, iteration)
    if not status["seed_count"]:
        return False
    payload = json.loads((run_dir / "scores.json").read_text(encoding="utf-8"))
    iterations = payload.get("iterations") if isinstance(payload, dict) else None
    if isinstance(iterations, list) and iterations:
        return False
    return bool(status["ready_to_promote"])


def cmd_prepare(args: argparse.Namespace) -> int:
    if args.source is not None:
        source_path = args.source
        source_text = read_source_text(source_path)
        slug = args.slug or derive_slug_from_path(source_path)
    else:
        raw = sys.stdin.buffer.read()
        try:
            source_text = raw.decode("utf-8")
        except UnicodeDecodeError:
            print("source must be UTF-8", file=sys.stderr)
            return 1
        validate_source_text(source_text)
        if not args.slug:
            print("--slug is required when source is read from stdin", file=sys.stderr)
            return 1
        slug = args.slug

    aliases = None
    if args.cast_aliases is not None:
        try:
            aliases = load_aliases_file(args.cast_aliases)
        except (OSError, ValueError) as exc:
            print(str(exc), file=sys.stderr)
            return 1

    held_out_text = None
    if args.held_out is not None:
        try:
            raw = args.held_out.read_bytes()
        except OSError as exc:
            print(f"cannot read held-out: {args.held_out}", file=sys.stderr)
            return 1
        try:
            held_out_text = raw.decode("utf-8")
        except UnicodeDecodeError:
            print(f"held-out must be UTF-8: {args.held_out}", file=sys.stderr)
            return 1
        try:
            validate_source_text(held_out_text, min_words=HELD_OUT_MIN_WORDS)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1

    if (args.reserved_validation_id is None) ^ (args.reserved_validation_path is None):
        print(
            "reserved_validation_id and reserved_validation_path must be provided together",
            file=sys.stderr,
        )
        return 1

    try:
        result = prepare_run(
            slug,
            source_text,
            runs_base=args.runs_base,
            force=args.force,
            aliases=aliases,
            held_out_text=held_out_text,
            reserved_validation_id=args.reserved_validation_id,
            reserved_validation_path=args.reserved_validation_path,
        )
    except (FileExistsError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if result.held_out_warning:
        print(result.held_out_warning, file=sys.stderr)

    out = {
        "run_dir": str(result.run_dir),
        "slug": result.slug,
        "words": result.words,
        "source": str(result.source_path),
        "calibration": str(result.calibration_path),
        "cast_aliases": str(result.cast_aliases_path) if result.cast_aliases_path else None,
        "held_out": str(result.held_out_path) if result.held_out_path else None,
        "held_out_words": result.held_out_words,
    }
    print(json.dumps(out, indent=2))
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    block = resolve_block(args.block.read_text(encoding="utf-8"))
    config = HillclimbConfig(
        style_block=block,
        topic=args.topic,
        max_iterations=args.max_iterations,
        min_delta=args.min_delta,
        early_stop=args.early_stop,
    )
    try:
        run_dir = init_run(
            args.slug,
            config,
            runs_base=args.runs_base,
            force=args.force,
            climb_metric=args.climb_metric,
            preference_judge_model=args.preference_judge_model,
        )
    except FileExistsError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    out = {
        "run_dir": str(run_dir),
        "slug": args.slug,
        "topic": args.topic,
        "max_iterations": args.max_iterations,
        "min_delta": args.min_delta,
        "early_stop": args.early_stop,
        "climb_metric": args.climb_metric,
        "preference_judge_model": args.preference_judge_model,
    }
    print(json.dumps(out, indent=2))
    return 0


def cmd_record(args: argparse.Namespace) -> int:
    run_dir = args.run_dir
    if not (run_dir / "scores.json").is_file():
        print(f"run not initialized: {run_dir}", file=sys.stderr)
        return 1

    try:
        require_tuning_allowed(run_dir)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    blocking = seed_round_blocks_record_for_run(run_dir)
    if blocking:
        payload = json.loads((run_dir / "scores.json").read_text(encoding="utf-8"))
        if uses_reference_preference(payload):
            print(
                "cannot record while seed preference jobs are unfinished; "
                "complete preference for all seeds first",
                file=sys.stderr,
            )
        elif uses_style_fidelity(payload) or uses_pairwise_style(payload):
            print(
                "cannot record while seed qualitative scores are unfinished; "
                "finish qualitative JSON for all seeds first",
                file=sys.stderr,
            )
        else:
            print(
                "cannot record while seed discrimination jobs are unfinished; "
                "complete discrimination for all seeds first",
                file=sys.stderr,
            )
        return 1
    if pending_seed_promotion(run_dir):
        print(
            "cannot record iter 1 directly while seed jobs await promotion; "
            "run seed-promote --record after all seeds are scored",
            file=sys.stderr,
        )
        return 1

    draft = args.draft.read_text(encoding="utf-8")
    qualitative_json = None
    if args.qualitative is not None:
        qualitative_json = args.qualitative.read_text(encoding="utf-8")

    record, stop, reason = record_iteration(
        run_dir,
        draft,
        qualitative_json=qualitative_json,
    )
    out = {
        "iteration": record.iteration,
        "draft": record.draft_file,
        "total": record.score.total,
        "delta": record.delta,
        "stop": stop,
        "reason": reason,
        "retry": not stop,
    }
    print(json.dumps(out, indent=2))
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    run_dir = args.run_dir
    if not (run_dir / "scores.json").is_file():
        print(f"run not initialized: {run_dir}", file=sys.stderr)
        return 1
    status = run_status(run_dir)
    print(json.dumps(status, indent=2))
    return 0


def cmd_inspect(args: argparse.Namespace) -> int:
    run_dir = args.run_dir
    try:
        inspection = inspect_run_dir(run_dir)
    except (OSError, ValueError, json.JSONDecodeError, TypeError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(inspection.to_dict(), indent=2))
    return 0


def cmd_record_discrimination(args: argparse.Namespace) -> int:
    run_dir = args.run_dir
    if not (run_dir / "scores.json").is_file():
        print(f"run not initialized: {run_dir}", file=sys.stderr)
        return 1
    latest = latest_iteration(run_dir)
    if latest is None:
        print("no iterations recorded", file=sys.stderr)
        return 1
    blocking = unfinished_seed_jobs(run_dir, iteration=latest)
    if blocking:
        print(
            "cannot record-discrimination while seed jobs are unfinished; "
            "complete discrimination for all seeds first",
            file=sys.stderr,
        )
        return 1
    try:
        require_tuning_allowed(run_dir)
        result = json.loads(args.result.read_text(encoding="utf-8"))
        out = record_discrimination(run_dir, result)
    except (OSError, ValueError, json.JSONDecodeError, TypeError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0


def cmd_record_preference(args: argparse.Namespace) -> int:
    run_dir = args.run_dir
    if not (run_dir / "scores.json").is_file():
        print(f"run not initialized: {run_dir}", file=sys.stderr)
        return 1
    try:
        require_tuning_allowed(run_dir)
        result = json.loads(args.result.read_text(encoding="utf-8"))
        derived = require_preference_outcome(
            result,
            expected=args.preference_outcome,
        )
        out = record_preference(
            run_dir,
            result,
            preference_outcome=derived,
            held_out=args.held_out,
            held_out_outcome=args.held_out_outcome,
        )
    except (OSError, ValueError, json.JSONDecodeError, TypeError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0


def cmd_decision(args: argparse.Namespace) -> int:
    run_dir = args.run_dir
    if not (run_dir / "scores.json").is_file():
        print(f"run not initialized: {run_dir}", file=sys.stderr)
        return 1
    try:
        require_tuning_allowed(run_dir)
        row = append_decision(
            run_dir,
            args.hypothesis,
            change=args.change,
            verdict=args.verdict,
            note=args.note,
            tests=args.tests,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(row, indent=2))
    return 0


def cmd_seed_status(args: argparse.Namespace) -> int:
    print(json.dumps(seed_round_status(args.run_dir, args.iteration), indent=2))
    return 0


def cmd_seed_promote(args: argparse.Namespace) -> int:
    run_dir = args.run_dir
    if not (run_dir / "scores.json").is_file():
        print(f"run not initialized: {run_dir}", file=sys.stderr)
        return 1
    try:
        require_tuning_allowed(run_dir)
        if args.record:
            out = finalize_seed_winner(run_dir, args.iteration)
        else:
            out = promote_seed_winner(run_dir, args.iteration)
    except (OSError, ValueError, json.JSONDecodeError, TypeError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0


def cmd_freeze(args: argparse.Namespace) -> int:
    run_dir = args.run_dir
    if not (run_dir / "scores.json").is_file():
        print(f"run not initialized: {run_dir}", file=sys.stderr)
        return 1
    try:
        out = freeze_finalist(
            run_dir,
            parent_manifest_path=args.parent_manifest,
            finalist_iteration=args.finalist_iteration,
        )
    except (OSError, ValueError, json.JSONDecodeError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0


def cmd_prompt_hash(args: argparse.Namespace) -> int:
    try:
        digest = agent_prompt_hash(args.agent)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(digest)
    return 0


def cmd_validation_open(args: argparse.Namespace) -> int:
    run_dir = args.run_dir
    if not (run_dir / "scores.json").is_file():
        print(f"run not initialized: {run_dir}", file=sys.stderr)
        return 1
    try:
        out = open_validation(
            run_dir,
            reserved_validation_id=args.reserved_validation_id,
            reserved_validation_sha256=args.reserved_validation_sha256,
        )
    except (OSError, ValueError, json.JSONDecodeError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2))
    return 0
