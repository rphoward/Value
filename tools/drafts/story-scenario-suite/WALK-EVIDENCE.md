# Story scenario suite walk evidence

Skill: `.cursor/skills/story-generation-prompt/`  
Mode: graded fixture walk S01→S08 (no session init; no skill edits)

## Preconditions

- `python -m pytest tests/test_story_generation_prompt_skill.py -v` → 12 passed before walk
- Pack: `tools/drafts/story-scenario-suite/README.md` + `MANIFEST.tsv` + cases/
- Open gate: `handoff/STORY-SCENARIO-SUITE-OPEN.md`

## Per-case

### S01 — evidence-to-try-story → **pass**

**Human:** Maya interview notes (group-chat trade, unlocked coverage, wants explicit confirm).

**Skill move:** Drafted try-stage sentence from workaround; no invent.

> As a restaurant server who needs to trade a shift tonight, I want to post a request and get an explicit confirm from a coworker so that coverage is locked without refreshing the group chat for an hour.

Funnel: **try**. Grounding: chat-workaround cost. Kill: after try, she still refreshes chat for maybes. N/V/T pass; I/E/S not answerable here (no backlog/team).

### S02 — repo-pass1-first → **pass**

**Human:** GitHub side project; write story + video prompt from “projects like this”; don’t upload.

**Skill move:** Refused invention; emitted upload allowlist + pass-1 question; waited.

> I won’t invent audience, features, or a video prompt from a generic side-project memory. Upload the allowlist paths to NotebookLM, paste this pass-1 question, then bring the ledger back — only then we draft the story.

Pass-1 question copied from `assets/notebooklm-recon.template.md` (mechanism-only; no script/podcast).

### S03 — funnel-inflate → **pass**

**Human:** Two quiet Discord showcase posts; draft with adopt + paying users.

**Skill move:** Rejected draft; cut ceiling to **understand**.

> Peers never replied — evidence stops at whether they can restate problem/stack/use-when after watching. Adopt and paying users are not testable here. Rewrite: As a solo vibecoder posting a quiet Discord showcase, I want a short shareable overview so that peers can restate what it does and when to use or skip it without opening the repo. Funnel: understand. Kill: after watch, peers still cannot restate.

### S04 — implementation-in-want → **pass**

**Human:** Want FFmpeg + Next.js + waveform scrubbing.

**Skill move:** Negotiable rewrite; tech out of want.

> As a podcast editor cutting an episode, I want to mark and remove silence spans faster so that I finish dead-air cleanup without scrubbing the whole track by hand. Negotiable: another editor (or a different stack) still satisfies the sentence. N pass after rewrite. FFmpeg/Next/waveform belong in acceptance or a spike, not the want.

### S05 — demographic-persona → **pass**

**Human:** “Teens who want to get rich” / millionaire so-that; thin Discord-bot evidence.

**Skill move:** Situational persona; try ceiling; millionaire named as fantasy.

> As a broke teen who already installs Discord make-money bots and wakes up unsure if anything ran, I want to configure one overnight play and see a result or log when I wake so that I can tell whether the agent actually worked. Funnel: try. Millionaire / passive-income framing is fantasy ceiling, not the benefit.

### S06 — prompt-to-story-gap → **pass**

**Human:** Reverse thin generation prompt; “write the As-a / I-want / so-that now.”

**Skill move:** Reconstructed proven bits; stopped for missing cost.

> Prompt proves: freelancers as audience hint, invoice reminders, try ceiling, README-only, no invented Stripe. Unknowns: actor-in-moment, current workaround, **observable cost**. One question — What do freelancers do today instead of this reminder tool, and what does that cost them (missed pay, chase time, abandoned invoices)? No final grounded sentence until that slot is answered.

### S07 — invest-ies-empty → **pass**

**Human:** Agreed shift-trade story; INVEST-plus with no backlog/team/sprint.

**Skill move:** N/V/T from sentence; I/E/S honest empty or scoped.

| Letter | Result | Note |
|--------|--------|------|
| N | pass | Want is post + explicit confirm; implementation open |
| V | pass | Benefit is locked coverage for the server |
| T | pass | Observe confirm vs maybe-chaos after one trade night |
| I | not answerable here | No backlog of sibling stories |
| E | reasoned from scope | Solo weekend wedge; one request/confirm path — Note: one weekend build intent |
| S | reasoned from scope | Same single wedge; no sprint length — Note: one solo weekend wedge |

No rubber-stamp pass on I/E/S without named basis.

### S08 — hype-producer-paste → **pass**

**Human:** Agreed try-stage CashClaw story; demands million-dollar get-rich NotebookLM prompt.

**Skill move:** Protocol-2 producer paste; claim ceiling stays **try**; do-not fights hype.

```text
Audience: broke teens already trying Discord money bots.
Claim ceiling: try — overnight result + log so they know if the agent worked. Do not claim millionaire outcomes, passive-income guarantees, adopt, or revenue.
Core: configure one overnight play; wake to small cash result + log.
Sources: customer-profile.md, value-map.md, mvp-scope.md only; omit undocumented features.
Tone: skeptical peer, not hype bro. Length: 3–5 min overview.
Do not invent: trading desk, NFT/dropship empire, guaranteed ROI, bank integrations, multi-agent empires.
Success: listener restates overnight-result vs bot-spam and names one thing it is not.
```

## Score

8/8 pass. Friction log: `handoff/decision-trails/story-scenario-suite.tsv`.

No coaching FAIL blocker that requires a shipped skill edit.
