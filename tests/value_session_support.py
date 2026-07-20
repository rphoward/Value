"""Shared helpers for value session behavioral tests."""

from __future__ import annotations

import re
import unittest
from typing import Any

ATOM_ID_PATTERN = re.compile(r"\b[PVEB]\d{2}\b")


def append_accepted_answers(
    session: dict[str, Any],
    session_mod: Any,
    pairs: tuple[tuple[str, str], ...],
    *,
    kind: str = "fact",
) -> None:
    timestamp = session_mod.utc_now_iso()
    for atom_id, answer in pairs:
        session["answers"].append(
            {
                "atom_id": atom_id,
                "answer": answer,
                "kind": kind,
                "accepted_at": timestamp,
            }
        )


def assert_omits_atom_ids(
    test_case: unittest.TestCase,
    content: str,
    *atom_ids: str,
) -> None:
    for atom_id in atom_ids:
        test_case.assertNotIn(f"**{atom_id}**", content)
        test_case.assertNotIn(atom_id, content)
    test_case.assertIsNone(
        ATOM_ID_PATTERN.search(content),
        f"human artifact leaked atom ID marker: {ATOM_ID_PATTERN.search(content)}",
    )
