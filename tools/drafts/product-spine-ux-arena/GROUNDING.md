# Architect grounding — product-spine UX (Phase A)

## Problem
Product-spine was rewritten as a journey guide. UX still risks dumping Maya after naming a door, orphaning her after lean MVP (lean has no `/product-spine` cue), or skipping claim/NotebookLM. Fix guide voice and sibling re-entry without inventing spine `session.json` or a fifth coordinator.

## Constraints (non-negotiable)
- Spine carries phase, destination, done-enough, claim exit.
- Siblings own grilling and `session.json`.
- Spine may run `status.py` read-only; never init/accept/import.
- Claim phase: read and follow `story-generation-prompt` in that turn.
- clarity-ready / mvp-ready derived via `module_outcome` (completed|bypassed), not status brief alone.
- Data shape: journey phases `{clarity, mvp, claim, return-after-learning}` + sibling sessions under shared slug. No new spine ledger.
- Ship: prefer `.cursor/skills/product-spine/` (+ digest-match `skills/product-spine/`). Sibling edits only if mock proves handoff hole.
- Model lock for this session: composer-2.5 and cursor-grok-4.5-high only.

## Known UX gaps
1. Lean-mvp has zero `/product-spine` mentions → post-mvp "which skill?" orphan.
2. Two-slash tax (spine names /value or /lean-mvp then stops) — by design; voice must make next step unmistakable.
3. Claim must not feel like triage-and-abandon; spine inlines story skill.
4. status.py brief shows active module, not readiness — agents must not confuse them.
5. Walk harness triage drift is draft-only; SKILL/path is truth.

## Persona
Maya / ShiftSwap / slug `shiftswap` — weekend vibecode so restaurant servers trade shifts without group-chat chaos. Success: honest pitch + NotebookLM producer paste.
