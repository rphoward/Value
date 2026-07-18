# Phase 6 — Pipeline / persistence seam

Back-link: [overview.md](overview.md)

## Goal

Make full-pipeline's definition of done name the unattended entry (driver **or** `/hillclimb` if spike deferred), and keep ADR/STATE honest about the new job artifact. No Start Climb button.

## Changes

- If phase 4 chose A or B: `.cursor/skills/pipeline/SKILL.md` protocol-0 step-4 says after distiller → analyze → prepare, run `python tools/sdk-climb.py --slug <slug> --init-if-missing` (or `/hillclimb resume <slug>`). Catalog success row names both.
- If phase 4 chose C: pipeline/catalog/STATE point at `/hillclimb` only; do not claim `sdk-climb.py` exists.
- Wizard prepare copy (`_prepare_step.html` or equivalent): when driver ships, two lines for `--init-if-missing` and unattended climb; when deferred, point at `/hillclimb`. No new POST route.
- `docs/adr/001-run-persistence.md` variant A: add `discrimination-job-v{n}.json` and `discrimination-job-v1{a,b,c}.json`; note trials/verdicts/discrimination/decision/calibration as existing convention.
- `handoff/STATE.md`: open gate for job board + SDK driver (spike-gated); point at this plan directory.
- Use **create-skill** / **unslop** for skill and handoff prose. Domain ADR edit is a light extension of an accepted ADR (no full grill session unless vocabulary changes).

## Data structures

ADR file list only. No new runtime types.

## Verification

**Static.** Grep confirms pipeline skill and catalog match the spike outcome (driver named, or `/hillclimb` only). ADR lists the job file(s).

**Runtime.** Open prepare step in the wizard (control-ui if convenient) and confirm the handoff line is visible. Docs-only otherwise.
