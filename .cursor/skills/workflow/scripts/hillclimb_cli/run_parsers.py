"""Argparse registration for core hillclimb run-folder subcommands."""

from __future__ import annotations

import argparse
from pathlib import Path

from eliotapp.application.workflow.climb_metrics import (
    CLIMB_METRIC_INDIS,
    CLIMB_METRIC_PAIRWISE_STYLE,
    CLIMB_METRIC_REFERENCE_PREFERENCE,
    CLIMB_METRIC_STYLE_FIDELITY,
)
from eliotapp.application.workflow.prepare import HELD_OUT_MIN_WORDS

from hillclimb_cli.common import (
    DEFAULT_PREFERENCE_AGENT,
    DEFAULT_RUNS_BASE,
    resolve_run_dir_arg,
)
from hillclimb_cli.run import (
    cmd_decision,
    cmd_freeze,
    cmd_init,
    cmd_inspect,
    cmd_prepare,
    cmd_prompt_hash,
    cmd_record,
    cmd_record_discrimination,
    cmd_record_preference,
    cmd_seed_promote,
    cmd_seed_status,
    cmd_status,
    cmd_validation_open,
)


def register_run_parsers(sub: argparse._SubParsersAction) -> None:
    prepare_parser = sub.add_parser(
        "prepare",
        help="Copy external source into tools/runs/<slug>/ and write calibration.json",
    )
    prepare_parser.add_argument(
        "--slug",
        default=None,
        help="Run folder name (default: derived from --source filename)",
    )
    prepare_parser.add_argument(
        "--source",
        type=Path,
        default=None,
        help="Source prose file (any path); omit to read UTF-8 text from stdin",
    )
    prepare_parser.add_argument(
        "--cast-aliases",
        type=Path,
        default=None,
        help="JSON map of CAST name to alias strings for calibration and scoring",
    )
    prepare_parser.add_argument(
        "--held-out",
        type=Path,
        default=None,
        help=(
            "Same-book continuous excerpt for discrimination genuine "
            f"(copied to held-out.txt; floor {HELD_OUT_MIN_WORDS} words)"
        ),
    )
    prepare_parser.add_argument(
        "--reserved-validation-id",
        default=None,
        help="Reserved validation identity to register in evidence-manifest.json",
    )
    prepare_parser.add_argument(
        "--reserved-validation-path",
        type=Path,
        default=None,
        help="Reserved validation bytes outside the run dir (paired with --reserved-validation-id)",
    )
    prepare_parser.add_argument("--runs-base", type=Path, default=DEFAULT_RUNS_BASE)
    prepare_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing prepared run (default: refuse if source.txt or scores.json exists)",
    )
    prepare_parser.set_defaults(func=cmd_prepare)

    init_parser = sub.add_parser("init", help="Create tools/runs/<slug>/ with style-block.md")
    init_parser.add_argument("--slug", required=True, help="Run folder name under runs base")
    init_parser.add_argument("--block", type=Path, required=True, help="Dense Style Block file")
    init_parser.add_argument("--topic", required=True, help="Emulation topic for this run")
    init_parser.add_argument("--max-iterations", type=int, default=3)
    init_parser.add_argument("--min-delta", type=float, default=1.5)
    init_parser.add_argument(
        "--early-stop",
        action="store_true",
        help="Stop before max_iterations when delta < min_delta (skips future draft+eval)",
    )
    init_parser.add_argument(
        "--climb-metric",
        default=CLIMB_METRIC_PAIRWISE_STYLE,
        choices=(
            CLIMB_METRIC_PAIRWISE_STYLE,
            CLIMB_METRIC_STYLE_FIDELITY,
            CLIMB_METRIC_INDIS,
            CLIMB_METRIC_REFERENCE_PREFERENCE,
        ),
        help=(
            "Climb decision metric (default: pairwise_style_v1 pairwise-vs-best; "
            "style_fidelity is legacy qualitative mean)"
        ),
    )
    init_parser.add_argument(
        "--preference-judge-model",
        default=None,
        help=(
            "Required for --climb-metric reference_preference_v1 (inherit rejected). "
            "Optional for pairwise_style_v1; otherwise pass --judge-model on pref-job-open"
        ),
    )
    init_parser.add_argument("--runs-base", type=Path, default=DEFAULT_RUNS_BASE)
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing run folder (default: refuse if scores.json exists)",
    )
    init_parser.set_defaults(func=cmd_init)

    record_parser = sub.add_parser("record", help="Score a draft and append scores.json")
    record_parser.add_argument(
        "--run-dir", type=resolve_run_dir_arg, required=True, help="Existing run folder"
    )
    record_parser.add_argument("--draft", type=Path, required=True, help="Draft prose from emulate step")
    record_parser.add_argument(
        "--qualitative",
        type=Path,
        default=None,
        help="JSON array from eval-audit subagent",
    )
    record_parser.set_defaults(func=cmd_record)

    status_parser = sub.add_parser("status", help="Resume snapshot for an existing run")
    status_parser.add_argument(
        "--run-dir", type=resolve_run_dir_arg, required=True, help="Existing run folder"
    )
    status_parser.set_defaults(func=cmd_status)

    inspect_parser = sub.add_parser(
        "inspect",
        help="Read-only run classification (one next_action JSON; changes no files)",
    )
    inspect_parser.add_argument(
        "--run-dir", type=resolve_run_dir_arg, required=True, help="Existing run folder"
    )
    inspect_parser.set_defaults(func=cmd_inspect)

    disc_parser = sub.add_parser(
        "record-discrimination",
        help="Attach discrimination result to the latest iteration (climb metric)",
    )
    disc_parser.add_argument(
        "--run-dir", type=resolve_run_dir_arg, required=True, help="Existing run folder"
    )
    disc_parser.add_argument(
        "--result",
        type=Path,
        required=True,
        help="JSON from discrimination_v2.py score (indistinguishability, detection_rate, tells)",
    )
    disc_parser.set_defaults(func=cmd_record_discrimination)

    pref_parser = sub.add_parser(
        "record-preference",
        help="Attach reference preference result to the latest iteration (climb metric)",
    )
    pref_parser.add_argument(
        "--run-dir", type=resolve_run_dir_arg, required=True, help="Existing run folder"
    )
    pref_parser.add_argument(
        "--result",
        type=Path,
        required=True,
        help="JSON from reference_preference_v1.py score",
    )
    pref_parser.add_argument(
        "--preference-outcome",
        required=False,
        choices=("incumbent", "challenger", "TIE"),
        help="Optional check against result JSON; outcome is always derived from --result",
    )
    pref_parser.add_argument(
        "--held-out",
        action="store_true",
        help="Apply prefer-vs-held-out anti-cheat overlay on latest accept",
    )
    pref_parser.add_argument(
        "--held-out-outcome",
        choices=("incumbent", "challenger", "TIE"),
        default=None,
        help="Held-out prefer outcome; defaults to derived preference outcome when --held-out",
    )
    pref_parser.set_defaults(func=cmd_record_preference)

    decision_parser = sub.add_parser(
        "decision", help="Append a decision.tsv row for the latest iteration"
    )
    decision_parser.add_argument(
        "--run-dir", type=resolve_run_dir_arg, required=True, help="Existing run folder"
    )
    decision_parser.add_argument("--hypothesis", required=True, help="One-line theory for this iteration")
    decision_parser.add_argument("--change", default="", help="What the drafter did")
    decision_parser.add_argument(
        "--verdict",
        default="kept",
        choices=("kept", "reverted", "stopped"),
        help="Outcome label for this row",
    )
    decision_parser.add_argument("--note", default="", help="Free-text note")
    decision_parser.add_argument("--tests", default="green", help="Regression gate status")
    decision_parser.set_defaults(func=cmd_decision)

    seed_status = sub.add_parser(
        "seed-status",
        help="Best-of-n seed job snapshot and whether seed-promote may run",
    )
    seed_status.add_argument(
        "--run-dir", type=resolve_run_dir_arg, required=True, help="Existing run folder"
    )
    seed_status.add_argument("--iteration", type=int, default=1)
    seed_status.set_defaults(func=cmd_seed_status)

    seed_promote = sub.add_parser(
        "seed-promote",
        help="Pick winner by climb metric; copy draft-vN.md; optional --record",
    )
    seed_promote.add_argument(
        "--run-dir", type=resolve_run_dir_arg, required=True, help="Existing run folder"
    )
    seed_promote.add_argument("--iteration", type=int, default=1)
    seed_promote.add_argument(
        "--record",
        action="store_true",
        help="Also record iter N into scores.json with winner qualitative + climb sidecar",
    )
    seed_promote.set_defaults(func=cmd_seed_promote)

    freeze_parser = sub.add_parser(
        "freeze-finalist",
        help="Freeze finalist configuration after development tuning stops",
    )
    freeze_parser.add_argument(
        "--run-dir", type=resolve_run_dir_arg, required=True, help="Existing run folder"
    )
    freeze_parser.add_argument(
        "--parent-manifest",
        type=Path,
        required=True,
        help="Experiment manifest with prompt_hashes and model_roles",
    )
    freeze_parser.add_argument(
        "--finalist-iteration",
        type=int,
        default=None,
        help="Iteration to freeze (default: best climb metric)",
    )
    freeze_parser.set_defaults(func=cmd_freeze)

    validation_open_parser = sub.add_parser(
        "validation-open",
        help="Verify reserved validation identity/hash and open validation",
    )
    validation_open_parser.add_argument(
        "--run-dir",
        type=resolve_run_dir_arg,
        required=True,
        help="Existing run folder",
    )
    validation_open_parser.add_argument(
        "--reserved-validation-id",
        required=True,
        help="Reserved validation identity from evidence-manifest.json",
    )
    validation_open_parser.add_argument(
        "--reserved-validation-sha256",
        required=True,
        help="Reserved validation SHA-256 from evidence-manifest.json",
    )
    validation_open_parser.set_defaults(func=cmd_validation_open)

    prompt_hash_parser = sub.add_parser(
        "prompt-hash",
        help="Print SHA-256 of a judge agent prompt file for pref-job-open manifests",
    )
    prompt_hash_parser.add_argument(
        "--agent",
        default=DEFAULT_PREFERENCE_AGENT,
        help="Agent name under .cursor/agents/ (default: reference-preference)",
    )
    prompt_hash_parser.set_defaults(func=cmd_prompt_hash)
