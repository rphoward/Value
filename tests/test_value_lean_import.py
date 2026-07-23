"""Lean bridge import for value skill."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / "skills" / "value" / "scripts"


class ValueLeanImportTests(unittest.TestCase):
    def _init_value_session(self, root: Path, slug: str) -> Path:
        init = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "init_session.py"),
                "--name",
                "Acme Scheduler",
                "--slug",
                slug,
                "--root",
                str(root / "workproduct" / "value-proposition"),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(init.returncode, 0, init.stderr)
        return root / "workproduct" / "value-proposition" / slug / "session.json"

    def _write_lean_session(self, root: Path, slug: str, answers: list[dict]) -> Path:
        lean_dir = root / "workproduct" / "lean-mvp" / slug
        lean_dir.mkdir(parents=True, exist_ok=True)
        lean_session = {
            "schema_version": "1.1",
            "project": {
                "slug": slug,
                "name": "Acme Scheduler",
                "created_at": "2026-07-20T12:00:00Z",
                "updated_at": "2026-07-20T12:00:00Z",
            },
            "position": {
                "module": "customer-context",
                "atom_id": "C02",
                "status": "in_progress",
            },
            "ledger": {
                "phase": "Customer Context",
                "active_module": "customer-context",
                "completion_pct": 10,
                "validation_milestone": "None",
                "unvalidated_bombs": [],
            },
            "answers": answers,
            "evidence": [],
            "assumptions": [],
            "decisions": [],
            "unknowns": [],
            "artifacts": [],
        }
        lean_path = lean_dir / "session.json"
        lean_path.write_text(json.dumps(lean_session), encoding="utf-8")
        return lean_path

    def test_imports_c01_into_p01_with_lean_import_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            slug = "acme-scheduler"
            value_path = self._init_value_session(root, slug)
            self._write_lean_session(
                root,
                slug,
                [
                    {
                        "atom_id": "C01",
                        "answer": "Independent cleaners in metro areas",
                        "kind": "fact",
                        "accepted_at": "2026-07-20T12:01:00Z",
                    }
                ],
            )

            imp = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS_DIR / "import_lean_context.py"),
                    str(value_path),
                    "--lean-root",
                    str(root / "workproduct" / "lean-mvp"),
                ],
                cwd=SCRIPTS_DIR,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(imp.returncode, 0, imp.stderr)
            payload = json.loads(imp.stdout)
            self.assertIn("P01", payload["imported"])

            value_session = json.loads(value_path.read_text(encoding="utf-8"))
            imported = [
                record
                for record in value_session["answers"]
                if record.get("provenance") == "lean-import"
            ]
            self.assertEqual(len(imported), 1)
            self.assertEqual(imported[0]["atom_id"], "P01")
            self.assertEqual(imported[0]["source_atom"], "C01")
            self.assertEqual(imported[0]["answer"], "Independent cleaners in metro areas")
            self.assertIn("lean_import", value_session)

    def test_skips_when_value_atom_already_answered(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            slug = "acme-scheduler"
            value_path = self._init_value_session(root, slug)
            value_session = json.loads(value_path.read_text(encoding="utf-8"))
            value_session["answers"].append(
                {
                    "atom_id": "P01",
                    "answer": "Existing segment answer",
                    "kind": "fact",
                    "accepted_at": "2026-07-20T12:05:00Z",
                }
            )
            value_path.write_text(json.dumps(value_session), encoding="utf-8")

            self._write_lean_session(
                root,
                slug,
                [
                    {
                        "atom_id": "C01",
                        "answer": "Lean segment answer",
                        "kind": "fact",
                        "accepted_at": "2026-07-20T12:01:00Z",
                    }
                ],
            )

            imp = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS_DIR / "import_lean_context.py"),
                    str(value_path),
                    "--lean-root",
                    str(root / "workproduct" / "lean-mvp"),
                ],
                cwd=SCRIPTS_DIR,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(imp.returncode, 0, imp.stderr)
            payload = json.loads(imp.stdout)
            self.assertEqual(payload["imported"], [])

            value_session = json.loads(value_path.read_text(encoding="utf-8"))
            p01_answers = [
                record for record in value_session["answers"] if record["atom_id"] == "P01"
            ]
            self.assertEqual(len(p01_answers), 1)
            self.assertEqual(p01_answers[0]["answer"], "Existing segment answer")
            self.assertNotIn("provenance", p01_answers[0])

    def test_missing_lean_session_returns_reason_exit_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            slug = "acme-scheduler"
            value_path = self._init_value_session(root, slug)

            imp = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS_DIR / "import_lean_context.py"),
                    str(value_path),
                    "--lean-root",
                    str(root / "workproduct" / "lean-mvp"),
                ],
                cwd=SCRIPTS_DIR,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(imp.returncode, 0, imp.stderr)
            self.assertEqual(
                json.loads(imp.stdout),
                {"imported": [], "reason": "no lean session"},
            )

    def test_imports_p01_and_p09_when_lean_has_c01_and_ms01(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            slug = "acme-scheduler"
            value_path = self._init_value_session(root, slug)
            self._write_lean_session(
                root,
                slug,
                [
                    {
                        "atom_id": "C01",
                        "answer": "Independent cleaners in metro areas",
                        "kind": "fact",
                        "accepted_at": "2026-07-20T12:01:00Z",
                    },
                    {
                        "atom_id": "MS01",
                        "answer": "Spreadsheets and pen-and-paper schedules",
                        "kind": "fact",
                        "accepted_at": "2026-07-20T12:02:00Z",
                    },
                ],
            )

            imp = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS_DIR / "import_lean_context.py"),
                    str(value_path),
                    "--lean-root",
                    str(root / "workproduct" / "lean-mvp"),
                ],
                cwd=SCRIPTS_DIR,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(imp.returncode, 0, imp.stderr)
            payload = json.loads(imp.stdout)
            self.assertEqual(set(payload["imported"]), {"P01", "P09"})

            value_session = json.loads(value_path.read_text(encoding="utf-8"))
            imported_ids = {
                record["atom_id"]
                for record in value_session["answers"]
                if record.get("provenance") == "lean-import"
            }
            self.assertEqual(imported_ids, {"P01", "P09"})


if __name__ == "__main__":
    unittest.main()
