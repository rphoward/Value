# S04 — Implementation in want → negotiable rewrite

| Field | Value |
|-------|--------|
| Band | adversarial |
| Axis | implementation-in-want |
| Skill | story-generation-prompt protocol-1 (Negotiable test) |
| Refs | `references/drafting-inputs.md`, `references/invest-plus.md` |

## Input (human)

> As a podcast editor, I want to integrate FFmpeg and a Next.js dashboard with waveform scrubbing so that I can cut dead air faster.

## Forbidden

- Keeping FFmpeg / Next.js / waveform as the fixed want
- Treating the sentence as pass without Negotiable rewrite

## Required

- Rewrite want as an **outcome** (e.g. cut dead air faster / mark silence spans)
- Apply Negotiable test: another implementation must still satisfy the sentence
- Mark N pass only after rewrite
- Optional one-line: implementation belongs in acceptance or later spike, not want

## Pass check

PASS if want has no required tech stack and N is justified.  
FAIL if FFmpeg/Next/waveform remain load-bearing in the want clause.
