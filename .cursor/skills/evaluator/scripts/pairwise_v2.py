#!/usr/bin/env python3
"""Thin CLI: scorer v2 Phase 3 pairwise judging (prepare jobs, score verdicts).

Two steps, because the LLM judgments happen between them. First PREPARE the blind
comparison jobs from a draft and an anchor (the source, or the best draft):

    python pairwise_v2.py prepare --draft DRAFT.md --anchor SOURCE.md \
        --anchor-label source --n 5 --seed 7 --jobs-out jobs.json

`jobs.json` is the answer key (it records which side is the draft). Stdout carries
only the BLIND view (job_id, axis, question, passage_a, passage_b) — dispatch one
pair-judge subagent per job on that blind view, collect each {job_id, winner,
evidence}, and write them as a JSON array to verdicts.json. Then SCORE:

    python pairwise_v2.py score --jobs jobs.json --verdicts verdicts.json

Score per axis is the draft's win rate against the anchor; parity is the ceiling.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from eliotapp.core.evaluator.pairwise import (
    ComparisonJob,
    aggregate,
    build_comparison_jobs,
    parse_verdicts,
)


def _prepare(args: argparse.Namespace) -> int:
    draft = args.draft.read_text(encoding="utf-8")
    anchor = args.anchor.read_text(encoding="utf-8")
    jobs = build_comparison_jobs(draft, anchor, n_per_axis=args.n, seed=args.seed)
    if args.jobs_out is not None:
        args.jobs_out.parent.mkdir(parents=True, exist_ok=True)
        args.jobs_out.write_text(
            json.dumps([asdict(job) for job in jobs], indent=2),
            encoding="utf-8",
        )
    blind = {"anchor_label": args.anchor_label, "jobs": [job.blind() for job in jobs]}
    print(json.dumps(blind, indent=2))
    return 0


def _score(args: argparse.Namespace) -> int:
    jobs = tuple(
        ComparisonJob(**item)
        for item in json.loads(args.jobs.read_text(encoding="utf-8"))
    )
    verdicts = parse_verdicts(args.verdicts.read_text(encoding="utf-8"))
    result = aggregate(jobs, verdicts, args.anchor_label)
    print(json.dumps(result.to_dict(), indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Scorer v2 Phase 3 pairwise judging")
    sub = parser.add_subparsers(dest="command", required=True)

    prepare = sub.add_parser("prepare", help="Build blind comparison jobs")
    prepare.add_argument("--draft", type=Path, required=True)
    prepare.add_argument("--anchor", type=Path, required=True, help="Source or best draft")
    prepare.add_argument("--anchor-label", default="source")
    prepare.add_argument("--n", type=int, default=5, help="Comparisons per axis")
    prepare.add_argument("--seed", type=int, default=0, help="Side-randomization seed")
    prepare.add_argument("--jobs-out", type=Path, default=None, help="Write the answer key here")
    prepare.set_defaults(func=_prepare)

    score = sub.add_parser("score", help="Aggregate verdicts into pairwise scores")
    score.add_argument("--jobs", type=Path, required=True, help="Answer key from prepare")
    score.add_argument("--verdicts", type=Path, required=True, help="Judge verdicts array")
    score.add_argument("--anchor-label", default="source")
    score.set_defaults(func=_score)

    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
