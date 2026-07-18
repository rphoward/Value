---
name: distiller
description: >
  Extract thematic payload from rough ideas and match authors plus source passages for
  ELIOT analysis. Use when the user says distill, brainstorm topic, find an author,
  thematic payload, idea extraction, author matching, source passage, register routing,
  or upstream workflow before analyze. When the user also wants several new drafts or a
  short piece under that author, hand off to pipeline invent session — do not stop at
  Distiller-only. Loads phases 1–4 from this package and uses exa MCP for author and
  passage discovery. NOT for ELIOT analyze/emulate scoring, hillclimb loops, cold drift
  audit, or writing the seed drafts themselves (pipeline owns that job).
paths: .cursor/skills/distiller/**, eliotapp/core/distiller/**
metadata:
  activation: intent
  version: "1.3"
  upstream-engine: eliotworkflow/ELIOT_DISTILLER_v1_2_1.md
---

(def-sop distiller
  (context
    (target "distiller-skill-agent")
    (optimization "thin-orchestrator-phases-1-4-exa-discovery-agent-payload-python")
    (paired-modules "eliotapp/core/distiller/")
    (cli "scripts/discover_format.py")
    (mcp "plugin-exa-exa — web_search_exa, web_fetch_exa"))

  <central_idea>
  (center-of-gravity
    (invariant "Distiller extracts IDEAS not STYLE from rough text, maps to ELIOT-native ThematicPayload, suggests 3–5 register-routed author+work matches, locates or resolves a concrete source passage (200–2000 words), and emits payload-driven seed prompts before analyze or invent. Phases 1–4 ship in this gate."))
  </central_idea>

  (protocol-1-input
    (shape "{rough_text | topic | pierce_transcript}")
    (adr "docs/adr/001-run-persistence.md — slug rules, git policy, sidecar naming")
    (persistence "tools/runs/<slug>/[<YYYY-MM-DD>/] distiller layout (variant B)")
    (files "discovery.json required for smoke; thematic-payload.sexp optional; rough-input.md optional; emulation-prompts.json optional")
    (slug "same rules as workflow; dated subfolder when multiple smokes share slug prefix")
    (detection "read references/activation.md")
    (originating-constraints "user prompt constraints override Exa query templates — see references/exa-discovery.md")
    (if-no-text "prompt: Paste rough brainstorm notes or a topic sentence. I will extract ideas and find authors whose voices could carry them."))

  (protocol-2-phases
    (phase-1 "load references/idea-extraction.md — CoreThesis, GoverningTensions, ImageField, etc.")
    (phase-2 "load references/eliot-mapping.md — ArchetypeActivation, DwellTargets, SceneSeeds → (:ThematicPayload ...)")
    (phase-3 "load references/register-detection.md + references/author-matching.md + references/exa-discovery.md — register declaration, recommend best + list a few probables, PassageCandidate via exa / owned corpus / file ref / paste")
    (phase-4 "load references/emulation-prompts.md — numbered prompts per author; payload + craft direction → seeds, not pastiche-by-default")
    (resolve_passage "Exa OR catalog OR explicit file path OR markdown paste; slice 200–2000 words (prefer 800–1200); set provenance, word_count; see docs/adr/002-owned-corpus-registry.md")
    (forbidden 'analyze-prose-texture 'carry-source-vocabulary-into-payload 'title-only-work-references))

  (protocol-3-output
    (smoke-gate "author + passage candidate JSON — no ELIOT analyze yet")
    (format "read references/output-format.md")
    (record "write discovery.json; optional thematic-payload.sexp and emulation-prompts.json sidecars per ADR 001")
    (validate "python .cursor/skills/distiller/scripts/discover_format.py validate --json <file> [--payload thematic-payload.sexp]")
    (full-output-order ["STYLE CANDIDATES prose" "EMULATION PROMPTS numbered" "THEMATIC PAYLOAD fenced S-expression last"]))

  (protocol-4-contracts
    (shapes "eliotapp/core/distiller/shapes.py — AuthorCandidate, PassageCandidate, DiscoveryResult")
    (bounds "eliotapp/core/distiller/passage_bounds.py — MIN 200, MAX 2000, RECOMMENDED 800–1200")
    (payload "eliotapp/core/distiller/payload.py — validate_thematic_payload")
    (style-blocks "eliotapp/core/distiller/style_blocks.py — style_block_id, install_style_block; library tools/style-blocks/")
    (owned-corpus "sources/catalog.schema.json; user catalog.json gitignored per ADR 002")
    (forbidden 'reimplement-eliot-analysis 'score-in-python)))
