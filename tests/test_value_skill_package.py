"""Package contract for .cursor/skills/value/ and skills/value/."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


def repo_root() -> Path:
    """Locate the repository root from this test module."""
    here = Path(__file__).resolve()
    for candidate in (here.parent, *here.parents):
        if (candidate / "pyproject.toml").is_file():
            return candidate
    raise RuntimeError(
        "Could not locate repository root from tests/test_value_skill_package.py"
    )


ROOT = repo_root()
CANONICAL_SKILL_ROOT = ROOT / "skills" / "value"
SKILL_ROOT = ROOT / ".cursor" / "skills" / "value"
SKILL_MD = SKILL_ROOT / "SKILL.md"
REFERENCES_DIR = SKILL_ROOT / "references"
ASSETS_DIR = SKILL_ROOT / "assets"
SCRIPTS_DIR = SKILL_ROOT / "scripts"

REFERENCE_FILES = (
    "profile.md",
    "value-map.md",
    "business-model.md",
    "experiments.md",
    "session-contract.md",
)

MODULE_FILES = (
    "profile.md",
    "value-map.md",
    "business-model.md",
    "experiments.md",
)

MODULE_NAMES = {
    "profile.md": "profile",
    "value-map.md": "value-map",
    "business-model.md": "business-model",
    "experiments.md": "experiments",
}

TEMPLATE_FILES = (
    "customer-profile.template.md",
    "value-map.template.md",
    "business-model.template.md",
    "experiment-plan.template.md",
    "product-design-brief.template.md",
    "ux-brief.template.md",
    "app-design-brief.template.md",
    "test-card.template.md",
    "learning-card.template.md",
)

SYNC_IGNORE_NAMES = {".DS_Store", "Thumbs.db"}


def iter_skill_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.name not in SYNC_IGNORE_NAMES
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    )

REQUIRED_KB_KEYS = (
    "visual_grounding_analogies",
    "customer_profile_triggers",
    "high_value_job_rubric",
    "value_map_categories",
    "osterwalder_7_bm_questions",
    "experiment_library",
    "data_traps",
    "validation_funnel",
    "phase_module_map",
)

REQUIRED_SCHEMA_PROPERTIES = (
    "schema_version",
    "project",
    "position",
    "ledger",
    "answers",
    "evidence",
    "assumptions",
    "decisions",
    "unknowns",
    "artifacts",
)

ATOM_FIELDS = ("id", "teaches", "asks", "accepts", "writes", "unlocks")

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
REFERENCE_LINK_RE = re.compile(r"references/([^\s\"')\]]+)")
ATOM_ID_RE = re.compile(r"\(id\s+([^)\s]+)\)")
BRACKET_TOKEN_RE = re.compile(r"\[[^\]\r\n]+\](?!\s*\()")


def read_skill_md() -> str:
    if not SKILL_MD.is_file():
        raise FileNotFoundError(f"Missing skill entrypoint: {SKILL_MD}")
    return SKILL_MD.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> str:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return ""
    return match.group(1)


def frontmatter_field(block: str, field: str) -> str:
    folded = re.search(rf"^{field}:\s*>\s*\n((?:  .+\n?)+)", block, re.MULTILINE)
    if folded:
        lines = folded.group(1).splitlines()
        return " ".join(
            line[2:] if line.startswith("  ") else line.strip() for line in lines
        ).strip()

    inline = re.search(rf"^{field}:\s*(.+)$", block, re.MULTILINE)
    if not inline:
        return ""

    value = inline.group(1).strip()
    if value == ">":
        return ""
    return value.strip("\"'")


def extract_reference_links(text: str) -> list[str]:
    return REFERENCE_LINK_RE.findall(text)


def split_atoms(text: str) -> list[str]:
    matches = list(ATOM_ID_RE.finditer(text))
    if not matches:
        return []

    atoms: list[str] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        atoms.append(text[start:end])
    return atoms


def atom_field(atom_text: str, field: str) -> str:
    match = re.search(rf'\({field}\s+"([^"]*)"\)', atom_text)
    return match.group(1) if match else ""


def record_operations(writes: str) -> list[tuple[str, str, str]]:
    return re.findall(
        r"\b(append|upsert)\s+([a-z]+)\s+record\s+\{([^}]*)\}",
        writes,
    )


def module_atom_ids() -> dict[str, list[str]]:
    return {
        MODULE_NAMES[module_name]: ATOM_ID_RE.findall(
            (REFERENCES_DIR / module_name).read_text(encoding="utf-8")
        )
        for module_name in MODULE_FILES
    }


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_script(script_name: str, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    script_path = SCRIPTS_DIR / script_name
    return subprocess.run(
        [sys.executable, str(script_path), *args],
        cwd=cwd or ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class ValueSkillMirrorTests(unittest.TestCase):
    def test_canonical_and_cursor_trees_match(self) -> None:
        mismatches: list[str] = []
        canonical_files = iter_skill_files(CANONICAL_SKILL_ROOT)
        mirror_files = iter_skill_files(SKILL_ROOT)

        for canonical in canonical_files:
            relative = canonical.relative_to(CANONICAL_SKILL_ROOT)
            mirror = SKILL_ROOT / relative
            if not mirror.is_file():
                mismatches.append(f"missing mirror {relative.as_posix()}")
                continue
            if file_digest(canonical) != file_digest(mirror):
                mismatches.append(f"digest mismatch {relative.as_posix()}")

        canonical_relatives = {
            path.relative_to(CANONICAL_SKILL_ROOT) for path in canonical_files
        }
        for mirror in mirror_files:
            relative = mirror.relative_to(SKILL_ROOT)
            if relative not in canonical_relatives:
                mismatches.append(f"extra mirror {relative.as_posix()}")

        self.assertEqual(mismatches, [], "\n".join(mismatches))


class ValueSkillAssetTests(unittest.TestCase):
    def test_knowledge_base_has_required_keys(self) -> None:
        kb = json.loads((ASSETS_DIR / "knowledge-base.json").read_text(encoding="utf-8"))
        missing = [key for key in REQUIRED_KB_KEYS if key not in kb]
        self.assertEqual(missing, [])

    def test_atoms_json_covers_every_module_atom_id(self) -> None:
        expected = module_atom_ids()
        all_expected = {atom for atoms in expected.values() for atom in atoms}
        payload = json.loads((ASSETS_DIR / "atoms.json").read_text(encoding="utf-8"))
        indexed = {atom["id"]: atom for atom in payload["atoms"]}
        missing = sorted(all_expected - set(indexed))
        self.assertEqual(missing, [])
        for module_key, atom_ids in expected.items():
            for atom_id in atom_ids:
                self.assertEqual(indexed[atom_id]["module"], module_key)

    def test_schema_defines_ledger(self) -> None:
        schema = json.loads((ASSETS_DIR / "session.schema.json").read_text(encoding="utf-8"))
        self.assertIn("ledger", schema["required"])
        ledger = schema["$defs"]["ledger"]
        for field in (
            "phase",
            "active_module",
            "completion_pct",
            "validation_milestone",
            "unvalidated_bombs",
        ):
            self.assertIn(field, ledger["required"])


class ValueSkillScriptSmokeTests(unittest.TestCase):
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

            status = run_script("status.py", str(session_path))
            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertIn("Ledger:", status.stdout)

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


def import_session_helper():
    sys.path.insert(0, str(SCRIPTS_DIR))
    import _session

    _session._atom_indexes_built = False
    return _session


class ValueSkillReviewContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill_text = read_skill_md()
        cls.frontmatter = parse_frontmatter(cls.skill_text)
        cls.contract_text = (
            REFERENCES_DIR / "session-contract.md"
        ).read_text(encoding="utf-8")
        cls.schema = json.loads(
            (ASSETS_DIR / "session.schema.json").read_text(encoding="utf-8")
        )

    def test_intent_skill_is_discoverable_repo_wide(self) -> None:
        self.assertIsNone(
            re.search(r"^paths\s*:", self.frontmatter, re.MULTILINE),
            "Intent-discovered value skill must omit paths so fresh prompts can load it",
        )

    def test_missing_session_creation_is_one_question_then_consent(self) -> None:
        required_contract = (
            '(ask-first "project slug and display name only")',
            '(wait-for "explicit consent before creating session.json")',
            '(initial-position profile P01 in_progress)',
            '(initial-arrays answers evidence assumptions decisions unknowns artifacts :empty t)',
            '(initial-timestamps created_at updated_at :rfc3339 t :same-value t)',
            '(write "complete schema-valid session.json immediately after consent")',
        )
        missing = [
            statement
            for statement in required_contract
            if statement not in self.contract_text
        ]
        self.assertEqual(
            missing,
            [],
            "Missing-session creation contract is incomplete: " + ", ".join(missing),
        )

    def test_skill_declares_script_orchestration(self) -> None:
        for needle in (
            "scripts/status.py",
            "scripts/next_question.py",
            "scripts/accept_answer.py",
            "scripts/write_design_briefs.py",
            "assets/knowledge-base.json",
            "assets/atoms.json",
        ):
            self.assertIn(needle, self.skill_text)

    def test_briefs_require_every_module_gate_outcome(self) -> None:
        self.assertIn(
            '(gate-prerequisite "profile, value-map, business-model, and experiments '
            'must each be completed or explicitly bypassed")',
            self.skill_text,
        )
        self.assertIn("app-design-brief.md", self.skill_text)

    def test_bypass_records_exact_resulting_position(self) -> None:
        decision = self.schema["$defs"]["decisionRecord"]
        resulting_fields = {
            "resulting_module",
            "resulting_atom",
            "resulting_status",
        }
        self.assertTrue(resulting_fields.issubset(decision["properties"]))
        self.assertTrue(resulting_fields.issubset(decision["required"]))
        self.assertIn(
            "(resulting-position resulting_module resulting_atom resulting_status)",
            self.contract_text,
        )
        self.assertIn(
            '(resulting_module "requested target phase")',
            self.contract_text,
        )
        self.assertIn(
            '(resulting_atom "first atom id in the target module")',
            self.contract_text,
        )
        self.assertIn("(resulting_status in_progress)", self.contract_text)
        self.assertIn(
            '(position-update "set position.module, position.atom_id, and '
            "position.status exactly to the decision's resulting_module, "
            'resulting_atom, and resulting_status")',
            self.contract_text,
        )

    def test_schema_timestamp_patterns_enforce_rfc3339(self) -> None:
        timestamp_schemas = (
            self.schema["$defs"]["project"]["properties"]["created_at"],
            self.schema["$defs"]["project"]["properties"]["updated_at"],
            self.schema["$defs"]["answerRecord"]["properties"]["accepted_at"],
        )
        for timestamp_schema in timestamp_schemas:
            pattern = timestamp_schema.get("pattern")
            self.assertTrue(pattern, "RFC 3339 timestamp fields must define a pattern")
            valid_timestamps = (
                "2026-07-18T12:34:56Z",
                "2024-02-29T23:59:59+14:00",
                "2026-01-01T00:00:00.123-05:30",
            )
            invalid_timestamps = (
                "2023-02-29T12:34:56Z",
                "2026-02-31T12:34:56Z",
                "2026-04-31T12:34:56Z",
                "2026-07-18T12:34:56",
                "2026-07-18T12:34:56+1400",
                "2026-07-18T12:34:56+24:00",
                "2026-07-18T12:34:56+12:60",
            )
            for timestamp in valid_timestamps:
                with self.subTest(timestamp=timestamp):
                    self.assertIsNotNone(re.fullmatch(pattern, timestamp))
            for timestamp in invalid_timestamps:
                with self.subTest(timestamp=timestamp):
                    self.assertIsNone(re.fullmatch(pattern, timestamp))

    def test_conflicts_and_assumptions_have_schema_valid_sources(self) -> None:
        assumption = self.schema["$defs"]["assumptionRecord"]
        self.assertIn("source_atom", assumption["properties"])
        self.assertIn("source_atom", assumption["required"])
        self.assertIn(
            '(on-conflict "append a blocking unknown with the conflicting statements; '
            'preserve both accepted answers")',
            self.contract_text,
        )
        self.assertIn(
            '(resolution "append a decision naming the governing statement, reason, '
            'source_atom, and resulting position; remove the blocking unknown")',
            self.contract_text,
        )

    def test_accepted_answer_refreshes_project_updated_at(self) -> None:
        self.assertIn(
            '(refresh "project.updated_at to the accepted_at RFC 3339 timestamp")',
            self.skill_text,
        )

    def test_project_slug_is_path_safe(self) -> None:
        slug_schema = self.schema["$defs"]["project"]["properties"]["slug"]
        self.assertEqual(slug_schema.get("pattern"), r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        pattern = slug_schema["pattern"]
        for slug in ("value", "cleaner-scheduler", "v2"):
            with self.subTest(slug=slug):
                self.assertIsNotNone(re.fullmatch(pattern, slug))
        for slug in ("../escape", "a/b", r"a\b", "/absolute", "Two Words", "-bad"):
            with self.subTest(slug=slug):
                self.assertIsNone(re.fullmatch(pattern, slug))
        self.assertIn(
            '(slug-format "lowercase ASCII letters, digits, and single hyphens only; '
            'must match ^[a-z0-9]+(?:-[a-z0-9]+)*$")',
            self.contract_text,
        )

    def test_schema_pairs_each_module_with_its_atoms(self) -> None:
        expected = module_atom_ids()
        position_pairs = {
            branch["properties"]["module"]["const"]: set(
                branch["properties"]["atom_id"]["enum"]
            )
            for branch in self.schema["$defs"]["position"]["oneOf"]
        }
        self.assertEqual(position_pairs, {key: set(value) for key, value in expected.items()})

        decision = self.schema["$defs"]["decisionRecord"]
        resulting_pairs = {
            branch["properties"]["resulting_module"]["const"]: set(
                branch["properties"]["resulting_atom"]["enum"]
            )
            for branch in decision["oneOf"]
        }
        self.assertEqual(resulting_pairs, {key: set(value) for key, value in expected.items()})

        all_atoms = {atom for atoms in expected.values() for atom in atoms}
        answer_atoms = set(
            self.schema["$defs"]["answerRecord"]["properties"]["atom_id"]["enum"]
        )
        source_atoms = set(decision["properties"]["source_atom"]["enum"])
        self.assertEqual(answer_atoms, all_atoms)
        self.assertEqual(source_atoms, all_atoms)

    def test_module_outcomes_are_derived_from_durable_records(self) -> None:
        required_contract = (
            '(position-only "position is only the current active atom; it is not module history")',
            '(completed "latest gate decision for the module is pass and its milestone artifact status is final")',
            '(bypassed "latest applicable decision uses decision bypass <module> gate and names the waived module")',
            '(pending "neither completed nor bypassed by the durable records")',
        )
        for statement in required_contract:
            self.assertIn(statement, self.contract_text)

    def test_pressure_test_checklist_names_live_scenarios(self) -> None:
        pressure_text = (ROOT / "docs" / "value-skill-pressure-tests.md").read_text(
            encoding="utf-8"
        )
        scenarios = (
            "session creation write",
            "accepted-answer persistence",
            "resume from valid state",
            "post-session bypass",
            "gate artifact write",
            "product, UX, and app brief generation",
        )
        for scenario in scenarios:
            with self.subTest(scenario=scenario):
                self.assertRegex(
                    pressure_text,
                    rf"(?:PENDING live|Live) — {re.escape(scenario)}\. Success: [^\n]+",
                )


class ValueSkillPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill_text = read_skill_md()
        cls.frontmatter = parse_frontmatter(cls.skill_text)

    def test_skill_md_is_readable(self) -> None:
        self.assertTrue(SKILL_MD.is_file(), f"Expected skill file at {SKILL_MD}")
        self.assertTrue(self.skill_text.strip(), "SKILL.md must not be empty")

    def test_frontmatter_name_is_value(self) -> None:
        name = frontmatter_field(self.frontmatter, "name")
        self.assertEqual(
            name,
            "value",
            f"Expected frontmatter name 'value', got {name!r}",
        )

    def test_frontmatter_description_triggers(self) -> None:
        description = frontmatter_field(self.frontmatter, "description")
        self.assertTrue(
            description.startswith("Use when"),
            f"Description must begin with 'Use when'; got: {description!r}",
        )

        required_phrases = (
            "value proposition",
            "grill",
            "customer profile",
            "UX brief",
        )
        missing = [phrase for phrase in required_phrases if phrase not in description]
        self.assertEqual(
            missing,
            [],
            f"Description missing required phrases {missing}: {description!r}",
        )
        self.assertIn("Not for", description)
        self.assertIn("generic product requirements", description)

    def test_skill_links_all_reference_files(self) -> None:
        linked = set(extract_reference_links(self.skill_text))
        expected = set(REFERENCE_FILES)
        missing = sorted(expected - linked)
        self.assertEqual(
            missing,
            [],
            f"SKILL.md must link all reference files directly; missing: {missing}",
        )

    def test_skill_rejects_nested_reference_links(self) -> None:
        nested = [
            f"references/{path}"
            for path in extract_reference_links(self.skill_text)
            if "/" in path
        ]
        self.assertEqual(
            nested,
            [],
            "Reference links must be one level below references/: "
            + ", ".join(nested),
        )

    def test_modules_define_required_atom_fields(self) -> None:
        for module_name in MODULE_FILES:
            module_path = REFERENCES_DIR / module_name
            self.assertTrue(
                module_path.is_file(),
                f"Missing module reference: {module_path}",
            )
            module_text = module_path.read_text(encoding="utf-8")
            atoms = split_atoms(module_text)
            self.assertTrue(
                atoms,
                f"{module_name} must define at least one atom with (id ...)",
            )

            for atom_index, atom_text in enumerate(atoms, start=1):
                missing_fields = [
                    field
                    for field in ATOM_FIELDS
                    if not re.search(rf"\({field}\s+", atom_text)
                ]
                self.assertEqual(
                    missing_fields,
                    [],
                    f"{module_name} atom {atom_index} missing fields "
                    f"{missing_fields}: {atom_text[:200]!r}",
                )

    def test_atom_ids_are_unique_across_modules(self) -> None:
        seen: dict[str, str] = {}
        duplicates: list[str] = []

        for module_name in MODULE_FILES:
            module_path = REFERENCES_DIR / module_name
            if not module_path.is_file():
                self.fail(f"Missing module reference: {module_path}")
            module_text = module_path.read_text(encoding="utf-8")
            for atom_id in ATOM_ID_RE.findall(module_text):
                if atom_id in seen:
                    duplicates.append(
                        f"{atom_id} in {seen[atom_id]} and {module_name}"
                    )
                else:
                    seen[atom_id] = module_name

        self.assertEqual(
            duplicates,
            [],
            "Atom IDs must be unique across modules: " + "; ".join(duplicates),
        )

    def test_each_atom_asks_contains_one_question_mark(self) -> None:
        for module_name in MODULE_FILES:
            module_text = (REFERENCES_DIR / module_name).read_text(encoding="utf-8")
            for atom_text in split_atoms(module_text):
                atom_id = ATOM_ID_RE.search(atom_text).group(1)
                asks = atom_field(atom_text, "asks")
                self.assertEqual(
                    asks.count("?"),
                    1,
                    f"{atom_id} must contain exactly one question mark in asks: {asks!r}",
                )

    def test_atom_record_writes_use_exact_closed_schema_fields(self) -> None:
        schema = json.loads(
            (ASSETS_DIR / "session.schema.json").read_text(encoding="utf-8")
        )
        record_defs = {
            "answers": "answerRecord",
            "evidence": "evidenceRecord",
            "assumptions": "assumptionRecord",
            "decisions": "decisionRecord",
            "unknowns": "unknownRecord",
            "artifacts": "artifactRecord",
        }

        for module_name in MODULE_FILES:
            module_text = (REFERENCES_DIR / module_name).read_text(encoding="utf-8")
            for atom_text in split_atoms(module_text):
                atom_id = ATOM_ID_RE.search(atom_text).group(1)
                writes = atom_field(atom_text, "writes")
                operations = record_operations(writes)
                declared_operations = re.findall(
                    r"\b(?:append|upsert)\s+([a-z]+)\s+record\b",
                    writes,
                )
                self.assertEqual(
                    len(operations),
                    len(declared_operations),
                    f"{atom_id} record writes must use a braced record block",
                )
                answer_writes = [
                    block
                    for operation, collection, block in operations
                    if operation == "append" and collection == "answers"
                ]
                self.assertEqual(
                    len(answer_writes),
                    1,
                    f"{atom_id} must append exactly one complete answers record",
                )

                for _, collection, block in operations:
                    definition = record_defs[collection]
                    field_tokens = set(
                        re.findall(r"(?:^|,\s*)([a-z_]+)(?=\s)", block)
                    )
                    required = schema["$defs"][definition]["required"]
                    missing = [field for field in required if field not in field_tokens]
                    self.assertEqual(
                        missing,
                        [],
                        f"{atom_id} {collection} write misses exact fields "
                        f"{missing}: {block!r}",
                    )

                for position_field in ("position.module", "position.atom_id", "position.status"):
                    self.assertIn(
                        position_field,
                        writes,
                        f"{atom_id} write must set {position_field}",
                    )
                self.assertIn(
                    "project.updated_at to accepted_at",
                    writes,
                    f"{atom_id} write must refresh project.updated_at",
                )

    def test_scale_constraint_can_remain_blocking_unknown(self) -> None:
        module_text = (REFERENCES_DIR / "business-model.md").read_text(
            encoding="utf-8"
        )
        b06 = next(
            atom for atom in split_atoms(module_text) if "(id B06)" in atom
        )
        accepts = atom_field(b06, "accepts")
        self.assertIn("blocking unknown", accepts)
        self.assertIn("keeps B06 active", accepts)
        writes = atom_field(b06, "writes")
        self.assertIn("append unknowns record", writes)
        self.assertIn("blocking true", writes)
        self.assertIn(
            "when constraint is unknown keep position.module business-model, "
            "position.atom_id B06, position.status in_progress",
            writes,
        )
        self.assertIn(
            "when constraint is accepted set position.module business-model, "
            "position.atom_id B07, position.status in_progress",
            writes,
        )
        self.assertEqual(
            atom_field(b06, "unlocks"),
            "when constraint is unknown keep B06; when constraint is accepted unlock B07",
        )

    def test_test_and_learning_cards_keep_atomic_asks(self) -> None:
        module_text = (REFERENCES_DIR / "experiments.md").read_text(
            encoding="utf-8"
        )
        atoms = {
            ATOM_ID_RE.search(atom).group(1): atom for atom in split_atoms(module_text)
        }
        self.assertEqual(
            atom_field(atoms["E07"], "asks"),
            "Do you accept the assembled test card as written?",
        )
        self.assertEqual(
            atom_field(atoms["E08"], "asks"),
            "What observable result did the test produce?",
        )
        self.assertIn("waits until a test result exists", atom_field(atoms["E08"], "teaches"))
        self.assertIn("blocking unknown", atom_field(atoms["E08"], "teaches"))
        e08_writes = atom_field(atoms["E08"], "writes")
        self.assertIn(
            "when result is absent keep position.module experiments, "
            "position.atom_id E08, position.status in_progress",
            e08_writes,
        )
        self.assertIn(
            "when result is accepted set position.module experiments, "
            "position.atom_id E09, position.status in_progress",
            e08_writes,
        )
        self.assertEqual(
            atom_field(atoms["E08"], "unlocks"),
            "when result is absent keep E08; when result is accepted unlock E09",
        )

    def test_assumption_records_wait_for_accepted_criticality(self) -> None:
        module_text = (REFERENCES_DIR / "experiments.md").read_text(
            encoding="utf-8"
        )
        atoms = {
            ATOM_ID_RE.search(atom).group(1): atom for atom in split_atoms(module_text)
        }
        e01_writes = atom_field(atoms["E01"], "writes")
        self.assertNotIn("append assumptions record", e01_writes)
        self.assertNotIn("medium default", e01_writes)
        self.assertIn("append assumptions record", atom_field(atoms["E02"], "writes"))

        e09_writes = atom_field(atoms["E09"], "writes")
        self.assertIn(
            "when criticality is accepted append assumptions record",
            e09_writes,
        )
        self.assertIn(
            "otherwise append unknowns record",
            e09_writes,
        )
        self.assertIn(
            "position.atom_id E10, position.status in_progress",
            e09_writes,
        )

    def test_boundary_answers_preserve_supported_kind(self) -> None:
        atom_locations = (
            ("profile.md", "P01"),
            ("value-map.md", "V01"),
        )
        for module_name, atom_id in atom_locations:
            module_text = (REFERENCES_DIR / module_name).read_text(encoding="utf-8")
            atom = next(
                candidate
                for candidate in split_atoms(module_text)
                if f"(id {atom_id})" in candidate
            )
            writes = atom_field(atom, "writes")
            self.assertIn(
                "kind decision for an explicit scope choice or the accepted supported kind",
                writes,
            )
            self.assertNotIn("kind fact or unknown", writes)
            self.assertIn("append decisions record", writes)
            self.assertIn("blocking true", writes)
            self.assertIn(
                f"when boundary is unresolved keep position.module {MODULE_NAMES[module_name]}, "
                f"position.atom_id {atom_id}, position.status in_progress",
                writes,
            )
            self.assertIn(
                f"when boundary is accepted set position.module {MODULE_NAMES[module_name]}, "
                f"position.atom_id {atom_id[0]}02, position.status in_progress",
                writes,
            )
            self.assertEqual(
                atom_field(atom, "unlocks"),
                f"when boundary is unresolved keep {atom_id}; "
                f"when boundary is accepted unlock {atom_id[0]}02",
            )

    def test_experiment_gate_requires_the_result_that_e08_blocks_on(self) -> None:
        module_text = (REFERENCES_DIR / "experiments.md").read_text(
            encoding="utf-8"
        )
        atoms = {
            ATOM_ID_RE.search(atom).group(1): atom for atom in split_atoms(module_text)
        }
        self.assertIn("keeps E08 active", atom_field(atoms["E08"], "accepts"))
        e10_accepts = atom_field(atoms["E10"], "accepts")
        self.assertIn("accepted observed result", e10_accepts)
        self.assertNotIn("result or explicit unknown", e10_accepts)

    def test_session_schema_parses_as_json(self) -> None:
        schema_path = ASSETS_DIR / "session.schema.json"
        self.assertTrue(
            schema_path.is_file(),
            f"Missing session schema: {schema_path}",
        )
        try:
            json.loads(schema_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            self.fail(f"session.schema.json is not valid JSON: {exc}")

    def test_session_schema_requires_canonical_fields(self) -> None:
        schema_path = ASSETS_DIR / "session.schema.json"
        self.assertTrue(
            schema_path.is_file(),
            f"Missing session schema: {schema_path}",
        )
        schema = json.loads(schema_path.read_text(encoding="utf-8"))

        required = schema.get("required", [])
        missing = [
            field for field in REQUIRED_SCHEMA_PROPERTIES if field not in required
        ]
        self.assertEqual(
            missing,
            [],
            f"session.schema.json must require {list(REQUIRED_SCHEMA_PROPERTIES)}; "
            f"missing from required: {missing}",
        )

    def test_bracket_token_scanner_ignores_markdown_links_and_images(self) -> None:
        template_text = (
            "# [Project name]\n"
            "Read the [research notes](references/research.md).\n"
            "![Evidence map](assets/evidence-map.png)\n"
        )

        self.assertEqual(BRACKET_TOKEN_RE.findall(template_text), ["[Project name]"])

    def test_templates_exist_without_unfilled_bracket_tokens(self) -> None:
        offenders: list[str] = []

        for template_name in TEMPLATE_FILES:
            template_path = ASSETS_DIR / template_name
            if not template_path.is_file():
                offenders.append(f"missing file: {template_path}")
                continue

            tokens = BRACKET_TOKEN_RE.findall(template_path.read_text(encoding="utf-8"))
            if tokens:
                offenders.append(
                    f"{template_name} contains unfilled bracket tokens: {tokens}"
                )

        self.assertEqual(
            offenders,
            [],
            "Template contract failures:\n" + "\n".join(offenders),
        )


if __name__ == "__main__":
    unittest.main()
