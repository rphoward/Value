#!/usr/bin/env python3
"""Smoke-test a draft skill: audit DAG, init session, ask next question."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from _paths import SCRIPTS_DIR


def run_script(
    scripts: Path, script: str, *args: str
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(scripts / script), *args],
        cwd=scripts,
        capture_output=True,
        text=True,
        check=False,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke-test a draft paced skill")
    parser.add_argument(
        "draft",
        type=Path,
        help="Path to draft skill root (folder that contains SKILL.md)",
    )
    args = parser.parse_args()
    draft = args.draft.resolve()
    if not (draft / "SKILL.md").is_file():
        print(f"Draft skill not found: {draft}", file=sys.stderr)
        return 1

    audit = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS_DIR / "audit_dag.py"),
            str(draft),
            "--mode",
            "standard",
        ],
        check=False,
    )
    if audit.returncode != 0:
        return audit.returncode

    tmp = Path(tempfile.mkdtemp(prefix="psc-smoke-"))
    try:
        wp = tmp / "workproduct" / "smoke"
        wp.mkdir(parents=True)
        scripts = draft / "scripts"
        init = run_script(
            scripts,
            "init_session.py",
            "--name",
            "Smoke Project",
            "--slug",
            "smoke",
            "--root",
            str(wp),
        )
        if init.returncode != 0:
            print(init.stderr or init.stdout, file=sys.stderr)
            return init.returncode
        session = wp / "smoke" / "session.json"

        brief = run_script(scripts, "status.py", str(session), "--brief")
        if brief.returncode != 0:
            print(brief.stderr or brief.stdout, file=sys.stderr)
            return brief.returncode
        if not brief.stdout.strip():
            print("status --brief produced empty output", file=sys.stderr)
            return 1

        nxt = run_script(scripts, "next_question.py", str(session))
        if nxt.returncode != 0:
            print(nxt.stderr or nxt.stdout, file=sys.stderr)
            return nxt.returncode
        payload = json.loads(nxt.stdout)
        if "atom_id" not in payload:
            print(f"Unexpected next_question output: {nxt.stdout}", file=sys.stderr)
            return 1
        print(nxt.stdout)

        atoms_by_id = {
            a["id"]: a
            for a in json.loads((draft / "assets" / "atoms.json").read_text(encoding="utf-8"))[
                "atoms"
            ]
        }
        config = json.loads((draft / "assets" / "skill-config.json").read_text(encoding="utf-8"))

        # Walk non-gate atoms until the first module gate (expanded curricula are not stub S01→G01).
        gate_id: str | None = None
        for _ in range(len(atoms_by_id) + 1):
            atom_id = payload.get("atom_id")
            if not atom_id:
                print(f"Unexpected next_question output: {payload}", file=sys.stderr)
                return 1
            atom = atoms_by_id.get(atom_id)
            if atom is None:
                print(f"Unknown atom_id from next_question: {atom_id}", file=sys.stderr)
                return 1
            if atom.get("gate"):
                gate_id = atom_id
                break
            accept_entry = run_script(
                scripts,
                "accept_answer.py",
                str(session),
                "--atom-id",
                atom_id,
                "--answer",
                "smoke seed",
                "--kind",
                "fact",
            )
            if accept_entry.returncode != 0:
                print(accept_entry.stderr or accept_entry.stdout, file=sys.stderr)
                return accept_entry.returncode
            nxt = run_script(scripts, "next_question.py", str(session))
            if nxt.returncode != 0:
                print(nxt.stderr or nxt.stdout, file=sys.stderr)
                return nxt.returncode
            payload = json.loads(nxt.stdout)

        if not gate_id:
            print("No gate atom reached after walking curriculum", file=sys.stderr)
            return 1

        gate_atom = atoms_by_id[gate_id]
        module_id = gate_atom["module"]
        pass_phrase = config["canonical_gate_pass"][module_id]

        gate_accept = run_script(
            scripts,
            "accept_answer.py",
            str(session),
            "--atom-id",
            gate_id,
            "--answer",
            pass_phrase,
            "--kind",
            "decision",
            "--gate-pending",
        )
        if gate_accept.returncode != 0:
            print(gate_accept.stderr or gate_accept.stdout, file=sys.stderr)
            return gate_accept.returncode

        milestone = run_script(
            scripts,
            "write_milestone.py",
            str(session),
            "--module",
            module_id,
        )
        if milestone.returncode != 0:
            print(milestone.stderr or milestone.stdout, file=sys.stderr)
            return milestone.returncode

        print("smoke ok")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
