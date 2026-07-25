# Rationale (candidate 3)

## Principles applied

- **Subtract before you add:** Remove `match_board_for_atom` and `MATCH_BOARD_ATOMS` before adding coaching; they are provably dead in lean-mvp and teach the wrong skill.
- **Model the domain:** The turn contract is a **resolved** `CoachingPayload`, not references. `kb_refs` exist only in the static asset; stdout never exposes them.
- **Boundary discipline:** `status` + `warnings` + per-row `prior_answers.status` let the interview continue without throwing from the CLI.
- **Encode lessons in structure:** Coverage and DAG closure tests fail in CI when someone adds C33 without coaching; runtime fallback is the safety net.

## Alternatives considered and rejected

### A. Agent reads `knowledge-base.json` each turn (status quo + stronger SKILL.md)

Rejected: Grounding shows the package already says `kb-load`; the failure mode is delivery, not discovery. Requiring a second file read breaks turn-completeness and repeats shape-handling in the agent.

### B. Embed full teaching text in `atoms.json`

Rejected: Bloats the scheduler asset, complicates value-bridge import, and mixes scheduling with pedagogy. A sidecar `atom-coaching.json` keeps atoms stable and lets coaching evolve without touching unlock DAG.

### C. Rewrite `match_board_for_atom` for lean-mvp

Rejected: The value skill's parts×pains grid does not map to lean-mvp's linear chain. A rewrite would reintroduce special-case atom ids. `prior_answers` from `builds_on` / `gate_review` is simpler and matches how operators actually stall (forgot what they said on MS03, not "match offering parts").

### D. Resolve KB at authoring time (pre-render concepts into JSON)

Rejected: Duplicates KB strings in two places; widening `invest_user_story_rubric` would drift from `knowledge-base.json`. Runtime resolution keeps a single source of truth and matches the story-generation test that already keys off KB letters.

### E. New `_session/kb_resolver.py` + `_session/coaching_build.py`

Rejected: Two files for one caller (`assemble_coaching_payload`) violates thermonuclear "split must be earned." One `coaching.py` until a second consumer appears.

### F. Ship `reads` / `slots` from the original plan

Rejected: `reads` duplicated `builds_on` without labels; `slots` duplicated `answer_checklist` with a vaguer name. Collapsing to labeled `builds_on` + explicit checklist reduces author confusion.

### G. Subprocess-only tests, no golden MS05 concepts

Rejected half of G: Subprocess on `next_question.py` is still required to prove wiring, but JSON-only tests give faster failure on author mistakes without `sys.path` collision.

## MS05 / INVEST-plus tension

`mvp-scope.md` and `accepts_summary` still say "INVEST pass/fail notes." `invest-plus.md` (story-generation skill) forbids passing I, E, S from the sentence alone. **This design does not change those files** (out of scope). Coaching carries the scoring policy in `inline_concepts` on MS05 so the agent can deliver a teaching turn aligned with invest-plus without a second skill read. Longer-term, `accepts_summary` and `mvp-scope.md` should converge on "N/V/T plus not answerable here for I/E/S" — noted as follow-up, not in this diff.

## Riskiest part

**KB resolver completeness.** Authors will add new top-level keys with a fifth shape (e.g. list of objects). An unhandled shape silently becomes an empty concept block with a warning the agent may ignore. Mitigation: test that every `kb_refs` value in all 32 entries round-trips to non-empty `body_markdown` via a small subprocess or a dedicated `resolve_kb_ref` test module that imports only `coaching.py` in isolation — but importing `_session` in pytest is forbidden, so the safe approach is either (1) test resolution by subprocess on a one-off CLI, or (2) move pure `resolve_kb_ref` into `scripts/_session/kb_render.py` with **no** `runtime` import so tests can import it without collision. The sketch prefers (1) for minimal files; **(2) is the escape hatch if collision blocks (1).** That fork is the highest implementation risk.

## If forced to halve the diff

Cut in this order:

1. **Gate `gate_review` structure** — use flat `builds_on` listing all module atoms for gates; lose section grouping in payload.
2. **`worked_example` on non-stall atoms** — keep only on MS05, C01, and gates.
3. **`inline_concepts` on MS05** — fold into `why_it_matters` prose (worse INVEST compliance).
4. **Subprocess integration test** — keep JSON-only coverage tests only.

Do **not** cut: deleting match board, resolved `concepts` in payload, or 32-key coverage test.
