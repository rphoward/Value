---
name: evaluator
description: >
  Score draft fidelity against a Dense Style Block on 13 block sections (3 deterministic
  + 10 qualitative axes), or run legacy UWE writing critique. Use when the user says
  evaluate, score, style-block diff,
  fidelity, hillclimb score, eval audit, UWE, or compare draft to style block. Loads
  progressive-disclosure references from this package. NOT for ELIOT analysis/emulation
  or hillclimb loops (those are separate skills).
paths: .cursor/skills/evaluator/**, eliotapp/core/evaluator/**
metadata:
  activation: intent
  version: "3.0"
  strippable: references/extras.md
---

(def-sop evaluator
  (context
    (target "evaluator-skill-agent")
    (optimization "block-native-13-axis-scoring-with-deterministic-core")
    (references
      (input-detection references/input-detection.md)
      (style-block-diff references/style-block-diff.md)
      (style-block-rubric references/style-block-rubric.md)
      (workflows references/workflows.md)
      (modes references/modes.md)
      (lenses references/lenses.md)
      (engine references/engine.md)
      (rubric references/rubric.md)
      (output-format references/output-format.md)
      (extras references/extras.md :strippable t)))

  <central_idea>
  (center-of-gravity
    (invariant "Every Dense Style Block section is a scored axis. Three axes (SURFACE, PROSODY, CAST) are deterministic Python; ten are qualitative rubric scores. Both blend into one EvaluatorScore with a fixed 14-slot vector comparable run-to-run for hillclimb delta(score). DraftOnly mode is legacy UWE on draft alone."))
  </central_idea>

  (protocol-1-workflow-entry
    (on-activation
      1 "read references/input-detection.md — StyleBlockDiff vs DraftOnly"
      2 "if StyleBlockDiff: load references/style-block-diff.md — the 13-axis map"
      3 "if DraftOnly: load references/workflows.md (:DraftOnly steps) — legacy UWE"
      4 "before any DraftOnly output: references/output-format.md and references/rubric.md"))

  (protocol-2-style-block-diff
    (input "{draft, style_block}")
    (contract "eliotapp/core/shapes/score.py — BLOCK_SECTIONS, SectionScore, EvaluatorScore")
    (deterministic-axes "SURFACE PROSODY CAST — eliotapp/core/evaluator/score_draft.py; CLI scripts/score_fixture.py")
    (qualitative-axes "the other ten — score with references/style-block-rubric.md")
    (fresh-context "prefer spawning the eval-audit subagent (.cursor/agents/eval-audit.md) with only {draft, style_block}; cold eyes prevent emulation-history bias")
    (merge "parse the subagent JSON with parse_qualitative_scores; blend with combine_scores; or pass --qualitative to scripts/score_fixture.py"))

  (protocol-3-scoring
    (cli "scripts/scorer_cli.py — preferred entrypoint: score | score-v2 | gate | pairwise | discrimination | authorprint")
    (vector "14 slots: one per BLOCK_SECTIONS entry in order, -1.0 sentinel when unscored, last slot total")
    (total "0.5 * deterministic mean + 0.5 * qualitative mean; deterministic-only when qualitative absent")
    (tier-anchoring "name the tier (Sharp/Functional/Soft/Broken) before the number — references/rubric.md")
    (hillclimb "delta(total) on the same draft lineage is the loop signal"))

  (protocol-3b-content-adherence
    (module "eliotapp/core/evaluator/content_adherence.py")
    (agent ".cursor/agents/content-adherence.md")
    (packet "{content_brief, draft} only — no source, style block, calibration, scores, or reserved evidence")
    (identifiers "stable REQ-* under required: and FOB-* under forbidden: in the content brief body")
    (output "strict pass/fail JSON: one finding per identifier with draft evidence; reject scores, unknowns, duplicates, missing findings")
    (artifact "content-adherence.json — never written into scores.json or climb totals")
    (gate "open_validation refuses when the brief declares identifiers and no recorded pass exists")
    (cast-scene "source-derived cast/scene replay stays diagnostic unless the brief names them"))

  (protocol-3c-quality-veto
    (module "eliotapp/core/evaluator/quality_veto.py")
    (agent ".cursor/agents/quality-judge.md")
    (packet "blind {job_id, question, passage_a, passage_b} only — no candidate side, source, style block, content brief, score history, author, or filename")
    (axes "coherence, repetition, completeness, obvious factual failure — not source-relative pairwise axes")
    (winners "A, B, or TIE")
    (aggregation "candidate wins + ties toward pass; incumbent wins toward veto; unresolved disagreement → human_review")
    (defaults "judge_count=3; required_agreement_for_pass=2; required_agreement_for_veto=2; tie_rule=pass")
    (output "outcome pass|veto|human_review with win counts — never a numeric quality score; never alters fidelity ranking")
    (live "fixture mechanics only in phase 9; live reliability UNPROVEN until phase 13 smoke"))

  (protocol-4-draft-only-legacy
    (workflows references/workflows.md)
    (lenses references/modes.md references/lenses.md references/engine.md)
    (extras references/extras.md)
    (note "discovery tags and title assessment only when DraftOnly total >= thresholds")))
