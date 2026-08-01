"""Voice rendering helpers: sticky labels and optional match-board hooks."""

from __future__ import annotations

import re
from typing import Any

from .constants import (
    MATCH_BOARD_ATOMS,
    _LINE_ITEM_RE,
    _NUMBERED_ITEM_RE,
)


_TAXONOMY_PREFIX_RE = re.compile(
    r"^(?:"
    r"priority\s+job(?:\s*\([^)]*\))?|"
    r"job|"
    r"extreme|severe|mild|"
    r"situation|trigger|audience|"
    r"buying|co-creating|transferring|"
    r"usual|sometimes|big temptation|"
    r"offering|gains?\s+for[^:]*|"
    r"excluded"
    r")\s*:\s*",
    flags=re.IGNORECASE,
)


def _strip_voice_prefixes(text: str) -> str:
    """Drop interview labels so paste copy stays plain language."""
    cleaned = re.sub(r"\s+", " ", text).strip()
    cleaned = re.sub(r"^[\(\[]?\d+[\)\].:]?\s*", "", cleaned)
    cleaned = re.sub(r"^[-*•]\s*", "", cleaned)
    cleaned = re.sub(
        r"^\((?:extreme|severe|expected|desired|unexpected)[^)]*\)\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )
    for _ in range(3):
        next_cleaned = _TAXONOMY_PREFIX_RE.sub("", cleaned).strip()
        if next_cleaned == cleaned:
            break
        cleaned = next_cleaned
    return cleaned


def sticky_label(text: str, max_words: int = 10) -> str:
    """Short sticky-note summary for voice rendering (aim ≤10 words)."""
    cleaned = _strip_voice_prefixes(text)
    words = cleaned.split()
    if len(words) <= max_words:
        return cleaned
    return " ".join(words[:max_words])


def pitch_clause(text: str, max_words: int = 18) -> str:
    """Paste-ready clause: strip labels, prefer first natural clause, soft trim."""
    cleaned = _strip_voice_prefixes(text)
    for splitter in (";", ". ", " — ", " - ", ": "):
        if splitter in cleaned:
            head = cleaned.split(splitter, 1)[0].strip(" ,")
            if len(head.split()) >= 4:
                cleaned = head
                break
    cleaned = re.sub(
        r"^(also named|also called)\b.*$",
        "",
        cleaned,
        flags=re.IGNORECASE,
    ).strip(" ,;—-:")
    words = cleaned.split()
    if len(words) <= max_words:
        return cleaned
    trimmed = " ".join(words[:max_words]).rstrip(" ,;—-:")
    return trimmed


def split_sticky_items(text: str) -> list[str]:
    """Split an answer into sticky items; fall back to one block."""
    raw = text.strip()
    if not raw:
        return []

    numbered = [part.strip(" ;.") for part in _NUMBERED_ITEM_RE.split(raw) if part.strip(" ;.")]
    numbered_items = [part for part in numbered if not part.isdigit()]
    if len(numbered_items) >= 2:
        if len(numbered_items[0].split()) <= 4 and not re.search(
            r"\b(pain|gain|product|service|include)\b",
            numbered_items[0],
            flags=re.IGNORECASE,
        ):
            numbered_items = numbered_items[1:] or numbered_items
        return numbered_items

    line_parts = [part.strip(" ;.") for part in _LINE_ITEM_RE.split(raw) if part.strip(" ;.")]
    if len(line_parts) >= 2:
        if len(line_parts[0].split()) <= 4:
            line_parts = line_parts[1:] or line_parts
        return line_parts

    semi = [part.strip() for part in raw.split(";") if part.strip()]
    if len(semi) >= 2:
        return semi
    return [raw]


def match_board_for_atom(session: dict[str, Any], atom_id: str) -> dict[str, Any] | None:
    """Match boards are Values-only. brand-identity leaves MATCH_BOARD_ATOMS empty."""
    del session  # API parity with Values / BMG session runtime
    if atom_id not in MATCH_BOARD_ATOMS:
        return None
    raise RuntimeError(
        "brand-identity has no match-board adapter; clear MATCH_BOARD_ATOMS "
        f"or implement one (got {atom_id!r})"
    )
