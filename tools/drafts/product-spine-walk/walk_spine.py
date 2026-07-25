#!/usr/bin/env python3
"""Walk product-spine triage with mock sessions. Surfaces human UX bottlenecks.

Run from repo root:

    python tools/drafts/product-spine-walk/walk_spine.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
VALUE_SCRIPTS = REPO / ".cursor" / "skills" / "value" / "scripts"
LEAN_SCRIPTS = REPO / ".cursor" / "skills" / "lean-mvp" / "scripts"
STORY_SKILL = REPO / ".cursor" / "skills" / "story-generation-prompt" / "SKILL.md"
SPINE_SKILL = REPO / ".cursor" / "skills" / "product-spine" / "SKILL.md"

# Minimal answers to reach value profile + value-map gates (P12, V12).
VALUE_THROUGH_VALUE_MAP: tuple[tuple[str, str, str], ...] = (
    ("P01", "Solo vibecoders shipping side projects, excluding funded teams.", "hypothesis"),
    ("P02", "Sunday night before they paste a Discord showcase link.", "hypothesis"),
    ("P03", "Get peers to understand the project without opening the repo.", "hypothesis"),
    ("P04", "Jobs stay problem-space: explain, share, decide whether to try.", "decision"),
    ("P05", "Importance high: without a clear share, the project dies unread.", "inference"),
    ("P06", "Frequency weekly when shipping; severity is wasted evenings.", "inference"),
    ("P07", "Peers bounce after the README; poster rewrites the pitch each time.", "fact"),
    ("P08", "A short overview peers can watch before cloning.", "hypothesis"),
    ("P09", "Raw README paste, long demo video, silence.", "fact"),
    ("P10", "Evidence from three Discord threads where READMEs went unread.", "fact"),
    ("P11", "Priority job: get one peer to understand before opening the repo.", "decision"),
    ("P12", "pass profile gate", "decision"),
    ("V01", "One short overview from repo facts, not a full marketing site.", "decision"),
    ("V02", "Cuts the rewrite-the-pitch pain.", "hypothesis"),
    ("V03", "Creates a watchable overview gain.", "hypothesis"),
    ("V04", "Overview <- peer understands without clone.", "decision"),
    ("V05", "No orphan parts in v1 box.", "decision"),
    ("V06", "Fit is conditional on honest repo facts.", "inference"),
    ("V07", "Beats raw README paste on time-to-understanding.", "hypothesis"),
    ("V12", "pass value-map gate", "decision"),
)

LEAN_THROUGH_MS05: tuple[tuple[str, str, str], ...] = (
    ("C01", "Solo operators shipping a first paid product alone.", "hypothesis"),
    ("C02", "The Lone Shipper. Twelve half-built things, no finish order.", "hypothesis"),
    ("C03", "28-45, income 40-90k, high tech comfort.", "inference"),
    ("C04", "Early adopter. Buys tools on a hunch.", "hypothesis"),
    ("C05", "Has the problem; workaround is a notes file; budget under $50/mo.", "fact"),
    ("C06", "Watch three operators screen-share Sunday planning.", "decision"),
    ("C12", "pass customer-context gate", "decision"),
    ("U01", "Help a solo operator decide which one thing to finish next.", "hypothesis"),
    ("U02", "Reduce time spent re-deciding the same scope question.", "hypothesis"),
    ("U03", "Fear of sinking another month into the wrong build.", "inference"),
    ("U04", "Importance 90%, satisfaction 20%.", "inference"),
    ("U05", "Deciding what to finish next: highest opportunity.", "inference"),
    ("U12", "pass underserved-needs gate", "decision"),
    ("MS01", "Notion templates, notes file, Trello. Pen and paper wins.", "fact"),
    ("MS02", "Capture candidates, durable across sessions, one screen.", "decision"),
    ("MS03", "Offense on decision quality. Cede collaboration.", "decision"),
    ("MS04", "No delighter in v1.", "decision"),
)

LEAN_GATES = {
    "C12": "customer-context",
    "U12": "underserved-needs",
    "MS12": "mvp-scope",
}

VALUE_GATES = {
    "P12": "profile",
    "V12": "value-map",
}


@dataclass
class Bottleneck:
    severity: str
    case: str
    title: str
    human_cost: str
    evidence: str


@dataclass
class CaseResult:
    name: str
    triage: str
    human_steps: list[str] = field(default_factory=list)
    script_ok: bool = True
    notes: list[str] = field(default_factory=list)
    bottlenecks: list[Bottleneck] = field(default_factory=list)


def run(script_dir: Path, args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=cwd or script_dir,
        capture_output=True,
        text=True,
        check=False,
    )


def accept_chain(
    scripts: Path,
    session: Path,
    answers: tuple[tuple[str, str, str], ...],
    gate_modules: dict[str, str],
    stop_before: str | None = None,
) -> None:
    for atom_id, answer, kind in answers:
        if stop_before and atom_id == stop_before:
            break
        cmd = [
            str(scripts / "accept_answer.py"),
            str(session),
            "--atom-id",
            atom_id,
            "--answer",
            answer,
            "--kind",
            kind,
        ]
        if atom_id in gate_modules:
            cmd.append("--gate-pending")
        accepted = run(scripts, cmd)
        if accepted.returncode != 0:
            raise RuntimeError(f"accept {atom_id} failed: {accepted.stderr}")
        if atom_id in gate_modules:
            milestone = run(
                scripts,
                [
                    str(scripts / "write_milestone.py"),
                    str(session),
                    "--module",
                    gate_modules[atom_id],
                ],
            )
            if milestone.returncode != 0:
                raise RuntimeError(f"milestone {atom_id} failed: {milestone.stderr}")


def triage(
    work: Path,
    slug: str,
    human_ask: str,
) -> str:
    """Mirror product-spine protocol-1 rules as an executable check."""
    value_session = work / "value-proposition" / slug / "session.json"
    lean_session = work / "lean-mvp" / slug / "session.json"
    value_exists = value_session.is_file()
    lean_exists = lean_session.is_file()

    def gate_done(session_path: Path, gate_ids: tuple[str, ...]) -> bool:
        data = json.loads(session_path.read_text(encoding="utf-8"))
        answered = {a["atom_id"] for a in data.get("answers", [])}
        decisions = data.get("decisions") or []
        for gate in gate_ids:
            if gate in answered:
                continue
            if any(gate in str(d) for d in decisions):
                continue
            # also check decisions with resulting module completed markers
            return False
        return True

    if value_exists and lean_exists:
        value_profile_vm = gate_done(value_session, ("P12", "V12"))
        lean_incomplete = not gate_done(lean_session, ("C12", "U12", "MS12"))
        value_incomplete = not gate_done(value_session, ("P12", "V12", "B12", "E12"))
        if value_incomplete and lean_incomplete:
            return "value" if not value_profile_vm else "lean-mvp"
        if value_incomplete:
            return "value"
        if lean_incomplete:
            return "lean-mvp"
        return "value"  # both complete: prefer value for experiments / learn
    if value_exists:
        return "value"
    if lean_exists:
        return "lean-mvp"
    ask = human_ask.lower()
    if any(w in ask for w in ("repo", "readme", "overview", "discord", "claim", "notebooklm")):
        return "story-generation-prompt"
    if any(w in ask for w in ("mvp", "feature set", "kano", "scope")):
        return "lean-mvp"
    return "value"


def case_bare_idea(work: Path) -> CaseResult:
    slug = "spine-bare-idea"
    ask = "I have a vibecoded idea for a planning tool and want it to be valuable"
    choice = triage(work, slug, ask)
    result = CaseResult(
        name="bare-idea",
        triage=choice,
        human_steps=[
            "Invoke /product-spine",
            "Read triage paragraph naming value",
            "Invoke /value (or ask agent to open value skill)",
            "Answer missing-session name question",
            "Consent to init_session",
            "Begin P01 grilling",
        ],
    )
    if choice != "value":
        result.script_ok = False
        result.notes.append(f"expected value, got {choice}")
    result.bottlenecks.append(
        Bottleneck(
            "high",
            result.name,
            "Slash handoff is not automatic",
            "Human must invoke /product-spine then separately open /value. Two slash commands before the first product question.",
            "spine protocol-0 stops after naming destination; value has its own activation",
        )
    )
    result.bottlenecks.append(
        Bottleneck(
            "medium",
            result.name,
            "Missing-session consent tax",
            "After triage to value, human still answers display name + consent before P01.",
            "value protocol-1 missing-session creation",
        )
    )
    return result


def case_repo_claim(work: Path) -> CaseResult:
    slug = "spine-repo-claim"
    ask = "I finished a side project repo and need an honest Discord overview claim"
    choice = triage(work, slug, ask)
    result = CaseResult(
        name="repo-claim",
        triage=choice,
        human_steps=[
            "Invoke /product-spine",
            "Agent reads story-generation-prompt/SKILL.md",
            "Human runs NotebookLM pass 1 (outside Cursor) or pastes ledger",
            "Story card emitted in chat",
            "Human decides whether to open lean-mvp / value next",
        ],
    )
    if choice != "story-generation-prompt":
        result.script_ok = False
        result.notes.append(f"expected story-generation-prompt, got {choice}")
    if not STORY_SKILL.is_file():
        result.script_ok = False
        result.notes.append("story SKILL.md missing")
    result.bottlenecks.append(
        Bottleneck(
            "high",
            result.name,
            "NotebookLM is outside the Cursor loop",
            "Spine routes to story, but pass-1 recon requires leaving Cursor, uploading sources, pasting a ledger back. Long idle gap with no session.json.",
            "story protocol-6 + tutorial NotebookLM path",
        )
    )
    result.bottlenecks.append(
        Bottleneck(
            "medium",
            result.name,
            "No workproduct trail for story-only path",
            "A repo-claim walk leaves no slug session. Later /product-spine cannot resume; human re-explains context.",
            "spine has no session; story forbidden from writing session.json",
        )
    )
    return result


def case_value_only(work: Path) -> CaseResult:
    slug = "spine-value-only"
    init = run(
        VALUE_SCRIPTS,
        [
            str(VALUE_SCRIPTS / "init_session.py"),
            "--name",
            "Spine Value Only",
            "--slug",
            slug,
            "--root",
            str(work / "value-proposition"),
        ],
    )
    result = CaseResult(name="value-only-resume", triage="", human_steps=[])
    if init.returncode != 0:
        result.script_ok = False
        result.notes.append(init.stderr)
        return result
    session = work / "value-proposition" / slug / "session.json"
    status = run(VALUE_SCRIPTS, [str(VALUE_SCRIPTS / "status.py"), str(session)])
    nextq = run(VALUE_SCRIPTS, [str(VALUE_SCRIPTS / "next_question.py"), str(session)])
    choice = triage(work, slug, "where was I")
    result.triage = choice
    result.human_steps = [
        "Invoke /product-spine",
        f"Triage names value (session at {session.relative_to(work)})",
        "Open /value; activation runs status + import_lean",
        "Hear voice-recipe for first ready atom",
    ]
    result.notes.append(f"status: {status.stdout.strip()}")
    if nextq.returncode == 0:
        payload = json.loads(nextq.stdout)
        result.notes.append(f"next atom: {payload.get('atom_id')}")
    else:
        result.script_ok = False
        result.notes.append(nextq.stderr)
    if choice != "value":
        result.script_ok = False
    result.bottlenecks.append(
        Bottleneck(
            "medium",
            result.name,
            "Slug discovery is silent and easy to miss",
            "Spine rules assume a shared slug, but the human is never shown which slug was derived. Resuming requires remembering the display name or hunting workproduct/.",
            f"session path {session}",
        )
    )
    return result


def case_dual_sessions(work: Path) -> CaseResult:
    slug = "spine-dual"
    result = CaseResult(name="dual-session-precedence", triage="", human_steps=[])
    value_dir = work / "value-proposition" / slug
    lean_dir = work / "lean-mvp" / slug
    value_dir.mkdir(parents=True)
    lean_dir.mkdir(parents=True)

    # Hand-crafted sessions: value past profile+value-map; lean still early.
    # Avoids value gate --records ceremony that humans also stumble on.
    now = "2026-07-25T12:00:00Z"
    value_session = {
        "schema_version": "1.1",
        "project": {"slug": slug, "name": "Spine Dual", "created_at": now, "updated_at": now},
        "position": {"module": "business-model", "atom_id": "B01", "status": "in_progress"},
        "ledger": {
            "phase": "Evolve",
            "active_module": "business-model",
            "completion_pct": 40,
            "validation_milestone": "value-map",
            "unvalidated_bombs": [],
        },
        "answers": [
            {"atom_id": "P01", "answer": "Solo vibecoders", "kind": "hypothesis", "accepted_at": now},
            {"atom_id": "P12", "answer": "pass profile gate", "kind": "decision", "accepted_at": now},
            {"atom_id": "V01", "answer": "Short overview", "kind": "decision", "accepted_at": now},
            {"atom_id": "V12", "answer": "pass value-map gate", "kind": "decision", "accepted_at": now},
        ],
        "evidence": [],
        "assumptions": [],
        "decisions": [
            {
                "decision": "pass profile gate",
                "reason": "fixture",
                "source_atom": "P12",
                "resulting_module": "value-map",
                "resulting_atom": "V01",
                "resulting_status": "in_progress",
            },
            {
                "decision": "pass value-map gate",
                "reason": "fixture",
                "source_atom": "V12",
                "resulting_module": "business-model",
                "resulting_atom": "B01",
                "resulting_status": "in_progress",
            },
        ],
        "unknowns": [],
        "artifacts": [],
    }
    (value_dir / "session.json").write_text(json.dumps(value_session, indent=2), encoding="utf-8")

    l_init = run(
        LEAN_SCRIPTS,
        [
            str(LEAN_SCRIPTS / "init_session.py"),
            "--name",
            "Spine Dual",
            "--slug",
            slug,
            "--root",
            str(work / "lean-mvp"),
        ],
    )
    if l_init.returncode:
        result.script_ok = False
        result.notes.append(l_init.stderr)
        return result

    lean_session = lean_dir / "session.json"
    imported = run(
        LEAN_SCRIPTS,
        [str(LEAN_SCRIPTS / "import_value_context.py"), str(lean_session)],
    )
    result.notes.append(f"import_value: rc={imported.returncode} out={imported.stdout.strip()[:240]}")

    choice = triage(work, slug, "resume my product path")
    result.triage = choice
    result.human_steps = [
        "Invoke /product-spine",
        "Triage: value profile+value-map done, lean incomplete → lean-mvp",
        "Open /lean-mvp; import mapped atoms",
        "Continue grilling non-imported lean atoms",
    ]
    if choice != "lean-mvp":
        result.script_ok = False
        result.notes.append(f"expected lean-mvp after value-map done, got {choice}")

    slug2 = "spine-dual-both"
    for kind, scripts, root_name in (
        ("value", VALUE_SCRIPTS, "value-proposition"),
        ("lean", LEAN_SCRIPTS, "lean-mvp"),
    ):
        init = run(
            scripts,
            [
                str(scripts / "init_session.py"),
                "--name",
                "Both Incomplete",
                "--slug",
                slug2,
                "--root",
                str(work / root_name),
            ],
        )
        if init.returncode:
            result.script_ok = False
            result.notes.append(f"{kind} init: {init.stderr}")
    both = triage(work, slug2, "resume")
    result.notes.append(f"both-incomplete triage → {both}")
    if both != "value":
        result.script_ok = False
        result.bottlenecks.append(
            Bottleneck(
                "high",
                result.name,
                "Both-incomplete preference broken",
                "Plan says prefer value until profile/value-map done.",
                f"got {both}",
            )
        )

    result.bottlenecks.append(
        Bottleneck(
            "high",
            result.name,
            "Human cannot see dual-session state",
            "Spine triage depends on two session.json files and gate atoms. No status strip in product-spine. Human cannot verify why they were sent to lean vs value.",
            "product-spine forbids running status scripts",
        )
    )
    result.bottlenecks.append(
        Bottleneck(
            "medium",
            result.name,
            "Value gate pass needs a records sidecar",
            "Walk harness could not drive value P12→milestone with answer text alone. Humans hit the same ceremony (decision JSON) when agents forget --records.",
            "write_milestone: Module profile has no canonical pass decision",
        )
    )
    return result


def case_ms05_story_paste(work: Path) -> CaseResult:
    slug = "spine-ms05"
    result = CaseResult(name="ms05-story-paste", triage="lean-mvp", human_steps=[])
    init = run(
        LEAN_SCRIPTS,
        [
            str(LEAN_SCRIPTS / "init_session.py"),
            "--name",
            "Spine MS05",
            "--slug",
            slug,
            "--root",
            str(work / "lean-mvp"),
        ],
    )
    if init.returncode:
        result.script_ok = False
        result.notes.append(init.stderr)
        return result
    session = work / "lean-mvp" / slug / "session.json"
    try:
        accept_chain(
            LEAN_SCRIPTS,
            session,
            LEAN_THROUGH_MS05,
            LEAN_GATES,
            stop_before=None,
        )
    except RuntimeError as exc:
        result.script_ok = False
        result.notes.append(str(exc))
        return result

    nextq = run(LEAN_SCRIPTS, [str(LEAN_SCRIPTS / "next_question.py"), str(session)])
    if nextq.returncode:
        result.script_ok = False
        result.notes.append(nextq.stderr)
        return result
    payload = json.loads(nextq.stdout)
    result.notes.append(f"focus atom: {payload.get('atom_id')}")
    coaching = payload.get("coaching") or {}
    result.notes.append(f"coaching keys: {sorted(coaching)}")
    if payload.get("atom_id") != "MS05":
        result.script_ok = False
        result.notes.append("expected MS05 focus")
    if "story_assist" not in coaching:
        result.bottlenecks.append(
            Bottleneck(
                "high",
                result.name,
                "story_assist never reaches the turn payload",
                "atom-coaching.json has story_assist, but next_question coaching block may not forward unknown fields. Agent must rely on SKILL turn-recipe prose alone.",
                f"coaching keys={sorted(coaching)}",
            )
        )
    else:
        result.notes.append(f"story_assist present: {coaching.get('story_assist')[:80]}")

    result.human_steps = [
        "Lean-mvp asks MS05 (and should offer story skill)",
        "Human invokes /story-generation-prompt or agent path-reads SKILL.md",
        "Draft story card in chat",
        "Human copies one sentence",
        "Human pastes back into lean chat",
        "Agent runs accept_answer for MS05",
        "Continue MS06",
    ]
    result.bottlenecks.append(
        Bottleneck(
            "high",
            result.name,
            "Manual paste across skill boundary",
            "Seven human actions from MS05 focus to accepted atom. Easy to lose the sentence, invent a weaker one, or skip INVEST letters.",
            "mvp-scope forbidden auto-accept; tutorial requires paste",
        )
    )
    result.bottlenecks.append(
        Bottleneck(
            "medium",
            result.name,
            "Context switch kills coaching continuity",
            "Coaching why/complete_when for MS05 is in lean turn; story skill has its own voice. Human hears two teachers for one sentence.",
            "lean coaching-delivery vs story protocol-1",
        )
    )
    return result


def case_mvp_ask_no_session(work: Path) -> CaseResult:
    ask = "I know my customer well enough; help me scope an MVP feature set"
    choice = triage(work, "unused", ask)
    result = CaseResult(
        name="mvp-ask-no-session",
        triage=choice,
        human_steps=[
            "Invoke /product-spine",
            "Triage names lean-mvp",
            "Open /lean-mvp; missing-session name+consent",
            "Start C01 with no value import (empty value tree)",
        ],
    )
    if choice != "lean-mvp":
        result.script_ok = False
    result.bottlenecks.append(
        Bottleneck(
            "high",
            result.name,
            "Spine trusts 'customer clarity enough' on self-report",
            "Human can skip value entirely. Lean C01 still grills segment from scratch. Feels like the spine lied about a shortcut.",
            "no-session-mvp rule has no evidence check",
        )
    )
    return result


def main() -> int:
    if not SPINE_SKILL.is_file():
        print("product-spine skill missing", file=sys.stderr)
        return 2

    bottlenecks: list[Bottleneck] = []
    results: list[CaseResult] = []

    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "workproduct"
        work.mkdir()
        for builder in (
            case_bare_idea,
            case_repo_claim,
            case_value_only,
            case_dual_sessions,
            case_ms05_story_paste,
            case_mvp_ask_no_session,
        ):
            print(f"\n=== {builder.__name__} ===")
            result = builder(work)
            results.append(result)
            bottlenecks.extend(result.bottlenecks)
            print(f"triage → {result.triage}  ok={result.script_ok}")
            for step in result.human_steps:
                print(f"  human: {step}")
            for note in result.notes:
                print(f"  note: {note}")

    print("\n======== UX BOTTLENECK REPORT ========")
    order = {"high": 0, "medium": 1, "low": 2}
    for item in sorted(bottlenecks, key=lambda b: order.get(b.severity, 9)):
        print(f"\n[{item.severity}] {item.case}: {item.title}")
        print(f"  cost: {item.human_cost}")
        print(f"  evidence: {item.evidence}")

    failed = [r for r in results if not r.script_ok]
    print(f"\nCases: {len(results)}  script failures: {len(failed)}")
    print(f"Bottlenecks: {len(bottlenecks)}")
    out = REPO / "tools" / "drafts" / "product-spine-walk" / "last-walk.json"
    out.write_text(
        json.dumps(
            {
                "results": [
                    {
                        "name": r.name,
                        "triage": r.triage,
                        "ok": r.script_ok,
                        "steps": r.human_steps,
                        "notes": r.notes,
                    }
                    for r in results
                ],
                "bottlenecks": [b.__dict__ for b in bottlenecks],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {out.relative_to(REPO)}")
    return 1 if failed else 0


if __name__ == "__main__":
    # fix shebang typo if any — actual entry:
    raise SystemExit(main())
