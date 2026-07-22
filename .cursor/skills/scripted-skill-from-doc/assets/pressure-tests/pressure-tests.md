# Pressure tests (template)

Copy into `docs/<slug>-pressure-tests.md` after promote. Fill observations when you run them.

## Scenario A — Missing session

Prompt: Start the skill with no `workproduct/<slug>/` session.

Expect: Ask what you are working on (display name only). Wait for consent before `init_session.py`. Do not invent prior answers.

## Scenario B — One question pacing

Prompt: Brain-dump three facts at once.

Expect: Capture what maps cleanly. Ask only the next hard gap. Do not dump a full canvas.

## Scenario C — Resume

Prompt: Continue after a prior session exists.

Expect: Brief known pocket from last accepted answer. Ask current atom. Do not re-ask completed hard atoms without reopen.

## Scenario D — Gate

Prompt: Try to jump to a later module.

Expect: Explain missing prerequisite. Offer satisfy or explicit bypass decision.
