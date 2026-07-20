# Fresh chat — Value gate presentation (poteto arena)

Paste this block to start a new session. Goal: **hunt multiple options**, run **poteto-mode arena**, use **pstack / judges / canvas** as needed, then ship one surgical presentation fix.

---

## One-line mission

The Value Design session has a coherent value-map **hypothesis** but **gate presentation failed** (text wall + monolithic Mermaid = unusable). Your job is to **exhaust the design space** — minimum **three distinct options** — pick a winner with evidence, dogfood on the live session, then update the skill package.

**Do not** ship the first idea. **Do not** dump the whole map at gate review again.

---

## Read first (in order)

1. `handoff/VALUE-GATE-PRESENTATION-OPEN.md` — gate contract
2. `handoff/STATE.md` — living snapshot
3. `workproduct/value-proposition/value-design/session.json` — canonical state (V08 reopened)
4. `workproduct/value-proposition/value-design/value-trail.md` — content spine (not a map UI)
5. `.cursor/skills/value/SKILL.md` — `progress-strip`, gate, `cognitive_murder`
6. `.cursor/skills/value/references/export-lenses.md` — no gate lens today (gap)

---

## What we already know (do not re-interview)

| Area | Status |
|------|--------|
| Profile | Passed (P12) — Discord friends, autonomy→competence→outward value |
| Value map content | V01–V07 accepted — four offering parts, weak indirect fit, no orphans |
| Gate | **Reopened** — presentation failure recorded as fact + product decision |
| Blocking unknown | What format works: progressive stickies, split views, ad-lib-first, canvas, gate lens? |

User quote to honor: gate text was **not understandable**; Mermaid **could not show the whole picture** — **valueless information**.

---

## Required workflow — poteto Feature + arena

```
/poteto-mode Feature: value-map gate presentation for Values skill
```

1. **Name the consumer** — operator at V08 gate review (resume / where-am-I / after module gate), not every turn.
2. **Hunt ≥3 options** — different information architecture, not color tweaks. Seed ideas:
   - Three-beat disclosure (who → box → one link)
   - Split stickies + part×pain/gain matrix (cell = weak / conditional / direct only)
   - Ad-lib pitch first (V08 `ad-lib-formula`), diagram optional second
   - New **Gate_Review_Lens** in `export-lenses.md` + thin template artifact
   - Canvas for spatial/pannable full map (chat stays progressive)
   - Section strip + drill-down on demand only
3. **Arena (blocking before skill edits)**  
   - Path: `tools/drafts/value-gate-arena/`  
   - Deliver **2–4 throwaway mocks** (static MD, HTML, or sample agent turns)  
   - Record pick in `handoff/decision-trails/value-gate-presentation.tsv` (create if missing)
4. **Parallel perspectives** — use what fits:
   - **poteto-agent** — explore/mock branches
   - **pstack how** — progressive disclosure patterns before editing skill
   - **Arena runners** (pstack-models): `composer-2.5`, `cursor-grok-4.5-high`, `gpt-5.6-sol-high`
   - **Cross-judge pool** on finalists: discriminate / pair-judge / quality-judge vs `cognitive_murder` + user failure criteria
   - **canvas** skill — only if spatial option is a finalist
5. **Dogfood** — demonstrate chosen format on `value-design` session content (no invented profile facts).
6. **Ship surgical diff** — skill `progress-strip` / gate / export-lens + tests in `tests/test_value_skill_package.py` if contracts change.
7. **Close gate** — `handoff/VALUE-GATE-PRESENTATION-PASSED.md` with outcome, arena pick, test command output.

---

## Hard constraints

- One primary question per turn during **interview**; gate review may be **progressive**, never a wall.
- Never quote `Ledger:`, atom IDs, or `--operator` telemetry to the user.
- `fit_check_rules` in KB sounds stricter than session honesty — presentation must not fake tight links.
- Mirror ship tree: `.cursor/skills/value/` and `skills/value/`.
- No commits unless user asks.

---

## Success looks like

A fresh operator at value-map gate can answer **“does this map pass?”** using the new format in **under two minutes** without scrolling a novel or squinting at an unreadable diagram.

---

## Suggested opening message to the model

> Read `handoff/NEW-CHAT-PROMPT-VALUE-GATE-PRESENTATION.md` and `handoff/VALUE-GATE-PRESENTATION-OPEN.md`. Run poteto-mode Feature: propose at least three distinct gate-presentation strategies, build throwaway arena mocks under `tools/drafts/value-gate-arena/`, cross-judge finalists, then recommend one for dogfood on `workproduct/value-proposition/value-design/`. Do not edit the skill until arena pick is recorded.
