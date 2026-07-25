"""Lean-mvp gate UX: autofill decisions, refuse stay-on-gate, status --brief."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / "skills" / "lean-mvp" / "scripts"


def run_script(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / args[0]), *args[1:]],
        cwd=cwd or ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def seed_ready_for_gate(session_path: Path, gate_id: str = "C12") -> None:
    """Mark all customer-context atoms before the gate as answered."""
    from tests.skill_session_loader import load_skill_session

    session_mod = load_skill_session(SCRIPTS_DIR)
    load_atoms = session_mod.load_atoms
    load_session = session_mod.load_session
    save_session = session_mod.save_session

    session = load_session(session_path)
    atoms = load_atoms()
    timestamp = "2026-07-21T12:00:00Z"
    for atom in atoms:
        if atom["module"] != "customer-context":
            continue
        if atom["id"] == gate_id:
            continue
        session["answers"].append(
            {
                "atom_id": atom["id"],
                "answer": "seed",
                "kind": "fact",
                "accepted_at": timestamp,
            }
        )
    session["position"] = {
        "module": "customer-context",
        "atom_id": gate_id,
        "status": "in_progress",
    }
    save_session(session_path, session)


class LeanMvpGateUxTests(unittest.TestCase):
    def test_gate_pending_autofills_decisions_without_records(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "workproduct" / "lean-mvp"
            init = run_script(
                "init_session.py",
                "--name",
                "Gate Autofill",
                "--slug",
                "gate-autofill",
                "--root",
                str(root),
            )
            self.assertEqual(init.returncode, 0, init.stderr)
            session_path = root / "gate-autofill" / "session.json"
            seed_ready_for_gate(session_path)

            accept = run_script(
                "accept_answer.py",
                str(session_path),
                "--atom-id",
                "C12",
                "--answer",
                "pass customer-context gate",
                "--kind",
                "decision",
                "--gate-pending",
            )
            self.assertEqual(accept.returncode, 0, accept.stderr)

            session = json.loads(session_path.read_text(encoding="utf-8"))
            self.assertEqual(session["position"]["status"], "gate_pending")
            self.assertTrue(
                any(
                    d.get("decision") == "pass customer-context gate"
                    and d.get("source_atom") == "C12"
                    for d in session.get("decisions", [])
                ),
                session.get("decisions"),
            )

            milestone = run_script(
                "write_milestone.py",
                str(session_path),
                "--module",
                "customer-context",
            )
            self.assertEqual(milestone.returncode, 0, milestone.stderr)
            self.assertTrue((session_path.parent / "customer-context.md").is_file())

    def test_stay_on_gate_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "workproduct" / "lean-mvp"
            init = run_script(
                "init_session.py",
                "--name",
                "Stay Gate",
                "--slug",
                "stay-gate",
                "--root",
                str(root),
            )
            self.assertEqual(init.returncode, 0, init.stderr)
            session_path = root / "stay-gate" / "session.json"
            seed_ready_for_gate(session_path)

            stay = run_script(
                "accept_answer.py",
                str(session_path),
                "--atom-id",
                "C12",
                "--answer",
                "Paused before gate",
                "--kind",
                "unknown",
                "--stay",
            )
            self.assertNotEqual(stay.returncode, 0)
            self.assertIn("--stay is not allowed on gate atom", stay.stderr)

            session = json.loads(session_path.read_text(encoding="utf-8"))
            self.assertFalse(
                any(a["atom_id"] == "C12" for a in session.get("answers", []))
            )

            nxt = run_script("next_question.py", str(session_path))
            self.assertEqual(nxt.returncode, 0, nxt.stderr)
            payload = json.loads(nxt.stdout)
            self.assertEqual(payload.get("atom_id"), "C12")
            self.assertNotEqual(payload.get("done"), True)

    def test_status_brief_alias_exits_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "workproduct" / "lean-mvp"
            init = run_script(
                "init_session.py",
                "--name",
                "Brief Alias",
                "--slug",
                "brief-alias",
                "--root",
                str(root),
            )
            self.assertEqual(init.returncode, 0, init.stderr)
            session_path = root / "brief-alias" / "session.json"
            brief = run_script("status.py", str(session_path), "--brief")
            self.assertEqual(brief.returncode, 0, brief.stderr)
            self.assertTrue(brief.stdout.strip())

    def test_foreign_bypass_in_records_does_not_force_gate_pending(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "workproduct" / "lean-mvp"
            init = run_script(
                "init_session.py",
                "--name",
                "Bypass Trap",
                "--slug",
                "bypass-trap",
                "--root",
                str(root),
            )
            self.assertEqual(init.returncode, 0, init.stderr)
            session_path = root / "bypass-trap" / "session.json"
            seed_ready_for_gate(session_path)
            records_path = Path(tmp) / "foreign-bypass.json"
            records_path.write_text(
                json.dumps(
                    {
                        "decisions": [
                            {
                                "decision": "bypass underserved-needs gate",
                                "reason": "foreign",
                                "source_atom": "U12",
                                "resulting_module": "underserved-needs",
                                "resulting_atom": "U12",
                                "resulting_status": "in_progress",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            accept = run_script(
                "accept_answer.py",
                str(session_path),
                "--atom-id",
                "C12",
                "--answer",
                "not a pass",
                "--kind",
                "decision",
                "--records",
                str(records_path),
            )
            self.assertEqual(accept.returncode, 0, accept.stderr)
            session = json.loads(session_path.read_text(encoding="utf-8"))
            self.assertNotEqual(session["position"]["status"], "gate_pending")
            self.assertFalse(
                any(
                    d.get("decision") == "pass customer-context gate"
                    for d in session.get("decisions", [])
                )
            )

    def test_reopen_pass_does_not_duplicate_decisions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "workproduct" / "lean-mvp"
            init = run_script(
                "init_session.py",
                "--name",
                "Reopen Gate",
                "--slug",
                "reopen-gate",
                "--root",
                str(root),
            )
            self.assertEqual(init.returncode, 0, init.stderr)
            session_path = root / "reopen-gate" / "session.json"
            seed_ready_for_gate(session_path)
            first = run_script(
                "accept_answer.py",
                str(session_path),
                "--atom-id",
                "C12",
                "--answer",
                "pass customer-context gate",
                "--kind",
                "decision",
                "--gate-pending",
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            second = run_script(
                "accept_answer.py",
                str(session_path),
                "--atom-id",
                "C12",
                "--answer",
                "pass customer-context gate",
                "--kind",
                "decision",
                "--gate-pending",
                "--reopen",
                "--conflict-note",
                "confirm pass",
            )
            self.assertEqual(second.returncode, 0, second.stderr)
            session = json.loads(session_path.read_text(encoding="utf-8"))
            passes = [
                d
                for d in session.get("decisions", [])
                if d.get("decision") == "pass customer-context gate"
                and d.get("source_atom") == "C12"
            ]
            self.assertEqual(len(passes), 1, session.get("decisions"))

    def test_accept_bulk_refuses_gate_atoms(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "workproduct" / "lean-mvp"
            init = run_script(
                "init_session.py",
                "--name",
                "Bulk Gate",
                "--slug",
                "bulk-gate",
                "--root",
                str(root),
            )
            self.assertEqual(init.returncode, 0, init.stderr)
            session_path = root / "bulk-gate" / "session.json"
            seed_ready_for_gate(session_path)
            map_path = Path(tmp) / "gate-map.json"
            map_path.write_text(
                json.dumps(
                    {
                        "mappings": [
                            {
                                "atom_id": "C12",
                                "answer": "pass customer-context gate",
                                "kind": "decision",
                                "satisfied": True,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            bulk = run_script(
                "accept_bulk.py",
                str(session_path),
                "--map",
                str(map_path),
            )
            self.assertNotEqual(bulk.returncode, 0)
            self.assertIn("module gate", bulk.stderr)
            session = json.loads(session_path.read_text(encoding="utf-8"))
            self.assertFalse(
                any(a["atom_id"] == "C12" for a in session.get("answers", []))
            )


if __name__ == "__main__":
    unittest.main()
