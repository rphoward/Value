---
name: story-generation-prompt
description: >
  Drafts an INVEST-style user story from raw evidence when no sentence exists
  yet, converts a story (and optional acceptance brief) into a producer-facing
  generation prompt for NotebookLM, video overviews, or similar, and can reverse
  a generation prompt back into a story with gaps labeled. Keeps a claim honest
  between the person making it and the tool amplifying it: the so-that clause
  and the prompt both stop at the funnel stage the evidence can test. Explains
  story elements, funnel honesty, and INVEST constraints for reuse across MVP
  efforts. Use when the user mentions user stories, MS05, story to prompt,
  generation brief, NotebookLM overview, NotebookLM recon or fact ledger from repo
  sources, lean MVP feature slicing, writing a story from interview notes or Kano
  output, a release note, or a launch post.
  Not for full lean-mvp session pacing, value proposition canvas, or UX flow
  diagrams.
metadata:
  activation: explicit
  distribution: monorepo
  pairs_with: lean-mvp
  tutorial_form: >
    references/tutorial.md is deliberately plain-language markdown rather than
    def-ref. It teaches a first-time operator the NotebookLM two-pass path, and
    step-by-step prose reads better for that than an s-expression. The rule
    shape in skill-authoring.mdc protocol-3b still governs every other file
    under references/.
disable-model-invocation: true
---

(def-sop story-generation-prompt
  (context
    (target "story-generation-prompt-agent")
    (optimization "honest-claims-from-evidence-to-story-to-generation-prompt")
    (references
      (story-elements references/story-elements.md)
      (drafting-inputs references/drafting-inputs.md)
      (invest-plus references/invest-plus.md)
      (conversion-workflow references/conversion-workflow.md)
      (source-fidelity references/source-fidelity.md)
      (positioning-inference references/positioning-inference.md)
      (examples references/examples.md)
      (tutorial references/tutorial.md))
    (assets
      (evidence-intake assets/evidence-intake.template.md)
      (story-card assets/story-card.template.md)
      (generation-prompt assets/generation-prompt.template.md)
      (notebooklm-recon assets/notebooklm-recon.template.md)))

  <central_idea>
  (center-of-gravity
    (invariant "A claim stays honest between the person making it and the tool amplifying it. Draft the story from observed evidence, hold the so-that clause to the funnel stage that evidence can test, then carry the same ceiling into the generation prompt. Require source fidelity in the prompt: facts in produced copy must trace to operator sources, not to narrative glue. Reverse direction reconstructs the story and labels what the prompt cannot prove."))
  </central_idea>

  (protocol-0-activation
    (on-activation
      1 "read references/story-elements.md"
      2 "read references/drafting-inputs.md when the user has evidence but no story sentence"
      3 "read references/conversion-workflow.md when converting in either direction"
      4 "read assets/notebooklm-recon.template.md when the operator uses NotebookLM on a repo or pastes a pass-1 fact ledger")
    (direction
      (draft-story "default when no story sentence exists yet")
      (story-to-prompt "default when a story sentence already exists")
      (notebooklm-recon "when the factual evidence is a repo or docs rather than observation — whether or not NotebookLM has been opened yet; follow protocol-6")
      (prompt-to-story "only when the user asks for the reverse"))
    (teaching "references/tutorial.md walks the whole path end to end for a user who has not used this skill before")
    (note "disable-model-invocation is true, so a model does not pick this skill up on its own — the user invokes it. lean-mvp arrives by a different road: its references/mvp-scope.md names this SKILL.md by path, and reading a named file is not model invocation, so the flag does not block that handoff."))

  (protocol-1-draft-story
    (when "user has evidence — interview notes, Kano output, tickets, observed workarounds — and no story sentence")
    (pre-flight
      (require actor "a specific actor in a specific moment")
      (require current-behaviour "what that actor currently does instead")
      (require cost "an observable cost of doing it that way")
      (on-missing-slot "ask one question for the missing slot")
      (on-repo-evidence "when the facts the story needs live in a repo or doc set rather than in observation, run protocol-6 first and emit the pass-1 question before asking the operator to summarise the project from memory")
      (on-sibling-workproduct "when /product-spine (or the human) names a workproduct slug, or hands paths under workproduct/value-proposition/<slug>/, read customer-profile.md, value-map.md, and north-star-blurb.md if present before asking for a paste — fill evidence intake from those files; say the paths you used in plain words")
      (forbidden 'invent-the-missing-slot 'ask-human-to-paste-profile-map-or-north-star-when-those-files-exist))
    (workflow
      1 "Fill assets/evidence-intake.template.md from sibling workproduct files and/or what the user supplied; leave a slot blank rather than guessing at it."
      2 "Write the so-that clause first, capped at the funnel stage the evidence can test (see story-elements funnel-honesty)."
      3 "Write the want clause as the outcome that produces that benefit, then apply the Negotiable test from references/drafting-inputs.md."
      4 "Name the persona last, from the actor and moment in the intake — not from a demographic label."
      5 "Emit assets/story-card.template.md filled, including the Grounding and Kill signal rows."
      6 "Run protocol-4-invest-plus."
      7 "Offer protocol-2 as the next step; do not run it unasked.")
    (forbidden 'invent-evidence 'demographic-persona 'implementation-in-want-clause))

  (protocol-2-story-to-prompt
    (inputs "User story required; acceptance criteria and verbatim brief optional")
    (workflow
      1 "Fill assets/story-card.template.md — persona, outcome, benefit, funnel stage, grounding, INVEST-plus, kill signal, test hook"
      2 "Read references/source-fidelity.md when the producer will use repo or doc sources (default for overview/video)."
      3 "Fill assets/generation-prompt.template.md — audience, claim ceiling from the funnel stage, source allowlist, fidelity rules, brief (verbatim if operator supplied), output format, do-not list, Producer paste block filled"
      4 "Emit the user story as one sentence for MS05 or captions"
      5 "When the human needs NotebookLM or video next: emit the Human how-to block from assets/generation-prompt.template.md — numbered steps only, one upload folder path, Box A for chat, Box B for video; do not bury the steps in prose"
      6 "If user also wants literacy, add a short plain-English pointer to story-elements sections (persona vs flow vs brief) after the how-to, not instead of it")
    (forbidden 'inflate so-that beyond validated funnel stage 'drop INVEST without user opt-out 'narrative-glue-hallucinations 'high-risk-debate-format-without-accuracy-pass 'notebooklm-directions-as-long-essay 'conflicting-upload-options-in-the-same-turn))

  (protocol-3-prompt-to-story
    (when "user requests reverse or only has a generation brief")
    (workflow
      1 "Infer As a / I want / so that"
      2 "State funnel stage and unknowns"
      3 "Run protocol-4-invest-plus and give one question for each fail"))

  (protocol-4-invest-plus
    (rubric references/invest-plus.md)
    (checkable-from-the-sentence N V T)
    (needs-backlog-and-team I E S)
    (default-for-needs-backlog "not answerable here")
    (extra-rows
      (grounding "which observation this story came from")
      (kill-signal "what result would drop this story"))
    (note "INVEST is a delivery rubric being applied at a validation moment; three of its letters have no honest answer from the sentence alone.")
    (forbidden 'pass-marks-on-I-E-S-without-supplied-backlog-context))

  (protocol-5-output-shape
    (order-by-direction
      (draft-story "Story card → INVEST-plus → Test hook → Evidence intake gaps")
      (story-to-prompt "User story (one sentence) → Generation prompt → Producer paste block → Story card → INVEST-plus → Test hook")
      (notebooklm-recon "Pass-1 question or ledger → positioning inference table → protocol-1 draft → same output order as story-to-prompt")
      (prompt-to-story "Reconstructed story → Unknowns → INVEST-plus → Questions for the operator"))
    (voice "Generation prompt: imperative, producer-facing. Story card: product-facing.")
    (sections "omit empty optional blocks")
    (examples references/examples.md)
    (after-emit
      "Remind the human to paste the one sentence into lean-mvp MS05 when that atom is open"
      "If the claim exposed a customer gap, offer opening the value skill"
      "Optional re-triage via /product-spine — do not read product-spine/SKILL.md in a loop"))

  (protocol-6-notebooklm-recon
    (when "the project's facts live in a repo or doc set — operator names a repo, mentions NotebookLM, asks for the recon question, or pastes pass-1 ledger output")
    (workflow
      1 "If no fact ledger exists yet, emit the upload allowlist and the pass-1 question from assets/notebooklm-recon.template.md as copy-paste text, then wait. Emit them unprompted rather than asking whether the operator wants them."
      2 "On pasted ledger, fill evidence intake Source fact ledger; read references/source-fidelity.md."
      3 "Run protocol-7 — derive positioning from mechanism; confirm only what the sentence needs before drafting clauses."
      4 "If actor, workaround, or cost missing, ask one question — neither the ledger nor the inference table can supply observation."
      5 "Run protocol-1 steps 2–6, grounding factual clauses in the ledger and positioning clauses in confirmed inference."
      6 "Run protocol-2; Producer paste block targets NotebookLM pass 2 on the same sources.")
    (forbidden 'pass-1-script-or-podcast-request 'ask-sources-for-audience-or-benefit-they-never-state 'treat-ledger-as-verbatim-without-spot-check))

  (protocol-7-positioning-inference
    (when "sources are a codebase or doc set that states mechanism but not audience, positioning, use, or skip — the normal case for a repo README")
    (rubric references/positioning-inference.md)
    (frames "Load the named entries from the lean-mvp knowledge base — pmf_pyramid_hierarchy, kano_model_categories, earlyvangelist_ladder, adoption_lifecycle, visual_grounding_analogies.space_pen_mirage — rather than paraphrasing the playbook from memory.")
    (scope "Derive a draft reading so the sentence is not blocked. lean-mvp owns the interview that settles each row; the ownership map in the reference is agent-internal so you know what not to re-run here.")
    (voice "The operator is in creative flow on their product. Keep atom codes, protocol numbers, and curriculum vocabulary out of the turn — value already lists atom IDs under forbidden-user-facing and lean-mvp asks for priors without naming atom ids. Say the session will come back to it, not which atom owns it.")
    (workflow
      1 "Read the mechanism ledger and apply the derivation moves — install preconditions, integration points, defaults and refusals, absence as skip, README claims, test names."
      2 "Emit one short scannable table: the reading, how sure it is, and what it rests on. Rows: problem, audience, when to use, when to skip, must-have core, workaround displaced."
      3 "Label every line fact, inference, hypothesis, or unknown. Problem-space rows derived from solution-space code are inference or hypothesis, never fact."
      4 "Ask only for the rows the sentence needs now, and offer the rest back to the session in one plain sentence."
      5 "Record confirmed rows as grounding with the operator as source; leave deferred rows labeled and out of the producer prompt.")
    (forbidden 'unlabeled-positioning-line 'promote-readme-claim-to-validated-benefit 'send-unconfirmed-inference-to-the-producer 'state-problem-in-mechanism-vocabulary 'rerun-the-customer-context-or-underserved-needs-interview 'block-the-sentence-until-every-row-is-confirmed 'speak-atom-codes-or-curriculum-vocabulary-to-the-operator)))
