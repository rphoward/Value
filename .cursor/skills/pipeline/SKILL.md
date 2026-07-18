---
name: pipeline
description: >
  Orchestrate brainstorm/Distiller thematic material → suited author → a few unscored
  drafts (invent session), or the full chain through ELIOT analyze and hillclimb. Use when
  the user brings thematic/brainstorm/Distiller material or payload for ELIOT, wants a
  suited or named author/work, and asks for a few drafts/versions/a short article or piece
  (optional craft: audience, tone, length, ending/reveal) stopping before scoring,
  preference, or discrimination — or says full pipeline, distill then hillclimb, invent
  session, upstream to hillclimb, or pre-UI pipeline end to end. Loads distiller, eliot,
  and workflow skills per step. NOT for hillclimb-only (existing style block +
  climb/score/prefer/resume) or distiller-only smoke unless chaining is explicit.
paths: .cursor/skills/pipeline/**, handoff/PIPELINE-UI-CATALOG.md
metadata:
  activation: intent
  version: "1.2"
---

(def-sop pipeline
  (context
    (target "pipeline-skill-agent")
    (optimization "documented-handoff-chain-no-new-loop-module")
    (catalog "handoff/PIPELINE-UI-CATALOG.md")
    (adr "docs/adr/001-run-persistence.md, docs/adr/002-owned-corpus-registry.md"))

  <central_idea>
  (center-of-gravity
    (invariant "Pipeline chains distiller → resolve_passage → ELIOT analyze → optional prepare → hillclimb, or invent session that stops at N seed drafts under a named style block. Reuse existing skills and CLIs; document contracts for Web UI provisioning."))
  </central_idea>

  (protocol-0-upstream-chain
    (step-1 "distiller skill — rough-input.md → discovery.json + thematic-payload.sexp + emulation prompts")
    (step-2 "resolve_passage — exa fetch OR sources/catalog.json local_path OR user file path OR paste; slice to 200–2000 words (target 800–1200); write tools/runs/<slug>/source-excerpt.md")
    (step-3-analyze "eliot skill on source-excerpt.md → style-block.md")
    (step-3b-prepare "when word_count >= 800 and hillclimb follows: python .cursor/skills/workflow/scripts/hillclimb_once.py prepare --source <excerpt> --slug <slug>")
    (step-3c-analyze-short "when 200 <= word_count < 800 and analyze-only: skip prepare; ELIOT on excerpt directly per ADR 002")
    (step-4 "after prepare + style-block.md: /hillclimb resume <slug> (or init then protocol-2). SDK driver deferred — see handoff/SDK-CLIMB-SPIKE.md option C. Discrimination uses hillclimb_once.py job-* mid-batch board.")
    (session-types "distiller-only | invent | full-pipeline | hillclimb-only — see PIPELINE-UI-CATALOG.md"))

  (protocol-0b-invent-session
    (activation "thematic/brainstorm/Distiller material or payload + suited or named author + a few drafts/versions/short piece; optional craft (audience, tone, length, ending); stop before score/prefer/discriminate — internal session name invent")
    (goal "new work under a suited voice — not pastiche/lost-chapter by default; stop before hillclimb/jobs")
    (step-1 "distiller (or accept existing thematic-payload.sexp / chat payload); respect originating prompt constraints")
    (step-2 "resolve_passage — Exa / catalog / file ref / paste per distiller exa-discovery; write source-excerpt.md")
    (step-3 "analyze-or-reuse named style block — style_block_id + install_style_block into tools/style-blocks/ and run style-block.md + style-block-id.txt; reuse library when id exists unless user forces re-analyze")
    (step-4 "craft ask if gaps — load references/craft-ask.md; ask only missing feel / example / storyline / N / register")
    (step-5 "write_content_contract (content-brief.md + passage-meta.json) + write_craft_brief → craft-brief-v1.md")
    (step-6 "N× emulate-drafter with output_path=draft-v1{a,b,c,…}.md; invent emulate posture from eliot skill")
    (step-7 "surface + cleanup — load references/invent-surface.md; call out paths; write INVENT.md; light cleanup ask")
    (forbidden 'scores.json-init 'job-board 'preference 'discrimination 'seed-promote)
    (modules
      "eliotapp/core/distiller/style_blocks.py"
      "eliotapp/application/workflow/content_contracts.py"
      "eliotapp/application/workflow/draft_inputs.py")
    (paired-agent ".cursor/agents/emulate-drafter.md"))

  (protocol-1-passage-bounds
    (module "eliotapp/core/distiller/passage_bounds.py")
    (reject "word_count > 2000 or < 200 at resolve_passage")
    (ui-bands "green 800–1200; yellow 200–799 and 1201–2000; red above 2000"))

  (protocol-2-sloppy-source
    (reference "eliot/references/sloppy-source.md")
    (note "OCR markdown, optional headers; analyze prose texture not layout"))

  (protocol-3-verification
    (smoke-record "handoff/PIPELINE-SMOKE-PASSED.md")
    (invent-dogfood "handoff/DISTILLER-BOARD-MAP.md — invent dogfood checklist")
    (fixture "tests/fixtures/ owned-corpus excerpt for CI; real paths in local catalog.json only"))

  (protocol-4-draft-inputs
    (module "eliotapp/application/workflow/draft_inputs.py")
    (immutable "content-brief.md verified before build_draft_inputs; style-block.md at build time")
    (mutable "craft-brief-v{n}.md per iteration via write_craft_brief")
    (precedence "content requirements override craft guidance on conflict")
    (paired-agents "emulate-drafter and revise-drafter share field names, precedence rule, forbidden list")
    (invent "build_draft_inputs succeeds after content contract + craft-brief-v1 even without scores.json")
    (adoption "loop.py wiring deferred to a later phase")))
