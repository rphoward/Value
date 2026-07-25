(def-ref conversion-workflow
  (linked-from protocol-1 protocol-2 protocol-3 protocol-5 protocol-6 protocol-7)

  (section evidence-to-story-draft
    (trigger "User has evidence — interview notes, Kano output, tickets, an observed workaround — and no story sentence yet.")
    (inputs required "At least one observed workaround, verbatim complaint with its situation, or switch account; see references/drafting-inputs.md for the ranking.")
    (inputs optional "Kano categories; competitor column; the funnel stage the operator believes is reachable.")
    (steps
      1 "Read references/drafting-inputs.md."
      2 "Fill assets/evidence-intake.template.md. Ask one question per missing ingredient instead of filling it in."
      3 "Write the so-that clause first, capped at the funnel stage the evidence can test."
      4 "Write the want clause as the outcome, then run the Negotiable test from drafting-inputs."
      5 "Name the persona from the actor and moment recorded in the intake."
      6 "Emit assets/story-card.template.md filled, Grounding and Kill signal rows included."
      7 "Emit the INVEST-plus reading from references/invest-plus.md — I, E, and S stay \"not answerable here\" unless the user supplied backlog, estimating team, or sprint length."
      8 "Emit the test hook: one sentence naming the observation that would settle the story."))

  (section notebooklm-recon-to-story
    (trigger "The facts the story needs live in a repo or doc set — operator names a repo, has uploaded sources to NotebookLM, or asks for the recon question before drafting.")
    (see assets/notebooklm-recon.template.md)
    (steps
      1 "If no ledger exists, emit the upload allowlist and the pass-1 question as copy-paste text and stop until the operator pastes the answer. Do not ask the operator to describe the repo from memory first."
      2 "Paste the answer into evidence intake Source fact ledger; read references/source-fidelity.md."
      3 "Run protocol-7 per references/positioning-inference.md — derive readings, confirm only what the sentence needs, defer the rest to the session without naming curriculum codes."
      4 "If actor, workaround, and cost are still missing, ask one question — neither ledger nor inference supplies observation."
      5 "Run evidence-to-story-draft steps 3–8, grounding factual clauses in the ledger, positioning clauses in confirmed inference, and behavioural clauses in intake."
      6 "Run story-to-prompt-default; include Producer paste block for NotebookLM pass 2."
      7 "Forbidden in pass 1: script or podcast requests, and asking the sources for an audience they never state."))

  (section story-to-prompt-default
    (inputs required "User story sentence (As a / I want / so that).")
    (inputs optional "Acceptance criteria; generation brief; funnel stage label; tool target (NotebookLM, slide deck, video overview); NotebookLM fact ledger from pass 1.")
    (steps
      1 "Read references/story-elements.md if not already loaded."
      2 "Extract persona, outcome, benefit, funnel stage from the story; flag inflation vs MS05-style honesty."
      3 "Emit story card (assets/story-card.template.md) filled."
      4 "Emit generation prompt (assets/generation-prompt.template.md) filled — set the claim ceiling from the funnel stage; list source allowlist and fidelity rules (references/source-fidelity.md); brief is an operator-editable block."
      5 "Emit Producer paste block (compact section of generation prompt template) filled for NotebookLM pass 2 when tool target is NotebookLM or video overview."
      6 "Emit the INVEST-plus reading from references/invest-plus.md with fix hints on any fail."
      7 "Emit test hook: one sentence on how to verify T from the story."
      8 "Emit user story as a single sentence line for MS05 paste."))

  (section prompt-to-story-reverse
    (trigger "User asks prompt → story, reverse, or decode a generation brief.")
    (steps
      1 "Parse prompt for implied audience, content pillars, tone, output format."
      2 "Reconstruct best-effort As a / I want / so that."
      3 "Label inferred funnel stage; mark missing persona or untestable benefit as unknowns."
      4 "List gaps: which INVEST-plus row fails or is unanswerable, and what to ask the operator."))

  (section output-contract
    (order-by-direction
      (draft "Story card → INVEST-plus → Test hook → Evidence intake gaps")
      (story-to-prompt "User story (one sentence) → Generation prompt → Producer paste block → Story card → INVEST-plus → Test hook")
      (notebooklm-recon "Pass-1 question OR intake from pasted ledger → draft story → same as story-to-prompt")
      (prompt-to-story "Reconstructed story → Unknowns → INVEST-plus → Questions for the operator"))
    (tone "Generation prompt: imperative, producer-facing; story card: product-facing.")
    (verbatim "If operator supplied exact brief wording, copy it verbatim into the brief section of the generation prompt."))

  (check draft-when-no-sentence "When the user has evidence and no story sentence, draft first — do not ask them to supply a sentence you could write for them.")
  (check story-to-prompt-default "When a sentence exists and the user has not asked for the reverse, run story-to-prompt.")
  (forbidden "Auto-accept lean-mvp atoms; forbidden invent session state."))
