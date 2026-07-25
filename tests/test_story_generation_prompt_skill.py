"""Package contract for .cursor/skills/story-generation-prompt/."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_ROOT = ROOT / ".cursor" / "skills" / "story-generation-prompt"
SKILL_MD = SKILL_ROOT / "SKILL.md"
REFERENCES_DIR = SKILL_ROOT / "references"
STORY_CARD = SKILL_ROOT / "assets" / "story-card.template.md"
GENERATION_PROMPT = SKILL_ROOT / "assets" / "generation-prompt.template.md"
NOTEBOOKLM_RECON = SKILL_ROOT / "assets" / "notebooklm-recon.template.md"
POSITIONING_INFERENCE = REFERENCES_DIR / "positioning-inference.md"
KNOWLEDGE_BASE = (
    ROOT / ".cursor" / "skills" / "lean-mvp" / "assets" / "knowledge-base.json"
)
LEAN_MVP_ATOMS = ROOT / ".cursor" / "skills" / "lean-mvp" / "assets" / "atoms.json"
ATOM_ID_RE = re.compile(r"\b(?:C|U|MS|UX|MT)\d{2}\b")

ALLOWED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "paths",
    "disable-model-invocation",
    "metadata",
}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
TOP_LEVEL_KEY_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):", re.MULTILINE)
PROTOCOL_HEAD_RE = re.compile(r"^\s*\((protocol-\d+)-[a-z0-9-]+", re.MULTILINE)
LINKED_FROM_RE = re.compile(r"\(linked-from\s+([^)]*)\)")
SKILL_PATH_RE = re.compile(r"(?:references|assets|scripts)/[^\s)]+")
TABLE_LETTER_RE = re.compile(r"^\|\s*([A-Z])\s*\|", re.MULTILINE)


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


class StoryGenerationPromptSkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill_text = SKILL_MD.read_text(encoding="utf-8")

    def test_frontmatter_keys_and_name_match_the_skill_folder(self) -> None:
        """Guards a skill Cursor silently refuses to load or index."""
        match = FRONTMATTER_RE.match(self.skill_text)
        self.assertIsNotNone(match, "SKILL.md must open with a frontmatter block")
        block = match.group(1)
        keys = set(TOP_LEVEL_KEY_RE.findall(block))
        self.assertEqual(
            keys - ALLOWED_FRONTMATTER_KEYS,
            set(),
            "Frontmatter carries keys outside the skill-authoring allowlist",
        )
        name = re.search(r"^name:\s*(\S+)$", block, re.MULTILINE)
        self.assertIsNotNone(name, "SKILL.md must declare a name")
        self.assertEqual(name.group(1), SKILL_ROOT.name)

    def test_declared_references_and_assets_exist_on_disk(self) -> None:
        """Guards dangling pointers: activation reads a path that is not there."""
        declared: list[str] = []
        for head in ("(references", "(assets"):
            declared.extend(
                SKILL_PATH_RE.findall(balanced_block(self.skill_text, head))
            )
        self.assertTrue(declared, "SKILL.md declares no references or assets")
        missing = [
            path for path in declared if not (SKILL_ROOT / path).is_file()
        ]
        self.assertEqual(missing, [])

    def test_every_reference_links_to_a_protocol_that_exists(self) -> None:
        """Guards drift: a renumbered body orphans the reference pointing at it."""
        protocols = set(PROTOCOL_HEAD_RE.findall(self.skill_text))
        self.assertTrue(protocols, "SKILL.md declares no protocols")
        dangling: list[str] = []
        for reference in sorted(REFERENCES_DIR.glob("*.md")):
            text = reference.read_text(encoding="utf-8")
            if not text.lstrip().startswith("(def-ref"):
                continue
            link = LINKED_FROM_RE.search(text)
            self.assertIsNotNone(
                link, f"{reference.name} is a def-ref without a linked-from line"
            )
            for named in link.group(1).split():
                if named not in protocols:
                    dangling.append(f"{reference.name} -> {named}")
        self.assertEqual(dangling, [])

    def test_story_card_invest_letters_match_lean_mvp_rubric(self) -> None:
        """Guards the MS05 handoff: a card lean-mvp's INVEST gate cannot read."""
        rubric = json.loads(KNOWLEDGE_BASE.read_text(encoding="utf-8"))[
            "invest_user_story_rubric"
        ]
        card_letters = set(TABLE_LETTER_RE.findall(STORY_CARD.read_text(encoding="utf-8")))
        self.assertEqual(card_letters, set(rubric))

    def test_story_card_keeps_invest_split_into_two_tables(self) -> None:
        """Guards the rubber stamp: one flat table invites pass marks on I, E, S."""
        card = STORY_CARD.read_text(encoding="utf-8")
        checkable, _, backlog = card.partition("### Needs backlog and team")
        self.assertTrue(backlog, "Story card must keep the needs-backlog block")
        self.assertIn("### Checkable from this sentence", checkable)
        self.assertEqual(set(TABLE_LETTER_RE.findall(checkable)), {"N", "V", "T"})
        self.assertEqual(set(TABLE_LETTER_RE.findall(backlog)), {"I", "E", "S"})
        self.assertIn("not answerable here", backlog)

    def test_generation_prompt_template_requires_fidelity_and_paste_block(self) -> None:
        """Guards the NotebookLM two-pass contract on the producer template."""
        text = GENERATION_PROMPT.read_text(encoding="utf-8")
        self.assertIn("## Source fidelity", text)
        self.assertIn("## Producer paste block", text)

    def test_notebooklm_recon_template_has_pass1_question_and_forbidden_script(self) -> None:
        """Guards pass 1 stays recon, not entertainment script generation."""
        text = NOTEBOOKLM_RECON.read_text(encoding="utf-8")
        question = text.partition("```text")[2].partition("```")[0]
        self.assertTrue(question.strip(), "recon template carries no pass-1 question block")
        self.assertIn("not in sources", question)
        self.assertIn("Do not write a script", question)
        self.assertIn("Do not infer audience", question)

    def test_tutorial_does_not_carry_its_own_copy_of_the_pass_one_question(self) -> None:
        """Guards the drift that shipped once: a stale question users copy-paste."""
        tutorial = (REFERENCES_DIR / "tutorial.md").read_text(encoding="utf-8")
        self.assertIn("assets/notebooklm-recon.template.md", tutorial)
        fenced = "\n".join(re.findall(r"```.*?\n(.*?)```", tutorial, re.DOTALL))
        for marker in ("cite the exact filename", "not in sources", "Do not infer"):
            self.assertNotIn(
                marker,
                fenced,
                "tutorial re-inlines the pass-1 question; point at the template instead",
            )

    def test_positioning_inference_labels_every_derived_row(self) -> None:
        """Guards the codebase case: unlabeled inference reads like a source fact."""
        text = POSITIONING_INFERENCE.read_text(encoding="utf-8")
        for label in ("fact", "inference", "hypothesis", "unknown"):
            self.assertIn(f"({label} ", text, f"labels section is missing {label}")
        self.assertIn("unlabeled-positioning-line", SKILL_MD.read_text(encoding="utf-8"))

    def test_operator_facing_surfaces_speak_no_atom_codes(self) -> None:
        """Guards flow state: curriculum codes belong to the agent, not the operator.

        MS05 is the one exception. It appears in the skill description as a phrase
        the operator types to invoke this skill, so it is their word, not jargon
        recited at them.
        """
        operator_facing = [
            REFERENCES_DIR / "tutorial.md",
            *sorted(SKILL_ROOT.glob("assets/*.md")),
        ]
        leaked = {}
        for path in operator_facing:
            found = set(ATOM_ID_RE.findall(path.read_text(encoding="utf-8"))) - {"MS05"}
            if found:
                leaked[path.name] = sorted(found)
        self.assertEqual(leaked, {})

    def test_every_cited_atom_id_exists_in_lean_mvp(self) -> None:
        """Guards the deferral promise: pointing an operator at an atom that is gone."""
        atoms = json.loads(LEAN_MVP_ATOMS.read_text(encoding="utf-8"))
        known = {atom["id"] for atom in atoms["atoms"]}
        cited: dict[str, set[str]] = {}
        for path in [SKILL_MD, *sorted(REFERENCES_DIR.glob("*.md")), *sorted(SKILL_ROOT.glob("assets/*.md"))]:
            found = set(ATOM_ID_RE.findall(path.read_text(encoding="utf-8")))
            if found - known:
                cited[path.name] = found - known
        self.assertEqual(cited, {})

    def test_positioning_inference_frames_exist_in_lean_mvp_knowledge_base(self) -> None:
        """Guards a frame name this skill cites that lean-mvp does not actually define."""
        rubric = json.loads(KNOWLEDGE_BASE.read_text(encoding="utf-8"))
        text = POSITIONING_INFERENCE.read_text(encoding="utf-8")
        cited = {
            name
            for name in re.findall(r"[a-z_]{6,}", text)
            if name in {
                "pmf_pyramid_hierarchy",
                "kano_model_categories",
                "earlyvangelist_ladder",
                "adoption_lifecycle",
                "visual_grounding_analogies",
            }
        }
        self.assertTrue(cited, "positioning-inference cites no lean-mvp frame by name")
        self.assertEqual(sorted(cited - set(rubric)), [])


if __name__ == "__main__":
    unittest.main()
