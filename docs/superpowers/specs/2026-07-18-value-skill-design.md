# Value skill design

## Goal

Build a GitHub-distributed Cursor skill that teaches value proposition design while helping the user produce design evidence. The skill conducts a paced interview, explains the current concept briefly, asks one primary question, records the accepted answer, and unlocks the next dependent question.

The source prompt suite supplies the curriculum map. Cursor's skill format supplies the package. An atom and session layer supplies the missing teaching pace and durable state.

## Package boundary

The first version is one skill package at `.cursor/skills/value/`. It is one orchestrator, not one content monolith.

```text
.cursor/skills/value/
  SKILL.md
  references/
    profile.md
    value-map.md
    business-model.md
    experiments.md
    session-contract.md
  assets/
    session.schema.json
    customer-profile.template.md
    value-map.template.md
    business-model.template.md
    experiment-plan.template.md
    product-design-brief.template.md
    ux-brief.template.md
```

Every reference is linked directly from `SKILL.md`. There are no nested reference folders because this repo requires one-level progressive disclosure.

Python is deferred until use reveals a repeated, fragile operation. Cursor can write and update the first version's JSON and Markdown files directly. This avoids preserving the incorrectly scaffolded HTTP app merely to justify a script.

## Orchestrator

`SKILL.md` owns:

- discovery triggers such as “grill me on this value proposition,” “map this customer,” “test this product idea,” and “turn this idea into a product or UX brief”;
- session start, resume, and completion behavior;
- phase order and prerequisites;
- the one-question pacing contract;
- rules for loading only the active module reference;
- state writes after an answer is accepted;
- milestone artifact generation.

The orchestrator does not contain the full question bank, scoring rubrics, experiment library, or output templates.

## Curriculum modules

The four direct references preserve the source document's useful dependency order:

1. `profile.md`: customer segment, jobs, pains, gains, evidence, and priority.
2. `value-map.md`: products and services, pain relievers, gain creators, and fit.
3. `business-model.md`: delivery requirements, costs, revenues, scale, and defensibility.
4. `experiments.md`: assumptions, evidence quality, test cards, learning cards, and next decisions.

Each module contains ordered atoms. An atom has:

- `id`: stable identifier used by session state;
- `teaches`: two or three sentences explaining the concept and why it comes now;
- `visual`: one compact original analogy or schematic when it improves understanding;
- `asks`: one primary question;
- `accepts`: the minimum information required to advance;
- `writes`: the state field changed by the answer;
- `unlocks`: the next atom or milestone.

The agent stays on the current atom when an answer is vague, inferred, or missing evidence. It asks one focused follow-up rather than advancing.

## Interaction contract

The default turn has this shape:

1. Brief orientation: current module and why this atom follows.
2. Micro-lesson or visual analogy when useful.
3. One primary question.

The skill waits for the user's answer. It may ask up to three tightly related questions only when the user explicitly requests batching. It never emits a full canvas, matrix, or scorecard before the required answers exist.

The skill distinguishes:

- `fact`: supplied by the user or observed in evidence;
- `inference`: reasoned from facts and labeled as such;
- `hypothesis`: unvalidated statement that requires a test;
- `decision`: an explicit choice and its reason;
- `unknown`: required information not yet established.

## Session state

Each engagement uses:

```text
workproduct/value-proposition/<project-slug>/
  session.json
  customer-profile.md
  value-map.md
  business-model.md
  experiment-plan.md
  product-design-brief.md
  ux-brief.md
```

`session.json` is canonical. It stores the schema version, project identity, current module and atom, accepted answers, evidence, assumptions, decisions, unknowns, and artifact status.

The agent writes `session.json` after each accepted answer. It writes the module Markdown file at the module gate. It writes product and UX briefs only from accepted facts, labeled inferences, decisions, and unresolved assumptions.

On resume, the agent reads `session.json`, reports the last accepted decision in one sentence, and asks the current atom. It does not repeat completed questions unless the user reopens a decision.

## Source-document corrections

The prompt suite is design input, not verified authority. The implementation retains useful concepts but corrects these behaviors:

- A hidden or printed YAML ledger becomes durable `session.json`.
- Full-module prompt dumps become one atom per turn.
- Text descriptions of book images become original compact analogies or schematics; the skill does not claim to reproduce the book's figures.
- “Five whys” is optional and stops when evidence becomes speculative.
- A job's rubric result is evidence for discussion, not an automatic truth.
- An unmatched feature is parked as an orphan candidate; it is not deleted without a decision.
- Business-model scores remain `unknown` when evidence is absent; the agent does not invent precision.
- Experiment evidence is ranked by behavior and commitment, while spoken feedback remains usable but weak.

## Failure handling

- Missing session: offer to create one; do not invent prior answers.
- Invalid session JSON: stop, identify the invalid field, and preserve the file.
- Conflicting answer: record the conflict and ask which statement governs.
- Premature solution request: capture it in a parking lot, then return to the current profile atom.
- Requested phase jump: explain the missing prerequisite and offer either to satisfy it or explicitly record a bypass decision.
- Unknown evidence: mark `unknown`; do not convert it to an inference.

## Verification

Before distribution:

1. Validate frontmatter, skill name, description triggers, and direct reference links.
2. Validate `session.schema.json` and each template path.
3. Run baseline and skill-present scenarios for:
   - one-question pacing;
   - refusal to invent missing state;
   - profile-before-value-map ordering;
   - evidence labels;
   - session resume;
   - milestone product and UX brief generation.
4. Run the repository test suite.

## Deferred work

- Python state mutation and validation CLI.
- Browser or app UI.
- OCR or image ingestion.
- Separate discoverable subskills.
- Removal or repurposing of `src/value/`.

These follow only after the Markdown-led workflow demonstrates a repeated need.
