"""Value skill DAG and pacing tests."""

from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

from tests.value_skill_support import (
    ASSETS_DIR,
    ATOM_FIELDS,
    ATOM_ID_RE,
    BRACKET_TOKEN_RE,
    MODULE_FILES,
    MODULE_NAMES,
    REFERENCE_FILES,
    REFERENCES_DIR,
    REQUIRED_KB_KEYS,
    REQUIRED_SCHEMA_PROPERTIES,
    ROOT,
    SCRIPTS_DIR,
    SKILL_MD,
    SKILL_ROOT,
    TEMPLATE_FILES,
    atom_field,
    extract_reference_links,
    file_digest,
    frontmatter_field,
    import_session_helper,
    module_atom_ids,
    parse_frontmatter,
    read_skill_md,
    record_operations,
    run_script,
    split_atoms,
)

class ValueSkillDagTests(unittest.TestCase):
    def test_atoms_json_dag_metadata(self) -> None:
        payload = json.loads((ASSETS_DIR / "atoms.json").read_text(encoding="utf-8"))
        for atom in payload["atoms"]:
            for field in ("requires", "section", "soft"):
                self.assertIn(field, atom, f"{atom['id']} missing {field}")
            self.assertIsInstance(atom["requires"], list)
            self.assertIsInstance(atom["soft"], bool)
        session_mod = import_session_helper()
        cycles = session_mod.detect_dag_cycles(payload["atoms"])
        self.assertEqual(cycles, [], f"DAG cycles detected: {cycles}")

    def test_parallel_ready_after_p03(self) -> None:
        session_mod = import_session_helper()
        atoms = session_mod.load_atoms()
        session = session_mod.default_session("demo", "Demo")
        timestamp = session_mod.utc_now_iso()
        for atom_id in ("P01", "P02", "P03"):
            session["answers"].append(
                {
                    "atom_id": atom_id,
                    "answer": f"answer for {atom_id}",
                    "kind": "fact",
                    "accepted_at": timestamp,
                }
            )
        ready = set(session_mod.ready_atoms(session, atoms))
        for atom_id in ("P04", "P05", "P06", "P07", "P08"):
            self.assertIn(atom_id, ready, f"{atom_id} should be ready after P03")

    def test_p08_accepts_unknown_kind(self) -> None:
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
            session_path.write_text(json.dumps(session, indent=2), encoding="utf-8")
            accept = run_script(
                "accept_answer.py",
                str(session_path),
                "--atom-id",
                "P08",
                "--answer",
                "More bookings; relevance labels unknown.",
                "--kind",
                "unknown",
            )
            self.assertEqual(accept.returncode, 0, accept.stderr)

    def test_accept_bulk_from_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            work_root = Path(tmp) / "workproduct" / "value-proposition"
            session_path = work_root / "demo" / "session.json"
            map_path = Path(tmp) / "draft-map.json"
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
            timestamp = "2026-07-18T12:00:00Z"
            session["answers"].append(
                {
                    "atom_id": "P01",
                    "answer": "Independent cleaners",
                    "kind": "decision",
                    "accepted_at": timestamp,
                }
            )
            session_path.write_text(json.dumps(session, indent=2), encoding="utf-8")
            map_path.write_text(
                json.dumps(
                    {
                        "source": "user_brain_dump",
                        "mappings": [
                            {
                                "atom_id": "P02",
                                "answer": "New booking request arrives",
                                "kind": "fact",
                                "satisfied": True,
                            },
                            {
                                "atom_id": "P03",
                                "answer": "Fill open slots quickly",
                                "kind": "fact",
                                "satisfied": True,
                            },
                            {
                                "atom_id": "P07",
                                "answer": "No-shows and gaps",
                                "kind": "unknown",
                                "satisfied": True,
                                "gaps": ["severity labels"],
                            },
                        ],
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
            self.assertEqual(bulk.returncode, 0, bulk.stderr)
            session = json.loads(session_path.read_text(encoding="utf-8"))
            answered = {record["atom_id"] for record in session["answers"]}
            self.assertTrue({"P02", "P03", "P07"}.issubset(answered))

    def test_gaps_no_hard_when_only_soft_missing(self) -> None:
        session_mod = import_session_helper()
        atoms = session_mod.load_atoms()
        session = session_mod.default_session("demo", "Demo")
        timestamp = session_mod.utc_now_iso()
        for atom_id in ("P01", "P02", "P03"):
            session["answers"].append(
                {
                    "atom_id": atom_id,
                    "answer": f"answer for {atom_id}",
                    "kind": "fact",
                    "accepted_at": timestamp,
                }
            )
        hard = session_mod.hard_gaps_by_section(session, atoms)
        self.assertEqual(hard, {})

    def test_gaps_module_filter_ignores_other_modules(self) -> None:
        """Adversarial: scoped gaps must not leak ready atoms from another module."""
        session_mod = import_session_helper()
        atoms = session_mod.load_atoms()
        session = session_mod.default_session("demo", "Demo")
        timestamp = session_mod.utc_now_iso()
        profile_ids = [
            atom["id"] for atom in atoms if atom["module"] == "profile"
        ]
        for atom_id in profile_ids:
            session["answers"].append(
                {
                    "atom_id": atom_id,
                    "answer": f"answer for {atom_id}",
                    "kind": "decision" if atom_id == "P12" else "fact",
                    "accepted_at": timestamp,
                }
            )
        session["decisions"].append(
            {
                "decision": "pass profile gate",
                "reason": "ready",
                "source_atom": "P12",
                "resulting_module": "profile",
                "resulting_atom": "P12",
                "resulting_status": "gate_pending",
            }
        )
        session_mod.upsert_artifact(session, "customer-profile.md", "final")
        session["position"] = {
            "module": "value-map",
            "atom_id": "V01",
            "status": "in_progress",
        }
        session["answers"].append(
            {
                "atom_id": "V01",
                "answer": "A booking fill product",
                "kind": "fact",
                "accepted_at": timestamp,
            }
        )
        profile_gaps = session_mod.hard_gaps_by_section(session, atoms, "profile")
        value_gaps = session_mod.hard_gaps_by_section(session, atoms, "value-map")
        self.assertEqual(profile_gaps, {})
        self.assertIn("Offering", value_gaps)
        self.assertIn("V02", value_gaps["Offering"])

    def test_stay_rejects_off_focus_atom(self) -> None:
        session_mod = import_session_helper()
        session = session_mod.default_session("demo", "Demo")
        allowed, hint = session_mod.can_accept_atom(
            session, "V05", reopen=False, stay=True, records_payload=None
        )
        self.assertFalse(allowed)
        self.assertIsNotNone(hint)
        self.assertIn("--stay only applies to the active atom", hint)

    def test_gate_pending_flag_required_to_hold_gate(self) -> None:
        session_mod = import_session_helper()
        atoms = session_mod.load_atoms()
        index = session_mod.atom_by_id(atoms)
        session = session_mod.default_session("demo", "Demo")
        session["position"] = {
            "module": "profile",
            "atom_id": "P12",
            "status": "in_progress",
        }
        session_mod.advance_position_after_accept(
            session,
            index["P12"],
            "P12",
            reopen=False,
            stay=False,
            gate_pending=False,
            next_atom_override="",
            records_payload=None,
        )
        self.assertNotEqual(session["position"]["status"], "gate_pending")

    def test_gate_pending_flag_holds_with_pending_artifact(self) -> None:
        session_mod = import_session_helper()
        atoms = session_mod.load_atoms()
        index = session_mod.atom_by_id(atoms)
        session = session_mod.default_session("demo", "Demo")
        session["position"] = {
            "module": "profile",
            "atom_id": "P12",
            "status": "in_progress",
        }
        session_mod.advance_position_after_accept(
            session,
            index["P12"],
            "P12",
            reopen=False,
            stay=False,
            gate_pending=True,
            next_atom_override="",
            records_payload=None,
        )
        self.assertEqual(session["position"]["status"], "gate_pending")
        self.assertEqual(
            session_mod.artifact_status(session, "customer-profile.md"),
            "pending",
        )

    def test_records_gate_pending_upserts_pending_artifact(self) -> None:
        session_mod = import_session_helper()
        atoms = session_mod.load_atoms()
        index = session_mod.atom_by_id(atoms)
        session = session_mod.default_session("demo", "Demo")
        session["position"] = {
            "module": "profile",
            "atom_id": "P12",
            "status": "in_progress",
        }
        session_mod.advance_position_after_accept(
            session,
            index["P12"],
            "P12",
            reopen=False,
            stay=False,
            gate_pending=False,
            next_atom_override="",
            records_payload={
                "decisions": [
                    {
                        "decision": "pass profile gate",
                        "reason": "ready",
                        "source_atom": "P12",
                        "resulting_module": "profile",
                        "resulting_atom": "P12",
                        "resulting_status": "gate_pending",
                    }
                ]
            },
        )
        self.assertEqual(session["position"]["status"], "gate_pending")
        self.assertEqual(
            session_mod.artifact_status(session, "customer-profile.md"),
            "pending",
        )

    def test_adr_refresh_removes_orphan_files(self) -> None:
        session_mod = import_session_helper()
        with tempfile.TemporaryDirectory() as tmp:
            session_dir = Path(tmp)
            adr_dir = session_dir / "docs" / "adr"
            adr_dir.mkdir(parents=True)
            stale = adr_dir / "0001-segment-boundary-locked.md"
            stale.write_text("# stale\n", encoding="utf-8")
            session = {
                "decisions": [
                    {
                        "decision": "park orphan feature X",
                        "reason": "out of scope",
                        "source_atom": "V06",
                    }
                ]
            }
            written = session_mod.write_hard_decision_adrs(session, session_dir)
            self.assertEqual(len(written), 1)
            self.assertTrue(written[0].is_file())
            self.assertFalse(stale.exists())
            names = sorted(path.name for path in adr_dir.glob("*.md"))
            self.assertEqual(names, [written[0].name])

    def test_adr_empty_hard_decisions_leaves_existing_files(self) -> None:
        session_mod = import_session_helper()
        with tempfile.TemporaryDirectory() as tmp:
            session_dir = Path(tmp)
            adr_dir = session_dir / "docs" / "adr"
            adr_dir.mkdir(parents=True)
            keep = adr_dir / "0001-manual-note.md"
            keep.write_text("# keep\n", encoding="utf-8")
            written = session_mod.write_hard_decision_adrs({"decisions": []}, session_dir)
            self.assertEqual(written, [])
            self.assertTrue(keep.is_file())

    def test_milestone_recovers_when_final_artifact_file_missing(self) -> None:
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
            session["position"] = {
                "module": "value-map",
                "atom_id": "V01",
                "status": "in_progress",
            }
            session["decisions"].append(
                {
                    "decision": "pass profile gate",
                    "reason": "ready",
                    "source_atom": "P12",
                    "resulting_module": "profile",
                    "resulting_atom": "P12",
                    "resulting_status": "gate_pending",
                }
            )
            session["artifacts"].append(
                {"path": "customer-profile.md", "status": "final"}
            )
            session_path.write_text(json.dumps(session, indent=2), encoding="utf-8")
            milestone = run_script(
                "write_milestone.py",
                str(session_path),
                "--module",
                "profile",
            )
            self.assertEqual(milestone.returncode, 0, milestone.stderr)
            self.assertTrue((session_path.parent / "customer-profile.md").is_file())

    def test_fill_section_missing_heading_raises(self) -> None:
        session_mod = import_session_helper()
        with self.assertRaises(ValueError) as ctx:
            session_mod.fill_section("# Title\n\n## Present\n\nbody\n", "Missing", "NEW")
        self.assertIn("Missing section heading", str(ctx.exception))

    def test_save_session_is_atomic_replace(self) -> None:
        session_mod = import_session_helper()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "session.json"
            session = session_mod.default_session("demo", "Demo")
            session_mod.save_session(path, session)
            self.assertTrue(path.is_file())
            self.assertFalse(path.with_name("session.json.tmp").exists())
            loaded = session_mod.load_session(path)
            self.assertEqual(loaded["project"]["slug"], "demo")

    def test_status_sections_strip(self) -> None:
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
            timestamp = "2026-07-18T12:00:00Z"
            session["answers"].append(
                {
                    "atom_id": "P01",
                    "answer": "Independent cleaners",
                    "kind": "decision",
                    "accepted_at": timestamp,
                }
            )
            session_path.write_text(json.dumps(session, indent=2), encoding="utf-8")
            result = run_script("status.py", str(session_path), "--sections")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Segment✓", result.stdout)
            self.assertIn("Situation·", result.stdout)

    def test_express_pacing_skips_to_priority_job_spine(self) -> None:
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
                    "--pacing-mode",
                    "express",
                ).returncode,
                0,
            )
            session = json.loads(session_path.read_text(encoding="utf-8"))
            self.assertEqual(session.get("pacing_mode"), "express")
            accept = run_script(
                "accept_answer.py",
                str(session_path),
                "--atom-id",
                "P01",
                "--answer",
                "Independent cleaners",
                "--kind",
                "decision",
            )
            self.assertEqual(accept.returncode, 0, accept.stderr)
            payload = json.loads(run_script("next_question.py", str(session_path)).stdout)
            self.assertEqual(payload["atom_id"], "P03")
            self.assertEqual(payload["pacing_mode"], "express")

    def test_set_pacing_mode_switch(self) -> None:
        session_mod = import_session_helper()
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
                "set_pacing_mode.py",
                str(session_path),
                "--mode",
                "express",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            session = json.loads(session_path.read_text(encoding="utf-8"))
            self.assertEqual(session.get("pacing_mode"), "express")
            self.assertEqual(
                run_script(
                    "set_pacing_mode.py",
                    str(session_path),
                    "--mode",
                    "standard",
                ).returncode,
                0,
            )
            session = json.loads(session_path.read_text(encoding="utf-8"))
            self.assertNotIn("pacing_mode", session)


if __name__ == "__main__":
    unittest.main()
