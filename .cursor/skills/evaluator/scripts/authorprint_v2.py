#!/usr/bin/env python3
"""Thin CLI: scorer v2 AUTHORPRINT diagnostic (measure margins, score a draft).

Measure held-out margins after widening the Dostoevsky corpus:

    python authorprint_v2.py measure \
        --dost-dir tools/runs/scorer-v2/corpus/dostoevsky \
        --rilke tools/runs/scorer-v2/corpus/rilke/source.txt \
        --out tools/runs/scorer-v2/authorprint/margins.json

Score a draft against the built author profiles (diagnostic only, not EvaluatorScore):

    python authorprint_v2.py score --draft DRAFT.md --author dostoevsky \
        --dost-dir tools/runs/scorer-v2/corpus/dostoevsky \
        --rilke tools/runs/scorer-v2/corpus/rilke/source.txt
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from eliotapp.core.evaluator.authorprint import (
    build_author_profiles,
    measure_corpus_margins,
    score_text,
)


def _load_dost_text(dost_dir: Path) -> str:
    paths = sorted(dost_dir.glob("*.txt"))
    if not paths:
        raise SystemExit(f"no dostoevsky corpus under {dost_dir}")
    return "\n\n".join(p.read_text(encoding="utf-8") for p in paths)


def _measure(args: argparse.Namespace) -> int:
    rilke_text = args.rilke.read_text(encoding="utf-8")
    dost_chunks = sorted(args.dost_dir.glob("*.txt"))
    if not dost_chunks:
        raise SystemExit(f"no dostoevsky corpus under {args.dost_dir}")

    history: list[dict] = []
    accumulated: list[str] = []
    for i, path in enumerate(dost_chunks, 1):
        accumulated.append(path.read_text(encoding="utf-8"))
        row = measure_corpus_margins("\n\n".join(accumulated), rilke_text)
        row["chunks_included"] = i
        row["timestamp"] = datetime.now(timezone.utc).isoformat()
        history.append(row)
        print(
            f"chunk {i}: dost={row['word_counts']['dostoevsky']}w "
            f"margin_rilke={row['margin_rilke']:.4f} margin_dost={row['margin_dost']:.4f}"
        )

    payload = {"measurements": history, "final": history[-1]}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    final = history[-1]
    if final["margin_rilke"] <= 0 or final["margin_dost"] <= 0:
        print("margins not positive in both directions", file=sys.stderr)
        return 1
    print(json.dumps(payload, indent=2))
    return 0


def _score(args: argparse.Namespace) -> int:
    dost_text = _load_dost_text(args.dost_dir)
    rilke_text = args.rilke.read_text(encoding="utf-8")
    profiles = build_author_profiles(dost_text, rilke_text)
    draft = args.draft.read_text(encoding="utf-8")

    if args.author == "dostoevsky":
        result = score_text(
            draft,
            profiles.dost_profile,
            profiles.rilke_profile,
            profiles.stats,
            "dostoevsky",
        )
    elif args.author == "rilke":
        result = score_text(
            draft,
            profiles.rilke_profile,
            profiles.dost_profile,
            profiles.stats,
            "rilke",
        )
    else:
        raise SystemExit(f"unknown author {args.author!r}")

    print(json.dumps(result.to_dict(), indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Scorer v2 AUTHORPRINT diagnostic")
    sub = parser.add_subparsers(dest="command", required=True)

    measure = sub.add_parser("measure", help="Measure held-out margins and write margins.json")
    measure.add_argument(
        "--dost-dir",
        type=Path,
        default=Path("tools/runs/scorer-v2/corpus/dostoevsky"),
        help="Dostoevsky corpus chunks directory",
    )
    measure.add_argument(
        "--rilke",
        type=Path,
        default=Path("tools/runs/scorer-v2/corpus/rilke/source.txt"),
        help="Rilke source fixture",
    )
    measure.add_argument(
        "--out",
        type=Path,
        default=Path("tools/runs/scorer-v2/authorprint/margins.json"),
        help="Write margin history here",
    )
    measure.set_defaults(func=_measure)

    score = sub.add_parser("score", help="Score a draft against author profiles")
    score.add_argument("--draft", type=Path, required=True, help="Draft prose file")
    score.add_argument("--author", choices=("dostoevsky", "rilke"), required=True)
    score.add_argument(
        "--dost-dir",
        type=Path,
        default=Path("tools/runs/scorer-v2/corpus/dostoevsky"),
    )
    score.add_argument(
        "--rilke",
        type=Path,
        default=Path("tools/runs/scorer-v2/corpus/rilke/source.txt"),
    )
    score.set_defaults(func=_score)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
