#!/usr/bin/env python3
"""Thin CLI: reference preference prepare windows and score verdicts.

Prepare (stdout blind packets + optional manifest/window files):

    python reference_preference_v1.py prepare \\
        --reference held-out.txt --candidate-a draft-a.md --candidate-b draft-b.md \\
        --judge-model composer-2.5-fast --prompt-hash <sha256> \\
        --windows-out windows.json --manifest-out manifest.json

Dispatch one reference-preference subagent per window order on each blind packet.
Collect {window_id, order, winner, evidence} objects into verdicts.json, then score:

    python reference_preference_v1.py score \\
        --windows windows.json --verdicts verdicts.json --manifest manifest.json
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from eliotapp.core.evaluator.reference_preference import (
    PreferenceManifest,
    ReferenceWindow,
    WindowVerdict,
    aggregate_pair,
    all_window_orders,
    build_manifest,
    build_reference_windows,
    check_candidate_overlap,
    parse_window_verdict,
)


def _prepare(args: argparse.Namespace) -> int:
    reference = args.reference.read_text(encoding="utf-8")
    candidate_a = args.candidate_a.read_text(encoding="utf-8")
    candidate_b = args.candidate_b.read_text(encoding="utf-8")
    manifest = build_manifest(
        judge_model=args.judge_model,
        prompt_hash=args.prompt_hash,
        reference=reference,
        candidate_a=candidate_a,
        candidate_b=candidate_b,
    )
    rejections = check_candidate_overlap(reference, candidate_a, candidate_b)
    windows = build_reference_windows(reference, candidate_a, candidate_b)
    if args.windows_out is not None:
        args.windows_out.parent.mkdir(parents=True, exist_ok=True)
        args.windows_out.write_text(
            json.dumps([asdict(window) for window in windows], indent=2),
            encoding="utf-8",
        )
    if args.manifest_out is not None:
        args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
        args.manifest_out.write_text(
            json.dumps(manifest.to_dict(), indent=2),
            encoding="utf-8",
        )
    blind = {
        "metric": manifest.to_dict()["metric"],
        "rejections": [item.to_dict() for item in rejections],
        "pending_orders": list(all_window_orders(windows)),
        "packets": [
            window.blind_packet(order)
            for window in windows
            for order in ("ab", "ba")
        ],
    }
    print(json.dumps(blind, indent=2))
    return 0


def _score(args: argparse.Namespace) -> int:
    windows = tuple(
        ReferenceWindow(**item)
        for item in json.loads(args.windows.read_text(encoding="utf-8"))
    )
    manifest_payload = json.loads(args.manifest.read_text(encoding="utf-8"))
    manifest = PreferenceManifest(
        judge_model=manifest_payload["judge_model"],
        prompt_hash=manifest_payload["prompt_hash"],
        reference_hash=manifest_payload["reference_hash"],
        candidate_a_hash=manifest_payload["candidate_a_hash"],
        candidate_b_hash=manifest_payload["candidate_b_hash"],
        policy_hash=manifest_payload["policy_hash"],
    )
    verdicts = tuple(
        parse_window_verdict(json.dumps(item))
        for item in json.loads(args.verdicts.read_text(encoding="utf-8"))
    )
    result = aggregate_pair(windows, verdicts, manifest)
    print(json.dumps(result.to_dict(), indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Reference preference v1 evaluator")
    sub = parser.add_subparsers(dest="command", required=True)

    prepare = sub.add_parser("prepare", help="Build reference windows and blind packets")
    prepare.add_argument("--reference", type=Path, required=True)
    prepare.add_argument("--candidate-a", type=Path, required=True)
    prepare.add_argument("--candidate-b", type=Path, required=True)
    prepare.add_argument("--judge-model", required=True)
    prepare.add_argument("--prompt-hash", required=True)
    prepare.add_argument("--windows-out", type=Path, default=None)
    prepare.add_argument("--manifest-out", type=Path, default=None)
    prepare.set_defaults(func=_prepare)

    score = sub.add_parser("score", help="Aggregate window verdicts")
    score.add_argument("--windows", type=Path, required=True)
    score.add_argument("--verdicts", type=Path, required=True)
    score.add_argument("--manifest", type=Path, required=True)
    score.set_defaults(func=_score)

    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
