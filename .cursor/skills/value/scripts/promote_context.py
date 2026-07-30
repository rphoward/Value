#!/usr/bin/env python3
"""Draft or apply Term / _Avoid_ glossary from CONTEXT.product.md seed."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
FRAGMENT_PATH = SKILL_ROOT / "assets" / "AGENTS.fragment.md"
FRAGMENT_MARKER = "Product-Spine and Values notes"

SKIP_SECTIONS = frozenset(
    {
        "flagged unknowns",
    }
)

BOILERPLATE_LINES = (
    "customer-domain glossary for coding agents",
    "terms only — not a spec",
    "tighten into term / _avoid_ form",
)

EVIDENCE_BULLET_RE = re.compile(r"^-\s+\((\w+)\)\s+(.*)$", re.IGNORECASE)
TERM_BLOCK_RE = re.compile(r"^\*\*(.+?)\*\*:\s*$", re.MULTILINE)
AVOID_RE = re.compile(r"^_Avoid_:\s*(.*)$", re.IGNORECASE)


def resolve_seed(path: Path) -> Path:
    path = path.resolve()
    if path.name == "CONTEXT.product.md":
        return path
    if path.name == "session.json":
        candidate = path.parent / "CONTEXT.product.md"
        if candidate.is_file():
            return candidate
        print(f"Missing seed beside session: {candidate}", file=sys.stderr)
        raise SystemExit(1)
    print(
        "Expected session.json or CONTEXT.product.md; "
        f"got {path}",
        file=sys.stderr,
    )
    raise SystemExit(1)


def find_repo_root(start: Path | None = None) -> Path:
    candidates: list[Path] = []
    if start is not None:
        candidates.append(start.resolve())
    candidates.append(Path.cwd().resolve())
    seen: set[Path] = set()
    for base in candidates:
        current = base
        while current not in seen:
            seen.add(current)
            if (current / "workproduct").is_dir():
                return current
            if current.parent == current:
                break
            current = current.parent
    return Path.cwd().resolve()


def is_boilerplate_line(line: str) -> bool:
    lowered = line.lower().strip()
    if not lowered:
        return True
    if lowered in {"unknown", "tbd"}:
        return True
    return any(fragment in lowered for fragment in BOILERPLATE_LINES)


def provisional_term(text: str) -> str:
    named = re.match(r"^([A-Za-z][A-Za-z0-9_-]+)\s*:\s*", text)
    if named:
        return named.group(1)
    clause = re.split(r"[;.\n]", text, maxsplit=1)[0].strip()
    words = clause.split()
    if not words:
        return "Term"
    label = " ".join(words[:5])
    if len(label) > 48:
        label = " ".join(words[:3])
    return label[0].upper() + label[1:] if label else "Term"


def definition_from_bullet(text: str) -> str:
    named = re.match(r"^([A-Za-z][A-Za-z0-9_-]+)\s*:\s*(.+)$", text)
    if named:
        return named.group(2).strip()
    return text.strip()


def dedupe_terms(terms: list[dict[str, str]]) -> list[dict[str, str]]:
    """Keep the first draft for each term name (case-insensitive)."""
    seen: set[str] = set()
    unique: list[dict[str, str]] = []
    for term in terms:
        key = term["term"].strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        unique.append(term)
    return unique


def parse_seed_terms(content: str) -> list[dict[str, str]]:
    terms: list[dict[str, str]] = []
    current_section = ""
    index = 0
    lines = content.splitlines()
    while index < len(lines):
        line = lines[index].rstrip()
        if line.startswith("## "):
            current_section = line[3:].strip()
            index += 1
            continue
        if line.startswith("**") and line.endswith(":**"):
            term_name = line[2:-3].strip()
            index += 1
            definition_lines: list[str] = []
            avoid = "(tighten with human)"
            while index < len(lines):
                inner = lines[index].rstrip()
                if inner.startswith("## ") or (
                    inner.startswith("**") and inner.endswith(":**")
                ):
                    break
                avoid_match = AVOID_RE.match(inner)
                if avoid_match:
                    avoid = avoid_match.group(1).strip() or avoid
                elif inner.strip():
                    definition_lines.append(inner.strip())
                index += 1
            terms.append(
                {
                    "term": term_name,
                    "definition": "\n".join(definition_lines).strip(),
                    "avoid": avoid,
                }
            )
            continue
        bullet = EVIDENCE_BULLET_RE.match(line)
        if bullet and current_section.lower() not in SKIP_SECTIONS:
            body = bullet.group(2).strip()
            if body and not is_boilerplate_line(body):
                term_name = provisional_term(body)
                if term_name.lower() == current_section.lower() and len(body) > 48:
                    term_name = provisional_term(definition_from_bullet(body))
                terms.append(
                    {
                        "term": term_name,
                        "definition": definition_from_bullet(body),
                        "avoid": "(tighten with human)",
                    }
                )
        index += 1
    return dedupe_terms(terms)


def format_term_block(term: dict[str, str]) -> str:
    definition = term["definition"].strip()
    avoid = term["avoid"].strip() or "(tighten with human)"
    return f"**{term['term']}**:\n{definition}\n_Avoid_: {avoid}"


def format_language_section(terms: list[dict[str, str]]) -> str:
    blocks = [format_term_block(term) for term in terms if term["term"].strip()]
    return "## Language\n\n" + "\n\n".join(blocks) + ("\n" if blocks else "")


def parse_existing_terms(content: str) -> dict[str, str]:
    existing: dict[str, str] = {}
    for match in TERM_BLOCK_RE.finditer(content):
        existing[match.group(1).strip().lower()] = match.group(1).strip()
    return existing


def merge_language_into_context(context_path: Path, new_terms: list[dict[str, str]]) -> tuple[str, list[str]]:
    existing_names = set()
    if context_path.is_file():
        text = context_path.read_text(encoding="utf-8")
        existing_names = set(parse_existing_terms(text).keys())
    else:
        text = "# Project context\n\n"

    to_add = [
        term
        for term in new_terms
        if term["term"].strip().lower() not in existing_names
    ]
    if not to_add:
        return text, []

    addition_blocks = "\n\n".join(format_term_block(term) for term in to_add)
    if "## Language" in text:
        updated = re.sub(
            r"(## Language\s*\n)",
            r"\1" + addition_blocks + "\n\n",
            text,
            count=1,
        )
    else:
        separator = "\n\n" if text.endswith("\n") else "\n\n"
        updated = text.rstrip() + separator + "## Language\n\n" + addition_blocks + "\n"
    return updated, [term["term"] for term in to_add]


def append_agents_fragment(agents_path: Path) -> bool:
    fragment = FRAGMENT_PATH.read_text(encoding="utf-8").strip() + "\n"
    if agents_path.is_file():
        current = agents_path.read_text(encoding="utf-8")
        if FRAGMENT_MARKER in current:
            return False
        updated = current.rstrip() + "\n\n" + fragment
    else:
        updated = "# Agents\n\n" + fragment
    agents_path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Draft or apply Term / _Avoid_ glossary from CONTEXT.product.md."
    )
    parser.add_argument(
        "target",
        type=Path,
        help="Path to session.json or CONTEXT.product.md",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Force draft-only (no writes). Wins over --apply/--agents when combined.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Merge draft terms into repo-root CONTEXT.md (default is dry-run only)",
    )
    parser.add_argument(
        "--agents",
        action="store_true",
        help=(
            "Separate write gate: append AGENTS.fragment.md to repo-root AGENTS.md "
            "when the Product-Spine block is missing (does not require --apply)"
        ),
    )
    args = parser.parse_args()

    if not args.target.exists():
        print(f"Missing target: {args.target}", file=sys.stderr)
        return 1

    seed_path = resolve_seed(args.target)
    if not seed_path.is_file():
        print(f"Missing seed: {seed_path}", file=sys.stderr)
        return 1

    terms = parse_seed_terms(seed_path.read_text(encoding="utf-8"))
    draft = format_language_section(terms)
    print(draft.rstrip())

    write_apply = args.apply and not args.dry_run
    write_agents = args.agents and not args.dry_run
    if not write_apply and not write_agents:
        print(
            "\n(dry-run — no files written; pass --apply and/or --agents to write)",
            file=sys.stderr,
        )
        return 0

    repo_root = find_repo_root(seed_path.parent)
    if write_apply:
        context_path = repo_root / "CONTEXT.md"
        updated, added = merge_language_into_context(context_path, terms)
        if added:
            context_path.write_text(updated, encoding="utf-8")
            print(f"Wrote {len(added)} term(s) to {context_path}: {', '.join(added)}")
        else:
            print("No new terms to add to CONTEXT.md")

    if write_agents:
        agents_path = repo_root / "AGENTS.md"
        if append_agents_fragment(agents_path):
            print(f"Appended Product-Spine block to {agents_path}")
        else:
            print(f"AGENTS.md already contains Product-Spine block ({agents_path})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
