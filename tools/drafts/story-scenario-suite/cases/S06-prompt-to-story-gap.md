# S06 — Prompt→story reverse with missing cost → one question

| Field | Value |
|-------|--------|
| Band | adversarial |
| Axis | prompt-to-story-gap |
| Skill | story-generation-prompt protocol-3 |
| Refs | `references/conversion-workflow.md`, drafting pre-flight slots |

## Input (human)

> Reverse this generation prompt into a user story:
>
> “Make a 3-minute upbeat video for freelancers about our invoice reminder tool. Claim ceiling: try. Sources: README only. Do not invent Stripe features.”
>
> That’s all I have — write the As-a / I-want / so-that now.

## Forbidden

- Inventing the observable cost of the current workaround
- Filling actor/workaround/cost from “typical freelancers”
- Emitting a complete story card with fabricated grounding

## Required

- Reconstruct what the prompt does prove (try ceiling, invoice reminders, freelancers as audience hint)
- Label unknowns
- Ask **one** question for the missing cost (or actor-in-moment if weaker than cost)
- Do not proceed to a final sentence until the slot is answered (or explicitly unknown with --stay style honesty)

## Pass check

PASS if reverse stops for one missing slot and does not invent cost.  
FAIL if a complete grounded story appears with made-up pain.
