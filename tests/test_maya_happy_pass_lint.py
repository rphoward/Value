"""Structural Maya encode: happy-PASS walk evidence must not cite bulk-accept drivers."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRAFTS = ROOT / "tools" / "drafts"

DRIVE_LEG_RE = re.compile(r"drive_\w+_leg\.py")
BULK_VEHICLE_RE = re.compile(
    r"(?i)(?<!not )(?<!never )(?:drivers?\s*:|via\s+)\s*.{0,60}(?:drive_\w+_leg\.py|bulk-accept)"
    r"|(?<!not )(?<!never )bulk-accept\s+(?:walk|driver)s?\b"
)
METHOD_FAIL_BANNER_RE = re.compile(
    r"^.{0,800}?METHOD-FAIL.{0,200}?PRODUCT-SPINE-MAYA-HAPPY-PATH-FAILED",
    re.IGNORECASE | re.DOTALL,
)
HAPPY_CLAIM_RE = re.compile(
    r"happy[- ]?path|Happy PASS|Mode:\s*full grill",
    re.IGNORECASE,
)


def walk_evidence_files() -> list[Path]:
    if not DRAFTS.is_dir():
        return []
    return sorted(DRAFTS.rglob("WALK-EVIDENCE.md"))


def cites_compressed_vehicle(text: str) -> bool:
    if DRIVE_LEG_RE.search(text):
        return True
    return bool(BULK_VEHICLE_RE.search(text))


def claims_happy_pass(path: Path, text: str) -> bool:
    folder = path.parent.name.lower()
    if "unhappy" in folder:
        return False
    if "happy" in folder:
        return True
    return bool(HAPPY_CLAIM_RE.search(text))


def has_historical_method_fail_banner(text: str) -> bool:
    """Exemption only for historical Maya FAIL evidence with banner + FAILED gate cite."""
    return bool(METHOD_FAIL_BANNER_RE.search(text))


class MayaHappyPassLintTests(unittest.TestCase):
    def test_happy_pass_walk_evidence_rejects_drive_leg_vehicle(self) -> None:
        """Guards repeating Maya: compressed drive_*_leg / bulk-accept counted as happy PASS."""
        violations: list[str] = []
        for path in walk_evidence_files():
            text = path.read_text(encoding="utf-8")
            if not cites_compressed_vehicle(text):
                continue
            if not claims_happy_pass(path, text):
                continue
            if has_historical_method_fail_banner(text):
                continue
            rel = path.relative_to(ROOT).as_posix()
            violations.append(
                f"{rel}: cites drive_*_leg.py or bulk-accept without METHOD-FAIL+FAILED gate banner"
            )
        self.assertEqual(violations, [])

    def test_lint_fails_on_deliberately_broken_happy_evidence(self) -> None:
        """Done-when proof: broken happy evidence without METHOD-FAIL must trip the rule."""
        fake = (
            "# Fake happy-path walk\n\n"
            "Mode: full grill\n\n"
            "**Drivers:** tools/drafts/fake/drive_value_leg.py\n"
        )
        self.assertTrue(cites_compressed_vehicle(fake))
        self.assertTrue(claims_happy_pass(Path("tools/drafts/fake-happy-path/WALK-EVIDENCE.md"), fake))
        self.assertFalse(has_historical_method_fail_banner(fake))

    def test_bare_method_fail_phrase_does_not_exempt(self) -> None:
        """Guards papering over happy PASS by sprinkling METHOD-FAIL without FAILED cite."""
        fake = (
            "# Fake happy-path walk\n\n"
            "METHOD-FAIL somehow\n\n"
            "**Drivers:** tools/drafts/fake/drive_value_leg.py\n"
        )
        self.assertTrue(cites_compressed_vehicle(fake))
        self.assertTrue(claims_happy_pass(Path("tools/drafts/fake-happy-path/WALK-EVIDENCE.md"), fake))
        self.assertFalse(has_historical_method_fail_banner(fake))


if __name__ == "__main__":
    unittest.main()
