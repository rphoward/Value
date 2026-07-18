# Reverse-engineering phase 1

Back-link: [Reverse-engineering quality master plan](reverse-engineering-quality-master_da289ff7.plan.md)

## Goal

Freeze the baseline and experiment protocol without opening reserved-validation prose.

## Prerequisites

- Work from the repository root.
- Read-only verification of the master plan has passed.
- Do not commit or call live models in this phase.

## Read first

1. `AGENTS.md`
2. `handoff/STATE.md`
3. `.cursor/plans/archive/reverse-engineering/reverse-engineering-quality-master_da289ff7.plan.md`
4. `docs/adr/001-run-persistence.md`
5. `.cursor/skills/workflow/SKILL.md`
6. `.cursor/skills/workflow/references/one-command.md`
7. `.cursor/commands/hillclimb.md`
8. `handoff/SCORER-V2-PASSED.md`

## In scope

- Create `tools/runs/reverse-engineering-quality/experiment-manifest.json`.
- Record the current commit, dirty paths, workflow and pipeline versions, prompt hashes, configured model roles, trial budgets, and fixed evaluation budget.
- Register four targets with two benchmark item identities each.
- Register reserved-validation identities only. Store no reserved text, excerpt, path, URL, or answer key.
- Freeze separate outcome fields for fidelity, content, general quality, originality, cost, and wall time.
- Freeze `PASS`, `FAIL`, and `INCONCLUSIVE` rules. Do not combine the fields into one weighted score.
- Freeze the finalist-quality judge count, required agreement, tie rule, and disagreement path.
- Freeze the multi-passage pilot target, passage count, reversal definition, reversal margin, and uncertainty rule.
- Freeze staged-evaluation policy inputs: initial blind-batch size, decision-boundary width, minimum winner agreement, minimum content-veto agreement, minimum quality-veto agreement, minimum cost reduction, maximum wall-time ratio, hard trial maximum, and tie handling.
- Freeze the item-level severe-collapse rule and the minimum number of complete paired benchmark items.
- If a model role or threshold is absent from current contracts, stop and obtain an explicit owner decision rather than guessing.

## Out of scope

- Runtime Python changes.
- Benchmark prose, drafts, or live judgments.
- Historical run repair.
- Reading reserved-validation content.

## Files

Allowed:

- Create `tools/runs/reverse-engineering-quality/experiment-manifest.json`.
- Modify `handoff/STATE.md` after the gate.
- Modify `.cursor/plans/README.md` after the gate.

Forbidden:

- `src/**`
- `tests/**`
- `.cursor/agents/**`
- `.cursor/skills/**`
- Existing `tools/runs/**` evidence

## Test-first steps

1. Run a manifest-absent assertion and confirm it fails.
2. Create the manifest from current repository facts.
3. Validate required keys, eight unique benchmark item identities, hash formats, and the three allowed outcome labels.
4. Assert that reserved entries contain identity fields only.
5. Recompute every recorded prompt and protocol hash and require an exact match.
6. Run `$env:PYTHONPATH="src"; python -m pytest tests/ -q`.

## Gate

PASS only when the manifest validates, all hashes reproduce, reserved content remains unopened, and the full suite passes.

## Handoff

Record the manifest path, SHA-256, current commit, dirty paths, verification commands, and actual results in `handoff/REVERSE-ENGINEERING-PHASE-1-PASSED.md` and `handoff/STATE.md`.

## Stop conditions

- A required role, threshold, or benchmark identity is ambiguous.
- Reserved content must be opened to complete the manifest.
- A protocol input changes during the phase.
- Any validation or test fails.
