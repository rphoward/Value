# Phase 04 — Empty-run Studio-lite

Back-link: [overview.md](overview.md)

## Goal

Empty-run onboarding into the canvas via `pipeline_wizard`. Studio steps 1–4 as a short path, not a permanent wizard chrome.

## Changes

- Empty-run detection routes to Studio-lite
- Reuse `pipeline_wizard`; migrate toward `studio-state` if needed
- After onboarding, land in Document Canvas

## Data structures

- `studio-state` phase index for empty-run onboarding (or wizard-state bridge)

## Verification

**Static.** Wizard / onboarding pytest.

**Runtime.** control-ui: create empty run → complete Studio-lite → canvas.
