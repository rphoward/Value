"""Contract tests for lean-mvp atom-coaching assets and next_question wiring."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CANONICAL_SKILL = ROOT / "skills" / "lean-mvp"
SCRIPTS_DIR = CANONICAL_SKILL / "scripts"
ASSETS = CANONICAL_SKILL / "assets"
SKILL_MD = CANONICAL_SKILL / "SKILL.md"
KNOWLEDGE_BASE = ASSETS / "knowledge-base.json"
ATOM_COACHING = ASSETS / "atom-coaching.json"
ATOMS = ASSETS / "atoms.json"

SKILL_PATH_RE = re.compile(r"(?:references|assets|scripts)/[^\s)]+")


def balanced_block(text: str, head: str) -> str:
    """Return the s-expression starting at ``head``, parentheses balanced."""
    start = text.index(head)
    depth = 0
    for index in range(start, len(text)):
        if text[index] == "(":
            depth += 1
        elif text[index] == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise AssertionError(f"Unbalanced parentheses after {head!r} in SKILL.md")


def load_atoms_by_id() -> dict[str, dict[str, Any]]:
    payload = json.loads(ATOMS.read_text(encoding="utf-8"))
    return {atom["id"]: atom for atom in payload["atoms"]}


def predecessor_ids(atom_id: str, by_id: dict[str, dict[str, Any]]) -> set[str]:
    """Every atom that must be satisfied before ``atom_id``, walked through requires."""
    seen: set[str] = set()
    pending = list(by_id.get(atom_id, {}).get("requires") or [])
    while pending:
        current = pending.pop()
        if current in seen or current not in by_id:
            continue
        seen.add(current)
        pending.extend(by_id[current].get("requires") or [])
    return seen


def gate_atom_ids(by_id: dict[str, dict[str, Any]]) -> set[str]:
    return {atom_id for atom_id, atom in by_id.items() if atom.get("gate")}


def run_script(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / args[0]), *args[1:]],
        cwd=cwd or SCRIPTS_DIR,
        capture_output=True,
        text=True,
        check=False,
    )


GATE_MODULE = {
    "C12": "customer-context",
    "U12": "underserved-needs",
    "MS12": "mvp-scope",
    "UX12": "ux-prototype",
    "MT12": "metrics",
}

ATOMS_REQUIRING_KB_REFS = frozenset(
    {"C02", "C03", "C04", "C05", "U02", "U03", "MS06", "MT04"}
)

DEMO_ANSWERS: tuple[tuple[str, str, str], ...] = (
    ("C01", "Solo operators shipping a first paid product alone, excluding funded teams.", "hypothesis"),
    ("C02", "The Lone Shipper. \"I have twelve half-built things and no idea which one to finish.\"", "hypothesis"),
    ("C03", "28-45, income 40-90k, high tech comfort, low risk appetite on spend.", "inference"),
    ("C04", "Early adopter. They already buy tools on a hunch and abandon them.", "hypothesis"),
    ("C05", "Has the problem yes; knows it yes; searches yes; workaround is a notes file; budget under $50/mo.", "fact"),
    ("C06", "Watch three operators screen-share a Sunday planning session end to end.", "decision"),
    ("C12", "pass customer-context gate", "decision"),
    ("U01", "Help a solo operator decide which one thing to finish next.", "hypothesis"),
    ("U02", "Reduce the time spent re-deciding the same scope question.", "hypothesis"),
    ("U03", "Underneath it is fear of sinking another month into the wrong build.", "inference"),
    ("U04", "Importance 90%, satisfaction 20%, from the three screen-share sessions.", "inference"),
    ("U05", "Deciding what to finish next: 90% x 0.8 = 72 opportunity, highest of the two.", "inference"),
    ("U12", "pass underserved-needs gate", "decision"),
    ("MS01", "Notion templates, a plain notes file, and Trello. Pen and paper is the real incumbent.", "fact"),
    ("MS02", "Capture the candidate list, keep it durable across sessions, show it on one screen.", "decision"),
    ("MS03", "Offense on decision quality. Cede collaboration and mobile entirely.", "decision"),
    ("MS04", "No delighter in v1. Defer until the decision loop holds up.", "decision"),
)


def seed_session_through_ms05(session_path: Path) -> None:
    for atom_id, answer, kind in DEMO_ANSWERS:
        accepted = run_script(
            "accept_answer.py",
            str(session_path),
            "--atom-id",
            atom_id,
            "--answer",
            answer,
            "--kind",
            kind,
        )
        if accepted.returncode != 0:
            raise RuntimeError(accepted.stderr)
        if atom_id.endswith("12"):
            milestone = run_script(
                "write_milestone.py",
                str(session_path),
                "--module",
                GATE_MODULE[atom_id],
            )
            if milestone.returncode != 0:
                raise RuntimeError(milestone.stderr)


class LeanMvpCoachingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.atoms_by_id = load_atoms_by_id()
        cls.atom_ids = set(cls.atoms_by_id)
        cls.gate_ids = gate_atom_ids(cls.atoms_by_id)
        cls.coaching = json.loads(ATOM_COACHING.read_text(encoding="utf-8"))
        cls.knowledge_base = json.loads(KNOWLEDGE_BASE.read_text(encoding="utf-8"))
        cls.kb_keys = set(cls.knowledge_base)

    def test_every_atom_has_coaching_entry_and_no_stray_ids(self) -> None:
        """Guards shipping turns with coaching null because the sidecar forgot an atom."""
        coaching_ids = set(self.coaching)
        missing = sorted(self.atom_ids - coaching_ids)
        stray = sorted(coaching_ids - self.atom_ids)
        self.assertEqual(stray, [])
        self.assertEqual(
            missing,
            [],
            f"missing coaching for: {', '.join(missing)}",
        )

    def test_kb_refs_resolve_to_readable_text(self) -> None:
        """Guards the original stall: a payload promising a definition and carrying none."""
        bad: list[str] = []
        for atom_id, entry in self.coaching.items():
            for ref in entry.get("kb_refs") or []:
                node: Any = self.knowledge_base
                for segment in ref.split("."):
                    node = node.get(segment) if isinstance(node, dict) else None
                if not node:
                    bad.append(f"{atom_id} -> {ref}")
        self.assertEqual(bad, [])

    def test_key_atoms_ship_non_empty_kb_refs(self) -> None:
        """Guards the eight atoms that previously shipped silent definitions."""
        thin: list[str] = []
        for atom_id in sorted(ATOMS_REQUIRING_KB_REFS):
            refs = self.coaching.get(atom_id, {}).get("kb_refs") or []
            if not refs:
                thin.append(atom_id)
        self.assertEqual(thin, [])

    def test_reads_are_prior_content_atoms_not_gates(self) -> None:
        """Guards surfacing pass <module> gate as fake evidence in priors.

        is_ceremony_answer only filters text holding both "bypass" and "gate", so the
        canonical gate answer would reach the human as evidence they never supplied.
        """
        violations: list[str] = []
        for atom_id, entry in self.coaching.items():
            preds = predecessor_ids(atom_id, self.atoms_by_id)
            for read in entry.get("reads") or []:
                read_id = read.get("atom")
                if read_id not in self.atoms_by_id:
                    violations.append(f"{atom_id}: unknown read {read_id}")
                    continue
                if read_id in self.gate_ids:
                    violations.append(f"{atom_id}: gate read {read_id}")
                if read_id not in preds:
                    violations.append(
                        f"{atom_id}: read {read_id} is not a DAG predecessor"
                    )
        self.assertEqual(violations, [])

    def test_every_read_names_what_it_contributes(self) -> None:
        """Guards a prior board that recites answers instead of connecting them."""
        bare: list[str] = []
        for atom_id, entry in self.coaching.items():
            for index, read in enumerate(entry.get("reads") or []):
                if not isinstance(read, dict):
                    bare.append(f"{atom_id}.reads[{index}] is not an object")
                elif not (read.get("why") or "").strip():
                    bare.append(f"{atom_id}.reads[{index}] has no why clause")
        self.assertEqual(bare, [])

    def test_required_coaching_fields_are_non_empty(self) -> None:
        """Guards placeholder coaching that would teach nothing on a turn."""
        empty: list[str] = []
        for atom_id, entry in self.coaching.items():
            for field in (
                "why_it_matters",
                "complete_when",
                "worked_example",
                "common_miss",
            ):
                value = entry.get(field)
                if not value or (isinstance(value, list) and not any(value)):
                    empty.append(f"{atom_id}.{field}")
        self.assertEqual(empty, [])

    def test_skill_md_declared_paths_exist_on_disk(self) -> None:
        """Guards activation reading a references/ or assets/ path that is not on disk."""
        skill_text = SKILL_MD.read_text(encoding="utf-8")
        declared: list[str] = []
        for head in ("(references", "(assets", "(scripts"):
            declared.extend(SKILL_PATH_RE.findall(balanced_block(skill_text, head)))
        missing = [path for path in declared if not (CANONICAL_SKILL / path).is_file()]
        self.assertEqual(missing, [])

    def test_next_question_emits_resolved_coaching_block(self) -> None:
        """Guards wiring that leaves kb key names or missing prior text in the payload."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            created = run_script(
                "init_session.py",
                "--name",
                "Coaching Wire",
                "--slug",
                "coaching-wire",
                "--root",
                str(root),
            )
            self.assertEqual(created.returncode, 0, created.stderr)
            session_path = root / "coaching-wire" / "session.json"
            seed_session_through_ms05(session_path)

            asked = run_script("next_question.py", str(session_path))
            self.assertEqual(asked.returncode, 0, asked.stderr)
            payload = json.loads(asked.stdout)
            self.assertEqual(payload.get("atom_id"), "MS05")
            coaching = payload.get("coaching")
            self.assertIsInstance(coaching, dict)

            definitions = coaching.get("definitions") or []
            self.assertTrue(definitions, "MS05 coaching should resolve invest rubric")
            self.assertIn(
                "story-generation-prompt",
                coaching.get("story_assist") or "",
                "MS05 must surface story_assist so the turn can offer the story skill",
            )
            for block in definitions:
                text = block.get("text") or ""
                self.assertNotEqual(
                    text.strip(),
                    block.get("ref"),
                    "definition text must not be an unresolved key name",
                )
            invest = next(
                block["text"]
                for block in definitions
                if block["ref"] == "invest_user_story_rubric"
            )
            self.assertIn("Overlap-free and implementable in any order", invest)
            self.assertIn("swap the implementation", invest)

            priors = {row["atom_id"]: row for row in coaching.get("priors") or []}
            self.assertEqual(priors["MS04"]["status"], "ok")
            self.assertIn("delighter", (priors["MS04"]["answer"] or "").lower())
            self.assertEqual(priors["MS04"]["label"], "MVP scope — Kano")
            self.assertTrue(priors["MS04"]["why"])
            self.assertEqual(priors["C02"]["status"], "ok")
            self.assertIn("Lone Shipper", priors["C02"]["answer"] or "")

    def test_interview_survives_a_missing_coaching_asset(self) -> None:
        """Guards the failure this layer exists to prevent: a packaging miss stalling a session."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_copy = root / "lean-mvp"
            shutil.copytree(
                CANONICAL_SKILL,
                skill_copy,
                ignore=shutil.ignore_patterns("__pycache__"),
            )
            (skill_copy / "assets" / ATOM_COACHING.name).unlink()
            scripts = skill_copy / "scripts"

            created = subprocess.run(
                [
                    sys.executable,
                    str(scripts / "init_session.py"),
                    "--name",
                    "No Coaching",
                    "--slug",
                    "no-coaching",
                    "--root",
                    str(root / "sessions"),
                ],
                cwd=scripts,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(created.returncode, 0, created.stderr)

            asked = subprocess.run(
                [
                    sys.executable,
                    str(scripts / "next_question.py"),
                    str(root / "sessions" / "no-coaching" / "session.json"),
                ],
                cwd=scripts,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(asked.returncode, 0, asked.stderr)
            payload = json.loads(asked.stdout)
            self.assertEqual(payload["atom_id"], "C01")
            self.assertIsNone(payload["coaching"])


if __name__ == "__main__":
    unittest.main()
