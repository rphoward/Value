"""Thermos regression guards for the promoted brand-identity skill."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRAND = ROOT / ".cursor" / "skills" / "brand-identity"
SCRIPTS = BRAND / "scripts"


def run_script(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / args[0]), *args[1:]],
        cwd=str(SCRIPTS),
        capture_output=True,
        text=True,
        check=False,
    )


def import_brand_session():
    sys.path.insert(0, str(SCRIPTS))
    import importlib

    if "_session" in sys.modules:
        del sys.modules["_session"]
    for name in list(sys.modules):
        if name.startswith("_session."):
            del sys.modules[name]
    return importlib.import_module("_session")


@unittest.skipUnless(BRAND.is_dir(), "brand-identity live skill missing")
class BrandIdentityThermosFixes(unittest.TestCase):
    def test_resolve_repo_root_from_live_skill_tree(self) -> None:
        mod = import_brand_session()
        root = mod.resolve_repo_root()
        self.assertIsNotNone(root)
        self.assertEqual(root.resolve(), ROOT.resolve())
        wp = mod.default_workproduct_root()
        self.assertEqual(wp.resolve(), (ROOT / "workproduct" / "brand-identity").resolve())

    def test_express_init_parks_on_spine_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / "wp"
            proc = run_script(
                "init_session.py",
                "--name",
                "Express Brand",
                "--slug",
                "express-brand",
                "--root",
                str(work),
                "--pacing-mode",
                "express",
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            session = json.loads((work / "express-brand" / "session.json").read_text(encoding="utf-8"))
            self.assertEqual(session.get("pacing_mode"), "express")
            self.assertEqual(session["position"]["atom_id"], "S04")
            mod = import_brand_session()
            atoms = mod.load_atoms()
            allowed, _hint = mod.can_accept_atom(
                session, "S01", reopen=False, stay=False, records_payload=None
            )
            self.assertFalse(allowed)
            self.assertIn("S04", mod.ready_atoms(session, atoms))
            self.assertNotIn("S01", mod.ready_atoms(session, atoms))

    def test_express_blocks_next_module_while_gate_pending(self) -> None:
        mod = import_brand_session()
        session = mod.default_session("gate-pending", "Gate Pending", pacing_mode="express")
        # Simulate express path answered through G01 with gate pending (no milestone).
        for atom_id, answer in (
            ("S04", "brief"),
            ("G01", "pass brand-strategist gate"),
        ):
            session["answers"].append(
                {
                    "atom_id": atom_id,
                    "answer": answer,
                    "kind": "decision",
                    "accepted_at": "2026-08-01T00:00:00Z",
                }
            )
        session["decisions"].append(
            {
                "decision": "pass brand-strategist gate",
                "reason": "enough",
                "source_atom": "G01",
                "resulting_module": "brand-strategist",
                "resulting_atom": "G01",
                "resulting_status": "completed",
            }
        )
        session["position"] = {
            "module": "brand-strategist",
            "atom_id": "G01",
            "status": "gate_pending",
        }
        atoms = mod.load_atoms()
        ready = mod.ready_atoms(session, atoms)
        self.assertNotIn("S06", ready)
        self.assertNotIn("S05", ready)
        allowed, _ = mod.can_accept_atom(
            session, "S06", reopen=False, stay=False, records_payload=None
        )
        self.assertFalse(allowed)

    def test_milestone_unknowns_are_module_scoped(self) -> None:
        mod = import_brand_session()
        session = mod.default_session("unk", "Unknowns")
        session["answers"].append(
            {
                "atom_id": "S01",
                "answer": "clinic scheduling",
                "kind": "fact",
                "accepted_at": "t",
            }
        )
        session["unknowns"] = [
            {
                "question": "Trademark class?",
                "blocking": True,
                "source_atom": "S01",
            },
            {
                "question": "Favicon contrast?",
                "blocking": False,
                "source_atom": "S06",
            },
        ]
        md = mod.fill_milestone_template(session, "brand-strategist")
        self.assertIn("Trademark class?", md)
        self.assertNotIn("Favicon contrast?", md)


if __name__ == "__main__":
    unittest.main()
