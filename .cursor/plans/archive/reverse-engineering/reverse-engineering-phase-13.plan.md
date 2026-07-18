# Reverse-engineering phase 13

Back-link: [Reverse-engineering quality master plan](reverse-engineering-quality-master_da289ff7.plan.md)  
Prior phase: [Reverse-engineering phase 12](reverse-engineering-phase-12.plan.md)

## Goal

Prove the live quality-veto contract on one bounded comparison, then execute and freeze the full development experiment without opening reserved validation.

## Prerequisites

- Phase 12 passed.
- The owner approved the fixed live development budget.
- All protocol, benchmark, prompt, model, seed, and instrument hashes match.
- `development-001` does not exist.

## Read first

1. Phase 9 and 12 handoffs
2. Experiment and benchmark manifests
3. Frozen drafter, reviser, evaluator, discriminator, content-adherence, and quality-judge contracts
4. Workflow one-command reference

Do not read reserved-validation files.

## In scope

- Run a three-comparison live quality-veto smoke on one approved development fixture.
- Require balanced sides and a stable `pass`, `veto`, or `human_review` result under Phase 1 rules.
- Stop before the full experiment if the smoke is invalid or unstable.
- Create `development-001` from the locked benchmark.
- Use analysis and development evidence only.
- Treat each baseline output as the matched incumbent.
- Generate treatment drafts within the fixed budget and permit development tells to guide revisions.
- Apply content adherence and blind general-quality vetoes.
- Preserve explicit no-finalist results.
- Record calls, available token and cost facts, and wall time.
- Freeze both arms and every finalist hash.

## Out of scope

- Instrument, prompt, agent, test, protocol, or benchmark edits.
- Reserved-validation access.
- Increased budgets or new items.
- Treating disagreement as a pass.
- Benchmark PASS/FAIL conclusions.

## Files

Allowed:

- Create `tools/runs/reverse-engineering-quality/quality-smoke-001/**`.
- Create `tools/runs/reverse-engineering-quality/development-001/**`.
- Create `handoff/REVERSE-ENGINEERING-PHASE-13-PASSED.md`.
- Modify `handoff/STATE.md` after the gate.

Forbidden:

- `src/**`
- `tests/**`
- `.cursor/agents/**`
- `.cursor/skills/**`
- Protocol, benchmark, and dry-run inputs
- Reserved-validation files
- Historical run folders

## Test-first steps

1. Validate frozen hashes, budget approval, and zero reserved consumption.
2. Run the full suite.
3. Execute the bounded quality-veto smoke and record all three blind judgments.
4. Require valid orientation, complete judgments, and a terminal outcome before proceeding.
5. Initialize `development-001` and use its dispatch file as the only queue.
6. Complete baseline and treatment paths, both vetoes, and finalist or no-finalist for each item.
7. Require sixteen terminal arm/item results with complete lineage.
8. Freeze the generation.
9. Revalidate hashes and zero reserved consumption.
10. Run the full suite again.

## Gate

PASS only when the live quality smoke is valid, every benchmark item has terminal baseline and treatment results, each treatment finalist passes both vetoes, costs and time are recorded, both arms are frozen, and reserved evidence remains unopened.

## Handoff

Record smoke judgments and outcome, development freeze, finalist, cost, timing, lineage, and verification hashes in `handoff/REVERSE-ENGINEERING-PHASE-13-PASSED.md`. State that no tuning may follow without a new generation.

## Stop conditions

- The quality smoke is malformed, unstable, or exceeds its budget.
- A frozen input differs.
- The development budget is unavailable or exceeded.
- A worker requests reserved evidence.
- A harness defect appears.
- An item lacks lineage or a terminal result.
- Freeze or full-suite verification fails.
