#!/usr/bin/env python3
"""Thin CLI: scorer v2 Phase 3 machine discrimination (prepare trials, score verdicts).

Two steps, because the LLM judgments happen between them. First PREPARE blind trials
from a genuine held-out passage and a draft imitation:

    python discrimination_v2.py prepare --genuine GENUINE.txt --imitation DRAFT.md \
        --n 10 --seed 7 --trials-out trials.json

`trials.json` is the answer key (it records which side is genuine). Stdout carries
only the BLIND view (trial_id, passage_a, passage_b). Dispatch one discriminate
subagent per trial on that blind view, collect each {trial_id, genuine, tell}, and
write them as a JSON array to verdicts.json. Then SCORE:

    python discrimination_v2.py score --trials trials.json --verdicts verdicts.json

Indistinguishability is 1.0 at coin-flip detection (0.5); always caught scores 0.0.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from eliotapp.core.evaluator.discrimination import (
    DiscriminationTrial,
    aggregate,
    build_trials,
    parse_verdicts,
)


def _prepare(args: argparse.Namespace) -> int:
    genuine = args.genuine.read_text(encoding="utf-8")
    imitation = args.imitation.read_text(encoding="utf-8")
    trials = build_trials(genuine, imitation, n_trials=args.n, seed=args.seed)
    if args.trials_out is not None:
        args.trials_out.parent.mkdir(parents=True, exist_ok=True)
        args.trials_out.write_text(
            json.dumps([asdict(trial) for trial in trials], indent=2),
            encoding="utf-8",
        )
    blind = {"trials": [trial.blind() for trial in trials]}
    print(json.dumps(blind, indent=2))
    return 0


def _score(args: argparse.Namespace) -> int:
    trials = tuple(
        DiscriminationTrial(**item)
        for item in json.loads(args.trials.read_text(encoding="utf-8"))
    )
    verdicts = parse_verdicts(args.verdicts.read_text(encoding="utf-8"))
    result = aggregate(trials, verdicts)
    print(json.dumps(result.to_dict(), indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Scorer v2 Phase 3 machine discrimination")
    sub = parser.add_subparsers(dest="command", required=True)

    prepare = sub.add_parser("prepare", help="Build blind discrimination trials")
    prepare.add_argument("--genuine", type=Path, required=True, help="Held-out genuine passage")
    prepare.add_argument("--imitation", type=Path, required=True, help="Draft imitation")
    prepare.add_argument("--n", type=int, default=10, help="Trials per evaluation")
    prepare.add_argument("--seed", type=int, default=0, help="Side-randomization seed")
    prepare.add_argument("--trials-out", type=Path, default=None, help="Write the answer key here")
    prepare.set_defaults(func=_prepare)

    score = sub.add_parser("score", help="Aggregate spot verdicts into indistinguishability")
    score.add_argument("--trials", type=Path, required=True, help="Answer key from prepare")
    score.add_argument("--verdicts", type=Path, required=True, help="Judge verdicts array")
    score.set_defaults(func=_score)

    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
