"""Package contract for .cursor/skills/product-spine/ and sibling handoffs."""

from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_ROOT = ROOT / ".cursor" / "skills" / "product-spine"
SKILL_MD = SKILL_ROOT / "SKILL.md"
REFERENCES_DIR = SKILL_ROOT / "references"
PATH_REF = REFERENCES_DIR / "path.md"
BMG_ROOT = ROOT / ".cursor" / "skills" / "bmg"
BMG_SHIP_ROOT = ROOT / "skills" / "bmg"
MVP_SCOPE = ROOT / ".cursor" / "skills" / "lean-mvp" / "references" / "mvp-scope.md"
VALUE_SKILL = ROOT / ".cursor" / "skills" / "value" / "SKILL.md"
BMG_SKILL = BMG_ROOT / "SKILL.md"
LEAN_SKILL = ROOT / ".cursor" / "skills" / "lean-mvp" / "SKILL.md"
STORY_SKILL = ROOT / ".cursor" / "skills" / "story-generation-prompt" / "SKILL.md"

SIBLING_SKILL_PATHS = (
    ".cursor/skills/value/SKILL.md",
    ".cursor/skills/bmg/SKILL.md",
    ".cursor/skills/lean-mvp/SKILL.md",
    ".cursor/skills/story-generation-prompt/SKILL.md",
)

SHIP_MIRROR_ROOT = ROOT / "skills" / "product-spine"
SYNC_IGNORE_NAMES = {".DS_Store", "Thumbs.db"}

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
SKILL_PATH_RE = re.compile(r'(?:references|assets|scripts)/[^\s)"]+')


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


def iter_skill_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.name not in SYNC_IGNORE_NAMES
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    )


def mirror_mismatches(cursor_root: Path, ship_root: Path) -> list[str]:
    mismatches: list[str] = []
    for cursor_path in iter_skill_files(cursor_root):
        relative = cursor_path.relative_to(cursor_root)
        ship_path = ship_root / relative
        if not ship_path.is_file():
            mismatches.append(f"missing ship mirror {relative.as_posix()}")
            continue
        if hashlib.sha256(cursor_path.read_bytes()).hexdigest() != hashlib.sha256(
            ship_path.read_bytes()
        ).hexdigest():
            mismatches.append(f"digest mismatch {relative.as_posix()}")
    for ship_path in iter_skill_files(ship_root):
        relative = ship_path.relative_to(ship_root)
        if not (cursor_root / relative).is_file():
            mismatches.append(f"extra ship file {relative.as_posix()}")
    return mismatches


class ProductSpineSkillTests(unittest.TestCase):
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

    def test_disable_model_invocation_is_true(self) -> None:
        """Guards intent thrashing with value and lean-mvp on overlapping phrases."""
        match = FRONTMATTER_RE.match(self.skill_text)
        self.assertIsNotNone(match)
        block = match.group(1)
        flag = re.search(
            r"^disable-model-invocation:\s*(true|false)\s*$",
            block,
            re.MULTILINE,
        )
        self.assertIsNotNone(flag, "product-spine must declare disable-model-invocation")
        self.assertEqual(flag.group(1), "true")

    def test_declared_references_exist_on_disk(self) -> None:
        """Guards dangling pointers: activation reads a path that is not there."""
        declared = SKILL_PATH_RE.findall(balanced_block(self.skill_text, "(references"))
        self.assertTrue(declared, "SKILL.md declares no references")
        missing = [path for path in declared if not (SKILL_ROOT / path).is_file()]
        self.assertEqual(missing, [])

    def test_path_ref_links_to_protocols_that_exist(self) -> None:
        """Guards drift: a renumbered body orphans the reference pointing at it."""
        protocols = set(PROTOCOL_HEAD_RE.findall(self.skill_text))
        self.assertTrue(protocols, "SKILL.md declares no protocols")
        text = PATH_REF.read_text(encoding="utf-8")
        self.assertTrue(text.lstrip().startswith("(def-ref"))
        link = LINKED_FROM_RE.search(text)
        self.assertIsNotNone(link, "path.md is a def-ref without a linked-from line")
        dangling = [
            named for named in link.group(1).split() if named not in protocols
        ]
        self.assertEqual(dangling, [])

    def test_sibling_skill_paths_are_named_and_exist(self) -> None:
        """Guards a spine that routes into a skill that is not on disk."""
        missing_mentions = [
            path for path in SIBLING_SKILL_PATHS if path not in self.skill_text
        ]
        self.assertEqual(missing_mentions, [])
        missing_files = [
            path for path in SIBLING_SKILL_PATHS if not (ROOT / path).is_file()
        ]
        self.assertEqual(missing_files, [])

    def test_lean_mvp_scope_proactively_offers_story_skill(self) -> None:
        """Guards MS05 waiting for the human to invent the story-assist ask."""
        text = MVP_SCOPE.read_text(encoding="utf-8")
        self.assertIn("MS05", text)
        self.assertIn(".cursor/skills/story-generation-prompt/SKILL.md", text)
        self.assertIn("when-ms05-focus", text)
        self.assertTrue(STORY_SKILL.is_file())

    def test_business_phase_routes_to_bmg_with_business_ready_rule(self) -> None:
        """Guards a spine that names business without a live /bmg destination or readiness rule."""
        path_text = PATH_REF.read_text(encoding="utf-8")
        combined = f"{self.skill_text}\n{path_text}"
        for needle in (
            "/bmg",
            "business-ready",
            "workproduct/bmg",
            "canvas-mapper.md",
            ".cursor/skills/bmg/SKILL.md",
            "business-intent",
        ):
            self.assertIn(needle, combined, f"missing business phase wiring: {needle}")
        self.assertTrue(BMG_SKILL.is_file(), "promoted bmg skill missing")

    def test_bmg_declared_paths_and_resume_status_command(self) -> None:
        """Guards BMG asset drift and a resume command that omits session.json."""
        text = BMG_SKILL.read_text(encoding="utf-8")
        declared = SKILL_PATH_RE.findall(text)
        missing = [path for path in declared if not (BMG_ROOT / path).is_file()]
        self.assertEqual(missing, [])
        self.assertIn(
            "scripts/status.py workproduct/bmg/<project-slug>/session.json --brief",
            text,
        )

    def test_claim_phase_loads_value_notes_and_names_paths(self) -> None:
        """Guards claim dumping vibecoders into a file hunt instead of opening saved notes."""
        path_text = PATH_REF.read_text(encoding="utf-8")
        combined = f"{self.skill_text}\n{path_text}"
        for needle in (
            "protocol-3-claim-evidence-handoff",
            "customer-profile.md",
            "value-map.md",
            "north-star-blurb.md",
            "files-im-using",
            "ask-human-to-find-or-paste-profile-map-or-north-star-when-those-files-exist",
        ):
            self.assertIn(needle, combined, f"missing claim-evidence wiring: {needle}")
        self.assertIn("claim-evidence-handoff", path_text)
        self.assertIn("Files I'm using", path_text)
        self.assertIn("notebooklm-directions", self.skill_text)
        self.assertIn("Box A", path_text + self.skill_text)

    def test_reentry_you_are_here_carries_progress_so_far(self) -> None:
        """Guards amnesiac re-entry: progress so far in you-are-here, not a fifth beat or status dump."""
        path_text = PATH_REF.read_text(encoding="utf-8")
        combined = f"{self.skill_text}\n{path_text}"
        for needle in (
            "progress so far",
            "--sections",
            "you-are-here",
            "why-this-phase",
            "this-turn",
            "come-back-when",
            "quote-status-stdout",
        ):
            self.assertIn(needle, combined, f"missing re-entry progress wiring: {needle}")
        self.assertIn(
            "quoting status.py stdout, --brief, or section-strip symbols",
            self.skill_text,
        )
        self.assertIn("progress so far", path_text)
        self.assertIn("not a fifth beat", path_text)

    def test_spine_does_not_instruct_self_reload(self) -> None:
        """Guards circular handoffs that bounce the agent back into /product-spine forever."""
        self.assertNotIn("read .cursor/skills/product-spine", self.skill_text)

    def test_siblings_use_slash_not_path_read_for_spine(self) -> None:
        """Guards siblings loading spine SKILL.md every turn instead of slash re-triage."""
        path_read = "read .cursor/skills/product-spine/SKILL.md"
        for label, path in (
            ("value", VALUE_SKILL),
            ("bmg", BMG_SKILL),
            ("lean-mvp", LEAN_SKILL),
            ("story-generation-prompt", STORY_SKILL),
        ):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn(
                path_read,
                text,
                f"{label} must not path-read product-spine/SKILL.md",
            )
            if "product-spine" in text:
                self.assertIn(
                    "/product-spine",
                    text,
                    f"{label} mentions product-spine but not the slash entry",
                )

    def test_ship_tree_mirrors_cursor_tree(self) -> None:
        """Guards shipped skills pointing at /product-spine while the skill is missing from skills/."""
        self.assertTrue(SHIP_MIRROR_ROOT.is_dir(), "skills/product-spine/ missing")
        self.assertEqual(mirror_mismatches(SKILL_ROOT, SHIP_MIRROR_ROOT), [])

    def test_bmg_ship_tree_mirrors_cursor_tree(self) -> None:
        """Guards the declared BMG ship mirror from silently drifting."""
        self.assertTrue(BMG_SHIP_ROOT.is_dir(), "skills/bmg/ missing")
        self.assertEqual(mirror_mismatches(BMG_ROOT, BMG_SHIP_ROOT), [])


if __name__ == "__main__":
    unittest.main()
