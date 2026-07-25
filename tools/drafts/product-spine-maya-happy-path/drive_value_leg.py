"""Drive Maya/ShiftSwap value leg with real answers (no gate bypass)."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
VALUE_SCRIPTS = ROOT / ".cursor" / "skills" / "value" / "scripts"
SESSION = ROOT / "workproduct" / "value-proposition" / "shiftswap" / "session.json"


def run(*args: str) -> None:
    proc = subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise SystemExit(
            f"FAIL {' '.join(args)}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )


def accept(
    atom_id: str,
    answer: str,
    kind: str,
    *,
    records: dict | None = None,
    gate_pending: bool = False,
) -> None:
    cmd = [
        str(VALUE_SCRIPTS / "accept_answer.py"),
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
    if records is not None:
        with tempfile.NamedTemporaryFile(
            "w", suffix=".json", delete=False, encoding="utf-8"
        ) as fh:
            json.dump(records, fh)
            path = fh.name
        cmd.extend(["--records", path])
    run(*cmd)


def main() -> None:
    if SESSION.exists():
        raise SystemExit(f"session already exists: {SESSION}")

    run(
        str(VALUE_SCRIPTS / "init_session.py"),
        "--name",
        "ShiftSwap",
        "--slug",
        "shiftswap",
    )

    # Profile
    accept(
        "P01",
        "Restaurant servers on hourly schedules who need to trade a shift tonight; "
        "exclude managers, corporate HQ schedulers, and full-time salaried staff.",
        "decision",
        records={
            "decisions": [
                {
                    "decision": "accepted segment boundary",
                    "reason": "Hourly servers with same-night trades are the wedge; managers and HQ are out of scope.",
                    "source_atom": "P01",
                    "resulting_module": "profile",
                    "resulting_atom": "P02",
                    "resulting_status": "in_progress",
                }
            ]
        },
    )
    accept(
        "P02",
        "Trigger: a coworker texts or posts in the group chat that they need coverage "
        "for tonight or tomorrow because of illness, childcare, or a better tip night elsewhere.",
        "fact",
        records={
            "evidence": [
                {
                    "claim": "Same-night coverage asks start in group chat or DMs",
                    "kind": "fact",
                    "source": "Maya weekend vibecode interviews with two server friends",
                    "strength": "moderate",
                }
            ]
        },
    )
    accept(
        "P03",
        "Get a trusted coworker to cover my shift so I keep my job standing and the floor stays staffed.",
        "fact",
    )
    accept(
        "P04",
        "Want managers and peers to see them as reliable teammates who handle coverage without drama — not flaky.",
        "inference",
    )
    accept(
        "P05",
        "Want to feel relieved and in control, not anxious that the shift will fall through or that they will get written up.",
        "inference",
    )
    accept(
        "P06",
        "Buying: check who is already scheduled and available. Co-creating: confirm swap details with the cover. "
        "Transferring: tell the manager or update the schedule once coverage is locked.",
        "fact",
    )
    accept(
        "P07",
        "Group-chat chaos (scroll, @everyone noise, nobody commits). Risk of double-booking or no-show. "
        "Fear of looking flaky to the manager. Time spent chasing replies while already on the floor.",
        "hypothesis",
        records={
            "assumptions": [
                {
                    "claim": "Group-chat chaos is the top extreme pain for same-night trades",
                    "criticality": "high",
                    "evidence_status": "partial",
                    "source_atom": "P07",
                }
            ]
        },
    )
    accept(
        "P08",
        "A confirmed cover in one place. Clear who is taking which hours. Manager notified without a second chase. "
        "Faster yes/no so they can stop refreshing the chat.",
        "hypothesis",
    )
    accept(
        "P09",
        "Group chat + DMs, paper schedule board, calling coworkers one by one, or skipping the trade and working tired / calling out.",
        "fact",
        records={
            "evidence": [
                {
                    "claim": "Servers rely on group chat and one-by-one calls today",
                    "kind": "fact",
                    "source": "Maya observation + friend reports",
                    "strength": "moderate",
                }
            ]
        },
    )
    accept(
        "P10",
        "Friends already built ad-hoc swap spreadsheets and keep asking for a cleaner way; one asked Maya to ship something this weekend.",
        "fact",
        records={
            "evidence": [
                {
                    "claim": "Early action: improvising spreadsheets and requesting a tool",
                    "kind": "fact",
                    "source": "Maya friend requests",
                    "strength": "moderate",
                }
            ]
        },
    )
    accept(
        "P11",
        "Priority job: get a trusted coworker to cover my shift tonight without group-chat chaos — "
        "high importance, immediate trigger, current alternatives leave them dissatisfied.",
        "decision",
        records={
            "decisions": [
                {
                    "decision": "selected priority job",
                    "reason": "Same-night coverage is urgent, painful, and already triggering workarounds.",
                    "source_atom": "P11",
                    "resulting_module": "profile",
                    "resulting_atom": "P12",
                    "resulting_status": "in_progress",
                }
            ]
        },
    )
    accept(
        "P12",
        "Pass — segment, priority job, pains, gains, alternatives, and evidence labels are good enough to design against.",
        "decision",
        gate_pending=True,
        records={
            "decisions": [
                {
                    "decision": "pass profile gate",
                    "reason": "Bounded hourly-server segment, priority same-night cover job, pains/gains/alternatives explicit with labeled evidence.",
                    "source_atom": "P12",
                    "resulting_module": "profile",
                    "resulting_atom": "P12",
                    "resulting_status": "gate_pending",
                }
            ]
        },
    )
    run(str(VALUE_SCRIPTS / "write_milestone.py"), str(SESSION), "--module", "profile")

    # Value map
    accept(
        "V01",
        "ShiftSwap: a lightweight same-restaurant shift trade request + confirm flow for servers. "
        "Exclude full payroll, multi-location franchise HQ tools, and tip-pooling features.",
        "decision",
        records={
            "decisions": [
                {
                    "decision": "accepted offering boundary",
                    "reason": "Wedge is peer trade confirm, not restaurant ops suite.",
                    "source_atom": "V01",
                    "resulting_module": "value-map",
                    "resulting_atom": "V02",
                    "resulting_status": "in_progress",
                }
            ]
        },
    )
    accept(
        "V02",
        "Included: post a shift trade request with time window; see eligible coworkers; confirm/decline; "
        "notify requester + cover; optional manager ping when locked. Not included: auto-scheduling AI, payroll.",
        "hypothesis",
    )
    accept(
        "V03",
        "Post+confirm replaces noisy group-chat threads (chaos pain). Confirm+notify reduces no-show / double-book risk. "
        "Manager ping cuts the second chase and flaky-look fear. Structured request cuts floor-time chasing replies.",
        "hypothesis",
        records={
            "assumptions": [
                {
                    "claim": "Structured confirm reduces group-chat chaos and no-show risk",
                    "criticality": "high",
                    "evidence_status": "unsupported",
                    "source_atom": "V03",
                }
            ]
        },
    )
    accept(
        "V04",
        "Confirm flow creates a single clear yes/no and named cover (desired gain). Manager ping creates notified-without-chase. "
        "Eligible-coworker list creates faster resolution so they stop refreshing chat.",
        "hypothesis",
        records={
            "assumptions": [
                {
                    "claim": "Confirm + manager ping create the named gains",
                    "criticality": "medium",
                    "evidence_status": "unsupported",
                    "source_atom": "V04",
                }
            ]
        },
    )
    accept(
        "V05",
        "Post request → priority job (get cover). Confirm/decline → chaos + commitment pains. "
        "Manager ping → social/emotional jobs and notify gain. Eligible list → faster yes/no gain. No unmatched items.",
        "inference",
    )
    accept(
        "V06",
        "No orphan candidates — every listed item maps to an accepted job, pain, or gain.",
        "decision",
        records={
            "decisions": [
                {
                    "decision": "park named orphan candidates",
                    "reason": "Empty set — V05 matched every item.",
                    "source_atom": "V06",
                    "resulting_module": "value-map",
                    "resulting_atom": "V07",
                    "resulting_status": "in_progress",
                }
            ]
        },
    )
    accept(
        "V07",
        "Unlike group chat and one-by-one calls, ShiftSwap gives a single request with explicit confirm and a manager ping "
        "when locked — so coverage is a commitment, not a scroll of maybes.",
        "hypothesis",
        records={
            "assumptions": [
                {
                    "claim": "Explicit confirm beats group-chat ambiguity for same-night trades",
                    "criticality": "high",
                    "evidence_status": "unsupported",
                    "source_atom": "V07",
                }
            ]
        },
    )
    accept(
        "V08",
        "Pass — offering boundary, products, pain/gain links, fit, empty orphans, and alternative distinction are explicit enough to take into MVP.",
        "decision",
        gate_pending=True,
        records={
            "decisions": [
                {
                    "decision": "pass value-map gate",
                    "reason": "Coherent design hypothesis for ShiftSwap same-night trade confirm vs group chat.",
                    "source_atom": "V08",
                    "resulting_module": "value-map",
                    "resulting_atom": "V08",
                    "resulting_status": "gate_pending",
                }
            ]
        },
    )
    run(str(VALUE_SCRIPTS / "write_milestone.py"), str(SESSION), "--module", "value-map")

    session = json.loads(SESSION.read_text(encoding="utf-8"))
    print("position", session["position"])
    print(
        "module_outcomes",
        {
            m: session.get("module_outcomes", {}).get(m)
            for m in ("profile", "value-map")
        },
    )
    # fallback if module_outcomes shape differs
    outcomes = {
        a.get("path"): a.get("status")
        for a in session.get("artifacts", [])
        if a.get("path") in ("customer-profile.md", "value-map.md")
    }
    print("artifacts", outcomes)


if __name__ == "__main__":
    main()
