"""Value bridge import for lean-mvp skill."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / "skills" / "lean-mvp" / "scripts"


class LeanMvpValueImportTests(unittest.TestCase):
    def test_imports_mapped_atoms_from_value_session(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            slug = "acme-scheduler"
            value_dir = root / "workproduct" / "value-proposition" / slug
            lean_dir = root / "workproduct" / "lean-mvp" / slug
            value_dir.mkdir(parents=True)
            lean_dir.mkdir(parents=True)

            value_session = {
                "schema_version": "1.1",
                "project": {
                    "slug": slug,
                    "name": "Acme Scheduler",
                    "created_at": "2026-07-20T12:00:00Z",
                    "updated_at": "2026-07-20T12:00:00Z",
                },
                "position": {
                    "module": "profile",
                    "atom_id": "P03",
                    "status": "in_progress",
                },
                "ledger": {
                    "phase": "Canvas",
                    "active_module": "profile",
                    "completion_pct": 10,
                    "validation_milestone": "None",
                    "unvalidated_bombs": [],
                },
                "answers": [
                    {
                        "atom_id": "P01",
                        "answer": "Independent cleaners in metro areas",
                        "kind": "fact",
                        "accepted_at": "2026-07-20T12:01:00Z",
                    },
                    {
                        "atom_id": "P03",
                        "answer": "Fill open slots without no-shows",
                        "kind": "fact",
                        "accepted_at": "2026-07-20T12:02:00Z",
                    },
                ],
                "evidence": [],
                "assumptions": [],
                "decisions": [],
                "unknowns": [],
                "artifacts": [],
            }
            value_path = value_dir / "session.json"
            value_path.write_text(json.dumps(value_session), encoding="utf-8")

            init = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS_DIR / "init_session.py"),
                    "--name",
                    "Acme Scheduler",
                    "--slug",
                    slug,
                    "--root",
                    str(root / "workproduct" / "lean-mvp"),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(init.returncode, 0, init.stderr)

            lean_path = lean_dir / "session.json"
            imp = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS_DIR / "import_value_context.py"),
                    str(lean_path),
                    "--value-root",
                    str(root / "workproduct" / "value-proposition"),
                ],
                cwd=SCRIPTS_DIR,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(imp.returncode, 0, imp.stderr)
            payload = json.loads(imp.stdout)
            self.assertIn("C01", payload["imported"])
            self.assertNotIn("U01", payload["imported"])

            lean_session = json.loads(lean_path.read_text(encoding="utf-8"))
            imported_ids = {
                record["atom_id"]
                for record in lean_session["answers"]
                if record.get("provenance") == "value-import"
            }
            self.assertEqual(imported_ids, {"C01"})
            self.assertEqual(lean_session["position"]["atom_id"], "C02")


if __name__ == "__main__":
    unittest.main()
