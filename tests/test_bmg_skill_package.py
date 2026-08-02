"""Thin package contract for .cursor/skills/bmg/ and skills/bmg/."""

from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CURSOR_ROOT = ROOT / ".cursor" / "skills" / "bmg"
SHIP_ROOT = ROOT / "skills" / "bmg"
SKILL_MD = CURSOR_ROOT / "SKILL.md"
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


class BmgSkillPackageTests(unittest.TestCase):
    def test_ship_tree_mirrors_cursor_tree(self) -> None:
        """Guards npx consumers getting a drifted bmg package."""
        self.assertTrue(SHIP_ROOT.is_dir(), "skills/bmg/ missing")
        self.assertEqual(mirror_mismatches(CURSOR_ROOT, SHIP_ROOT), [])

    def test_bounce_names_product_spine_slash(self) -> None:
        """Guards canvas-mapper done-enough losing the spine re-entry cue."""
        text = SKILL_MD.read_text(encoding="utf-8")
        self.assertIn("/product-spine", text)
        self.assertIn("after-canvas-mapper-gate", text)
        self.assertNotIn("read .cursor/skills/product-spine/SKILL.md", text)

    def test_workproduct_root_and_done_enough_milestone(self) -> None:
        """Guards session root or first-gate milestone renaming silently."""
        text = SKILL_MD.read_text(encoding="utf-8")
        self.assertIn("workproduct/bmg/", text)
        self.assertIn("canvas-mapper.md", text)


if __name__ == "__main__":
    unittest.main()
