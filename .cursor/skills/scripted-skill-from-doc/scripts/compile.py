#!/usr/bin/env python3
"""Parse prompt-suite markdown and scaffold a paced Cursor skill draft."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

from _paths import SAMPLE_FIXTURE, TEMPLATE_RUNTIME, find_repo_root
FORBIDDEN_SLUGS = frozenset({"value", "scripted-skill-from-doc"})
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

SUBSKILL_HEADING_RE = re.compile(
    r"^##\s+\d+\.\s+Subskill\s+\d+\s+Prompt\s+\(`([^`]+)`\)\s*$",
    re.MULTILINE,
)
ORCHESTRATOR_HEADING_RE = re.compile(
    r"^##\s+\d+\.\s+Master Orchestrator Prompt\s+\(`([^`]+)`\)\s*$",
    re.MULTILINE,
)
KB_HEADING_RE = re.compile(
    r"^##\s+\d+\.\s+Central Reference Knowledge Base",
    re.MULTILINE,
)
FENCE_JSON_RE = re.compile(r"```json\s*\n(.*?)```", re.DOTALL)
FENCE_MD_RE = re.compile(r"```markdown\s*\n(.*?)```", re.DOTALL)


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    slug = re.sub(r"-+", "-", slug)
    if not slug or not SLUG_RE.fullmatch(slug):
        raise ValueError(f"Cannot derive slug from {text!r}")
    return slug


def module_id_from_name(name: str, index: int) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    base = re.sub(r"-+", "-", base) or f"module-{index}"
    return base[:48]


def atom_prefix(module_id: str, index: int) -> str:
    letters = "".join(ch for ch in module_id.upper() if ch.isalpha())[:2] or "M"
    return f"{letters}{index:02d}" if len(letters) >= 2 else f"M{index:02d}"


def parse_suite(source: Path) -> dict[str, Any]:
    text = source.read_text(encoding="utf-8")
    title = "Untitled suite"
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break

    kb: dict[str, Any] = {}
    kb_match = KB_HEADING_RE.search(text)
    if kb_match:
        after = text[kb_match.end() :]
        json_match = FENCE_JSON_RE.search(after)
        if json_match:
            kb = json.loads(json_match.group(1))

    orchestrator_name = None
    orchestrator_prompt = ""
    orch = ORCHESTRATOR_HEADING_RE.search(text)
    if orch:
        orchestrator_name = orch.group(1)
        after = text[orch.end() :]
        md = FENCE_MD_RE.search(after)
        if md:
            orchestrator_prompt = md.group(1).strip()

    modules: list[dict[str, Any]] = []
    matches = list(SUBSKILL_HEADING_RE.finditer(text))
    for i, match in enumerate(matches):
        name = match.group(1)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]
        prompt = ""
        md = FENCE_MD_RE.search(block)
        if md:
            prompt = md.group(1).strip()
        mid = module_id_from_name(name, i + 1)
        modules.append(
            {
                "id": mid,
                "title": name,
                "prompt_markdown": prompt,
                "heading": match.group(0).strip(),
            }
        )

    return {
        "title": title,
        "source": str(source).replace("\\", "/"),
        "knowledge_base": kb,
        "orchestrator": {
            "name": orchestrator_name,
            "prompt_markdown": orchestrator_prompt,
        },
        "modules": modules,
    }


def assert_safe_out(out: Path, slug: str) -> None:
    if slug in FORBIDDEN_SLUGS:
        raise SystemExit(
            f"Refusing to scaffold slug {slug!r} — golden fixture 'value' is protected."
        )
    resolved = out.resolve()
    text = str(resolved).replace("\\", "/").lower()
    # Block writing into the live value skill trees
    if text.endswith("/skills/value") or "/skills/value/" in text + "/":
        raise SystemExit(f"Refusing to write into value skill path: {resolved}")
    if "/.cursor/skills/value" in text or text.endswith("/.cursor/skills/value"):
        raise SystemExit(f"Refusing to write into value skill path: {resolved}")
    # Block scaffolding directly into live Cursor skills (must draft then promote)
    if resolved.name.lower() == "skills" and resolved.parent.name == ".cursor":
        raise SystemExit(
            "Refusing to scaffold directly into .cursor/skills — "
            "use tools/drafts/skills (or another drafts folder) then promote."
        )
    parent = resolved.parent
    if parent.name.lower() == "skills" and parent.parent.name == ".cursor":
        raise SystemExit(
            "Refusing to scaffold directly into .cursor/skills — "
            "use tools/drafts/skills (or another drafts folder) then promote."
        )


def stub_atoms(modules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Minimal chain: entry + gate per module so scripts can smoke before agent fills."""
    atoms: list[dict[str, Any]] = []
    prev_gate: str | None = None
    for mi, mod in enumerate(modules):
        mid = mod["id"]
        entry_id = f"S{mi + 1:02d}"
        gate_id = f"G{mi + 1:02d}"
        requires = [prev_gate] if prev_gate else []
        atoms.append(
            {
                "id": entry_id,
                "module": mid,
                "asks": f"What is the first concrete fact for {mod['title']}?",
                "accepts_summary": "States a concrete fact or labels unknown.",
                "unlocks": gate_id,
                "gate": False,
                "requires": requires,
                "section": "Start",
                "soft": False,
            }
        )
        next_entry = f"S{mi + 2:02d}" if mi + 1 < len(modules) else None
        atoms.append(
            {
                "id": gate_id,
                "module": mid,
                "asks": f"Review {mod['title']}. Pass the gate, reopen, or record unknowns.",
                "accepts_summary": f"Pass with 'pass {mid} gate', reopen, or blocking unknowns.",
                "unlocks": next_entry,
                "gate": True,
                "requires": [entry_id],
                "section": "Gate",
                "soft": False,
            }
        )
        prev_gate = gate_id
    return atoms


def build_skill_config(slug: str, modules: list[dict[str, Any]], atoms: list[dict[str, Any]]) -> dict[str, Any]:
    module_ids = [m["id"] for m in modules]
    entry = atoms[0]["id"] if atoms else "S01"
    express_spine: dict[str, list[str]] = {}
    express_requires: dict[str, list[str]] = {}
    for mi, mid in enumerate(module_ids):
        e = f"S{mi + 1:02d}"
        g = f"G{mi + 1:02d}"
        express_spine[mid] = [e, g]
        express_requires[g] = [e]
        if mi == 0:
            express_requires[e] = []
        else:
            express_requires[e] = [f"G{mi:02d}"]
    return {
        "skill_slug": slug,
        "workproduct_root": f"workproduct/{slug}",
        "entry_atom": entry,
        "module_order": module_ids,
        "module_phase": {
            mid: f"Phase {i + 1}: {modules[i]['title']}" for i, mid in enumerate(module_ids)
        },
        "gate_artifacts": {mid: f"{mid}.md" for mid in module_ids},
        "milestone_templates": {mid: f"{mid}.template.md" for mid in module_ids},
        "canonical_gate_pass": {mid: f"pass {mid} gate" for mid in module_ids},
        "module_brief_labels": {
            mid: modules[i]["title"].replace("-", " ") for i, mid in enumerate(module_ids)
        },
        "express_spine": express_spine,
        "express_requires": express_requires,
    }


def write_skill_md(slug: str, title: str, modules: list[dict[str, Any]], source: str) -> str:
    refs = "\n".join(f"      ({m['id']} references/{m['id']}.md)" for m in modules)
    ref_session = "      (session-contract references/session-contract.md)"
    assets = """      (session-schema assets/session.schema.json)
      (atoms-index assets/atoms.json)
      (knowledge-base assets/knowledge-base.json)
      (skill-config assets/skill-config.json)"""
    seq = " ".join(m["id"] for m in modules)
    return f"""---
name: {slug}
description: >
  Use when the user asks to work through {title}. Paced interview with durable
  session state under workproduct/{slug}/. Not for unrelated product planning.
metadata:
  activation: intent
  source: {source}
  compiled_by: prompt-suite-compile
---

(def-sop {slug}
  (context
    (target "{slug}-skill-agent")
    (optimization "paced-curriculum-interview-with-durable-session-state")
    (references
{refs}
{ref_session})
    (assets
{assets})
    (scripts
      (init scripts/init_session.py)
      (status scripts/status.py)
      (next scripts/next_question.py)
      (accept scripts/accept_answer.py)
      (milestone scripts/write_milestone.py)))

  <central_idea>
  (center-of-gravity
    (invariant "Teach with DAG-paced atoms. Canonical state lives in workproduct/{slug}/<project-slug>/session.json. Scripts run silently; one human question per turn. Stub atoms are placeholders — complete curriculum via FOR_AGENTS before shipping."))
  </central_idea>

  (protocol-0-philosophy
    (one-question "One primary question per turn")
    (end-nudge "Close with one contextual next-step design decision")
    (kb-load "read assets/knowledge-base.json when applying suite rubrics"))

  (protocol-1-activation
    (on-activation
      1 "read references/session-contract.md"
      2 "when session.json exists run scripts/status.py --brief internally"
      3 "when absent ask display name only; derive slug; consent; scripts/init_session.py --name ...")
    (session-root "workproduct/{slug}/<project-slug>/")
    (forbidden 'invent-prior-answers 'quote-script-stdout-to-user 'ask-user-for-slug))

  (protocol-2-phase-order
    (sequence {seq})
    (load-only-active-module))

  (protocol-3-turn-recipe
    (voice-recipe
      (shape "one paragraph, one primary question")
      (question "rephrase scripts/next_question.py asks; never paste atom IDs"))))
"""


def scaffold(ir: dict[str, Any], slug: str, out_dir: Path) -> Path:
    assert_safe_out(out_dir, slug)
    if out_dir.exists():
        raise SystemExit(f"Output already exists: {out_dir} (refuse to overwrite)")
    if not TEMPLATE_RUNTIME.is_dir():
        raise SystemExit(f"Missing session runtime template: {TEMPLATE_RUNTIME}")

    modules = ir["modules"]
    if not modules:
        raise SystemExit("No subskill modules found in source doc")

    out_dir.mkdir(parents=True)
    (out_dir / "assets").mkdir()
    (out_dir / "references").mkdir()
    shutil.copytree(TEMPLATE_RUNTIME, out_dir / "scripts", dirs_exist_ok=True)
    # drop junk
    keep = out_dir / "scripts" / ".gitkeep"
    if keep.is_file():
        keep.unlink()

    atoms = stub_atoms(modules)
    config = build_skill_config(slug, modules, atoms)
    kb = ir.get("knowledge_base") or {}
    if "phase_module_map" not in kb:
        kb = dict(kb)
        kb["phase_module_map"] = config["module_phase"]

    (out_dir / "assets" / "knowledge-base.json").write_text(
        json.dumps(kb, indent=2) + "\n", encoding="utf-8"
    )
    (out_dir / "assets" / "atoms.json").write_text(
        json.dumps({"atoms": atoms}, indent=2) + "\n", encoding="utf-8"
    )
    (out_dir / "assets" / "skill-config.json").write_text(
        json.dumps(config, indent=2) + "\n", encoding="utf-8"
    )

    section_map: dict[str, Any] = {"milestones": {}, "design_briefs": {}}
    for mi, mod in enumerate(modules):
        mid = mod["id"]
        section_map["milestones"][mid] = {
            "Start": [f"S{mi + 1:02d}"],
        }
        template = (
            f"# {mod['title']}\n\n"
            f"> Draft from accepted {slug} session state.\n\n"
            f"## Start\n\n"
            f"## Unknowns\n\n"
            f"## Decisions\n"
        )
        (out_dir / "assets" / f"{mid}.template.md").write_text(template, encoding="utf-8")
        ref = (
            f"(def-ref {mid}\n"
            f"  (linked-from protocol-2)\n"
            f"  (source \"{ir.get('source', '')} — {mod['title']}\")\n\n"
            f"  (section module\n"
            f"    (name {mid})\n"
            f"    (artifact {mid}.md)\n"
            f"    (template assets/{mid}.template.md))\n\n"
            f"  (section gate-pass\n"
            f"    (canonical \"pass {mid} gate\"))\n\n"
            f"  (section stub-note\n"
            f"    (note \"Prompt cargo lives in the source suite; expand atoms via FOR_AGENTS\")))\n"
        )
        (out_dir / "references" / f"{mid}.md").write_text(ref, encoding="utf-8")

    (out_dir / "assets" / "section-map.json").write_text(
        json.dumps(section_map, indent=2) + "\n", encoding="utf-8"
    )

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": f"{slug} session",
        "type": "object",
        "required": [
            "schema_version",
            "project",
            "position",
            "ledger",
            "answers",
            "evidence",
            "assumptions",
            "decisions",
            "unknowns",
            "artifacts",
        ],
        "properties": {
            "schema_version": {"type": "string"},
            "pacing_mode": {"type": "string"},
            "project": {"type": "object"},
            "position": {"type": "object"},
            "ledger": {"type": "object"},
            "answers": {"type": "array"},
            "evidence": {"type": "array"},
            "assumptions": {"type": "array"},
            "decisions": {"type": "array"},
            "unknowns": {"type": "array"},
            "artifacts": {"type": "array"},
        },
    }
    (out_dir / "assets" / "session.schema.json").write_text(
        json.dumps(schema, indent=2) + "\n", encoding="utf-8"
    )

    contract = f"""(def-ref session-contract
  (linked-from protocol-1 protocol-3)

  (section canonical-fields
    (session-root "workproduct/{slug}/<project-slug>/")
    (canonical-file "session.json")
    (schema assets/session.schema.json)
    (atoms-index assets/atoms.json)
    (skill-config assets/skill-config.json))

  (section missing-session-creation
    (ask-first "what the user is working on — display name only")
    (wait-for "explicit consent before creating session.json")
    (init-command "scripts/init_session.py --name <display-name>"))

  (section scripts-silent
    (run "status --brief, next_question, accept_answer — parse JSON internally")
    (never "quote script stdout verbatim to the user"))

  (section gate-accept
    (gate-pending "accept_answer.py --gate-pending on gate atoms autofills decisions[] with canonical pass text")
    (refuse-stay "--stay is refused on gate atoms; leave unanswered or pass with --gate-pending")
    (bulk "accept_bulk refuses gate atoms; use accept_answer --gate-pending")))
"""
    (out_dir / "references" / "session-contract.md").write_text(contract, encoding="utf-8")

    (out_dir / "SKILL.md").write_text(
        write_skill_md(slug, ir["title"], modules, ir.get("source", "")),
        encoding="utf-8",
    )
    (out_dir / "COMPILE-NOTES.md").write_text(
        "# Compile notes\n\n"
        "This draft was scaffolded by `prompt-suite-compile`.\n\n"
        "- Knowledge base JSON extracted from the source suite.\n"
        "- Stub atoms (S## / G##) are placeholders. Expand via FOR_AGENTS under poteto-mode.\n"
        "- Run `python .cursor/skills/scripted-skill-from-doc/scripts/audit_dag.py <this-skill-dir>` before promote.\n"
        "- Do not promote over `value`.\n",
        encoding="utf-8",
    )
    (out_dir / "ir.json").write_text(json.dumps(ir, indent=2) + "\n", encoding="utf-8")
    return out_dir


def cmd_parse(args: argparse.Namespace) -> int:
    ir = parse_suite(Path(args.source))
    print(json.dumps(ir, indent=2))
    return 0


def cmd_scaffold(args: argparse.Namespace) -> int:
    source = Path(args.source)
    if not source.is_file():
        print(f"Missing source: {source}", file=sys.stderr)
        return 1
    ir = parse_suite(source)
    slug = args.slug or slugify(
        Path(source).stem.replace("prompt-suite", "").replace("(1)", "").strip(" -_")
        or ir["title"].split(":")[0]
    )
    out_root = Path(args.out)
    out_dir = out_root / slug
    path = scaffold(ir, slug, out_dir)
    print(json.dumps({"ok": True, "slug": slug, "path": str(path).replace("\\", "/")}))
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    """Self-check: parse the pack sample suite and require two modules + KB."""
    sample = SAMPLE_FIXTURE
    if not sample.is_file():
        print(f"Missing pack sample: {sample}", file=sys.stderr)
        return 1
    ir = parse_suite(sample)
    kb = ir.get("knowledge_base") or {}
    report = {
        "sample": str(sample).replace("\\", "/"),
        "modules": len(ir["modules"]),
        "kb_keys": sorted(kb.keys()),
        "ok": len(ir["modules"]) >= 2 and bool(kb),
    }
    # Optional golden overlap when running inside a repo that ships skills/value
    repo = find_repo_root()
    value_doc = repo / "docs" / "value-proposition-prompt-suite (1).md"
    value_kb = repo / "skills" / "value" / "assets" / "knowledge-base.json"
    if value_doc.is_file() and value_kb.is_file():
        vir = parse_suite(value_doc)
        extracted = set((vir.get("knowledge_base") or {}).keys())
        shipped = set(json.loads(value_kb.read_text(encoding="utf-8")).keys())
        report["value_fixture"] = {
            "modules": len(vir["modules"]),
            "kb_keys_only_in_skill": sorted(shipped - extracted),
            "kb_keys_only_in_suite": sorted(extracted - shipped),
            "note": "Atom digests are not compared. Judgment layer stays manual.",
        }
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Prompt-suite compile")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("parse", help="Parse suite markdown to IR JSON")
    p.add_argument("--source", required=True)
    p.set_defaults(func=cmd_parse)

    s = sub.add_parser("scaffold", help="Scaffold draft skill under --out/<slug>")
    s.add_argument("--source", required=True)
    s.add_argument("--slug", default=None)
    s.add_argument(
        "--out",
        default="tools/drafts/skills",
        help="Parent folder for the new draft (default: tools/drafts/skills)",
    )
    s.set_defaults(func=cmd_scaffold)

    c = sub.add_parser("check", help="Self-check using assets/fixtures/sample-prompt-suite.md")
    c.set_defaults(func=cmd_check)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
