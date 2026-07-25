# Tutorial: from repo to one honest sentence

This walkthrough lives in `.cursor/skills/story-generation-prompt/`. Every path it mentions is a file in that folder unless noted otherwise.

## What you are building

You need two things you can paste elsewhere: a **single user story sentence** (the bet you are making) and a **short producer prompt** (instructions for NotebookLM or another tool). The sentence says who you are helping and what success looks like. The producer prompt says how to generate an overview without promising more than you can test and without stating facts nobody can trace.

If you already have interview notes or tickets instead of a repository, skip ahead to [When you are not using NotebookLM](#when-you-are-not-using-notebooklm). The same skill still applies; only the first step changes.

## The NotebookLM path (start here)

Most showcase work begins in a repository. NotebookLM can read the docs you upload, but its instruction box stays small. For that reason the workflow runs in two passes. Pass 1 pulls **mechanism** out of the repo. The skill derives positioning from that mechanism, adds your real-world observation, and writes the **lead sentence**. Pass 2 uses the same uploaded sources and a **compact paste block** the skill writes for you.

One thing to expect before you start: your repositories are codebases, not marketing material. A README written by a coder says what to install and how to run it, and it says nothing about who the tool is for or when somebody should skip it. That is normal, and the workflow is built around it. Pass 1 does not ask the sources those questions, because the honest answer would be "not in sources" on every row you actually need.

### Step 1. Upload sources

Create a notebook and upload an allowlisted slice of the project, not necessarily every file. Good candidates include the README, AGENTS.md, install instructions, entry points and config schemas, `hooks/`, `skills/`, rule files such as `.mdc` autoloads, and a few test names where the tests describe real failures. Omit secrets, build output, lockfiles, and large binaries.

The full allowlist and the reasoning behind it sit in `assets/notebooklm-recon.template.md`.

### Step 2. Ask pass 1 (mechanism ledger, not a script)

The exact question lives in `assets/notebooklm-recon.template.md` under **Pass 1**. Copy it from there rather than from memory, and paste it into NotebookLM as your first message.

It asks for seven things a codebase can honestly answer: what the project does mechanically, install and run steps, entry points and surfaces, named subsystems kept separate, defaults and refusals, README claims quoted as *author claims* rather than proven benefits, and test names that describe a specific failure. Then it asks NotebookLM to list what the sources never state — audience, positioning, when to use, when to skip — and to write "not in sources" for each.

Copy the whole answer including that list of absences. The gaps are useful: they tell the skill which rows it has to derive rather than quote.

### Step 3. Invoke the skill and get your lead sentence

Open `assets/evidence-intake.template.md` and paste the NotebookLM answer into **Source fact ledger**. If you also have showcase evidence — for example, peers watched a draft video and still could not say what the project was for — add it under **Actor and moment**, **What they do instead today**, and **Observable cost**. The ledger supplies mechanism; your observation supplies the moment and the cost of the status quo. Neither one can substitute for the other.

Invoke `/story-generation-prompt` and paste the intake, or paste the ledger in chat with a line such as: “Draft the story from this NotebookLM recon.”

The skill first shows you a **positioning table**. It derives the rows you need — problem, audience, when to use, when to skip, must-have core, and the workaround this project displaces — from the mechanism in the ledger, using the derivation moves in `references/positioning-inference.md`. Install preconditions point at the audience. Opinionated defaults are the author asserting the old way was a problem. When-to-skip is usually the shadow of what the code requires, since nobody writes it down.

Every line says how sure it is — **fact**, **inference**, **hypothesis**, or **unknown** — and what mechanism it rests on. Confirm or correct the rows your sentence needs now, and leave the rest; the lean-mvp session comes back to who this is for, which problem leads, and what counts as table stakes, and a row left for later simply stays out of the producer prompt. Your wording always beats the derived wording, because you know the market and the code only knows itself.

Then the skill returns, in order:

1. **One sentence** in the form *As a … I want … so that …*
2. A filled **generation prompt** (audience, claim ceiling, source fidelity, brief)
3. A **Producer paste block** — short text meant only for NotebookLM pass 2

Read the sentence before you run pass 2. If the benefit sounds bigger than what you can test — “peers will adopt” when all you can observe is whether they **understand** — send it back for a tighter `so that` clause.

### Step 4. NotebookLM pass 2 (overview under the ceiling)

Leave the same sources attached. Paste **only** the Producer paste block into custom instructions or as your first message. Do not paste the whole repo into the instruction box again.

Pass 2 is amplification: tone, order of sections, and length. Pass 1 plus the skill already fixed **what you may claim** and **what may be stated as fact**. A confirmed positioning row may appear in the overview because you are its source; a row you left for lean-mvp may not. Details on that rule and on risky formats such as dual-host banter are in `references/source-fidelity.md`.

## How the lead sentence is written (inside the skill)

Whether the material came from NotebookLM or from an interview, the skill drafts the sentence **benefit first**. It writes `so that`, then `I want`, then `As a`.

The `so that` clause sets the **funnel ceiling** — the strongest outcome your evidence can actually test:

```text
post → seen → understand → try → adopt
```

A showcase where peers need to explain the project without opening the repo is usually **understand**. It does not, by itself, prove anyone will clone or adopt the tool, so those stages stay out of the sentence.

Example order on the page before the final sentence is assembled:

```text
so that   peers can state the problem, for whom, and when to use or skip
          without opening the repo
I want    a short shareable overview I can post as one link
As a      developer who just finished the project and is opening a showcase channel
```

Then run the **Negotiable test** from `references/drafting-inputs.md`. Swap NotebookLM for slides or a screen recording in your head. If the `I want` clause still makes sense, the outcome is fixed and the tool choice stays open. If the sentence collapses, the tool name was doing the work of the outcome; rewrite `I want` as what changes in the world.

## Story card and INVEST-plus

Fill `assets/story-card.template.md` when you want the full card, not only the sentence. **Grounding** cites where the story came from — ledger rows, positioning rows you confirmed, posts, tickets. **Kill signal** states what result would drop the story, for example three peers still cannot say what the project is for, or a stated fact contradicts the README.

INVEST-plus is split into two tables in `references/invest-plus.md`. **N**, **V**, and **T** can be judged from the sentence. **I**, **E**, and **S** need backlog and team context; without that, the honest mark is `not answerable here`, not `pass`.

## When you are not using NotebookLM

Open `assets/evidence-intake.template.md` and fill **Actor and moment**, **What they do instead today**, and **Observable cost** before any sentence is written. If a slot is empty, ask one question and wait; do not invent an interview.

`references/drafting-inputs.md` ranks evidence types. Observed workarounds rank highest; bare survey scores rank lowest because a number alone has no testable outcome.

Follow the benefit-first drafting section above, then run the skill for the generation prompt and paste block when you are ready to produce an overview in another tool.

## Use at MS05 in lean-mvp

At MS05, lean-mvp asks for one INVEST user story for the top MVP chunk. Run the steps above, then paste the **one sentence** into `accept_answer` yourself.

This skill does not write `session.json`. An agent may read this skill when you ask, but it may not auto-accept the atom. You read the card, you decide, you paste.

After you emit the card or prompt, remind the operator of that paste step. If the claim exposed a customer gap, offer the value skill. If they are lost on which tool is next, they can invoke `/product-spine` to re-triage.

The derived readings work the same way in reverse. Rows you left in step 3 get their real answers inside the session, where the questions arrive one at a time in the middle of the work rather than as a form to fill in. Bring those answers back and they replace the derived wording as confirmed grounding. Nothing here is meant to pre-empt that conversation; it exists so a codebase with no marketing in it can still produce one honest sentence today.

## Release notes and other non-story claims

A release note is not a user story, but it obeys the same funnel ceiling. Name the reader, name the highest stage the change can reach, and cut the claim to that stage. Fill funnel stage and grounding on the card; skip the rest if you do not need a full story.

```text
Draft:   Ship your overview in one click — teams adopt faster.
Wrong:   "Adopt" outruns the evidence; the reader may be a solo poster, not a team.
Held:    Get a short overview a peer can watch before opening the code.
```

## Troubleshooting

- **Benefit too strong.** Rewrite `so that` to match the highest funnel stage your evidence tests (`references/story-elements.md`).
- **Tool named in `I want`.** Run the Negotiable test; rewrite as outcome.
- **"As a user."** Name a moment under pressure, or split poster and peer into two stories.
- **Brief folded into the sentence.** Move tone and must-include lists to the generation prompt **Brief** block.
- **Pass 1 returned a script.** Re-run with the question in `assets/notebooklm-recon.template.md`; pass 1 is recon only.
- **Pass 1 answered "not in sources" for audience and positioning.** That is the expected result for a codebase, not a failure. Step 3 derives those rows from mechanism instead.
- **A positioning row feels wrong.** Correct it in your own words rather than arguing with the derivation; the skill takes operator wording over derived wording.
- **Overview facts wrong.** Use the pass 1 ledger, enforce **Source fidelity** on the generation prompt, and avoid debate-style formats until each claim maps to a source file or a row you confirmed.

## What this skill does not do

It does not run NotebookLM, render video, or write `session.json`. It does not decide whether your evidence is strong enough; it surfaces missing ingredients and asks. Supplying those ingredients remains your job.
