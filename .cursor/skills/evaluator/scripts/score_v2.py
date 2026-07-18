#!/usr/bin/env python3
"""Thin CLI: scorer v2 deterministic axes against a self-calibrated source.

Calibrate from a source fixture and score a draft in one call:

    python score_v2.py --draft DRAFT.md --source SOURCE.md \
        --calibration-out tools/runs/scorer-v2/calibration-dostoevsky.json

Or score against a previously written calibration sidecar:

    python score_v2.py --draft DRAFT.md --calibration cal.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from eliotapp.core.evaluator.calibration import measure
from eliotapp.infrastructure.calibration_store import (
    load_calibration,
    write_calibration,
)
from eliotapp.core.evaluator.cast_aliases import ALIAS_PROFILES
from eliotapp.core.evaluator.score_draft_v2 import score_draft_v2


def main() -> int:
    parser = argparse.ArgumentParser(description="Scorer v2 (self-calibrating deterministic axes)")
    parser.add_argument("--draft", type=Path, required=True, help="Draft prose file")
    parser.add_argument("--source", type=Path, default=None, help="Source fixture to calibrate from")
    parser.add_argument("--calibration", type=Path, default=None, help="Existing calibration JSON")
    parser.add_argument("--calibration-out", type=Path, default=None, help="Write calibration sidecar here")
    parser.add_argument(
        "--author",
        choices=sorted(ALIAS_PROFILES),
        default="dostoevsky",
        help="CAST alias profile to calibrate and score against",
    )
    args = parser.parse_args()

    aliases = ALIAS_PROFILES[args.author]

    if args.calibration is not None:
        calibration = load_calibration(args.calibration)
    elif args.source is not None:
        calibration = measure(args.source.read_text(encoding="utf-8"), aliases)
        if args.calibration_out is not None:
            write_calibration(calibration, args.calibration_out)
    else:
        print("provide --source (to calibrate) or --calibration (existing sidecar)", file=sys.stderr)
        return 2

    draft = args.draft.read_text(encoding="utf-8")
    score = score_draft_v2(draft, calibration, aliases)

    out = {"calibration": calibration.to_dict(), "score": score.to_dict()}
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
