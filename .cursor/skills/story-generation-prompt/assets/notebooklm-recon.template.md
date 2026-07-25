# NotebookLM reconnaissance (pass 1)

Run this **before** the skill writes the story sentence or the producer prompt. NotebookLM holds the repo as **sources**; this pass builds a **mechanism ledger**, not a showcase script and not marketing copy.

Ask a codebase only what a codebase knows. Most repositories are written by coders for themselves: they explain what to install and how to run it, and they say nothing about audience, positioning, or when someone should skip the tool. Asking the sources those questions returns "not in sources" on every row that matters. So pass 1 collects mechanism, and the skill derives positioning afterwards using `references/positioning-inference.md`.

## Upload allowlist

Prefer high-signal paths over the whole tree:

- README, AGENTS.md, install and setup docs
- Entry points, CLI definitions, and config schemas
- `hooks/`, `skills/`, rule autoloads (`.mdc`), example configs
- A few representative test names, when tests describe real failures

Skip secrets, build artifacts, lockfiles, and large binaries.

## Pass 1 — paste this question in NotebookLM

```text
These sources are a codebase, not marketing material. Report only what the sources show, and cite the exact filename on every line.

1. What the project does, in mechanism terms — the main things it actually performs.
2. Install and run steps, including any required runtime, editor, platform, or account.
3. Entry points and surfaces — commands, scripts, config keys, hook points, integration points.
4. Named subsystems and what each one does. List them separately; do not merge them.
5. Defaults, strict modes, and refusals — anything the project enforces or will not do.
6. Explicit claims the README or docs make about purpose or benefit. Quote them and mark them as author claims.
7. Any test or fixture names that describe a specific failure the project guards against.

Then, as a separate short list, name what the sources do NOT state: audience, positioning, when to use, when to skip, or comparisons to alternatives. Write "not in sources" for each missing item — this is expected for a codebase and is not a defect.

Do not infer audience or benefit. Do not merge subsystems for a cleaner story. Do not write a script, dialogue, or promotional copy.
```

Copy the whole answer, including the "not in sources" list. The absences tell the skill which rows it has to derive rather than quote.

## Bring it back to story-generation-prompt

Paste the answer into **Source fact ledger** on `assets/evidence-intake.template.md`, or paste it in chat when you invoke the skill.

The skill then:

1. Derives problem, audience, when to use, when to skip, and the must-have core from that mechanism, labeling each line **fact**, **inference**, **hypothesis**, or **unknown** per `references/positioning-inference.md`.
2. Shows you that table once. Confirm or correct the rows the sentence needs now; the rest get settled properly back in the lean-mvp session, not here.
3. Asks for the observation the repo cannot supply — the actor, the moment, what they do instead today, and what it costs them.
4. Emits the **one user story sentence**, the **generation prompt**, and the **Producer paste block**.

## Pass 2 — after the skill output

Keep the same sources attached. Paste only the **Producer paste block** as custom instructions or your first message. Confirmed inference may appear in the overview because you are its source; unconfirmed inference may not.

Do not ask for a dual-host podcast in pass 2 until the accuracy pass in `references/source-fidelity.md` passes.

## Forbidden in pass 1

- "Write a video script" or "AI code audit podcast"
- Asking the sources to name an audience or a benefit they never state
- Any request that prioritizes entertainment over the mechanism ledger
