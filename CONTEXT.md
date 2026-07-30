# Value skill pack

Shared language for turning a vibecoded idea into something others value — through clarity, business model, lean MVP scope, and an honest claim. Prefer these terms in docs, skills, and guide-turns.

## Language

### Path and entry

**Skill**:
A slash command and coaching pack the agent loads on request.
_Avoid_: plugin, bot, workflow file

**Slash**:
How a human opens a skill in Cursor (for example `/value` or `/product-spine`).
_Avoid_: invoke path, load SKILL.md

**Slug**:
Short folder name for one project, reused across every skill that touches that idea.
_Avoid_: project id, repo name (unless they intentionally match)

**Ship repo**:
Minimal GitHub install surface for `npx skills add` (Values, BMG, MVP, Product-Spine).
_Avoid_: monorepo, Value (the development repo)

**Monorepo**:
The Value development repo where skills are authored and mirrored under `skills/<name>/`.
_Avoid_: ship repo

### Session and progress

**Session**:
Saved progress for one skill under `workproduct/…/<slug>/session.json`.
_Avoid_: chat history, conversation

**Workproduct**:
On-disk session and milestone notes for skills; not product source code.
_Avoid_: output, build artifacts

**Atom**:
One coaching question in a skill. The human answers; the skill moves on.
_Avoid_: ticket, prompt, quiz item

**Module**:
A named block of atoms that ends in a gate (for example profile, value-map, canvas-mapper, mvp-scope).
_Avoid_: chapter, sprint

**Gate**:
Check at the end of a module. Pass it or bypass it on purpose before the next module.
_Avoid_: checkpoint (unless speaking casually), merge gate

**Bypass**:
An explicit decision to leave a module unfinished and move on; not silent skipping.
_Avoid_: skip (alone), ignore

**Milestone**:
Written notes the skill saves when a gate passes (for example `value-map.md` or `canvas-mapper.md`).
_Avoid_: artifact dump, export only

**Done enough**:
The finish line for a phase so the human can return to Product-Spine (or stop).
_Avoid_: complete, 100%, done forever

### Product-Spine journey

**Phase**:
Where Product-Spine says the human is on the path: clarity, business, mvp, or claim.
_Avoid_: stage, step (when you mean phase)

**Sibling**:
A grilling skill Product-Spine points into. Spine routes; siblings grill.
_Avoid_: child skill, subagent

**Guide-turn**:
Product-Spine’s fixed reply shape: where you are, why this phase, what to open this turn, when to come back.
_Avoid_: status dump, briefing

**Come back when**:
Return cue on a guide-turn: finish that leg’s done enough (or get lost), then invoke `/product-spine` again.
_Avoid_: callback, re-entry hook (in human-facing prose)

**Clarity**:
Phase for “who is this for, and why would they care?” Owned by Values (`/value`).
_Avoid_: discovery (alone), research phase

**Business**:
Phase for a classic Business Model Canvas and related Osterwalder work. Owned by BMG (`/bmg`).
_Avoid_: monetization phase, Strategyzer grilling (that is BMG’s job, not the phase name)

**MVP**:
Phase for a lean, shippable feature cut. Owned by lean-mvp (`/lean-mvp`).
_Avoid_: prototype phase (UX prototype is later inside lean-mvp), minimum product (vague)

**Claim**:
Phase for an honest pitch and optional NotebookLM video prompt. Product-Spine runs it with saved notes.
_Avoid_: marketing phase, launch (alone)

### Kinds of value

**Clarity value**:
Outward answer to who cares and why — profile, value map, north-star blurb.
_Avoid_: ICP doc (alone), persona pack

**Business value**:
How the model holds together — nine-block canvas, then optional patterns, strategy, ambidexterity.
_Avoid_: financial model (alone), pitch deck

**MVP value**:
The smallest useful ship that can learn in the market — underserved needs through mvp-scope.
_Avoid_: roadmap, backlog

**Claim value**:
Something honest you can share — INVEST-style story and optional NotebookLM paste.
_Avoid_: hype copy, feature list

### Roles of the skills

**Product-Spine**:
The guide skill that names phase, sibling slash, and come-back-when. It does not grill canvas or lean atoms.
_Avoid_: orchestrator (in human prose), router bot

**Values**:
The clarity grilling skill (`/value`); session under `workproduct/value-proposition/<slug>/`.
_Avoid_: Value (repo name) when you mean the skill

**BMG**:
The business grilling skill (`/bmg`) for classic Business Model Generation; session under `workproduct/bmg/<slug>/`.
_Avoid_: canvas tool, Osterwalder app

**lean-mvp**:
The MVP grilling skill (`/lean-mvp`) for Dan Olsen’s lean playbook; session under `workproduct/lean-mvp/<slug>/`.
_Avoid_: MVP (repo) when you mean the skill slash; lean canvas (different tool)

**Story**:
The claim drafting skill (`story-generation-prompt`) for INVEST-plus story and NotebookLM generation prompts. On claim, Product-Spine follows it with notes already on disk.
_Avoid_: copywriter, blog generator
