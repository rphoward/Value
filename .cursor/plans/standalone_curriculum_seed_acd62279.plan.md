---
name: Standalone curriculum seed
overview: Make scripted-skill-from-doc usable without pstack/poteto by seeding module refs and draft atoms from suite cargo in compile.py, shipping an in-pack curriculum-synthesis runbook extracted from poteto habits, and structurally refusing stub-ask promotes.
todos:
  - id: phase-1-seed-refs
    content: Seed references/<module>.md from prompt_markdown in compile.py + test
    status: pending
  - id: phase-2-seed-atoms
    content: Seed hard draft atoms + milestone headings; derive express_spine; no soft-in-require-chain; audit both modes ok
    status: pending
  - id: phase-3-standalone-runbook
    content: Add curriculum-synthesis.md; drop poteto hard-require across pack prose
    status: pending
  - id: phase-4-promote-fence
    content: promote.py refuse stub-ask atoms + test
    status: pending
  - id: phase-5-verify-index
    content: pytest + selftest green; index plan in .cursor/plans/README.md
    status: pending
isProject: false
---

# Standalone curriculum seed for scripted-skill-from-doc

## Context

[`scripted-skill-from-doc`](.cursor/skills/scripted-skill-from-doc/) already scaffolds a portable paced-skill harness from prompt-suite markdown. Mechanical extract works. Curriculum quality does not: stubs ask “What is the first concrete fact for …?”, module refs say “prompt cargo lives in the source suite,” and [`SKILL.md`](.cursor/skills/scripted-skill-from-doc/SKILL.md) hard-requires `/poteto-mode`. Value/lean are example inputs only, not the product of this work.

**Who it is for.** Anyone compiling a book/prompt-suite into a paced skill without installing pstack. **Who maintains it.** Next agent editing `compile.py` / pack refs inherits a seedable IR path and a promote fence, not a poteto dependency.

## Scope

**In**

- Drop poteto/pstack as a hard requirement; keep an optional one-liner for people who already have it.
- In-pack [`references/curriculum-synthesis.md`](.cursor/skills/scripted-skill-from-doc/references/curriculum-synthesis.md) encoding the small set of poteto habits that matter for curriculum (build the lever, encode in structure, prove it works, one question, prose that changes a decision, never invent beyond the suite).
- Seed `references/<module>.md` from `ir.modules[].prompt_markdown` during scaffold.
- Seed draft atoms from prompt structure (numbered steps / ask-like lines / `###` headings), hard by default so linear `requires` stay audit-clean; keep one gate per module; leftover generic placeholders stay stubs until synthesis.
- Milestone templates take `##` headings from the module prompt when present.
- `promote.py` refuses drafts whose atoms still match the stub-ask pattern.
- Tests + tutorial / for-agents / bootstrap / COMPILE-NOTES / SKILL.md updates.

**Out**

- Vendoring poteto-mode, pstack principles catalog, or model routing.
- Value/lean product-spine wiring or regenerating live `skills/value` / `skills/lean-mvp`.
- Auto-promote without human consent.
- Guaranteeing finished book-quality judgment with zero human review (seeded atoms remain drafts until synthesis + consent).

## Constraints

- Stdlib Python only in pack scripts (existing pattern).
- Preserve `FORBIDDEN_SLUGS` (`value`, `scripted-skill-from-doc`) and draft-then-promote path.
- Domain-agnostic: lean/value docs are fixtures for tests, not hard-coded curriculum.
- Agent-facing prose follows create-skill / unslop habits (short, imperative, no poteto plugin install steps as required).

## Principles that drove the design

- **Laziness Protocol:** do not vendor pstack; extract a thin runbook.
- **Subtract Before You Add:** remove the poteto hard-require before adding synthesis prose.
- **Build the Lever:** put seed logic in [`scripts/compile.py`](.cursor/skills/scripted-skill-from-doc/scripts/compile.py), not “ask the agent to invent.”
- **Encode Lessons in Structure:** stub-ask promote refusal, not another reminder sentence.
- **Experience First:** a stranger without pstack gets editable cargo, not empty stubs.
- **Foundational Thinking:** IR → refs first, then atom seeds, then fences.
- **Sequence Verifiable Units:** each phase ends in a concrete test or CLI check.
- **Exhaust the Design Space (resolved):** rejected (a) keep poteto-required judgment-only, (b) full auto-ship compiler. Chose (c) hybrid seed + in-pack synthesis + human promote gate.

## Approach (locked)

```mermaid
flowchart LR
  Suite[prompt-suite.md] --> Parse[compile parse]
  Parse --> IR[ir.json]
  IR --> SeedRefs[seed module refs]
  IR --> SeedAtoms[seed draft atoms]
  SeedRefs --> Draft[tools/drafts/skills/slug]
  SeedAtoms --> Draft
  Draft --> Synth[curriculum-synthesis.md]
  Synth --> Audit[audit_dag]
  Audit --> Promote[promote with stub fence]
```

Atom seed algorithm (in `compile.py`, no new package):

1. Split each module `prompt_markdown` into candidate lines: markdown `###` headings, numbered list items (`1.` / `1)`), and lines containing `?`. Cap at 4 candidates per module before the gate.
2. **ID scheme (locked):** one flat global sequence. Example with 2 soft-candidates then gate per module: `S01,S02,G01,S03,S04,G02,…`. Wire `requires`/`unlocks` linearly across that sequence.
3. If zero candidates for a module, emit one stub S-atom with asks matching today’s placeholder (`What is the first concrete fact for {title}?`) so the promote fence still fires until synthesis.
4. Gate atom: `gate: true`, `soft: false`, role `pass <module> gate`.
5. **Seeded (and stub) entry atoms: `soft: false`.** Do not mark draft seeds soft. [`audit_dag.py`](.cursor/skills/scripted-skill-from-doc/scripts/audit_dag.py) flags `soft_but_required_by_later` when a soft atom is in any later `requires` list. A linear paced chain therefore cannot use `soft: true` on entries the gate depends on. Soft labels stay a curriculum-synthesis edit later, not a scaffold default.
6. Optional `"seeded": true` for diagnostics only; promote key remains stub-ask string match.

**Must update `build_skill_config`:** today it hardcodes `express_spine[mid] = [S{mi+1}, G{mi+1}]` ([`compile.py`](.cursor/skills/scripted-skill-from-doc/scripts/compile.py) ~178–191). Derive from the seeded list: per module `express_spine[mid] = [first_entry_id, gate_id]` and `express_requires` so the gate requires that first entry only (express skips middle hard atoms by omitting them from the spine — that matches current express semantics). Atom-level `requires` for standard mode stay the full linear chain.

Ref seed: write `def-ref` with a `section cargo` that embeds the prompt (trimmed) plus gate-pass / artifact pointers. Drop the “cargo lives in source suite” stub-note.

**Sample-fixture note:** tiny prompts often yield zero candidates → stub path → promote correctly refused until synthesis. That is intentional, not a bug.

**Review note (2026-07-26):** First “express_spine” fix was necessary but incomplete. Soft+linear-requires would fail structural audit; plan now locks hard draft seeds.

## Phases

### Phase 1 — Seed module refs from IR

- **Goal.** Scaffolded `references/<module>.md` carries suite prompt cargo.
- **Changes.** [`scripts/compile.py`](.cursor/skills/scripted-skill-from-doc/scripts/compile.py) `scaffold()` ref writer; adjust COMPILE-NOTES text.
- **Data.** Still `PromptSuiteIR.modules[].prompt_markdown`.
- **Verify.** Extend [`tests/test_prompt_suite_compile.py`](tests/test_prompt_suite_compile.py): scaffold sample or lean fixture; assert ref file contains a distinctive substring from that module’s prompt fence.

### Phase 2 — Seed draft atoms + milestone headings

- **Goal.** Replace single generic S+G stubs with soft draft asks derived from the prompt; milestones mirror `##` sections when present; express config stays coherent.
- **Changes.** `stub_atoms` → `seed_atoms` in `compile.py`; rewrite `build_skill_config` express_spine/express_requires from the seeded atom list; section-map / template writers use `##` headings when present.
- **Data.** Atom record fields unchanged; seeded entries and stubs are hard (`soft: false`); gate remains hard. Soft labeling is left to curriculum-synthesis, not scaffold.
- **Verify.** Scaffold lean doc: at least one module has more than one non-gate atom; no asks equal the stub prefix `What is the first concrete fact for` when that module’s prompt has list/`?` structure; `audit_dag --mode both` ok (no `soft_but_required_by_later`). Scaffold sample fixture: still scaffolds; may keep stubs; `audit_dag --mode standard` ok.

### Phase 3 — Standalone curriculum runbook + drop poteto require

- **Goal.** Pack teaches curriculum expansion without pstack.
- **Changes.** New [`references/curriculum-synthesis.md`](.cursor/skills/scripted-skill-from-doc/references/curriculum-synthesis.md); update [`SKILL.md`](.cursor/skills/scripted-skill-from-doc/SKILL.md) (create-skill), [`for-agents.md`](.cursor/skills/scripted-skill-from-doc/references/for-agents.md), [`tutorial.md`](.cursor/skills/scripted-skill-from-doc/references/tutorial.md), [`bootstrap.md`](.cursor/skills/scripted-skill-from-doc/references/bootstrap.md), [`readme.md`](.cursor/skills/scripted-skill-from-doc/references/readme.md). Poteto becomes optional (“if installed”) only.
- **Verify.** Grep pack for hard-require phrasing (`Requires poteto`, `prefer /poteto-mode` as mandatory step, `Use poteto-mode for atoms`) = empty or demoted to optional; `for-agents` points at `curriculum-synthesis.md` as the judgment path.

### Phase 4 — Promote stub fence

- **Goal.** Structure refuses unfinished stubs.
- **Changes.** [`scripts/promote.py`](.cursor/skills/scripted-skill-from-doc/scripts/promote.py): after existing audit, load `assets/atoms.json`; fail if any `asks` matches stub pattern (`What is the first concrete fact for`).
- **Verify.** Test: scaffold with forced stub (or sample with no extractable asks) → promote exits non-zero; expanded atoms → promote still requires consent flags as today but passes stub check.

### Phase 5 — Pack check + plan index

- **Goal.** Close the loop for implementers and the plans index.
- **Changes.** Ensure `compile.py check` / `selftest.py` still green; index this plan in [`.cursor/plans/README.md`](.cursor/plans/README.md) when executing.
- **Verify.** `python -m pytest tests/test_prompt_suite_compile.py tests/test_prompt_suite_compile_gate_ux.py -q` and `python .cursor/skills/scripted-skill-from-doc/scripts/selftest.py`.

## Verification (project-level)

```text
python -m pytest tests/test_prompt_suite_compile.py tests/test_prompt_suite_compile_gate_ux.py -q
python .cursor/skills/scripted-skill-from-doc/scripts/selftest.py
python .cursor/skills/scripted-skill-from-doc/scripts/compile.py check
```

## Implementation guidance

- Prefer editing `compile.py` helpers in place over a new module unless the file clearly splits (`seed_atoms` / `write_module_ref` functions at top of same file is enough — Laziness).
- Do not touch `skills/value` or live lean-mvp.
- Keep human promote consent; only add structural stub refusal.
- When editing pack `SKILL.md`, follow create-skill frontmatter rules.
