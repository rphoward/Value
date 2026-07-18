#!/usr/bin/env python3
"""Thin CLI: EvaluatorScore for {draft, style_block}, optional qualitative merge."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from eliotapp.core.eliot.scorecard import extract_style_block
from eliotapp.core.evaluator.score_draft import score_draft_against_block
from eliotapp.core.shapes.score import combine_scores, parse_qualitative_scores


def _resolve_block(raw: str) -> str:
    extracted = extract_style_block(raw)
    return extracted if extracted else raw.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Score draft against Dense Style Block")
    parser.add_argument("--draft", type=Path, required=True, help="Draft prose file")
    parser.add_argument("--block", type=Path, required=True, help="Style block file or fenced markdown")
    parser.add_argument(
        "--qualitative",
        type=Path,
        default=None,
        help="JSON array of qualitative SectionScores (e.g. from the eval-audit subagent)",
    )
    parser.add_argument("--repeat", type=int, default=1, help="Run N times to verify reproducibility")
    args = parser.parse_args()

    draft = args.draft.read_text(encoding="utf-8")
    block = _resolve_block(args.block.read_text(encoding="utf-8"))

    scores = [score_draft_against_block(draft, block) for _ in range(args.repeat)]
    first = scores[0]
    reproducible = all(first.within_tolerance(s) for s in scores[1:])

    if args.qualitative is not None:
        try:
            qualitative = parse_qualitative_scores(args.qualitative.read_text(encoding="utf-8"))
        except ValueError as exc:
            print(f"qualitative JSON rejected: {exc}", file=sys.stderr)
            return 1
        first = combine_scores(first, qualitative)

    out = {
        "score": first.to_dict(),
        "reproducible": reproducible if args.repeat > 1 else None,
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
