"""Package contract for .cursor/skills/lean-mvp/ and skills/lean-mvp/."""

from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANONICAL_SKILL_ROOT = ROOT / "skills" / "lean-mvp"
SKILL_ROOT = ROOT / ".cursor" / "skills" / "lean-mvp"
SYNC_IGNORE_NAMES = {".DS_Store", "Thumbs.db"}


def iter_skill_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and path.name not in SYNC_IGNORE_NAMES
    )


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class LeanMvpSkillPackageTests(unittest.TestCase):
    def test_canonical_tree_mirrors_cursor_tree(self) -> None:
        canonical_files = iter_skill_files(CANONICAL_SKILL_ROOT)
        mirror_files = iter_skill_files(SKILL_ROOT)
        mismatches: list[str] = []
        for canonical in canonical_files:
            relative = canonical.relative_to(CANONICAL_SKILL_ROOT)
            mirror = SKILL_ROOT / relative
            if not mirror.is_file():
                mismatches.append(f"missing mirror {relative.as_posix()}")
                continue
            if file_digest(canonical) != file_digest(mirror):
                mismatches.append(f"digest mismatch {relative.as_posix()}")
        canonical_rels = {
            path.relative_to(CANONICAL_SKILL_ROOT) for path in canonical_files
        }
        for mirror in mirror_files:
            relative = mirror.relative_to(SKILL_ROOT)
            if relative not in canonical_rels:
                mismatches.append(f"extra mirror file {relative.as_posix()}")
        self.assertEqual(mismatches, [])


if __name__ == "__main__":
    unittest.main()
