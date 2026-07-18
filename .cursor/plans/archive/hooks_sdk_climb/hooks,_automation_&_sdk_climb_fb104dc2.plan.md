---
name: Hooks, Automation & SDK Climb
overview: Offload the hillclimb loop orchestration into a deterministic Python SDK driver (Inversion of Control), secure the API key via .env, and wire Cursor Automations to drive the milestones.
todos:
  - id: sdk-safety
    content: Setup .env.example, update .gitignore, install cursor-sdk & python-dotenv
    status: completed
  - id: sdk-probe
    content: Update tools/drafts/sdk-climb-spike.py to use dotenv and execute the live probe
    status: completed
  - id: sdk-orchestrator
    content: Implement tools/sdk-climb.py orchestrator with deterministic exit codes
    status: completed
  - id: automation-hooks
    content: Wire Cursor Automation for milestones and extend run_tests_on_stop.py for reporting
    status: completed
  - id: documentation
    content: Update handoff/SDK-CLIMB-SPIKE.md to PASS and mark milestone complete in STATE.md
    status: completed
isProject: false
---

# Hooks, Automations & SDK Climb

## Goal
Execute the architectural pivot defined in `ARCHITECTURE-SECOND-OPINION-2026-07.md`. Offload the repetitive `while/for` hillclimb loop from the LLM's working memory into a deterministic Python script using the Cursor SDK. Define milestones using Cursor Automations, and safely manage the required API keys.

## Shipped on branch (2026-07-15)

- `tools/sdk_bridge.py`, `tools/sdk_climb_lib.py`, `tools/sdk-climb.py` (discrimination + draft/record/eval + preference continue/record)
- `tests/test_sdk_climb_preflight.py`, `tests/test_sdk_climb_smoke.py` (fixture resume, no live API)
- `handoff/HOOKS-AUTOMATION.md` (IDE automation recipe + stop-hook verification)

## Platform requirement (non-negotiable)
Spike, `tools/sdk-climb.py`, and any bridge helpers **must work on Windows, WSL, Linux bash, and macOS**. Do not ship a Unix-only local-bridge path.

**Known hazard (2026-07-14):** stock `cursor_sdk` local bridge uses `selectors`/`select` on the bridge stderr pipe. On Windows that raises `WinError 10038` (WinSock only accepts sockets, not pipes). Probe workaround: poll stderr in `tools/drafts/sdk-climb-spike.py`. Carry an equivalent Windows-safe discovery wait into the shipped orchestrator (or upstream fix), and verify on at least one Unix shell (WSL or Linux/mac) before calling the spike PASS.

## Phase 1: SDK Safety & Preflight
1. **Secrets Management:**
   - Create a `.env.example` stub containing `CURSOR_API_KEY=`.
   - Verify `.gitignore` explicitly ignores `.env` (preventing accidental secret leakage per safety rules).
   - Add `cursor-sdk` and `python-dotenv` to the project's dependencies (e.g., `pyproject.toml` or `requirements.txt`).
2. **Live Probe (`SDK-CLIMB-SPIKE`):**
   - Update `tools/drafts/sdk-climb-spike.py` to use `dotenv.load_dotenv()` so it seamlessly picks up the key.
   - *Human Gate:* You will populate the `.env` file locally.
   - Run the live probe against a fixture run (`python tools/drafts/sdk-climb-spike.py --live --run-dir <fixture>`).
   - Goal: Prove that the SDK can successfully load project agents (like `discriminate` or `emulate-drafter`) and write one real JSON verdict sidecar.

## Phase 2: The SDK Orchestrator (`tools/sdk-climb.py`)
Once the spike passes, build the actual driver:
1. **Implementation:**
   - Create `tools/sdk-climb.py`. This script acts as the "traffic cop" replacing the chat LLM.
   - It will poll `hillclimb_once.py status`.
   - When work is needed, it uses `Agent.create(...)` from the Cursor SDK to dispatch isolated, fresh-context workers:
     - `emulate-drafter` (to write drafts)
     - `eval-audit` (to write qualitative scores)
     - `discriminate` (to write verdicts)
2. **Deterministic Exit Codes (Phase-5 plan):**
   - Exit `0`: Run finished (plateau, max iterations, or preference tie reached).
   - Exit `1`: Fatal error.
   - Exit `2`: Yield to human (needs manual decision or intervention).
   - Exit `3`: Safety loop limit hit.

## Phase 3: Cursor Automations & Stop Hooks
1. **Milestone Automations:**
   - Define a Cursor Automation rule (using the IDE's automation feature) that acts as the milestone trigger. 
   - Instead of the human prompting "continue the hillclimb", the Automation runs the `tools/sdk-climb.py` driver unattended.
2. **Extend Stop Hook:**
   - Update `.cursor/hooks.json` and `.cursor/hooks/run_tests_on_stop.py`.
   - Expand the stop hook so that, when an unattended automation run finishes or aborts, it surfaces a short summary of the hillclimb's progress (e.g., "Run `slug` advanced to Iteration 3").

## Verification
- `.gitignore` prevents `.env` leaks.
- `tools/drafts/sdk-climb-spike.py --live` successfully writes a sidecar without manual LLM chat intervention.
- `handoff/SDK-CLIMB-SPIKE.md` updated from `C — defer` to `PASS`.
- `tools/sdk-climb.py` successfully orchestrates a full hillclimb iteration unattended.