"""Adversarial integrity tests for value skill session scripts."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.value_session_support import append_accepted_answers, assert_omits_atom_ids


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in (here.parent, *here.parents):
        if (candidate / "pyproject.toml").is_file():
            return candidate
    raise RuntimeError("Could not locate repository root")


ROOT = repo_root()
SCRIPTS_DIR = ROOT / ".cursor" / "skills" / "value" / "scripts"
ASSETS_DIR = ROOT / ".cursor" / "skills" / "value" / "assets"


def run_script(script_name: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / script_name), *args],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


def import_session():
    sys.path.insert(0, str(SCRIPTS_DIR))
    import _session

    _session._atom_indexes_built = False
    return _session


class ValueSessionIntegrityTests(unittest.TestCase):
    def test_module_gate_passed_rejects_decoy_substrings(self) -> None:
        session_mod = import_session()
        decoy = {
            "decisions": [
                {
                    "decision": "do not pass profile gate yet",
                    "source_atom": "P12",
                    "reason": "no",
                }
            ]
        }
        self.assertFalse(session_mod.module_gate_passed(decoy, "profile"))

        bypass = {
            "decisions": [
                {
                    "decision": "bypass profile gate",
                    "source_atom": "P01",
                    "reason": "test",
                }
            ]
        }
        self.assertFalse(session_mod.module_gate_passed(bypass, "profile"))

        passed = {
            "decisions": [
                {
                    "decision": "pass profile gate",
                    "source_atom": "P12",
                    "reason": "ready",
                }
            ]
        }
        self.assertTrue(session_mod.module_gate_passed(passed, "profile"))

    def test_off_position_accept_refused_without_ceremony(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            work_root = Path(tmp) / "workproduct" / "value-proposition"
            session_path = work_root / "demo" / "session.json"
            self.assertEqual(
                run_script(
                    "init_session.py",
                    "--slug",
                    "demo",
                    "--name",
                    "Demo",
                    "--root",
                    str(work_root),
                ).returncode,
                0,
            )
            result = run_script(
                "accept_answer.py",
                str(session_path),
                "--atom-id",
                "V05",
                "--answer",
                "out of order",
                "--kind",
                "fact",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("not in the ready set", result.stderr)

    def test_off_position_accept_allowed_with_canonical_bypass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            work_root = Path(tmp) / "workproduct" / "value-proposition"
            session_path = work_root / "demo" / "session.json"
            records_path = Path(tmp) / "bypass.json"
            self.assertEqual(
                run_script(
                    "init_session.py",
                    "--slug",
                    "demo",
                    "--name",
                    "Demo",
                    "--root",
                    str(work_root),
                ).returncode,
                0,
            )
            records_path.write_text(
                json.dumps(
                    {
                        "decisions": [
                            {
                                "decision": "bypass profile gate",
                                "reason": "user requested phase jump",
                                "resulting_module": "value-map",
                                "resulting_atom": "V01",
                                "resulting_status": "in_progress",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            result = run_script(
                "accept_answer.py",
                str(session_path),
                "--atom-id",
                "P01",
                "--answer",
                "Bypass profile module.",
                "--kind",
                "decision",
                "--records",
                str(records_path),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            session = json.loads(session_path.read_text(encoding="utf-8"))
            self.assertEqual(session["position"]["atom_id"], "V01")

    def test_gate_atom_sets_gate_pending_instead_of_unlocking(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            work_root = Path(tmp) / "workproduct" / "value-proposition"
            session_path = work_root / "demo" / "session.json"
            records_path = Path(tmp) / "gate-pass.json"
            self.assertEqual(
                run_script(
                    "init_session.py",
                    "--slug",
                    "demo",
                    "--name",
                    "Demo",
                    "--root",
                    str(work_root),
                ).returncode,
                0,
            )
            session = json.loads(session_path.read_text(encoding="utf-8"))
            session["position"] = {
                "module": "profile",
                "atom_id": "P12",
                "status": "in_progress",
            }
            session_path.write_text(json.dumps(session, indent=2), encoding="utf-8")
            records_path.write_text(
                json.dumps(
                    {
                        "decisions": [
                            {
                                "decision": "pass profile gate",
                                "reason": "ready",
                                "resulting_module": "profile",
                                "resulting_atom": "P12",
                                "resulting_status": "gate_pending",
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
                "P12",
                "--answer",
                "Pass profile gate.",
                "--kind",
                "decision",
                "--records",
                str(records_path),
            )
            self.assertEqual(accept.returncode, 0, accept.stderr)
            session = json.loads(session_path.read_text(encoding="utf-8"))
            self.assertEqual(session["position"]["atom_id"], "P12")
            self.assertEqual(session["position"]["status"], "gate_pending")

    def test_write_milestone_requires_gate_pending(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            work_root = Path(tmp) / "workproduct" / "value-proposition"
            session_path = work_root / "demo" / "session.json"
            self.assertEqual(
                run_script(
                    "init_session.py",
                    "--slug",
                    "demo",
                    "--name",
                    "Demo",
                    "--root",
                    str(work_root),
                ).returncode,
                0,
            )
            blocked = run_script(
                "write_milestone.py",
                str(session_path),
                "--module",
                "profile",
            )
            self.assertNotEqual(blocked.returncode, 0)

    def test_milestone_sections_use_distinct_atom_content(self) -> None:
        session_mod = import_session()
        session = session_mod.default_session("demo", "Demo")
        timestamp = session_mod.utc_now_iso()
        answers = {
            "P01": "Independent cleaners",
            "P02": "New booking request arrives",
            "P03": "Fill the open slot quickly",
        }
        for atom_id, answer in answers.items():
            session["answers"].append(
                {
                    "atom_id": atom_id,
                    "answer": answer,
                    "kind": "fact",
                    "accepted_at": timestamp,
                }
            )
        content = session_mod.fill_milestone_template(session, "profile")
        self.assertIn("Independent cleaners", content)
        self.assertIn("New booking request arrives", content)
        self.assertIn("Fill the open slot quickly", content)
        assert_omits_atom_ids(self, content, "P01", "P02", "P03")
        segment_body = content.split("## Segment")[1].split("## Situation")[0]
        jobs_body = content.split("## Jobs")[1].split("## Pains")[0]
        self.assertIn("Independent cleaners", segment_body)
        self.assertNotIn("Fill the open slot quickly", segment_body)
        self.assertIn("Fill the open slot quickly", jobs_body)

    def test_human_artifacts_omit_atom_ids(self) -> None:
        session_mod = import_session()
        milestone_cases = (
            (
                "profile",
                (
                    ("P01", "Independent cleaners"),
                    ("P02", "New booking request arrives"),
                    ("P03", "Fill the open slot quickly"),
                ),
                ("P01", "P02", "P03"),
            ),
            (
                "value-map",
                (
                    ("V01", "Values skill offering"),
                    ("V03", "Pain relief hypothesis"),
                ),
                ("V01", "V03"),
            ),
            (
                "business-model",
                (("B01", "Deliver via installable skill"),),
                ("B01",),
            ),
            (
                "experiments",
                (("E01", "Segment will pay for guided value design"),),
                ("E01",),
            ),
        )
        for module, answers, atom_ids in milestone_cases:
            with self.subTest(artifact=f"milestone:{module}"):
                session = session_mod.default_session("demo", "Demo")
                append_accepted_answers(session, session_mod, answers)
                content = session_mod.fill_milestone_template(session, module)
                assert_omits_atom_ids(self, content, *atom_ids)

        brief_cases = (
            (
                "product-design-brief.template.md",
                (
                    ("P01", "Independent cleaners"),
                    ("V01", "Values skill offering"),
                    ("B01", "Deliver via installable skill"),
                ),
                ("P01", "V01", "B01"),
            ),
            (
                "ux-brief.template.md",
                (
                    ("P01", "Independent cleaners"),
                    ("P02", "New booking request arrives"),
                    ("P03", "Fill the open slot quickly"),
                ),
                ("P01", "P02", "P03"),
            ),
            (
                "app-design-brief.template.md",
                (
                    ("V01", "Values skill offering"),
                    ("V02", "Installable Cursor skill package"),
                ),
                ("V01", "V02"),
            ),
        )
        for template, answers, atom_ids in brief_cases:
            with self.subTest(artifact=f"brief:{template}"):
                session = session_mod.default_session("demo", "Demo")
                append_accepted_answers(session, session_mod, answers)
                content = session_mod.fill_design_brief(session, template)
                assert_omits_atom_ids(self, content, *atom_ids)

    def test_next_question_prefers_curriculum_gap_over_position(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            work_root = Path(tmp) / "workproduct" / "value-proposition"
            session_path = work_root / "demo" / "session.json"
            self.assertEqual(
                run_script(
                    "init_session.py",
                    "--slug",
                    "demo",
                    "--name",
                    "Demo",
                    "--root",
                    str(work_root),
                ).returncode,
                0,
            )
            session = json.loads(session_path.read_text(encoding="utf-8"))
            session["answers"].append(
                {
                    "atom_id": "P01",
                    "answer": "segment",
                    "kind": "decision",
                    "accepted_at": "2026-07-18T12:00:00Z",
                }
            )
            session["position"] = {
                "module": "value-map",
                "atom_id": "V01",
                "status": "in_progress",
            }
            session_path.write_text(json.dumps(session, indent=2), encoding="utf-8")
            payload = json.loads(run_script("next_question.py", str(session_path)).stdout)
            self.assertEqual(payload["atom_id"], "P02")

    def test_ready_off_position_accept_after_p03(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            work_root = Path(tmp) / "workproduct" / "value-proposition"
            session_path = work_root / "demo" / "session.json"
            self.assertEqual(
                run_script(
                    "init_session.py",
                    "--slug",
                    "demo",
                    "--name",
                    "Demo",
                    "--root",
                    str(work_root),
                ).returncode,
                0,
            )
            session_mod = import_session()
            session = json.loads(session_path.read_text(encoding="utf-8"))
            timestamp = "2026-07-18T12:00:00Z"
            for atom_id in ("P01", "P02", "P03"):
                session["answers"].append(
                    {
                        "atom_id": atom_id,
                        "answer": f"answer for {atom_id}",
                        "kind": "fact",
                        "accepted_at": timestamp,
                    }
                )
            session["position"] = {
                "module": "profile",
                "atom_id": "P04",
                "status": "in_progress",
            }
            session_path.write_text(json.dumps(session, indent=2), encoding="utf-8")
            result = run_script(
                "accept_answer.py",
                str(session_path),
                "--atom-id",
                "P07",
                "--answer",
                "Scheduling conflicts and no-shows.",
                "--kind",
                "unknown",
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_gate_pending_next_question_holds_until_milestone(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            work_root = Path(tmp) / "workproduct" / "value-proposition"
            session_path = work_root / "demo" / "session.json"
            self.assertEqual(
                run_script(
                    "init_session.py",
                    "--slug",
                    "demo",
                    "--name",
                    "Demo",
                    "--root",
                    str(work_root),
                ).returncode,
                0,
            )
            session_mod = import_session()
            atoms = session_mod.load_atoms()
            session = session_mod.default_session("demo", "Demo")
            timestamp = session_mod.utc_now_iso()
            for atom in atoms:
                if atom["module"] != "profile" or atom.get("gate"):
                    continue
                session["answers"].append(
                    {
                        "atom_id": atom["id"],
                        "answer": f"answer for {atom['id']}",
                        "kind": "fact",
                        "accepted_at": timestamp,
                    }
                )
            session["position"] = {
                "module": "profile",
                "atom_id": "P12",
                "status": "gate_pending",
            }
            session["artifacts"].append(
                {"path": "customer-profile.md", "status": "pending"}
            )
            session_path.write_text(json.dumps(session, indent=2), encoding="utf-8")
            payload = json.loads(run_script("next_question.py", str(session_path)).stdout)
            self.assertEqual(payload["atom_id"], "P12")
            self.assertEqual(payload["position_status"], "gate_pending")


if __name__ == "__main__":
    unittest.main()
