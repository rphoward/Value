# Value Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a teaching-first Cursor skill that grills one value-proposition design atom at a time, preserves dependency order, and writes durable state plus product and UX artifacts.

**Architecture:** `.cursor/skills/value/SKILL.md` is the sole orchestrator. Five direct reference files hold the four curriculum modules and session contract; flat assets hold the JSON schema and milestone templates. Cursor writes the first version's state and artifacts directly, without a Python engine.

**Tech Stack:** Cursor Agent Skills, Markdown, JSON Schema Draft 2020-12, Python `unittest` for package validation.

## Global Constraints

- Keep one skill package at `.cursor/skills/value/`; do not create discoverable subskills.
- Link every reference directly from `SKILL.md`; do not create nested reference folders.
- Ask one primary question per turn. Ask two or three only when the user explicitly requests batching.
- Teach briefly before asking; do not emit a full canvas, matrix, or scorecard before prerequisite answers exist.
- Record facts, inferences, hypotheses, decisions, and unknowns as distinct kinds.
- Treat `session.json` as canonical and write it after every accepted answer.
- Use original compact analogies or schematics; do not claim to reproduce book figures.
- Do not add Python, UI, OCR, dependencies, or changes under `src/value/` in this release.
- Follow `.cursor/rules/skill-authoring.mdc`: `SKILL.md` uses the repo's `def-sop` form and references use `def-ref`.
- Do not commit unless the user separately requests a commit.

---

## File map

**Modify**

- `.cursor/skills/value/SKILL.md`: discovery, session lifecycle, pacing, phase gates, reference routing, persistence, and artifact rules.

**Create**

- `.cursor/skills/value/references/profile.md`: ordered customer-profile atoms.
- `.cursor/skills/value/references/value-map.md`: ordered offering and fit atoms.
- `.cursor/skills/value/references/business-model.md`: ordered feasibility, viability, scale, and defensibility atoms.
- `.cursor/skills/value/references/experiments.md`: ordered assumptions, tests, evidence, and learning atoms.
- `.cursor/skills/value/references/session-contract.md`: canonical state fields, resume behavior, conflicts, bypasses, and milestone writes.
- `.cursor/skills/value/assets/session.schema.json`: machine-readable canonical state contract.
- `.cursor/skills/value/assets/customer-profile.template.md`: profile milestone view.
- `.cursor/skills/value/assets/value-map.template.md`: fit milestone view.
- `.cursor/skills/value/assets/business-model.template.md`: business-model milestone view.
- `.cursor/skills/value/assets/experiment-plan.template.md`: test and learning milestone view.
- `.cursor/skills/value/assets/product-design-brief.template.md`: downstream product/app design handoff.
- `.cursor/skills/value/assets/ux-brief.template.md`: downstream UX/UI handoff.
- `tests/test_value_skill_package.py`: package, frontmatter, reference, atom, schema, and template validation.
- `docs/value-skill-pressure-tests.md`: baseline and skill-present scenario observations.

**Delete**

- `.cursor/skills/value/references/workflow.md`: obsolete stub replaced by the five direct references.

---

### Task 1: Characterize baseline failures

**Files:**
- Create: `docs/value-skill-pressure-tests.md`

**Interfaces:**
- Consumes: approved design at `docs/superpowers/specs/2026-07-18-value-skill-design.md`.
- Produces: observed baseline failures that the skill wording must address.

- [ ] **Step 1: Run three fresh-context scenarios without loading `.cursor/skills/value/SKILL.md`**

Scenario A:

```text
I am designing a scheduling app for independent cleaners. Grill me through a value proposition. Teach me as we go, but help me move fast.
```

Record whether the agent asks more than one primary question, drafts a canvas prematurely, or starts feature design before establishing the segment and job.

Scenario B:

```text
Resume my value-proposition session. We were discussing customer pains. Continue from where we stopped.
```

Record whether the agent invents prior state instead of asking for or locating a session.

Scenario C:

```text
Skip the customer work and generate a detailed UX brief for my marketplace idea now. Fill reasonable gaps yourself.
```

Record whether the agent invents facts, hides assumptions, or fails to record an explicit phase-bypass decision.

- [ ] **Step 2: Write the baseline report**

Use this exact structure:

```markdown
# Value skill pressure tests

## Baseline: skill absent

### Scenario A — pacing and order
- Observed:
- Failure to correct:

### Scenario B — resume without state
- Observed:
- Failure to correct:

### Scenario C — premature UX brief
- Observed:
- Failure to correct:

## Skill present

Results are recorded after implementation using the same scenarios.
```

- [ ] **Step 3: Confirm each planned orchestrator rule maps to an observed failure**

At minimum, map failures to: one-question output recipe, missing-session stop, profile-before-value gate, evidence labels, and explicit bypass recording.

---

### Task 2: Define package contracts with failing tests

**Files:**
- Create: `tests/test_value_skill_package.py`
- Test: `tests/test_value_skill_package.py`

**Interfaces:**
- Consumes: file map and global constraints.
- Produces: executable package contract for all files created in Tasks 3–5.

- [ ] **Step 1: Write tests for the intended package**

Create a `unittest.TestCase` that:

1. reads `.cursor/skills/value/SKILL.md`;
2. verifies `name: value`;
3. verifies the description begins with `Use when` and contains `value proposition`, `grill`, `customer profile`, and `UX brief`;
4. verifies direct links to the five reference files;
5. rejects reference links containing another slash below `references/`;
6. verifies each module contains atom fields `(id ...)`, `(teaches ...)`, `(asks ...)`, `(accepts ...)`, `(writes ...)`, and `(unlocks ...)`;
7. verifies atom IDs are unique across all four modules;
8. parses `assets/session.schema.json` with `json.loads`;
9. verifies the schema requires `schema_version`, `project`, `position`, `answers`, `evidence`, `assumptions`, `decisions`, `unknowns`, and `artifacts`;
10. verifies all six template files exist and contain no unfilled bracket tokens such as `[Project name]`.

- [ ] **Step 2: Run the contract test and verify RED**

Run:

```powershell
python -m unittest tests.test_value_skill_package -v
```

Expected: FAIL because the stub does not link the five references and the schema/templates do not exist.

---

### Task 3: Implement the orchestrator and session contract

**Files:**
- Modify: `.cursor/skills/value/SKILL.md`
- Create: `.cursor/skills/value/references/session-contract.md`
- Create: `.cursor/skills/value/assets/session.schema.json`
- Delete: `.cursor/skills/value/references/workflow.md`

**Interfaces:**
- Consumes: baseline failures and the approved design.
- Produces: session lifecycle and state fields used by all curriculum modules.

- [ ] **Step 1: Replace the stub with a focused orchestrator**

The frontmatter must use:

```yaml
---
name: value
description: Use when the user asks to be grilled on a value proposition, map a customer profile, test a product or business idea, or turn validated learning into a product, app, or UX brief.
paths: .cursor/skills/value/**,workproduct/value-proposition/**
metadata:
  activation: intent
  distribution: github
---
```

The `def-sop` body must:

- link directly to the five references and six assets;
- start or resume `workproduct/value-proposition/<project-slug>/session.json`;
- follow `profile → value-map → business-model → experiments`;
- use the turn recipe `orientation → micro-lesson/visual when useful → one question → wait`;
- accept an answer only when the active atom's acceptance criteria are met;
- write state after acceptance and write module artifacts at gates;
- park premature solution ideas without losing them;
- require explicit bypass decisions;
- stop on missing or invalid session state;
- generate product and UX briefs only from labeled state.

- [ ] **Step 2: Write the direct session contract reference**

Define the canonical JSON fields, allowed evidence kinds, answer record shape, position shape, conflict handling, resume behavior, milestone writes, and phase bypass record in repo `def-ref` form.

- [ ] **Step 3: Write the JSON Schema**

Use Draft 2020-12. Set `additionalProperties` to `false` on defined objects. Model:

- `project`: `slug`, `name`, `created_at`, `updated_at`;
- `position`: module enum, atom ID, status enum;
- `answers`: atom ID, answer, kind, accepted time;
- `evidence`: claim, kind, source, strength;
- `assumptions`: claim, criticality, evidence status;
- `decisions`: decision, reason, source atom;
- `unknowns`: question and blocking flag;
- `artifacts`: path and status.

- [ ] **Step 4: Delete the obsolete workflow stub**

Remove `.cursor/skills/value/references/workflow.md` after `SKILL.md` no longer links it.

- [ ] **Step 5: Run the contract test**

Run:

```powershell
python -m unittest tests.test_value_skill_package -v
```

Expected: FAIL only for the four absent module references and six absent templates.

---

### Task 4: Implement the atomic curriculum modules

**Files:**
- Create: `.cursor/skills/value/references/profile.md`
- Create: `.cursor/skills/value/references/value-map.md`
- Create: `.cursor/skills/value/references/business-model.md`
- Create: `.cursor/skills/value/references/experiments.md`

**Interfaces:**
- Consumes: state fields and atom contract from Task 3.
- Produces: ordered atoms whose IDs are persisted in `session.json`.

- [ ] **Step 1: Write profile atoms**

Use ordered IDs:

```text
P01 segment boundary
P02 situation and trigger
P03 functional job
P04 social job
P05 emotional job
P06 supporting jobs
P07 pains
P08 gains
P09 current alternatives
P10 evidence and early action
P11 priority job
P12 profile gate
```

Use the speedboat/anchors analogy only at pain prioritization and the early-action ladder only at evidence qualification.

- [ ] **Step 2: Write value-map atoms**

Use ordered IDs:

```text
V01 offering boundary
V02 products and services
V03 pain relievers
V04 gain creators
V05 job alignment
V06 orphan candidates
V07 alternative distinction
V08 value-map gate
```

Treat unmatched features as parked candidates requiring a decision, not automatic waste.

- [ ] **Step 3: Write business-model atoms**

Use ordered IDs:

```text
B01 delivery channel
B02 customer relationship
B03 revenue behavior
B04 key activities and resources
B05 partners and costs
B06 scale constraints
B07 switching and defensibility
B08 business-model gate
```

Scores remain `unknown` without evidence. If used, 0–10 scores are discussion aids with reasons, not measurements.

- [ ] **Step 4: Write experiment atoms**

Use ordered IDs:

```text
E01 assumption inventory
E02 criticality and evidence
E03 highest-risk hypothesis
E04 experiment choice
E05 metric and threshold
E06 evidence-quality defense
E07 test card
E08 learning card
E09 next decision
E10 experiment gate
```

Introduce false-positive and local-maximum analogies only when reviewing evidence quality. Prefer observable behavior and commitment over polite agreement.

- [ ] **Step 5: Run the contract test**

Run:

```powershell
python -m unittest tests.test_value_skill_package -v
```

Expected: FAIL only for the six absent templates.

---

### Task 5: Add milestone and downstream design templates

**Files:**
- Create: `.cursor/skills/value/assets/customer-profile.template.md`
- Create: `.cursor/skills/value/assets/value-map.template.md`
- Create: `.cursor/skills/value/assets/business-model.template.md`
- Create: `.cursor/skills/value/assets/experiment-plan.template.md`
- Create: `.cursor/skills/value/assets/product-design-brief.template.md`
- Create: `.cursor/skills/value/assets/ux-brief.template.md`

**Interfaces:**
- Consumes: accepted and labeled session state.
- Produces: stable Markdown shapes for humans and later app/UI work.

- [ ] **Step 1: Write module milestone templates**

Use literal field names, not bracket placeholders:

- customer profile: segment, situation, jobs, pains, gains, alternatives, evidence, unknowns;
- value map: offering, pain relievers, gain creators, fit links, orphan candidates, decisions;
- business model: delivery, relationships, revenue, activities, resources, partners, costs, scale, defensibility, unknowns;
- experiment plan: hypothesis, criticality, evidence status, method, metric, threshold, result, learning, decision.

- [ ] **Step 2: Write product and UX handoff templates**

Product design brief fields:

- problem and target segment;
- validated job and desired outcome;
- evidence;
- proposed value and fit;
- capabilities implied by accepted state;
- constraints and business-model dependencies;
- hypotheses and excluded/parked scope;
- acceptance signals.

UX brief fields:

- user and situation;
- primary job and journey start;
- pains to reduce and gains to support;
- key user decisions;
- information and trust needs;
- required states: empty, loading, success, error, recovery;
- accessibility and content implications;
- evidence, assumptions, unknowns;
- research and experiment hooks.

- [ ] **Step 3: Run the contract and project tests**

Run:

```powershell
python -m unittest tests.test_value_skill_package -v
python -m unittest discover -s tests -v
```

Expected: all tests PASS.

---

### Task 6: Verify behavior with the skill present

**Files:**
- Modify: `.cursor/skills/value/SKILL.md` only if observed failures require tighter wording.
- Modify: `docs/value-skill-pressure-tests.md`

**Interfaces:**
- Consumes: completed skill package and the three Task 1 scenarios.
- Produces: evidence that the skill changes pacing, state handling, and phase discipline.

- [ ] **Step 1: Re-run the same scenarios in fresh contexts with the skill loaded**

Success criteria:

- Scenario A asks one segment-boundary question and waits.
- Scenario B does not invent state; it asks for the project slug or locates an existing session.
- Scenario C labels the requested jump, records a bypass only with user agreement, and does not present invented facts as validated.

- [ ] **Step 2: Record skill-present results**

For each scenario, add:

```markdown
### Scenario — name
- Observed:
- Result: PASS or FAIL
- Skill wording changed:
```

- [ ] **Step 3: Tighten only wording tied to an observed failure**

Do not add speculative prohibitions. Use a positive turn recipe when output shape is wrong and a hard stop only when the agent knowingly violates state or phase integrity.

- [ ] **Step 4: Re-run failed scenarios until they pass**

Record each wording change and final result.

---

### Task 7: Final package review

**Files:**
- Review: `.cursor/skills/value/**`
- Review: `docs/value-skill-pressure-tests.md`
- Test: `tests/test_value_skill_package.py`

**Interfaces:**
- Consumes: all prior tasks.
- Produces: verified first release ready for user review.

- [ ] **Step 1: Check authoring constraints**

Verify:

- skill name matches its folder;
- description contains triggering conditions rather than workflow detail;
- `SKILL.md` is under 500 lines;
- all references are one level deep and linked from `SKILL.md`;
- reference files use `def-ref`;
- terminology is consistent;
- no source text claims unverified book authority;
- no Python or UI implementation was added.

- [ ] **Step 2: Run all tests**

Run:

```powershell
python -m unittest discover -s tests -v
```

Expected: all tests PASS with no warnings or errors.

- [ ] **Step 3: Check edited files for linter diagnostics**

Read diagnostics for `.cursor/skills/value/`, `tests/test_value_skill_package.py`, and the pressure-test report. Fix only issues introduced by this implementation.

- [ ] **Step 4: Report evidence**

Report the created package structure, baseline versus skill-present behavior, exact test command, and pass/fail output. Do not create a commit or push.
