"""Regression guard: value and lean-mvp _session must not collide on sys.modules."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

from tests.skill_session_loader import load_skill_session
from tests.value_skill_support import SCRIPTS_DIR as VALUE_SCRIPTS_DIR

ROOT = Path(__file__).resolve().parent.parent
LEAN_MVP_SCRIPTS = ROOT / "skills" / "lean-mvp" / "scripts"


class SkillSessionIsolationTests(unittest.TestCase):
    def test_value_and_lean_mvp_module_order_stay_distinct(self) -> None:
        mods_before = set(sys.modules)
        lean = load_skill_session(LEAN_MVP_SCRIPTS)
        self.assertEqual(lean.MODULE_ORDER[0], "customer-context")
        self.assertEqual(len(lean.MODULE_ORDER), 5)

        value = load_skill_session(VALUE_SCRIPTS_DIR)
        self.assertEqual(value.MODULE_ORDER[0], "profile")
        self.assertEqual(len(value.MODULE_ORDER), 4)

        value_again = load_skill_session(VALUE_SCRIPTS_DIR)
        self.assertEqual(value_again.MODULE_ORDER[0], "profile")
        self.assertEqual(len(value_again.MODULE_ORDER), 4)
        self.assertIs(value_again, value)

        added = set(sys.modules) - mods_before
        self.assertFalse(any(name == "_session" or name.startswith("_session.") for name in added))


if __name__ == "__main__":
    unittest.main()
