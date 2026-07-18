#!/usr/bin/env python3
"""Thin CLI: scorer v2 Phase 4 validation gate (rank blind-read samples).

Ingest per-sample diagnostic JSON from the v2 stack and emit gate results:

    python gate_v2.py run --manifest tools/runs/scorer-v2/gate/manifest.json \
        --out-dir tools/runs/scorer-v2/gate

Manifest lists each sample's draft path plus paths to scored JSON from
pairwise_v2.py score, discrimination_v2.py score, and authorprint_v2.py score.
Deterministic axes are measured from the draft against the calibration sidecar.

Dry-run with fixture diagnostics (no live judges, unit-test parity):

    python gate_v2.py dry-run --out-dir tools/runs/scorer-v2/gate
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from eliotapp.infrastructure.calibration_store import load_calibration
from eliotapp.core.evaluator.cast_aliases import ALIAS_PROFILES
from eliotapp.core.evaluator.gate import (
    DEFAULT_MIN_DETERMINISTIC,
    SampleReport,
    run_gate,
)
from eliotapp.core.evaluator.score_draft_v2 import score_draft_v2
from eliotapp.core.shapes.score import DETERMINISTIC_SECTIONS

DRY_RUN_FIXTURES: dict[str, dict[str, Any]] = {
    "I": {
        "indistinguishability": 0.2,
        "pairwise_mean": 42.0,
        "authorprint_score": 35.0,
        "deterministic_axes": {"SURFACE": 72.0, "PROSODY": 68.0, "CAST": 75.0},
    },
    "II": {
        "indistinguishability": 1.0,
        "pairwise_mean": 100.0,
        "authorprint_score": 95.0,
        "deterministic_axes": {"SURFACE": 100.0, "PROSODY": 100.0, "CAST": 100.0},
    },
    "III": {
        "indistinguishability": 0.75,
        "pairwise_mean": 86.0,
        "authorprint_score": 78.0,
        "deterministic_axes": {"SURFACE": 88.0, "PROSODY": 85.0, "CAST": 100.0},
    },
    "IV": {
        "indistinguishability": 0.76,
        "pairwise_mean": 84.0,
        "authorprint_score": 80.0,
        "deterministic_axes": {"SURFACE": 86.0, "PROSODY": 82.0, "CAST": 100.0},
    },
}


def _deterministic_axes_from_draft(draft_path: Path, calibration_path: Path, author: str) -> dict[str, float]:
    calibration = load_calibration(calibration_path)
    aliases = ALIAS_PROFILES[author]
    draft = draft_path.read_text(encoding="utf-8")
    score = score_draft_v2(draft, calibration, aliases)
    return {section.section: section.score for section in score.deterministic}


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _report_from_manifest_entry(
    sample_id: str,
    entry: dict[str, Any],
    *,
    calibration_path: Path,
    author: str,
) -> SampleReport:
    draft_path = Path(entry["draft"])
    deterministic_axes = _deterministic_axes_from_draft(draft_path, calibration_path, author)

    pairwise = _load_json(Path(entry["pairwise"]))
    discrimination = _load_json(Path(entry["discrimination"]))
    authorprint_path = entry.get("authorprint")
    if authorprint_path:
        authorprint = _load_json(Path(authorprint_path))
        authorprint_score = float(authorprint["score"])
    else:
        authorprint_score = 0.0

    return SampleReport(
        sample_id=sample_id,
        indistinguishability=float(discrimination["indistinguishability"]),
        pairwise_mean=float(pairwise["mean_score"]),
        authorprint_score=authorprint_score,
        deterministic_axes=deterministic_axes,
    )


def _report_from_fixture(sample_id: str, fixture: dict[str, Any]) -> SampleReport:
    axes = {section: float(fixture["deterministic_axes"][section]) for section in DETERMINISTIC_SECTIONS}
    return SampleReport(
        sample_id=sample_id,
        indistinguishability=float(fixture["indistinguishability"]),
        pairwise_mean=float(fixture["pairwise_mean"]),
        authorprint_score=float(fixture["authorprint_score"]),
        deterministic_axes=axes,
    )


def _write_outputs(result: Any, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = result.to_dict()
    (out_dir / "results.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    ranking_payload = {
        "ranking": list(result.ranking),
        "accept": result.accept,
        "reason": result.reason,
    }
    (out_dir / "ranking.json").write_text(json.dumps(ranking_payload, indent=2) + "\n", encoding="utf-8")


def _run(args: argparse.Namespace) -> int:
    manifest = _load_json(args.manifest)
    calibration_path = Path(manifest["calibration"])
    author = manifest.get("author", "dostoevsky")
    min_det = float(manifest.get("min_deterministic", DEFAULT_MIN_DETERMINISTIC))
    source_sample = manifest.get("source_sample", "II")

    samples = manifest["samples"]
    if not isinstance(samples, dict):
        raise SystemExit("manifest samples must be an object")

    reports: dict[str, SampleReport] = {}
    for sample_id, entry in samples.items():
        if not isinstance(entry, dict):
            raise SystemExit(f"sample {sample_id} entry must be an object")
        reports[sample_id] = _report_from_manifest_entry(
            sample_id,
            entry,
            calibration_path=calibration_path,
            author=author,
        )

    result = run_gate(
        reports,
        source_sample=source_sample,
        min_deterministic=min_det,
    )
    _write_outputs(result, args.out_dir)
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.accept else 1


def _dry_run(args: argparse.Namespace) -> int:
    reports = {
        sample_id: _report_from_fixture(sample_id, fixture)
        for sample_id, fixture in DRY_RUN_FIXTURES.items()
    }
    result = run_gate(reports)
    _write_outputs(result, args.out_dir)
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.accept else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Scorer v2 Phase 4 validation gate")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Rank samples from a manifest of diagnostic JSON")
    run.add_argument("--manifest", type=Path, required=True, help="Gate manifest JSON")
    run.add_argument(
        "--out-dir",
        type=Path,
        default=Path("tools/runs/scorer-v2/gate"),
        help="Write results.json and ranking.json here",
    )
    run.set_defaults(func=_run)

    dry = sub.add_parser("dry-run", help="Rank built-in fixture diagnostics (no judges)")
    dry.add_argument(
        "--out-dir",
        type=Path,
        default=Path("tools/runs/scorer-v2/gate"),
        help="Write results.json and ranking.json here",
    )
    dry.set_defaults(func=_dry_run)

    args = parser.parse_args()
    try:
        return int(args.func(args))
    except (KeyError, ValueError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
