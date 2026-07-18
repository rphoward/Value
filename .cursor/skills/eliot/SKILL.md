---
name: eliot
description: >
  Analyze classical literature into a Dense Style Block and emulate a new piece or article
  in that voice. Use when the user says analyze, emulate, style block, style sheet, ELIOT,
  classical literature, dense style block, new piece/article in an author's voice, or
  pastiche from a source passage.   When pipeline invent session is already running, use
  InventEmulation posture (content + craft briefs → seed drafts). Loads progressive-
  disclosure references from this package. NOT for general writing coaching, UWE
  evaluation scoring, or hillclimb loops (those are separate skills).
paths: .cursor/skills/eliot/**, eliotapp/core/eliot/**
metadata:
  activation: intent
  version: "5.9"
  strippable: references/model-profile.md, references/user-aids.md
---

(def-sop eliot
  (context
    (target "eliot-skill-agent")
    (optimization "progressive-disclosure-analysis-and-emulation")
    (fixture assets/dostoevsky-source.txt)
    (references
      (workflows references/workflows.md)
      (validation references/validation.md)
      (output-format references/output-format.md)
      (engine references/engine.md)
      (extensions references/extensions.md)
      (ocean-facets references/ocean-facets.md)
      (default-voice references/default-voice.md)
      (input-detection references/input-detection.md)
      (examples-dostoevsky references/examples-dostoevsky.md)
      (model-profile references/model-profile.md :strippable t)
      (user-aids references/user-aids.md :strippable t)))

  <central_idea>
  (center-of-gravity
    (invariant "ELIOT v5.9: source passage → Dense Style Block (Analysis) or style block + brief → emulated prose (Emulation). Invent posture defaults to new seed drafts under the voice, not lost-chapter pastiche. Output is brief explanation then a separate fenced style block — never embedded in prose."))
  </central_idea>

  (protocol-1-workflow-entry
    (on-activation
      1 "read references/input-detection.md — AnalyzeMode vs WriteMode"
      2 "if AnalyzeMode: load references/workflows.md (:Analysis steps 1–14)"
      3 "if Emulation: load references/workflows.md (:Emulation steps 1–10); if invent session also load :InventEmulation"
      4 "before any output claim: read references/validation.md (:CompletenessGates)")
    (reference-load-order-analysis
      (always references/ocean-facets.md references/extensions.md references/engine.md)
      (before-output references/output-format.md references/validation.md))
    (strippable-default "automated pipelines omit model-profile and user-aids unless user requests")
    (invent-emulate
      (paired-agent ".cursor/agents/emulate-drafter.md")
      (inputs "style-block.md + content-brief.md + craft-brief-vN.md via draft_inputs / content_contracts")
      (posture "new piece carrying payload + craft direction; do not default to lost-chapter/pastiche")))

  (protocol-2-analysis-references
    (load-on-demand
      references/ocean-facets.md
      references/default-voice.md
      references/engine.md
      references/extensions.md)
    (cast-rule "populate idiolect + voice_sample BEFORE worldview/archetype per WORKFLOWS step 7"))

  (protocol-3-output
    (analysis-structure "2–4 sentence summary THEN complete style block in its own ``` fence")
    (forbidden 'style-block-in-prose 'single-fence-mixing-explanation-and-block)
    (follow references/output-format.md references/validation.md))

  (protocol-4-fixture
    (pinned-compare assets/dostoevsky-source.txt)
    (gold-shape references/examples-dostoevsky.md)
    (note "three-way compare: monolith 5.7, monolith 5.3, this skill — see handoff/ELIOT-SPLIT.md"))

  (protocol-5-optional-strippable
    (model-profile references/model-profile.md)
    (user-aids references/user-aids.md)))
