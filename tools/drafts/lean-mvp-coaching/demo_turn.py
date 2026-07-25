#!/usr/bin/env python3
"""Seed a throwaway lean-mvp session up to a target atom and print its next_question payload.

Evidence lever for the coaching layer: run it before and after the change and diff the payloads.

    python tools/drafts/lean-mvp-coaching/demo_turn.py MS05
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SCRIPTS = REPO / ".cursor" / "skills" / "lean-mvp" / "scripts"

GATE_MODULE = {
    "C12": "customer-context",
    "U12": "underserved-needs",
    "MS12": "mvp-scope",
    "UX12": "ux-prototype",
    "MT12": "metrics",
}

ANSWERS: tuple[tuple[str, str, str], ...] = (
    ("C01", "Solo operators shipping a first paid product alone, excluding funded teams.", "hypothesis"),
    ("C02", "The Lone Shipper. \"I have twelve half-built things and no idea which one to finish.\"", "hypothesis"),
    ("C03", "28-45, income 40-90k, high tech comfort, low risk appetite on spend.", "inference"),
    ("C04", "Early adopter. They already buy tools on a hunch and abandon them.", "hypothesis"),
    ("C05", "Has the problem yes; knows it yes; searches yes; workaround is a notes file; budget under $50/mo.", "fact"),
    ("C06", "Watch three operators screen-share a Sunday planning session end to end.", "decision"),
    ("C12", "pass customer-context gate", "decision"),
    ("U01", "Help a solo operator decide which one thing to finish next.", "hypothesis"),
    ("U02", "Reduce the time spent re-deciding the same scope question.", "hypothesis"),
    ("U03", "Underneath it is fear of sinking another month into the wrong build.", "inference"),
    ("U04", "Importance 90%, satisfaction 20%, from the three screen-share sessions.", "inference"),
    ("U05", "Deciding what to finish next: 90% x 0.8 = 72 opportunity, highest of the two.", "inference"),
    ("U12", "pass underserved-needs gate", "decision"),
    ("MS01", "Notion templates, a plain notes file, and Trello. Pen and paper is the real incumbent.", "fact"),
    ("MS02", "Capture the candidate list, keep it durable across sessions, show it on one screen.", "decision"),
    ("MS03", "Offense on decision quality. Cede collaboration and mobile entirely.", "decision"),
    ("MS04", "No delighter in v1. Defer until the decision loop holds up.", "decision"),
    ("MS05", "As a solo operator, I want one ranked next-thing-to-finish, so that I stop re-deciding.", "decision"),
    ("MS06", "High return, low effort. v1.", "decision"),
    ("MS12", "pass mvp-scope gate", "decision"),
    ("UX01", "A kanban column per project, not a nested folder tree.", "decision"),
    ("UX02", "Home lists active projects; tap opens the ranked next-thing card.", "decision"),
    ("UX03", "Open the app Sunday evening, pick the top ranked item, mark it done before Monday.", "decision"),
    ("UX04", "Qualitative product, clickable mockup, under two hours to build.", "decision"),
    ("UX05", "Intro: thanks for helping test a planning tool. Task: pick the top item and say why. PMF: How would you feel if you could no longer use this?", "decision"),
    ("UX12", "pass ux-prototype gate", "decision"),
    ("MT01", "Revenue equals active subscribers times price; levers are signups, trial conversion, and churn.", "hypothesis"),
)


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="Atom id to stop before, e.g. MS05")
    parser.add_argument("--json-only", action="store_true", help="Print the payload and nothing else")
    args = parser.parse_args()

    atoms_path = REPO / "skills" / "lean-mvp" / "assets" / "atoms.json"
    atom_ids = [a["id"] for a in json.loads(atoms_path.read_text(encoding="utf-8"))["atoms"]]
    if args.target not in atom_ids:
        print(f"target must be one of: {' '.join(atom_ids)}", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        created = run(
            [str(SCRIPTS / "init_session.py"), "--name", "Demo Turn", "--slug", "demo", "--root", str(root)],
            cwd=SCRIPTS,
        )
        if created.returncode != 0:
            print(created.stderr, file=sys.stderr)
            return 1
        session = root / "demo" / "session.json"

        for atom_id, answer, kind in ANSWERS:
            if atom_id == args.target:
                break
            accepted = run(
                [
                    str(SCRIPTS / "accept_answer.py"),
                    str(session),
                    "--atom-id",
                    atom_id,
                    "--answer",
                    answer,
                    "--kind",
                    kind,
                    *(["--gate-pending"] if atom_id.endswith("12") else []),
                ],
                cwd=SCRIPTS,
            )
            if accepted.returncode != 0:
                print(f"accept {atom_id} failed:\n{accepted.stderr}", file=sys.stderr)
                return 1
            if atom_id.endswith("12"):
                milestone = run(
                    [
                        str(SCRIPTS / "write_milestone.py"),
                        str(session),
                        "--module",
                        GATE_MODULE[atom_id],
                    ],
                    cwd=SCRIPTS,
                )
                if milestone.returncode != 0:
                    print(f"milestone after {atom_id} failed:\n{milestone.stderr}", file=sys.stderr)
                    return 1

        asked = run([str(SCRIPTS / "next_question.py"), str(session)], cwd=SCRIPTS)
        if asked.returncode != 0:
            print(asked.stderr, file=sys.stderr)
            return 1
        payload = json.loads(asked.stdout)
        if payload.get("atom_id") != args.target:
            print(
                f"scheduler landed on {payload.get('atom_id')}, expected {args.target}",
                file=sys.stderr,
            )
            return 1
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        if not args.json_only:
            print(f"\npayload keys: {sorted(payload)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
