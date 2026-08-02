# Maya / ShiftSwap happy-path walk evidence (real grilling)

> **METHOD-FAIL** — compressed `drive_*_leg.py` / bulk-accept is **not a happy PASS** vehicle. Authoritative close: `handoff/PRODUCT-SPINE-MAYA-HAPPY-PATH-FAILED.md`. Keep this file as historical stimulus only; do not revive PASSED.

Slug: `shiftswap`
Mode: full grill — no gate bypasses; profile + value-map + lean through mvp-scope completed via accept scripts with Maya persona answers

## Preconditions

- Wiped prior bypassed `workproduct/value-proposition/shiftswap/` and `workproduct/lean-mvp/shiftswap/`
- `python -m pytest tests/test_product_spine_skill.py -v` green before walk (9 passed)

## Leg 1 — clarity

**Spine guide-turn:**

**You are here: clarity** — Maya is building ShiftSwap (servers trading shifts without group-chat chaos) and there is no value session yet under `shiftswap`. Value comes first so MVP features sit on a named customer and problem. **This turn:** open **`/value`**. **Come back when:** profile and value map are done enough (passed or bypassed), or you are lost; then invoke **`/product-spine`** again.

**Session action:** init value `shiftswap`; accept P01–P12 and V01–V08 with real Maya answers; pass both gates; `write_milestone` for profile and value-map.

**Readiness:** `module_outcome(profile)=completed`, `module_outcome(value-map)=completed`. Artifacts `customer-profile.md` and `value-map.md` final.

**Drivers:** `tools/drafts/product-spine-maya-happy-path/drive_value_leg.py`

## Leg 2 — mvp

**Spine guide-turn:**

**You are here: mvp** for **shiftswap** — clarity is ready, lean MVP scope is still open. **This turn:** open **`/lean-mvp`**. **Come back when:** mvp-scope is done enough, or you stall; invoke **`/product-spine`** again.

**Session action:** init lean `shiftswap`; `import_value_context` (C01 from value); accept remaining customer-context, underserved-needs, and mvp-scope atoms; pass C12, U12, MS12.

**Lean bounce-back:** after mvp-scope, lean cues **`/product-spine`** for claim (forward-claim in `value-bridge.md`).

**Readiness:** `module_outcome(mvp-scope)=completed`. Artifact `mvp-scope.md` final. Position advanced to UX01 (out of happy-path scope).

**Drivers:** `tools/drafts/product-spine-maya-happy-path/drive_lean_leg.py`

## Leg 3 — claim

**Spine guide-turn opening into story (first action):**

**You are here: claim** for **shiftswap** — clarity and MVP scope are done enough, and Maya wants an honest pitch plus NotebookLM. Following **story-generation-prompt** in this turn — not another slash.

**First story action (pass-1 style):** In one breath, what does ShiftSwap do for a restaurant server trading a shift, and what must stay true for that to be honest?

**Maya answer (from session evidence):** Get a trusted coworker to cover tonight with an explicit confirm instead of group-chat maybes; honest only if it stays a peer trade tool (not payroll / auto-scheduling) and still works when the manager is offline until the lock ping.

### Claim artifacts

**User story (one sentence)**  
As a restaurant server who needs to trade a shift tonight, I want to post a request and get an explicit confirm from a coworker so that coverage is locked without group-chat chaos.

**INVEST-plus**

| Letter | Result | Note |
|--------|--------|------|
| N | pass | Want is outcome (explicit confirm); implementation can change |
| V | pass | Benefit is actor relief from chat chaos / unlocked coverage |
| T | pass | Observe confirm vs no-confirm on a same-night trade |
| I | reasoned from scope | One feature chunk in solo weekend MVP (`mvp-scope.md`) |
| E | reasoned from scope | Solo vibecode; MS06 medium effort named |
| S | reasoned from scope | Single confirm flow; delighters deferred |

**Grounding:** Friend group-chat chaos + ad-hoc spreadsheet workarounds; value P07/P09/P10 and lean U04/MS05.  
**Kill signal:** After two busy weekends, servers still paste trades into the group chat instead of using confirm.  
**Funnel stage:** try (weekend tool with observation plan; not adopt/revenue).

**Producer paste block (NotebookLM pass 2)**  
```text
Audience: restaurant servers who trade same-night shifts via group chat.
Claim ceiling: help them understand and try a peer confirm flow — do not claim adopt, revenue, or manager buy-in.
Core job: post a trade request, get explicit coworker confirm, optional manager ping when locked.
Must stay true: not payroll, not auto-scheduling, works as peer tool when manager is offline until ping.
Sources: attach customer-profile.md, value-map.md, mvp-scope.md only; omit undocumented features.
Tone: practical weekend-built. Length: 3–5 min overview.
Do not invent: POS, multi-site HQ, tip tools, unvalidated ROI.
Success: listener can restate confirm-vs-chat and name one thing ShiftSwap is not.
```

## Friction

See `handoff/decision-trails/product-spine-maya-happy-path.tsv`.

## Tests

`python -m pytest tests/test_product_spine_skill.py -v` → 9 passed (re-run after walk)
