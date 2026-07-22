"""Tests for .cursor/skills/scripted-skill-from-doc (prompt-suite-compile pack)."""

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
AUDIT = SCRIPTS / "audit_dag.py"
PROMOTE = SCRIPTS / "promote.py"
LEAN_DOC = ROOT / "docs" / "lean-product-playbook-prompt-suite.md"
VALUE_DOC = ROOT / "docs" / "value-proposition-prompt-suite (1).md"


def run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=cwd or ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class PromptSuiteCompileTests(unittest.TestCase):
    def test_parse_lean_has_four_modules_and_kb(self) -> None:
        proc = run([str(COMPILE), "parse", "--source", str(LEAN_DOC)])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        ir = json.loads(proc.stdout)
        self.assertEqual(len(ir["modules"]), 4)
        self.assertIn("kano_model_categories", ir["knowledge_base"])

    def test_parse_value_has_four_modules(self) -> None:
        proc = run([str(COMPILE), "parse", "--source", str(VALUE_DOC)])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        ir = json.loads(proc.stdout)
        self.assertEqual(len(ir["modules"]), 4)

    def test_scaffold_and_audit_and_refuses_value_slug(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "drafts"
            proc = run(
                [
                    str(COMPILE),
                    "scaffold",
                    "--source",
                    str(LEAN_DOC),
                    "--slug",
                    "lean-draft-test",
                    "--out",
                    str(out),
                ]
            )
            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            draft = out / "lean-draft-test"
            self.assertTrue((draft / "SKILL.md").is_file())
            self.assertTrue((draft / "assets" / "knowledge-base.json").is_file())
            self.assertFalse((ROOT / "skills" / "value" / "SKILL.md").samefile(
                draft / "SKILL.md"
            ) if (draft / "SKILL.md").exists() else True)

            audit = run([str(AUDIT), str(draft), "--mode", "standard"])
            self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)
            report = json.loads(audit.stdout)
            self.assertTrue(report["ok"])
            self.assertEqual(report["standard"]["missing_hard"], [])

            bad = run(
                [
                    str(COMPILE),
                    "scaffold",
                    "--source",
                    str(LEAN_DOC),
                    "--slug",
                    "value",
                    "--out",
                    str(out),
                ]
            )
            self.assertNotEqual(bad.returncode, 0)

    def test_check_fixture(self) -> None:
        proc = run([str(COMPILE), "check"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        report = json.loads(proc.stdout)
        self.assertTrue(report["ok"])
        self.assertGreaterEqual(report["modules"], 2)
        self.assertIn("value_fixture", report)

    def test_promote_refuses_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / "value"
            fake.mkdir()
            (fake / "SKILL.md").write_text("name: value\n", encoding="utf-8")
            (fake / "assets").mkdir()
            (fake / "assets" / "atoms.json").write_text(
                json.dumps(
                    {
                        "atoms": [
                            {
                                "id": "S01",
                                "module": "m",
                                "asks": "Q?",
                                "accepts_summary": "a",
                                "unlocks": None,
                                "gate": True,
                                "requires": [],
                                "section": "Gate",
                                "soft": False,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            proc = run([str(PROMOTE), str(fake)])
            self.assertNotEqual(proc.returncode, 0)

    def test_promote_refuses_pack_slug_and_force_needs_overwrite_slug(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pack_named = root / "scripted-skill-from-doc"
            pack_named.mkdir()
            (pack_named / "SKILL.md").write_text("x\n", encoding="utf-8")
            refused = run([str(PROMOTE), str(pack_named), "--repo", str(root)])
            self.assertNotEqual(refused.returncode, 0)

            out = root / "drafts"
            scaffold = run(
                [
                    str(COMPILE),
                    "scaffold",
                    "--source",
                    str(PACK / "assets" / "fixtures" / "sample-prompt-suite.md"),
                    "--slug",
                    "promo-safe",
                    "--out",
                    str(out),
                ]
            )
            self.assertEqual(scaffold.returncode, 0, scaffold.stderr + scaffold.stdout)
            draft = out / "promo-safe"
            live = root / ".cursor" / "skills" / "promo-safe"
            live.mkdir(parents=True)
            (live / "SKILL.md").write_text("old\n", encoding="utf-8")

            no_force = run([str(PROMOTE), str(draft), "--repo", str(root)])
            self.assertNotEqual(no_force.returncode, 0)

            force_only = run(
                [str(PROMOTE), str(draft), "--repo", str(root), "--force"]
            )
            self.assertNotEqual(force_only.returncode, 0)
            self.assertIn("overwrite-slug", force_only.stderr)

            ok = run(
                [
                    str(PROMOTE),
                    str(draft),
                    "--repo",
                    str(root),
                    "--force",
                    "--overwrite-slug",
                    "promo-safe",
                ]
            )
            self.assertEqual(ok.returncode, 0, ok.stderr + ok.stdout)
            self.assertTrue((live / "SKILL.md").is_file())

    def test_audit_both_fails_when_express_spine_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "drafts"
            scaffold = run(
                [
                    str(COMPILE),
                    "scaffold",
                    "--source",
                    str(PACK / "assets" / "fixtures" / "sample-prompt-suite.md"),
                    "--slug",
                    "audit-express",
                    "--out",
                    str(out),
                ]
            )
            self.assertEqual(scaffold.returncode, 0, scaffold.stderr)
            draft = out / "audit-express"
            cfg_path = draft / "assets" / "skill-config.json"
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            cfg.pop("express_spine", None)
            cfg_path.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
            audit = run([str(AUDIT), str(draft), "--mode", "both"])
            self.assertNotEqual(audit.returncode, 0)
            report = json.loads(audit.stdout)
            self.assertFalse(report["ok"])
            self.assertIn("error", report["express"])

    def test_scaffold_refuses_live_cursor_skills_out(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            live_parent = Path(tmp) / ".cursor" / "skills"
            live_parent.mkdir(parents=True)
            bad = run(
                [
                    str(COMPILE),
                    "scaffold",
                    "--source",
                    str(PACK / "assets" / "fixtures" / "sample-prompt-suite.md"),
                    "--slug",
                    "nope-live",
                    "--out",
                    str(live_parent),
                ]
            )
            self.assertNotEqual(bad.returncode, 0)


if __name__ == "__main__":
    unittest.main()
