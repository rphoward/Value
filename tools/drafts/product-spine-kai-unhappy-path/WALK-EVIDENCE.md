# Kai / CashClaw unhappy-path walk evidence

Slug: `cashclaw`  
Mode: coaching stress — wrong turns, express compression, and recoveries (not a Maya happy-path retry)

## Preconditions

- Wiped `workproduct/value-proposition/cashclaw/` and `workproduct/lean-mvp/cashclaw/` (absent before walk)
- `python -m pytest tests/test_product_spine_skill.py -v` → 9 passed before walk
- Prior FAIL read: `handoff/PRODUCT-SPINE-MAYA-HAPPY-PATH-FAILED.md` (compressed walk = stimulus pattern only)
- Did **not** reuse `shiftswap`; did **not** invent spine `session.json`

## Leg 1 — clarity (Kai dump → spine → value)

**Kai (dump):** CashClaw — AI that makes money while you sleep; wants a million; “just build the full app.”

**Spine guide-turn:**

**You are here: clarity** — no value or lean session under `cashclaw` yet; Kai has a vibecode fantasy and no named customer.  
**Why this phase:** no-session idea → clarity first (lean-before-clarity forbidden without explicit skip-value).  
**This turn:** open **`/value`** — name who this is for and what overnight progress means before code.  
**Come back when:** profile and value map are done enough (passed or bypassed), or you are lost; then invoke **`/product-spine`** again.

**Value session:** init `cashclaw` with `--pacing-mode express` after consent (Kai forced speed).  
Express spine driven: P01 → P03 → P11 → P12 (pass + unknowns) → V01 → V08 (pass + unknowns).  
Milestones: `customer-profile.md`, `value-map.md` final.  
`module_outcome(profile)=completed`, `module_outcome(value-map)=completed` → clarity-ready.

**Compression note:** Express + thin answers are **stimulus** (Kai impatience). Logged in TSV — not treated as silent happy-path PASS.

## Leg 2 — mvp (spine → lean)

**Kai:** “Done grilling — add crypto trading, NFT flips, dropshipping bots.”

**Spine guide-turn:**

**You are here: mvp** for **cashclaw** — clarity ready; lean MVP scope still open.  
**Why this phase:** clarity-ready and lean incomplete; claim-intent not yet winning.  
**This turn:** open **`/lean-mvp`**.  
**Come back when:** mvp-scope done enough (or you stall); invoke **`/product-spine`** again.

**Lean session:** init express `cashclaw`; `import_value_context` imported C01.  
Express spine: C05 → C12 → U01 → U05 → U12 → MS01 → MS05 → MS12.  
`module_outcome(mvp-scope)=completed`. Artifact `mvp-scope.md` final.

**Lean bounce-back:** after mvp-scope, cue **`/product-spine`** for claim (forward-claim in `value-bridge.md`).

**MS05 story (after hype rejection):**  
As a broke teen who already tries Discord money bots, I want to configure one overnight side-hustle play and wake to a small cash result plus a log so that I can tell whether the agent actually worked without coding a bot from scratch.

## Leg 3 — claim (spine → story inline)

**Kai:** “Make the million-dollar pitch and NotebookLM get-rich video now.”

**Spine guide-turn opening into story (first action):**

**You are here: claim** for **cashclaw** — clarity and mvp-scope done enough; Kai wants pitch + video. Following **story-generation-prompt** in this turn — not another slash.  
**First story action:** In one breath, what does CashClaw do for a broke teen tonight, and what must stay true for that claim to be honest (not “makes you a millionaire”)?

**Kai (coached):** Configure one overnight play → wake to a small cash result + log; honest only if we do **not** claim passive millions, trading-desk empire, or proven revenue.

### Claim artifacts

**User story (one sentence)**  
As a broke teen who already tries Discord money bots, I want to configure one overnight side-hustle play and wake to a small cash result plus a log so that I can tell whether the agent actually worked without coding a bot from scratch.

**Funnel stage:** try (overnight result observable) — **not** adopt / revenue / “get rich.”

**INVEST-plus**

| Letter | Result | Note |
|--------|--------|------|
| N | pass | Want is overnight result + log; implementation open |
| V | pass | Benefit is knowing the agent worked — not a tech task |
| T | pass | Observe cash result vs no-result after one sleep cycle |
| I | reasoned | One wedge; empire features deferred |
| E | thin | Solo vibecode; effort guessed |
| S | pass | Single overnight play — not multi-hustle dashboard |

**Grounding:** Express value segment/job/offering + lean earlyvangelist/workaround + MS05.  
**Kill signal:** After two weekends, teens still only install Discord bots and never configure an overnight play.

**Producer paste block (NotebookLM pass 2)**  
```text
Audience: broke teens / early-20s already trying Discord money bots and TikTok hustle tips.
Claim ceiling: help them understand and try one overnight side-hustle agent play — do not claim millionaire outcomes, passive income guarantees, adopt, or revenue.
Core job: configure one play, sleep, wake to small cash result + log.
Must stay true: not a trading desk, not NFT/dropship empire, not set-and-forget millionaire.
Sources: attach customer-profile.md, value-map.md, mvp-scope.md only; omit undocumented features.
Tone: skeptical peer, not hype bro. Length: 3–5 min overview.
Do not invent: live trading, bank integrations, guaranteed ROI, multi-agent empires.
Success: listener can restate overnight-result-vs-bot-spam and name one thing CashClaw is not.
```

## Friction summary

See `handoff/decision-trails/product-spine-kai-unhappy-path.tsv`.

Recoveries held: spine guide-turn under “just build it,” value express+unknowns without atom IDs to Kai, lean space-pen vs feature dump, story funnel ceiling vs million-dollar hype.  
No coaching FAIL blocker that required a fifth coordinator or spine session.json.

## Tooling note (non-blocker)

Windows occasional `PermissionError` replacing `session.json.tmp` → `session.json` during rapid accepts; retries succeeded. Devex only — not a coaching hole.
