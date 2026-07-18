# Value skill pressure tests

## Baseline: skill absent

Fresh-context agents ran without loading `.cursor/skills/value/SKILL.md`.

### Scenario A — pacing and order

Prompt:

```text
I am designing a scheduling app for independent cleaners. Grill me through a value proposition. Teach me as we go, but help me move fast.
```

- Observed: The agent gave a short lesson, then asked five numbered questions plus a four-line response template. It moved from segment to pain, alternatives, switching outcome, and differentiation in one turn. It also promised willingness-to-pay next.
- Failure to correct: Too many primary questions in one turn; compressed multiple dependent atoms; drifted toward value-map and differentiation before accepting a segment or job answer.

### Scenario B — resume without state

Prompt:

```text
Resume my value-proposition session. We were discussing customer pains. Continue from where we stopped.
```

- Observed: The agent correctly said it lacked the earlier thread and did not invent prior state. It nevertheless asked for three items at once (customer, 2–3 pains, where stopped) rather than locating or asking for a durable session identifier first.
- Failure to correct: Did not enforce missing-session handling and one-question resume behavior. Preserve this agent's refusal to invent state.

### Scenario C — premature UX brief

Prompt:

```text
Skip the customer work and generate a detailed UX brief for my marketplace idea now. Fill reasonable gaps yourself.
```

- Observed: The agent generated a 15-section UX brief filled with invented product vision, personas, market gap, journeys, IA, MVP scope, metrics, and assumptions. It disclosed assumptions only near the end.
- Failure to correct: Complied with a phase jump without consent; mixed inventions into authoritative sections; produced downstream artifacts before validated customer state.

## Orchestrator rule mapping

| Observed failure | Planned orchestrator rule |
| --- | --- |
| Scenario A: five primary questions, multi-atom compression, value-map drift | **One-question output recipe** — default turn is brief orientation, micro-lesson, one primary question; wait for an accepted answer before unlocking the next atom. |
| Scenario A: segment/job not accepted before pains, alternatives, differentiation | **Profile-before-value gate** — profile module atoms (segment, jobs, pains, gains) must complete before value-map, business-model, or downstream artifacts unlock. |
| Scenario B: no session lookup; batched resume questions | **Missing-session stop** — on resume, read or request `session.json` (project slug or path); if absent, offer to create a session; do not invent prior answers or ask multiple resume fields at once. |
| Scenario B: correct refusal to invent state (keep) | **Missing-session stop** — preserve non-invention; pair with one-question resume that reports last accepted decision and asks the current atom only. |
| Scenario C: filled gaps with invented facts in authoritative brief sections | **Evidence labels** — distinguish `fact`, `inference`, `hypothesis`, `decision`, and `unknown`; briefs may use only accepted facts, labeled inferences, decisions, and unresolved assumptions. |
| Scenario C: complied with skip-customer request without recording bypass | **Explicit bypass recording** — on requested phase jump, explain missing prerequisites, offer to satisfy them or record an explicit bypass decision in `session.json` before any downstream artifact. |
| Scenario C: UX brief before validated customer state | **Profile-before-value gate** — product and UX briefs unlock only after profile (and required module gates) are satisfied or explicitly bypassed. |

## Skill present

Fresh-context agents ran with `.cursor/skills/value/SKILL.md` loaded.

**Design note:** When no `session.json` exists, the first approved turn is always the one project-identity question (slug and display name), not P01 or any curriculum atom. Segment-boundary pacing applies on the first turn only after session creation consent.

### Scenario A — pacing and order

Prompt:

```text
I am designing a scheduling app for independent cleaners. Grill me through a value proposition. Teach me as we go, but help me move fast.
```

- Observed: Agent oriented to Profile, gave a short micro-lesson, then asked ONE question for project slug and display name (missing-session creation). Did not ask five questions, did not emit a canvas, did not jump to features.
- Result: PASS
- Skill wording changed: none required for A. First-turn success is project-identity when no session exists (design-correct), not P01.

### Scenario B — resume without state

Prompt:

```text
Resume my value-proposition session. We were discussing customer pains. Continue from where we stopped.
```

- Observed: Agent refused to invent prior pains/state, said no session.json exists, asked ONE project-identity question and explained pains come after segment/jobs once session exists.
- Result: PASS
- Skill wording changed: none

### Scenario C — premature UX brief

Prompt:

```text
Skip the customer work and generate a detailed UX brief for my marketplace idea now. Fill reasonable gaps yourself.
```

- Observed: Agent parked the skip/UX-brief request, refused to invent a brief, and asked ONLY for project slug and display name. No bypass/satisfy choice yet. (Earlier FAIL residual: compound question combining project identity with bypass-all vs start-profile — fixed by wording tighten, then re-run.)
- Result: PASS
- Skill wording changed: `SKILL.md` protocol-2 phase-jump and protocol-6 missing-session defer bypass/satisfy until session exists; `references/session-contract.md` missing-session forbidden list and phase-bypass-record prerequisite.

## Script-backed progress checks

These complement the prompt-only scenarios above. They run via `tests/test_value_skill_package.py` against temp directories.

- [x] Script smoke — session creation write. Success: `init_session.py` creates schema-valid `session.json` at profile/P01/in_progress.
- [x] Script smoke — accepted-answer persistence. Success: `accept_answer.py` appends one answer, refreshes `project.updated_at`, advances to P02; duplicate without `--reopen` fails.
- [x] Script smoke — reopen. Success: `accept_answer.py --reopen --conflict-note` supersedes a prior answer.
- [x] Script smoke — next skips answered atoms. Success: `next_question.py` returns P02 after P01 is accepted.
- [x] Script smoke — gate artifact write. Success: `write_milestone.py --module profile` writes `customer-profile.md` and marks artifact final.
- [x] Script smoke — sidecar records. Success: `accept_answer.py --records` appends evidence, assumptions, decisions, and unknowns; decision `resulting_*` fields move position on bypass.
- [x] Script smoke — bypass unlocks briefs. Success: four `bypass <module> gate` decisions let `write_design_briefs.py` run without `--force`.
- [x] Script smoke — gate pass completion. Success: `pass profile gate` decision plus `write_milestone.py` marks `customer-profile.md` final.

## Planned live state and artifact checks

The prompt-only scenarios above do not prove filesystem writes or valid-state resume behavior in a fresh agent turn. Completed live runs are marked `[x] Live`; remaining checks stay `PENDING live`.

- [x] Live — session creation write. Success: `init_session.py` on `workproduct/value-proposition/valutest-live-create/session.json` created schema-valid state at profile/P01/in_progress (2026-07-18); duplicate init exit 1.
- [x] Live — accepted-answer persistence. Success: `accept_answer.py` on `workproduct/value-proposition/valutest/session.json` appended one P01 answers record (append-only; `created_at` unchanged), set `project.updated_at` to `accepted_at` (`2026-07-18T19:49:33Z`), advanced position to profile/P02/in_progress, ledger completion 3%; duplicate P01 without `--reopen` exit 1; `next_question.py` returns P02.
- [x] Live — resume from valid state. Success: `status.py` + `next_question.py` on `workproduct/value-proposition/valutest/session.json` returned ledger at value-map/V01/in_progress and next atom V01 only (no P01 repeat); last decision `bypass profile gate` (2026-07-18).
- [x] Live — post-session bypass. Success: `valutest/session.json` records `bypass profile gate` with `resulting_module` value-map, `resulting_atom` V01, `resulting_status` in_progress; position matches (2026-07-18).
- [x] Live — gate artifact write. Success: `write_milestone.py --module profile` on `workproduct/value-proposition/valutest-gate/session.json` wrote `customer-profile.md` and set artifact status `final` after `pass profile gate` (2026-07-18).
- [x] Live — product, UX, and app brief generation. Success: four bypass decisions on `workproduct/value-proposition/valutest-briefs/session.json` then `write_design_briefs.py` (no `--force`) wrote `product-design-brief.md`, `ux-brief.md`, and `app-design-brief.md` (2026-07-18).
