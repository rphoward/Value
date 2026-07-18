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

Results are recorded after implementation using the same scenarios.
