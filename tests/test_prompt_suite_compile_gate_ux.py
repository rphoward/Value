"""Gate UX on prompt-suite-compile scaffold output (not lean-mvp directly)."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACK = ROOT / ".cursor" / "skills" / "scripted-skill-from-doc"
SCRIPTS = PACK / "scripts"
COMPILE = SCRIPTS / "compile.py"
SAMPLE = PACK / "assets" / "fixtures" / "sample-prompt-suite.md"


def run_compile(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(COMPILE), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def run_script(scripts_dir: Path, script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(scripts_dir / script), *args],
        cwd=scripts_dir,
        capture_output=True,
        text=True,
        check=False,
    )


def scaffold_draft(tmp: Path) -> Path:
    out = tmp / "drafts"
    proc = run_compile(
        "scaffold",
        "--source",
        str(SAMPLE),
        "--slug",
        "gate-ux-test",
        "--out",
        str(out),
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    return out / "gate-ux-test"


def gate_context(scripts_dir: Path, session_path: Path) -> tuple[str, str, str]:
    """Return (gate_id, module_id, canonical_pass) for the first module gate."""
    from tests.skill_session_loader import load_skill_session

    session_mod = load_skill_session(scripts_dir)
    MODULE_ATOMS = session_mod.MODULE_ATOMS
    MODULE_ORDER = session_mod.MODULE_ORDER
    _build_atom_indexes = session_mod._build_atom_indexes
    canonical_gate_pass_text = session_mod.canonical_gate_pass_text
    gate_atom_for_module = session_mod.gate_atom_for_module
    load_session = session_mod.load_session
    save_session = session_mod.save_session

    _build_atom_indexes()
    module = MODULE_ORDER[0]
    gate_id = gate_atom_for_module(module)
    session = load_session(session_path)
    timestamp = "2026-07-21T12:00:00Z"
    for atom_id in MODULE_ATOMS[module]:
        if atom_id == gate_id:
            continue
        session["answers"].append(
            {
                "atom_id": atom_id,
                "answer": "seed",
                "kind": "fact",
                "accepted_at": timestamp,
            }
        )
    session["position"] = {
        "module": module,
        "atom_id": gate_id,
        "status": "in_progress",
    }
    save_session(session_path, session)
    return gate_id, module, canonical_gate_pass_text(module)


class PromptSuiteCompileGateUxTests(unittest.TestCase):
    def test_gate_pending_autofills_decisions_without_records(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            draft = scaffold_draft(Path(tmp))
            scripts = draft / "scripts"
            wp = Path(tmp) / "workproduct" / "gate-ux-test"
            init = run_script(
                scripts,
                "init_session.py",
                "--name",
                "Gate Autofill",
                "--slug",
                "proj",
                "--root",
                str(wp),
            )
            self.assertEqual(init.returncode, 0, init.stderr)
            session_path = wp / "proj" / "session.json"
            gate_id, module_id, pass_phrase = gate_context(scripts, session_path)

            accept = run_script(
                scripts,
                "accept_answer.py",
                str(session_path),
                "--atom-id",
                gate_id,
                "--answer",
                pass_phrase,
                "--kind",
                "decision",
                "--gate-pending",
            )
            self.assertEqual(accept.returncode, 0, accept.stderr)

            session = json.loads(session_path.read_text(encoding="utf-8"))
            self.assertEqual(session["position"]["status"], "gate_pending")
            self.assertTrue(
                any(
                    d.get("decision") == pass_phrase and d.get("source_atom") == gate_id
                    for d in session.get("decisions", [])
                ),
                session.get("decisions"),
            )

            milestone = run_script(
                scripts,
                "write_milestone.py",
                str(session_path),
                "--module",
                module_id,
            )
            self.assertEqual(milestone.returncode, 0, milestone.stderr)
            artifact = json.loads(
                (draft / "assets" / "skill-config.json").read_text(encoding="utf-8")
            )["gate_artifacts"][module_id]
            self.assertTrue((session_path.parent / artifact).is_file())

    def test_stay_on_gate_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            draft = scaffold_draft(Path(tmp))
            scripts = draft / "scripts"
            wp = Path(tmp) / "workproduct" / "gate-ux-test"
            init = run_script(
                scripts,
                "init_session.py",
                "--name",
                "Stay Gate",
                "--slug",
                "proj",
                "--root",
                str(wp),
            )
            self.assertEqual(init.returncode, 0, init.stderr)
            session_path = wp / "proj" / "session.json"
            gate_id, _, _ = gate_context(scripts, session_path)

            stay = run_script(
                scripts,
                "accept_answer.py",
                str(session_path),
                "--atom-id",
                gate_id,
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
                any(a["atom_id"] == gate_id for a in session.get("answers", []))
            )

    def test_status_brief_alias_exits_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            draft = scaffold_draft(Path(tmp))
            scripts = draft / "scripts"
            wp = Path(tmp) / "workproduct" / "gate-ux-test"
            init = run_script(
                scripts,
                "init_session.py",
                "--name",
                "Brief Alias",
                "--slug",
                "proj",
                "--root",
                str(wp),
            )
            self.assertEqual(init.returncode, 0, init.stderr)
            session_path = wp / "proj" / "session.json"
            brief = run_script(scripts, "status.py", str(session_path), "--brief")
            self.assertEqual(brief.returncode, 0, brief.stderr)
            self.assertTrue(brief.stdout.strip())

    def test_foreign_bypass_in_records_does_not_force_gate_pending(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            draft = scaffold_draft(Path(tmp))
            scripts = draft / "scripts"
            wp = Path(tmp) / "workproduct" / "gate-ux-test"
            init = run_script(
                scripts,
                "init_session.py",
                "--name",
                "Bypass Trap",
                "--slug",
                "proj",
                "--root",
                str(wp),
            )
            self.assertEqual(init.returncode, 0, init.stderr)
            session_path = wp / "proj" / "session.json"
            gate_id, module_id, pass_phrase = gate_context(scripts, session_path)
            config = json.loads(
                (draft / "assets" / "skill-config.json").read_text(encoding="utf-8")
            )
            second_module = config["module_order"][1]
            second_gate = "G02"
            records_path = Path(tmp) / "foreign-bypass.json"
            records_path.write_text(
                json.dumps(
                    {
                        "decisions": [
                            {
                                "decision": f"bypass {second_module} gate",
                                "reason": "foreign",
                                "source_atom": second_gate,
                                "resulting_module": second_module,
                                "resulting_atom": second_gate,
                                "resulting_status": "in_progress",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            accept = run_script(
                scripts,
                "accept_answer.py",
                str(session_path),
                "--atom-id",
                gate_id,
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
                    d.get("decision") == pass_phrase
                    for d in session.get("decisions", [])
                )
            )

    def test_reopen_pass_does_not_duplicate_decisions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            draft = scaffold_draft(Path(tmp))
            scripts = draft / "scripts"
            wp = Path(tmp) / "workproduct" / "gate-ux-test"
            init = run_script(
                scripts,
                "init_session.py",
                "--name",
                "Reopen Gate",
                "--slug",
                "proj",
                "--root",
                str(wp),
            )
            self.assertEqual(init.returncode, 0, init.stderr)
            session_path = wp / "proj" / "session.json"
            gate_id, _, pass_phrase = gate_context(scripts, session_path)
            first = run_script(
                scripts,
                "accept_answer.py",
                str(session_path),
                "--atom-id",
                gate_id,
                "--answer",
                pass_phrase,
                "--kind",
                "decision",
                "--gate-pending",
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            second = run_script(
                scripts,
                "accept_answer.py",
                str(session_path),
                "--atom-id",
                gate_id,
                "--answer",
                pass_phrase,
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
                if d.get("decision") == pass_phrase and d.get("source_atom") == gate_id
            ]
            self.assertEqual(len(passes), 1, session.get("decisions"))

    def test_accept_bulk_refuses_gate_atoms(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            draft = scaffold_draft(Path(tmp))
            scripts = draft / "scripts"
            wp = Path(tmp) / "workproduct" / "gate-ux-test"
            init = run_script(
                scripts,
                "init_session.py",
                "--name",
                "Bulk Gate",
                "--slug",
                "proj",
                "--root",
                str(wp),
            )
            self.assertEqual(init.returncode, 0, init.stderr)
            session_path = wp / "proj" / "session.json"
            gate_id, _, pass_phrase = gate_context(scripts, session_path)
            map_path = Path(tmp) / "gate-map.json"
            map_path.write_text(
                json.dumps(
                    {
                        "mappings": [
                            {
                                "atom_id": gate_id,
                                "answer": pass_phrase,
                                "kind": "decision",
                                "satisfied": True,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            bulk = run_script(
                scripts,
                "accept_bulk.py",
                str(session_path),
                "--map",
                str(map_path),
            )
            self.assertNotEqual(bulk.returncode, 0)
            self.assertIn("module gate", bulk.stderr)
            session = json.loads(session_path.read_text(encoding="utf-8"))
            self.assertFalse(
                any(a["atom_id"] == gate_id for a in session.get("answers", []))
            )

    def test_milestone_path_rejects_traversal(self) -> None:
        runtime = PACK / "assets" / "session-runtime"
        if str(runtime) not in sys.path:
            sys.path.insert(0, str(runtime))
        from write_milestone import resolve_milestone_path

        with tempfile.TemporaryDirectory() as tmp:
            session = Path(tmp) / "proj" / "session.json"
            session.parent.mkdir(parents=True)
            session.write_text("{}", encoding="utf-8")
            ok = resolve_milestone_path(session, "module.md")
            self.assertEqual(ok, (session.parent / "module.md").resolve())
            with self.assertRaises(ValueError):
                resolve_milestone_path(session, "../../escaped.md")
            with self.assertRaises(ValueError):
                resolve_milestone_path(session, r"C:\Windows\escaped.md")


if __name__ == "__main__":
    unittest.main()
