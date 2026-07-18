# Reverse-engineering phase 4

Back-link: [Reverse-engineering quality master plan](reverse-engineering-quality-master_da289ff7.plan.md)  
Prior phase: [Reverse-engineering phase 3](reverse-engineering-phase-03.plan.md)

## Goal

Define one immutable content-brief and passage-provenance contract for web, owned, and manual source passages.

## Prerequisites

- Phases 1–3 passed.
- Generation and parent-manifest hashes are available.
- This phase defines the contract only; Phase 5 adopts it.

## Read first

1. `CONTEXT.md`
2. Phase 3 handoff
3. `docs/adr/001-run-persistence.md`
4. `docs/adr/002-owned-corpus-registry.md`
5. `src/eliotwf_skills/distiller/shapes.py`
6. `src/eliotwf_skills/workflow/prepare.py`
7. `src/eliotwf/infrastructure/run_store.py`
8. `src/eliotwf/application/pipeline_wizard.py`

## In scope

- Create `src/eliotwf_skills/workflow/content_contracts.py`.
- Define exact, versioned rendering for `content-brief.md`.
- Record source kind, source identity, source-content hash, author, work, location, word count, retrieval facts when applicable, brief hash, and parent artifact hashes.
- Reject incompatible locator fields for web, owned, and manual provenance.
- Validate source and parent hashes before writing.
- Permit identical replay and refuse replacement with different bytes.
- Load existing unversioned owned metadata as legacy without inventing missing facts or rewriting files.
- Document the artifact contracts in ADR 001.

## Out of scope

- Prepare, wizard, run-store, or drafter adoption.
- Content generation from source text.
- Legacy migration.
- Benchmark or reserved-validation material.

## Files

Allowed:

- Create `src/eliotwf_skills/workflow/content_contracts.py`.
- Create `tests/test_content_contracts.py`.
- Modify `docs/adr/001-run-persistence.md`.
- Modify `handoff/STATE.md` after the gate.

Forbidden:

- Existing distiller, prepare, application, or presentation code
- Agent and skill contracts
- Existing run artifacts

## Test-first steps

1. Add failing round-trip tests for web, owned, and manual provenance.
2. Add rejection tests for missing required facts, incompatible locator fields, path escape, and content-hash mismatch.
3. Add immutable-replay and differing-replacement tests.
4. Add legacy-load and absent-contract tests.
5. Implement validation, rendering, hashing, loading, and writes in the single module.
6. Run `$env:PYTHONPATH="src"; python -m pytest tests/test_content_contracts.py -q`.
7. Run adjacent distiller, prepare, run-store, and pipeline-wizard tests unchanged.
8. Run the full suite.

## Gate

PASS only when all provenance kinds round-trip, invalid combinations fail before writing, hashes match exact bytes, differing replacement is refused, and legacy reads remain honest.

## Handoff

Record public functions, schemas, filenames, compatibility behavior, parent-manifest hash, and test output in `handoff/REVERSE-ENGINEERING-PHASE-4-PASSED.md`.

## Stop conditions

- Validation would fabricate missing provenance.
- Existing differing content can be overwritten.
- Contract adoption is required to pass this contract-only phase.
- More than one runtime module is needed.
- Any focused or full-suite test fails.
