"""Drive Maya/ShiftSwap lean leg through mvp-scope with real answers (no bypass)."""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LEAN_SCRIPTS = ROOT / ".cursor" / "skills" / "lean-mvp" / "scripts"
SESSION = ROOT / "workproduct" / "lean-mvp" / "shiftswap" / "session.json"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    last: subprocess.CompletedProcess[str] | None = None
    for attempt in range(8):
        tmp = SESSION.with_name(SESSION.name + ".tmp")
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass
        last = subprocess.run(
            [sys.executable, *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if last.returncode == 0:
            return last
        if "PermissionError" not in (last.stderr or "") and "WinError 5" not in (
            last.stderr or ""
        ):
            break
        time.sleep(0.4 * (attempt + 1))
    assert last is not None
    raise SystemExit(
        f"FAIL {' '.join(args)}\nstdout:\n{last.stdout}\nstderr:\n{last.stderr}"
    )


def current_answers() -> dict[str, str]:
    session = json.loads(SESSION.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for row in session.get("answers", []):
        out[row["atom_id"]] = row["answer"]
    return out


def accept(
    atom_id: str,
    answer: str,
    kind: str,
    *,
    gate_pending: bool = False,
) -> None:
    if atom_id in current_answers():
        print(f"skip {atom_id} (already answered)")
        return
    cmd = [
        str(LEAN_SCRIPTS / "accept_answer.py"),
        str(SESSION),
        "--atom-id",
        atom_id,
        "--answer",
        answer,
        "--kind",
        kind,
    ]
    if gate_pending:
        cmd.append("--gate-pending")
    run(*cmd)
    print(f"accepted {atom_id}")


def pass_gate(atom_id: str, module: str, reason: str) -> None:
    if atom_id in current_answers():
        print(f"skip gate {atom_id}")
        return
    accept(
        atom_id,
        f"Pass — {reason}",
        "decision",
        gate_pending=True,
    )
    run(str(LEAN_SCRIPTS / "write_milestone.py"), str(SESSION), "--module", module)
    print(f"milestone {module}")


def main() -> None:
    if SESSION.exists():
        raise SystemExit(f"session already exists: {SESSION}")

    run(
        str(LEAN_SCRIPTS / "init_session.py"),
        "--name",
        "ShiftSwap",
        "--slug",
        "shiftswap",
    )
    imported = run(str(LEAN_SCRIPTS / "import_value_context.py"), str(SESSION))
    print("import:", imported.stdout.strip()[:500])

    # Customer context (C01/C06 may arrive from value)
    accept(
        "C01",
        "Restaurant servers on hourly schedules needing same-night shift trades; "
        "exclude managers and HQ schedulers.",
        "decision",
    )
    accept(
        "C02",
        "Archetype: The Closing Server. Quote (stand-in from friend chat): "
        "\"I just need someone solid for tonight — the group chat is useless.\"",
        "inference",
    )
    accept(
        "C03",
        "Age ~20–35. Hourly income, tips matter. Phone-first tech comfort (chat, Instagram). "
        "Low budget for apps; will try a free tool fast. Risk: wary of looking flaky to managers.",
        "hypothesis",
    )
    accept(
        "C04",
        "Early adopter hypothesis — already building spreadsheets and asking friends for a cleaner trade tool.",
        "hypothesis",
    )
    accept(
        "C05",
        "Has problem: yes (same-night coverage). Knows it: yes (complain unprompted). "
        "Searches: yes (asks friends / tries spreadsheets). Workaround: group chat + one-by-one calls + ad-hoc sheets. "
        "Budget: unknown for paid; willing to try free weekend tool.",
        "inference",
    )
    accept(
        "C06",
        "Watch two friends attempt a same-night trade in their real group chat this weekend; "
        "note how many messages until a firm yes and whether the manager gets notified. Recruit from Maya's server circle.",
        "hypothesis",
    )
    pass_gate(
        "C12",
        "customer-context",
        "segment, Closing Server persona, earlyvangelist ladder, and observation plan are good enough",
    )

    # Underserved needs
    accept(
        "U01",
        "Get a trusted coworker to cover my shift tonight without group-chat chaos.",
        "fact",
    )
    accept(
        "U02",
        "Keep looking reliable to the manager while the swap happens.",
        "inference",
    )
    accept(
        "U03",
        "Deeper why: avoid write-ups and lost tips from working exhausted or calling out when a trade fails.",
        "inference",
    )
    accept(
        "U04",
        "Importance 90% (estimate from friend urgency). Satisfaction with current group-chat workaround 25% (estimate).",
        "hypothesis",
    )
    accept(
        "U05",
        "Lead MVP with 'get trusted cover without group-chat chaos' — opportunity ≈ 90×(1−0.25)=67.5, "
        "higher than manager-reliability which rides along once confirm+notify exist.",
        "decision",
    )
    pass_gate(
        "U12",
        "underserved-needs",
        "top benefit, opportunity scores, and MVP lead need are explicit",
    )

    # MVP scope
    accept(
        "MS01",
        "Competitors/workarounds: restaurant group chats, one-by-one phone calls, paper schedule boards, "
        "generic team apps (Slack/Teams), doing nothing / calling out.",
        "fact",
    )
    accept(
        "MS02",
        "Must-haves (table stakes): post a trade request with time window; coworker can confirm or decline; "
        "both parties see the locked cover; basic notify when status changes.",
        "hypothesis",
    )
    accept(
        "MS03",
        "Offense: explicit confirm + manager ping when locked — commitment beats chat maybes. "
        "Cede: auto-scheduling AI, payroll, multi-location franchise tools.",
        "decision",
    )
    accept(
        "MS04",
        "Defer delighters (tip-split suggestions, gamified reputation) to post-PMF; v1 is confirm reliability only.",
        "decision",
    )
    accept(
        "MS05",
        "As a restaurant server who needs to trade a shift tonight, I want to post a request and get an explicit "
        "confirm from a coworker so that coverage is locked without group-chat chaos. "
        "INVEST: I pass (one persona). N pass (specific confirm flow). V pass (avoids write-up / chaos). "
        "E pass (weekend vibecodeable). S pass (one chunk). T pass (confirm/no-confirm observable).",
        "hypothesis",
    )
    accept(
        "MS06",
        "ROI: high return / medium effort → v1 now. Manager ping in v1; tip tools and multi-restaurant in v1.1+.",
        "decision",
    )
    pass_gate(
        "MS12",
        "mvp-scope",
        "competitors, must-haves, offense, no delighter, INVEST story, and ROI cut are explicit",
    )

    session = json.loads(SESSION.read_text(encoding="utf-8"))
    print("position", session["position"])
    arts = {
        a["path"]: a["status"]
        for a in session.get("artifacts", [])
        if a["path"].endswith(".md")
    }
    print("artifacts", arts)


if __name__ == "__main__":
    main()
