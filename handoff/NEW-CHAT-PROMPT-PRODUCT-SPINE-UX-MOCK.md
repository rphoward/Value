# Fresh chat — Product-Spine full UX mock (poteto + arenas)

Paste this block to start a new session.

---

## One-line mission

Dogfood the **rewritten `/product-spine` journey guide** end-to-end as a mock human (Maya / ShiftSwap), prove she can reach an **honest INVEST claim + NotebookLM video prompt** without getting lost, and use **`/poteto-mode`** (architect + arenas + interrogate as needed) to find and fix UX gaps — not to invent a fifth coordinator.

**Do not** treat spine as triage-only. **Do not** invent a spine `session.json`. **Do not** skip the claim/NotebookLM exit.

---

## Model lock (non-negotiable this session)

| Role | Allowed models |
|------|----------------|
| All agents, arena runners, architect runners, explorers, synthesizers | **`cursor-grok-4.5-high`** and **`composer-2.5` only** |
| Judge / cross-judge (only when a pick needs an outside vote) | **Opus low** — user intent: broader training, not deep reasoning. Prefer slug **`claude-4.6-opus-low-thinking`** if “opus 4.5 low” is unavailable in the agent model list |

Override `.cursor/rules/pstack-models.mdc` for this session: do **not** spawn `gpt-5.6-sol-high`, fable, or other models. If a playbook defaults elsewhere, re-pass the locked slugs.

---

## Read first (in order)

1. `handoff/PRODUCT-SPINE-UX-MOCK-OPEN.md` — gate contract
2. `handoff/STATE.md` — living snapshot
3. `.cursor/skills/product-spine/SKILL.md` — **guide** (phase, done-enough, claim exit)
4. `.cursor/skills/product-spine/references/path.md` — Maya happy path
5. `.cursor/skills/value/SKILL.md` — clarity leg
6. `.cursor/skills/lean-mvp/SKILL.md` — MVP leg
7. `.cursor/skills/story-generation-prompt/SKILL.md` + `references/tutorial.md` — INVEST + NotebookLM
8. Ship pack (optional): https://github.com/rphoward/Product-Spine (`f23e56b` journey rewrite)

---

## Mock persona (use this unless user renames)

| Field | Value |
|-------|--------|
| Human | **Maya** |
| Project | **ShiftSwap** — weekend vibecode so restaurant servers trade shifts without group-chat chaos |
| Slug | `shiftswap` (shared under `workproduct/value-proposition/` and `workproduct/lean-mvp/`) |
| Success | She can pitch honestly / get a NotebookLM overview prompt without buying a tablet and sketching alone |

Start with **no** sessions for this slug (or delete prior `shiftswap` mock sessions only if the user agrees). Do not use `value-design` as the mock slug.

---

## Required UX walk (blocking)

Play Maya in chat. Operator invokes skills as she would:

1. `/product-spine` — lost at vibecode idea → must land **clarity** → open `/value`
2. Run `/value` far enough that **profile + value-map** are done-enough (accept real answers; one atom per turn; no atom IDs to Maya)
3. `/product-spine` again → **mvp** → open `/lean-mvp`
4. Run `/lean-mvp` to **mvp-scope** done-enough (MS05 may use story assist inside lean)
5. `/product-spine` again → **claim** → spine must **read and follow** `story-generation-prompt` → INVEST sentence + generation / NotebookLM producer paste
6. Record friction in the decision trail whenever Maya would feel lost, double-asked, or dumped

If the walk breaks, **stop and fix the skill contract** (spine first), then resume — do not paper over with tutorial prose alone.

---

## Required workflow — poteto Feature + architect + arena

```
/poteto-mode Feature: product-spine full UX mock — guide Maya from vibecode to NotebookLM claim
```

1. **Todolist first item** — read poteto Principles in full (per poteto-mode SKILL).
2. **Architect (before large skill edits)** — parallel design exploration with locked models only; data shape = journey phases + sibling `session.json`, not a new spine ledger.
3. **Arena (blocking before shipping UX fixes)**  
   - Path: `tools/drafts/product-spine-ux-arena/`  
   - Deliver **2–4 throwaway mocks** of guide turns (spine replies at clarity / mvp / claim), not color tweaks  
   - Record pick: `handoff/decision-trails/product-spine-ux-mock.tsv`
4. **Interrogate** contested guide wording with locked runners; judge only if needed (Opus low).
5. **Dogfood** the winning guide voice on the live Maya walk.
6. **Ship surgical diff** — prefer `.cursor/skills/product-spine/` (+ digest-match `skills/product-spine/`); sync Product-Spine repo if ship surface changes. Sibling edits only if the mock proves a handoff hole.
7. **Verify** — `python -m pytest tests/test_product_spine_skill.py -v` (and sibling package tests if those skills change).
8. **Close gate** — `handoff/PRODUCT-SPINE-UX-MOCK-PASSED.md` with outcome, arena pick, walk evidence, test output.

---

## Hard constraints

- Spine **carries** the journey; siblings **own** grilling and `session.json`.
- Spine may run `status.py` **read-only**; never init/accept/import from spine.
- Claim phase: pitch / video / NotebookLM / INVEST → follow story skill **in that turn**.
- No commits unless user asks.
- No new Cursor agent as coordinator unless the arena proves a skill guide cannot work (ask user before that fork).

---

## Success looks like

- Maya reaches claim artifacts without orphan “which skill?” loops.
- Decision trail shows arena pick + why losers failed the lost-human test.
- Contract tests green; handoff CLOSED with PASS (or FAIL with one blocker).
