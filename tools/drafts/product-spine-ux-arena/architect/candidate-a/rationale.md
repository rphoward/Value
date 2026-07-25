# Candidate A — Phase-locked guide turn

## Problem

Maya opens `/product-spine` when she is lost, finished a leg, or wants the pitch. The skill already knows phases and siblings, but the **guide-turn contract** is implicit: agents can name `/value` or `/lean-mvp` and stop, confuse status brief with readiness, or treat claim as routing instead of **same-turn story work**. After lean MVP she has no in-skill cue to return. The fix is not more state — it is a **fixed reply shape** and **illegal transitions** spelled in prose so a lazy agent cannot represent “dump at the door” or “claim without story skill.”

## Usage (caller's view)

Maya always gets one short **guide turn** per `/product-spine` invocation — never a curriculum, never atom IDs, never status script pasted back.

1. **First visit, no sessions (ShiftSwap idea only)**  
   She hears: you are in **clarity**; why value comes first; open **`/value`** once; done-enough is profile + value map passed or bypassed; when lost or done, **`/product-spine`** again.

2. **After clarity-ready**  
   She hears: **mvp**; open **`/lean-mvp`** with the same slug; done-enough is mvp-scope passed or bypassed; return via **`/product-spine`**.

3. **After mvp-ready or when she asks for pitch / NotebookLM**  
   She hears: **claim**; spine **does not** send her to a third slash — it says it is following **story-generation-prompt** and **starts** that workflow in this chat (evidence → INVEST → generation prompt / producer paste). She stays in one thread until story work is underway or blocked on missing inputs she can supply.

4. **After learning or kill-signal**  
   She hears: **return-after-learning**; one sibling and one reason; same return cue.

The two-slash tax stays: she still opens `/value` or `/lean-mvp` herself on clarity and mvp legs. The contract makes that step **unmissable** and claim the **exception** where spine stays with her.

## Shape

**Domain model:** a four-state phase machine `{ clarity | mvp | claim | return-after-learning }` derived read-only from sibling `session.json` + `module_outcome` (completed|bypassed) + claim-intent precedence — never from status brief alone.

**Guide-turn envelope (mandatory every activation):**

| Slot | Role |
|------|------|
| You are here | Phase label + slug + one plain sentence of situation |
| Why this phase | Single precedence sentence (no jargon) |
| This turn | clarity/mvp/return: one destination slash + what happens there; **claim: read story skill and execute — forbidden to only name story skill** |
| Come back when | Done-enough for that leg + explicit `/product-spine` re-entry |

**Activation pipeline (unchanged mechanics, stricter output):** read `path.md` → discover slug → optional read-only `status.py` → compute phase → emit envelope → if claim, load story-generation-prompt before closing the turn.

**Illegal states (prose contract — agent must not produce these):**

- End clarity or mvp turn without **This turn** naming exactly one sibling slash and **Come back when**.
- Enter claim without reading and following story-generation-prompt in the **same** turn.
- Enter claim by routing (“open `/story-generation-prompt`”) — claim **is** inline story execution from spine.
- Open lean-mvp when not clarity-ready unless human explicitly skips value and spine states what re-grilling cost that buys.
- Treat active module from status brief as clarity-ready or mvp-ready.
- Init, accept, import, or refresh sibling sessions from spine.
- Grill canvas or lean atoms from spine.

No spine `session.json`. No fifth coordinator. Siblings keep grilling and sessions.

## Tradeoffs accepted

- **Rigid four-slot reply** can feel template-heavy; we accept repetition because lost humans need predictability over variety.
- **Claim stays in spine thread** increases spine turn length and couples spine to story skill churn; we accept that so Maya is not abandoned at the last door.
- **Two-slash tax remains** on clarity/mvp; we do not auto-invoke siblings (explicit human slash preserves skill boundaries).
- **Read-only inference only** — wrong or stale sibling JSON may mis-phase until she returns; re-entry is the recovery mechanism, not spine writes.

## Alternatives considered

| Alternative | Why rejected |
|-------------|----------------|
| Spine `session.json` ledger for “last phase shown” | Fifth store; duplicates sibling truth; violates grounding. |
| Coordinator subagent that owns journey | Same as above — extra orchestration layer. |
| Auto-chain `/value` after spine without user slash | Blurs skill activation; hides grilling ownership. |
| Claim = “open story-generation-prompt” routing only | Reproduces dump-at-door; fails NotebookLM/INVEST success criterion. |
| Long path tutorial in every reply | Agent convenience; overwhelms Maya. |
| Infer readiness from status brief only | Known gap; causes premature mvp/claim. |
| Full lean-mvp rewrite with spine on every module | Huge diff; orphan fix needs one surgical re-entry at leg completion. |

## Open questions and risks

- **Explicit skip-value path:** wording for “I hate canvases, go lean” must stay one clarifying exchange without spine accepting atoms.
- **MS05 story inside lean:** when story work happened under lean, claim turn should reuse artifacts — story skill must say how; spine should not duplicate MS05 logic.
- **Multi-slug repos:** slug disambiguation still blocks guide turn until one question is answered — envelope applies after slug is known.
- **Story skill length:** claim turns may hit context limits; risk mitigated by story skill’s own progressive steps, not spine summarizing it away.
- **Agent laziness:** envelope is only as good as enforcement in SKILL/path; walk harness drift stays draft-only.

## Next implementation step

1. Add **protocol-2-guide-turn** (four mandatory slots + illegal-state list) to `.cursor/skills/product-spine/SKILL.md`; tighten protocol-0 step 6 vs 5 so claim never “names only.”
2. Mirror **guide-turn** + **illegal-states** checks in `references/path.md` `(section voice)` and `(check ...)`.
3. Add **one** lean-mvp re-entry line at mvp-scope done-enough (see `skill-delta.md`).
4. Digest-match ship tree under `skills/product-spine/`.
5. Validate with three Maya mocks (usage-mocks.md) before any sibling expansion.

## Synthesis decision

(filled by parent)
