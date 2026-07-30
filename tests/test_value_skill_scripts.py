"""Value skill script smoke tests."""

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

class ValueSkillScriptSmokeTests(unittest.TestCase):
    def test_init_derives_slug_from_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            work_root = Path(tmp) / "workproduct" / "value-proposition"
            init = run_script(
                "init_session.py",
                "--name",
                "Cleaner Scheduler",
                "--root",
                str(work_root),
            )
            self.assertEqual(init.returncode, 0, init.stderr)
            session_path = work_root / "cleaner-scheduler" / "session.json"
            self.assertTrue(session_path.is_file())
            session = json.loads(session_path.read_text(encoding="utf-8"))
            self.assertEqual(session["project"]["slug"], "cleaner-scheduler")
            self.assertEqual(session["project"]["name"], "Cleaner Scheduler")

    def test_init_accept_next_milestone_and_briefs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            work_root = Path(tmp) / "workproduct" / "value-proposition"
            session_path = work_root / "demo" / "session.json"

            init = run_script(
                "init_session.py",
                "--slug",
                "demo",
                "--name",
                "Demo",
                "--root",
                str(work_root),
            )
            self.assertEqual(init.returncode, 0, init.stderr)

            status = run_script("status.py", str(session_path), "--operator")
            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertIn("Ledger:", status.stdout)

            brief = run_script("status.py", str(session_path))
            self.assertEqual(brief.returncode, 0, brief.stderr)
            self.assertNotIn("Ledger:", brief.stdout)
            self.assertIn("Customer profile", brief.stdout)
            self.assertIn("question: segment", brief.stdout)

            next_q = run_script("next_question.py", str(session_path))
            self.assertEqual(next_q.returncode, 0, next_q.stderr)
            payload = json.loads(next_q.stdout)
            self.assertEqual(payload["atom_id"], "P01")

            accept = run_script(
                "accept_answer.py",
                str(session_path),
                "--atom-id",
                "P01",
                "--answer",
                "Independent cleaners in metro areas; exclude enterprise franchises.",
                "--kind",
                "decision",
            )
            self.assertEqual(accept.returncode, 0, accept.stderr)

            next_after = run_script("next_question.py", str(session_path))
            self.assertEqual(next_after.returncode, 0, next_after.stderr)
            self.assertEqual(json.loads(next_after.stdout)["atom_id"], "P02")

            dup = run_script(
                "accept_answer.py",
                str(session_path),
                "--atom-id",
                "P01",
                "--answer",
                "duplicate",
                "--kind",
                "decision",
            )
            self.assertNotEqual(dup.returncode, 0)

            reopen = run_script(
                "accept_answer.py",
                str(session_path),
                "--atom-id",
                "P01",
                "--answer",
                "Revised segment boundary.",
                "--kind",
                "decision",
                "--reopen",
                "--conflict-note",
                "User narrowed segment.",
            )
            self.assertEqual(reopen.returncode, 0, reopen.stderr)

            briefs = run_script(
                "write_design_briefs.py",
                str(session_path),
                "--force",
            )
            self.assertEqual(briefs.returncode, 0, briefs.stderr)
            for name in (
                "product-design-brief.md",
                "ux-brief.md",
                "app-design-brief.md",
            ):
                self.assertTrue((session_path.parent / name).is_file(), name)

            session = json.loads(session_path.read_text(encoding="utf-8"))
            self.assertIn("ledger", session)
            self.assertIn("completion_pct", session["ledger"])

    def test_accept_records_sidecar_appends_session_arrays(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            work_root = Path(tmp) / "workproduct" / "value-proposition"
            session_path = work_root / "demo" / "session.json"
            records_path = Path(tmp) / "records.json"

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
                        "evidence": [
                            {
                                "claim": "Cleaner booked three clients manually last week",
                                "kind": "fact",
                                "source": "user interview",
                                "strength": "moderate",
                            }
                        ],
                        "assumptions": [
                            {
                                "claim": "Segment will pay for scheduling",
                                "criticality": "high",
                                "evidence_status": "unsupported",
                            }
                        ],
                        "decisions": [
                            {
                                "decision": "accepted segment boundary",
                                "reason": "Observable role with exclusion",
                                "resulting_module": "profile",
                                "resulting_atom": "P02",
                                "resulting_status": "in_progress",
                            }
                        ],
                        "unknowns": [
                            {
                                "question": "Budget evidence not established",
                                "blocking": False,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            accept = run_script(
                "accept_answer.py",
                str(session_path),
                "--atom-id",
                "P01",
                "--answer",
                "Independent cleaners in metro areas; exclude enterprise franchises.",
                "--kind",
                "decision",
                "--records",
                str(records_path),
            )
            self.assertEqual(accept.returncode, 0, accept.stderr)

            session = json.loads(session_path.read_text(encoding="utf-8"))
            self.assertEqual(len(session["evidence"]), 1)
            self.assertEqual(len(session["assumptions"]), 1)
            self.assertEqual(session["assumptions"][0]["source_atom"], "P01")
            self.assertEqual(len(session["decisions"]), 1)
            self.assertEqual(len(session["unknowns"]), 1)
            self.assertEqual(session["position"]["atom_id"], "P02")

    def test_build_pack_writes_ide_exports_and_skips_ceremony(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            work_root = Path(tmp) / "workproduct" / "value-proposition"
            session_path = work_root / "demo" / "session.json"
            self.assertEqual(
                run_script(
                    "init_session.py",
                    "--name",
                    "Demo Cleaners",
                    "--slug",
                    "demo",
                    "--root",
                    str(work_root),
                ).returncode,
                0,
            )
            session = json.loads(session_path.read_text(encoding="utf-8"))
            timestamp = "2026-07-18T12:00:00Z"
            session["answers"] = [
                {
                    "atom_id": "P01",
                    "answer": "Independent cleaners in metro areas; exclude franchises.",
                    "kind": "decision",
                    "accepted_at": timestamp,
                },
                {
                    "atom_id": "P03",
                    "answer": "Fill open slots the same day a booking request arrives.",
                    "kind": "fact",
                    "accepted_at": timestamp,
                },
                {
                    "atom_id": "V01",
                    "answer": "Recorded bypass value-map gate.",
                    "kind": "decision",
                    "accepted_at": timestamp,
                },
            ]
            session["decisions"] = [
                {
                    "decision": "bypass profile gate",
                    "reason": "pressure-test",
                    "source_atom": "P01",
                    "resulting_module": "value-map",
                    "resulting_atom": "V01",
                    "resulting_status": "in_progress",
                },
                {
                    "decision": "accepted segment boundary",
                    "reason": "Observable role with exclusion",
                    "source_atom": "P01",
                    "resulting_module": "profile",
                    "resulting_atom": "P02",
                    "resulting_status": "in_progress",
                },
            ]
            session["assumptions"] = [
                {
                    "claim": "Cleaners will pay monthly for scheduling",
                    "criticality": "high",
                    "evidence_status": "unsupported",
                    "source_atom": "P01",
                }
            ]
            session_path.write_text(json.dumps(session, indent=2), encoding="utf-8")

            pack = run_script("write_build_pack.py", str(session_path), "--force")
            self.assertEqual(pack.returncode, 0, pack.stderr)

            context = (session_path.parent / "CONTEXT.product.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("Independent cleaners", context)
            self.assertNotIn("Recorded bypass", context)
            self.assertIn("Fill open slots", context)

            agents = (session_path.parent / "AGENTS.product.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("## Always", agents)
            self.assertIn("## Ask first", agents)
            self.assertIn("Cleaners will pay monthly", agents)

            for name in (
                "ui-copy.md",
                "states-and-flows.md",
                "first-value.md",
                "north-star-blurb.md",
                "value-trail.md",
            ):
                self.assertTrue((session_path.parent / name).is_file(), name)

            blurb = (session_path.parent / "north-star-blurb.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("Independent cleaners", blurb)
            self.assertNotIn("P01", blurb)
            self.assertNotIn("Ledger:", blurb)
            self.assertIn("Draft from accepted session answers", blurb)

            adr_files = list((session_path.parent / "docs" / "adr").glob("*.md"))
            self.assertGreaterEqual(len(adr_files), 1)
            adr_text = "\n".join(path.read_text(encoding="utf-8") for path in adr_files)
            self.assertIn("bypass profile gate", adr_text)
            self.assertIn("accepted segment boundary", adr_text)

            brief = run_script(
                "write_design_briefs.py", str(session_path), "--force"
            )
            self.assertEqual(brief.returncode, 0, brief.stderr)
            product = (
                session_path.parent / "product-design-brief.md"
            ).read_text(encoding="utf-8")
            self.assertIn("Independent cleaners", product)
            self.assertNotIn("Recorded bypass value-map gate", product)

    def _trail_fixture_session(self, session_path: Path, *, with_v02: bool = False) -> None:
        session = json.loads(session_path.read_text(encoding="utf-8"))
        timestamp = "2026-07-19T12:00:00Z"
        session["answers"] = [
            {
                "atom_id": "P01",
                "answer": "Independent cleaners in metro areas; exclude franchises.",
                "kind": "decision",
                "accepted_at": timestamp,
            },
            {
                "atom_id": "P03",
                "answer": "Fill open slots the same day a booking request arrives.",
                "kind": "fact",
                "accepted_at": timestamp,
            },
            {
                "atom_id": "P07",
                "answer": (
                    "Extreme: no-shows wreck the day; Mild: late replies from clients."
                ),
                "kind": "inference",
                "accepted_at": timestamp,
            },
        ]
        if with_v02:
            session["answers"].append(
                {
                    "atom_id": "V02",
                    "answer": "Same-day slot matcher; SMS reminders; client reply inbox.",
                    "kind": "hypothesis",
                    "accepted_at": timestamp,
                }
            )
        session_path.write_text(json.dumps(session, indent=2), encoding="utf-8")

    def test_value_trail_smoke_matches_outward_pitch(self) -> None:
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
                    "Demo Cleaners",
                    "--root",
                    str(work_root),
                ).returncode,
                0,
            )
            self._trail_fixture_session(session_path)
            pack = run_script("write_build_pack.py", str(session_path), "--force")
            self.assertEqual(pack.returncode, 0, pack.stderr)

            trail = (session_path.parent / "value-trail.md").read_text(encoding="utf-8")
            blurb = (session_path.parent / "north-star-blurb.md").read_text(
                encoding="utf-8"
            )
            session = json.loads(session_path.read_text(encoding="utf-8"))
            pitch = session_mod.compose_outward_pitch(session)

            for title in (
                "Who it is for",
                "Progress they want",
                "Why it matters to someone else",
                "Outward pitch",
            ):
                self.assertIn(f"## {title}", trail, title)
            self.assertIn(pitch, trail)
            self.assertIn(pitch, blurb)
            self.assertIn("no-shows wreck the day", trail)
            self.assertNotIn("P01", trail)
            self.assertNotIn("Ledger:", trail)
            self.assertNotIn("npx skills add", trail)

    def test_value_trail_adds_parts_without_changing_pitch(self) -> None:
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
                    "Demo Cleaners",
                    "--root",
                    str(work_root),
                ).returncode,
                0,
            )
            self._trail_fixture_session(session_path)
            session = json.loads(session_path.read_text(encoding="utf-8"))
            pitch_before = session_mod.compose_outward_pitch(session)

            self._trail_fixture_session(session_path, with_v02=True)
            pack = run_script("write_build_pack.py", str(session_path), "--force")
            self.assertEqual(pack.returncode, 0, pack.stderr)

            trail = (session_path.parent / "value-trail.md").read_text(encoding="utf-8")
            session = json.loads(session_path.read_text(encoding="utf-8"))
            pitch_after = session_mod.compose_outward_pitch(session)

            self.assertIn("## What is in the box", trail)
            self.assertIn("Same-day slot matcher", trail)
            self.assertEqual(pitch_before, pitch_after)

    def test_outward_pitch_strips_labels_and_avoids_autonomy_slop(self) -> None:
        """Catastrophe: Discord paste leaks interview labels or autonomy-as-offering."""
        session_mod = import_session_helper()
        session = {
            "answers": [
                {
                    "atom_id": "P01",
                    "answer": (
                        "Cursor-using Discord friends who ship personal projects "
                        "but struggle to make them valuable to people outside; "
                        "Excluded: novelty-first vibecoders."
                    ),
                    "kind": "decision",
                    "accepted_at": "2026-07-19T12:00:00Z",
                },
                {
                    "atom_id": "P11",
                    "answer": (
                        "Priority job (elevated): Autonomy — safe space to create "
                        "freely with AI (also named creativity, liberty, freedom)."
                    ),
                    "kind": "decision",
                    "accepted_at": "2026-07-19T12:00:00Z",
                },
                {
                    "atom_id": "P07",
                    "answer": (
                        "Extreme: lack of marketing skills — group can program "
                        "but cannot articulate outward value; Mild: slow replies."
                    ),
                    "kind": "inference",
                    "accepted_at": "2026-07-19T12:00:00Z",
                },
            ]
        }
        pitch = session_mod.compose_outward_pitch(session)
        self.assertIn("They freeze on", pitch)
        self.assertIn("lack of marketing skills", pitch)
        self.assertIn("You get a clear outward pitch", pitch)
        self.assertNotIn("Priority job", pitch)
        self.assertNotIn("Extreme:", pitch)
        self.assertNotIn("help them", pitch)
        self.assertNotIn("Autonomy", pitch)

        cleaners = {
            "answers": [
                {
                    "atom_id": "P01",
                    "answer": "Independent cleaners in metro areas; exclude franchises.",
                    "kind": "decision",
                    "accepted_at": "2026-07-19T12:00:00Z",
                },
                {
                    "atom_id": "P03",
                    "answer": "Fill open slots the same day a booking request arrives.",
                    "kind": "fact",
                    "accepted_at": "2026-07-19T12:00:00Z",
                },
                {
                    "atom_id": "P07",
                    "answer": "Extreme: no-shows wreck the day; Mild: late replies.",
                    "kind": "inference",
                    "accepted_at": "2026-07-19T12:00:00Z",
                },
            ]
        }
        cleaners_pitch = session_mod.compose_outward_pitch(cleaners)
        self.assertIn("Independent cleaners in metro areas", cleaners_pitch)
        self.assertIn("They freeze on no-shows wreck the day", cleaners_pitch)
        self.assertIn("North star: fill open slots the same day", cleaners_pitch)
        self.assertNotIn("Extreme:", cleaners_pitch)
        self.assertNotIn("help them", cleaners_pitch)

        long_job = {
            "answers": [
                {
                    "atom_id": "P01",
                    "answer": (
                        "Cursor-using Discord friends who ship personal projects "
                        "but struggle to make them valuable to people outside."
                    ),
                    "kind": "decision",
                    "accepted_at": "2026-07-19T12:00:00Z",
                },
                {
                    "atom_id": "P03",
                    "answer": (
                        "Go from scattered try-post-and-hope showcase cycles to "
                        "seeing a clear direction: understand what they should "
                        "build next for someone else."
                    ),
                    "kind": "fact",
                    "accepted_at": "2026-07-19T12:00:00Z",
                },
                {
                    "atom_id": "P07",
                    "answer": "Extreme: lack of marketing skills — cannot articulate.",
                    "kind": "inference",
                    "accepted_at": "2026-07-19T12:00:00Z",
                },
            ]
        }
        long_pitch = session_mod.compose_outward_pitch(long_job)
        self.assertIn("They freeze on lack of marketing skills", long_pitch)
        self.assertIn("North star: go from scattered", long_pitch)
        self.assertIn("seeing a clear direction", long_pitch)
        self.assertNotIn("understand what they", long_pitch)
        self.assertNotIn("help them", long_pitch)

    def test_bypassed_modules_unlock_briefs_without_force(self) -> None:
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

            bypass_chain = (
                (
                    "P01",
                    "profile",
                    "bypass profile gate",
                    "value-map",
                    "V01",
                ),
                (
                    "V01",
                    "value-map",
                    "bypass value-map gate",
                    "business-model",
                    "B01",
                ),
                (
                    "B01",
                    "business-model",
                    "bypass business-model gate",
                    "experiments",
                    "E01",
                ),
                (
                    "E01",
                    "experiments",
                    "bypass experiments gate",
                    "experiments",
                    "E01",
                ),
            )
            for index, (atom_id, _module, decision_text, target_module, target_atom) in enumerate(
                bypass_chain
            ):
                records_path = Path(tmp) / f"bypass-{index}.json"
                records_path.write_text(
                    json.dumps(
                        {
                            "decisions": [
                                {
                                    "decision": decision_text,
                                    "reason": "pressure-test bypass",
                                    "resulting_module": target_module,
                                    "resulting_atom": target_atom,
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
                    atom_id,
                    "--answer",
                    f"Recorded {decision_text}.",
                    "--kind",
                    "decision",
                    "--records",
                    str(records_path),
                )
                self.assertEqual(result.returncode, 0, result.stderr)

            briefs = run_script("write_design_briefs.py", str(session_path))
            self.assertEqual(briefs.returncode, 0, briefs.stderr)
            for name in (
                "product-design-brief.md",
                "ux-brief.md",
                "app-design-brief.md",
            ):
                self.assertTrue((session_path.parent / name).is_file(), name)

    def test_gate_pass_decision_enables_module_completion(self) -> None:
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
                                "reason": "Segment, jobs, pains, gains, alternatives explicit",
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
                "Pass — profile is ready for value-map work.",
                "--kind",
                "decision",
                "--gate-pending",
                "--records",
                str(records_path),
            )
            self.assertEqual(accept.returncode, 0, accept.stderr)

            milestone = run_script(
                "write_milestone.py",
                str(session_path),
                "--module",
                "profile",
            )
            self.assertEqual(milestone.returncode, 0, milestone.stderr)

            session = json.loads(session_path.read_text(encoding="utf-8"))
            self.assertTrue(
                any(
                    item["path"] == "customer-profile.md" and item["status"] == "final"
                    for item in session["artifacts"]
                )
            )
            blurb_path = session_path.parent / "north-star-blurb.md"
            self.assertTrue(
                blurb_path.is_file(),
                "write_milestone must refresh build pack including north-star-blurb.md",
            )
            self.assertTrue((session_path.parent / "CONTEXT.product.md").is_file())

    def test_next_question_includes_match_board_for_v03(self) -> None:
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
            timestamp = "2026-07-19T12:00:00Z"
            session["answers"] = [
                {
                    "atom_id": "P01",
                    "answer": "Independent cleaners in metro areas; exclude franchises.",
                    "kind": "decision",
                    "accepted_at": timestamp,
                },
                {
                    "atom_id": "P07",
                    "answer": (
                        "Extreme: no-shows wreck the day; Mild: late replies from clients."
                    ),
                    "kind": "inference",
                    "accepted_at": timestamp,
                },
                {
                    "atom_id": "P08",
                    "answer": "Steady bookings; calmer mornings.",
                    "kind": "hypothesis",
                    "accepted_at": timestamp,
                },
                {
                    "atom_id": "V01",
                    "answer": "Scheduling assistant for independents; exclude franchise CRM.",
                    "kind": "decision",
                    "accepted_at": timestamp,
                },
                {
                    "atom_id": "V02",
                    "answer": (
                        "Included: (1) SMS reminder bot; (2) same-day slot board; "
                        "(3) deposit hold."
                    ),
                    "kind": "fact",
                    "accepted_at": timestamp,
                },
            ]
            session["decisions"] = [
                {
                    "decision": "bypass profile gate",
                    "reason": "match-board smoke",
                    "source_atom": "P01",
                    "resulting_module": "value-map",
                    "resulting_atom": "V01",
                    "resulting_status": "in_progress",
                }
            ]
            session["position"] = {
                "module": "value-map",
                "atom_id": "V03",
                "status": "in_progress",
            }
            session_path.write_text(json.dumps(session, indent=2), encoding="utf-8")
            payload = json.loads(run_script("next_question.py", str(session_path)).stdout)
            self.assertEqual(payload["atom_id"], "V03")
            self.assertIn("match_board", payload)
            board = payload["match_board"]
            self.assertGreaterEqual(len(board["parts"]), 2)
            self.assertGreaterEqual(len(board["targets"]), 1)
            self.assertEqual(len(board["part_labels"]), len(board["parts"]))
            self.assertEqual(len(board["target_labels"]), len(board["targets"]))
            for label in board["part_labels"] + board["target_labels"]:
                self.assertLessEqual(len(label.split()), 10, label)
            self.assertIn("match_prompt", payload)
            self.assertIn("Offering parts:", payload["match_prompt"])
            self.assertIn("Accepted pains:", payload["match_prompt"])
            self.assertTrue(
                any("Extreme" in item or "no-shows" in item for item in board["targets"])
            )

    def test_promote_context_dry_run_prints_terms_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            work_root = repo / "workproduct" / "value-proposition" / "demo"
            work_root.mkdir(parents=True)
            seed = work_root / "CONTEXT.product.md"
            seed.write_text(
                "# Demo\n\n## Offering\n\n"
                "- (decision) ShiftSwap: a lightweight shift trade flow for servers.\n",
                encoding="utf-8",
            )
            context_path = repo / "CONTEXT.md"
            result = run_script(
                "promote_context.py",
                str(seed),
                cwd=repo,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("**ShiftSwap**:", result.stdout)
            self.assertIn("_Avoid_:", result.stdout)
            self.assertFalse(context_path.is_file(), "dry-run must not write CONTEXT.md")

            flagged = run_script(
                "promote_context.py",
                str(seed),
                "--dry-run",
                cwd=repo,
            )
            self.assertEqual(
                flagged.returncode,
                0,
                "surface-promote cites --dry-run; flag must be accepted",
            )
            self.assertIn("**ShiftSwap**:", flagged.stdout)
            self.assertFalse(context_path.is_file())

    def test_promote_context_apply_writes_context_md(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            work_root = repo / "workproduct" / "value-proposition" / "demo"
            work_root.mkdir(parents=True)
            seed = work_root / "CONTEXT.product.md"
            seed.write_text(
                "# Demo\n\n## Offering\n\n"
                "- (decision) ShiftSwap: a lightweight shift trade flow for servers.\n",
                encoding="utf-8",
            )
            context_path = repo / "CONTEXT.md"
            dry = run_script("promote_context.py", str(seed), cwd=repo)
            self.assertEqual(dry.returncode, 0, dry.stderr)
            self.assertFalse(context_path.is_file())

            applied = run_script(
                "promote_context.py",
                str(seed),
                "--apply",
                cwd=repo,
            )
            self.assertEqual(applied.returncode, 0, applied.stderr)
            self.assertTrue(context_path.is_file())
            text = context_path.read_text(encoding="utf-8")
            self.assertIn("## Language", text)
            self.assertIn("**ShiftSwap**:", text)

    def test_promote_context_missing_seed_exits_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            session = repo / "workproduct" / "value-proposition" / "demo" / "session.json"
            session.parent.mkdir(parents=True)
            session.write_text("{}", encoding="utf-8")
            result = run_script("promote_context.py", str(session), cwd=repo)
            self.assertNotEqual(result.returncode, 0)

    def test_promote_context_dedupes_repeated_bullets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            work_root = repo / "workproduct" / "value-proposition" / "demo"
            work_root.mkdir(parents=True)
            seed = work_root / "CONTEXT.product.md"
            seed.write_text(
                "# Demo\n\n## Context\n\n"
                "- (decision) ShiftSwap: same-restaurant shift trade.\n\n"
                "## Offering\n\n"
                "- (decision) ShiftSwap: same-restaurant shift trade.\n",
                encoding="utf-8",
            )
            result = run_script("promote_context.py", str(seed), cwd=repo)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.count("**ShiftSwap**:"), 1)

    def test_promote_context_apply_preserves_existing_terms(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            work_root = repo / "workproduct" / "value-proposition" / "demo"
            work_root.mkdir(parents=True)
            seed = work_root / "CONTEXT.product.md"
            seed.write_text(
                "# Demo\n\n## Offering\n\n"
                "- (decision) ShiftSwap: a lightweight shift trade flow for servers.\n",
                encoding="utf-8",
            )
            context_path = repo / "CONTEXT.md"
            context_path.write_text(
                "# Project\n\n## Language\n\n"
                "**ShiftSwap**:\n"
                "existing definition kept\n"
                "_Avoid_: old\n",
                encoding="utf-8",
            )
            applied = run_script(
                "promote_context.py",
                str(seed),
                "--apply",
                cwd=repo,
            )
            self.assertEqual(applied.returncode, 0, applied.stderr)
            text = context_path.read_text(encoding="utf-8")
            self.assertIn("existing definition kept", text)
            self.assertEqual(text.count("**ShiftSwap**:"), 1)

    def test_promote_context_agents_writes_without_apply(self) -> None:
        """--agents is its own write gate; it must not require --apply."""
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            work_root = repo / "workproduct" / "value-proposition" / "demo"
            work_root.mkdir(parents=True)
            seed = work_root / "CONTEXT.product.md"
            seed.write_text(
                "# Demo\n\n## Offering\n\n"
                "- (decision) ShiftSwap: a lightweight shift trade flow for servers.\n",
                encoding="utf-8",
            )
            agents_path = repo / "AGENTS.md"
            result = run_script(
                "promote_context.py",
                str(seed),
                "--agents",
                cwd=repo,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(agents_path.is_file())
            self.assertIn("Product-Spine and Values notes", agents_path.read_text(encoding="utf-8"))
            self.assertFalse((repo / "CONTEXT.md").is_file())

    def test_promote_context_dry_run_wins_over_apply_and_agents(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            work_root = repo / "workproduct" / "value-proposition" / "demo"
            work_root.mkdir(parents=True)
            seed = work_root / "CONTEXT.product.md"
            seed.write_text(
                "# Demo\n\n## Offering\n\n"
                "- (decision) ShiftSwap: a lightweight shift trade flow for servers.\n",
                encoding="utf-8",
            )
            result = run_script(
                "promote_context.py",
                str(seed),
                "--dry-run",
                "--apply",
                "--agents",
                cwd=repo,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((repo / "CONTEXT.md").is_file())
            self.assertFalse((repo / "AGENTS.md").is_file())


if __name__ == "__main__":
    unittest.main()
