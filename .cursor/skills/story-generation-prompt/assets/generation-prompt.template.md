# Generation prompt

> Paste into NotebookLM, slide/video overview tool, or another generator. Edit the brief block; keep story fidelity.

## Context for the producer

- **Audience:** (from persona)
- **Funnel goal:** (post | seen | understand | try | adopt — one)
- **Claim ceiling:** (the funnel goal above; the copy may promise that stage and nothing past it)
- **Success signal:** (from test hook)

## Source material

- Repo / docs / links the operator will attach:
- 
- **Allowlist (paths the producer may cite):** (operator lists globs or files — hooks/, README, AGENTS.md, etc.)

## Source fidelity

- **Fact ledger:** Only state facts present in Source material above. If a detail is missing, omit it or say "not documented in sources" — never invent it to hold the narrative together.
- **Accuracy pass:** Before final output, list each named file, command, hook, or subsystem with the source path that supports it; delete unsupported lines from the script.
- **Format risk:** Dual-host debate and "code audit podcast" formats tend to hallucinate bridges — prefer single narrator or problem-first sections until fidelity passes.

## Brief (generation instructions)

(Operator brief — use verbatim when supplied.)

## Output format

- Length:
- Medium: (video overview | slides + voice | written summary)
- Must include:
- Must include when relevant: when **not** to use this
- Tone:

## Do not

- Say anything above the claim ceiling. Write the ceiling out here as a sentence, so the producer sees the line: for an **understand** ceiling, do not say peers will try it, adopt it, or ship faster because of it.
- Claim adoption or revenue outcomes the story does not promise.
- Invent features not in the story outcome.
- State facts not supported by Source material — see Source fidelity above.

## Producer paste block (compact)

Short instructions for NotebookLM pass 2 or a small instruction box. Sources stay attached separately; do not paste the repo body here.

```text
(≤120 words: claim ceiling, section order, fidelity rules, tone, success signal — operator fills from sections above)
```
