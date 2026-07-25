# Story scenario suite (draft)

Graded fixtures for `/story-generation-prompt` (and claim exit via `/product-spine`).  
One axis per case. Walk via `handoff/NEW-CHAT-PROMPT-STORY-SCENARIO-SUITE.md`.

## Layout

| Path | Role |
|------|------|
| `MANIFEST.tsv` | Index of all cases |
| `cases/S01-….md` … `S08-….md` | Fixtures: input → forbidden → required → pass check |
| Walk evidence (after run) | `tools/drafts/story-scenario-suite/WALK-EVIDENCE.md` |
| Friction log (after run) | `handoff/decision-trails/story-scenario-suite.tsv` |

## Rules for the walker

1. Read `.cursor/skills/story-generation-prompt/SKILL.md` once; load references named in each case.
2. Run cases **in order S01→S08**. Do not skip.
3. For each case: play the **Input** as the human; respond as the skill; score against **Pass check**.
4. Log one TSV row per case (`pass` or `fail` + one-line note).
5. Stop on first **fail** only if the OPEN gate says so; otherwise finish all eight and close with count.
6. Do not invent lean/value `session.json` unless a case explicitly says so. Do not ship skill edits in the walk session unless a FAIL blocker names one coaching hole to fix.

## Bands

- **typical** — happy path the skill should nail
- **boundary** — thin context; honest empty cells
- **adversarial** — human pushes hype, solution-speak, or reverse with gaps
