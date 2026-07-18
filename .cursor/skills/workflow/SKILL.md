---
name: workflow
description: >
  Orchestrate emulate/revise → evaluate → discriminate → keep or retry for
  style-block hillclimb. Use when the user says hillclimb, /hillclimb, workflow
  loop, emulate and score, revise draft, retry draft, resume hillclimb, or run
  the ELIOT iteration cycle. Loads ELIOT and evaluator skills per step. NOT for
  one-off analysis, cold drift audit, web UI, or thematic/brainstorm material →
  suited author → a few unscored drafts (that job is pipeline invent session).
paths: .cursor/skills/workflow/**, eliotapp/application/workflow/**
metadata:
  activation: intent
  version: "1.10"
---

(def-sop workflow
  (context
    (target "workflow-skill-agent")
    (optimization "thin-orchestrator-draft-agent-score-python-discriminate-stop-python")
    (paired-modules "eliotapp/application/workflow/climb_metrics.py, scores_io.py, prepare.py, held_out_gate.py")
    (cli "scripts/hillclimb_once.py, scripts/held_out_gate.py")
    (slash-command ".cursor/commands/hillclimb.md"))

  <central_idea>
  (center-of-gravity
    (invariant "Hillclimb is draft (emulate-drafter on iter 1; revise-drafter on iters 2+) then qualitative eval-audit then record (deterministic SURFACE/PROSODY/CAST in Python; ten qualitative sections via eval-audit) then optional blind spot-the-real (diagnostic tells only). Default climb signal: pairwise_style_v1 — challenger vs current-best preference; qualitative mean is diagnostic. Countable author voice is Python; judgment voice is model. Legacy runs may climb on style_fidelity, indistinguishability, or reference_preference_v1. Python owns score merge, history, and stop; agents own draft and qualitative rubric only."))
  </central_idea>

  (protocol-1-input
    (shape "{style_block, topic, max_iterations, min_delta}")
    (adr "docs/adr/001-run-persistence.md — slug rules, git policy, sidecar naming")
    (persistence "tools/runs/<slug>/ session layout (variant A)")
    (files "source.txt, held-out.txt (optional register-matched sibling genuine), evidence-manifest.json, held-out-brief.md, held-out-gate.json, content-brief.md, passage-meta.json, craft-brief-v{n}.md, calibration.json, cast-aliases.json, style-block.md, scores.json manifest, draft-v{n}.md; optional qualitative-v{n}.json, discrimination-job-v{n}.json (and v1a/v1b/v1c seed jobs), trials-v{n}.json, verdicts-v{n}.json, discrimination-v{n}.json, v2-scores.json, drift-audit-v{n}.md")
    (slug "lowercase [a-z0-9-], 3–48 chars, starts with letter; tmp-* gitignored")
    (prepare "python .cursor/skills/workflow/scripts/hillclimb_once.py prepare --source <path> [--slug <slug>] [--held-out <path>] [--cast-aliases <path>]")
    (genuine-path "eliotapp.application.workflow.prepare.genuine_path(run_dir) — compatibility alias for development_genuine_path")
    (development-genuine "eliotapp.application.workflow.evidence_roles.development_genuine_path(run_dir) → held-out.txt if present else source.txt")
    (init "python .cursor/skills/workflow/scripts/hillclimb_once.py init --slug <slug> --block <path> --topic <text>")
    (resume "status then job-status — see protocol-7 resume order; never invent ad-hoc verdict writers")
    (job-board "eliotapp/application/workflow/job_board.py — DiscriminationJob mid-batch progress")
    (init-guard "refuse init if scores.json exists; pass --force to overwrite")
    (prepare-guard "refuse prepare if source.txt or scores.json exists; pass --force to overwrite"))

  (protocol-2-loop
    (playbook "references/playbook.md — metric, frozen harness, decision log, one hypothesis per iter, plateau push, stop rules")
    (subagent-spawn "MANDATORY: parent uses Task tool with subagent_type emulate-drafter | revise-drafter | eval-audit | discriminate — never inline draft prose, qualitative rubric, or spot verdicts in parent context")
    (step-1-draft "iter 1: parent writes craft-brief-vN.md via eliotapp.application.workflow.draft_inputs.write_craft_brief; build_draft_inputs verifies content-brief hash; Task emulate-drafter with {style_block_path, content_brief_path, craft_brief_path, topic, output_path}; iters 2+: write craft-brief-vN.md; build_draft_inputs; Task revise-drafter with {style_block_path, content_brief_path, craft_brief_path, prior_draft_path, output_path}; content requirements precede craft guidance; forbidden: source.txt, calibration, scores, qualitative, discrimination, reserved-validation; model per protocol-3; forbidden: parent writes draft-vN.md; forbidden: regenerate blank-page on iters 2+")
    (step-2-evaluate-qualitative "Task subagent_type eval-audit (.cursor/agents/eval-audit.md) with {draft path, style_block path}; model per protocol-3; parent saves returned JSON to qualitative-vN.json then record --qualitative; forbidden: parent scores qualitative axes")
    (step-3-record "python .cursor/skills/workflow/scripts/hillclimb_once.py record --run-dir <dir> --draft <draft> [--qualitative <json>] — deterministic scoring via evaluate_draft inside record (v2 when calibration.json exists); total is diagnostic")
    (step-4-climb-metric "default pairwise_style_v1: qualitative seed promote; iter 2+ preference vs best. Legacy style_fidelity: seed-promote by qualitative mean; stop on qualitative delta. reference_preference_v1: pref-job-* chain. Legacy indistinguishability: job-open → discriminate → job-record. Optional blind job-* for tells only. Forbidden: hand-authored verdicts or winners")
    (step-5-status "hillclimb_once.py status — best_draft by climb_metric (pairwise: accepted walk; style_fidelity: max qualitative mean; legacy: indistinguishability); retry, stop_reason")
    (step-6-decision "python .cursor/skills/workflow/scripts/hillclimb_once.py decision --run-dir <dir> --hypothesis <text> [--change <text>] [--verdict kept|reverted|stopped] [--note <text>]")
    (step-7-stop "when status retry false, stop; else parent writes craft-brief-vN.md per references/one-command.md — craft language from block prose / recurring tells as craft, never score numbers — content-brief.md unchanged; and returns to step 1"))

  (protocol-3-model-config
    (defaults "{drafter: composer-2.5, reviser: composer-2.5, evaluator: composer-2.5, supervisor: inherit}")
    (override "user states per-run overrides in the prompt; parent passes chosen slug as Task model arg for drafter, revise-drafter, and eval-audit")
    (note "config lives in this skill; no ~/.cursor/rules file required"))

  (protocol-4-contracts
    (climb-metric "default pairwise_style_v1 — pairwise-vs-best preference. Legacy: style_fidelity qualitative mean; indistinguishability; reference_preference_v1.")
    (countable-voice "SURFACE, PROSODY, CAST — Python from draft text; diagnostic floor and tie-break")
    (judgment-voice "ten qualitative sections — eval-audit only; models weak at counting")
    (diagnostic "EvaluatorScore.total, qualitative mean sparkline, and optional blind spot-the-real — history and tells, not default climb")
    (stop "should_stop on preference outcome when climb_metric pairwise_style_v1 or reference_preference_v1; qualitative_delta on style_fidelity; indistinguishability_delta on legacy")
    (forbidden 'reimplement-scoring-in-skill-md 'emulate-in-python 'skip-evaluator-skill 'emulate-inline-in-parent 'qualitative-eval-inline-in-parent 'edit-scorer-or-rubric-mid-run 'regenerate-blank-page-iters-2+))

  (protocol-4-draft-inputs
    (module "eliotapp/application/workflow/draft_inputs.py")
    (immutable "content-brief.md hash verified before build_draft_inputs; style-block.md hashed at build time")
    (mutable "craft-brief-v{n}.md per iteration via write_craft_brief")
    (precedence "content requirements override craft guidance on conflict")
    (forbidden-to-drafters "source.txt, held-out.txt, calibration.json, scores.json, qualitative-v*, discrimination-*, trials-v*, verdicts-v*, reserved-validation evidence")
    (paired-agents "emulate-drafter and revise-drafter share field names, precedence rule, and forbidden list")
    (adoption "inspect_run uses run_snapshot load + core.progression.decide; this phase defines draft-input seams and contracts"))

  (protocol-4-evidence-roles
    (module "eliotapp/application/workflow/evidence_roles.py")
    (manifest "evidence-manifest.json written by prepare_run")
    (roles "analysis_source → source.txt; development_genuine → held-out.txt when present else source.txt; reserved_validation → id + sha256 only")
    (development-view "reserved_validation_registered boolean; no reserved path, text, or hash in development reports")
    (forbidden-in-development "resolve_evidence_path for reserved_validation; reserved bytes or external path in serialized development views")
    (legacy "runs without evidence-manifest.json remain readable; genuine_path aliases development_genuine_path")
    (adoption "generation_lifecycle freeze and validation-open verify reserved id/hash; discrimination formulas unchanged"))

  (protocol-4-generation-freeze
    (module "eliotapp/application/workflow/generation_lifecycle.py")
    (states "development → frozen → validation_opened on scores.json generation_state")
    (freeze "freeze_finalist after hillclimb stop; records finalist draft, content brief, style block, craft briefs, evidence manifest, config, parent prompt_hashes and model_roles")
    (content-adherence "finalist-only; Task content-adherence with {content_brief, draft}; persist content-adherence.json; never alter scores.json climb fields")
    (validation-open "open_validation requires content-adherence pass when the brief declares REQ-/FOB- ids; then verifies reserved id/hash; writes validation-opened.json; no reserved text in run folder")
    (post-validation-lock "POST_VALIDATION_TUNING_ERROR — start a new slug; record, discrimination, decision, seed-promote, and job commands refuse when manifest exists")
    (cli "hillclimb_once.py freeze-finalist --parent-manifest <path>; validation-open --reserved-validation-id … --reserved-validation-sha256 …"))

  (protocol-5-principles
    (prove-it-works "measured indistinguishability only; total is diagnostic; no wins from inspection")
    (build-the-lever "freeze scorer and rubric before iter 1; never edit mid-run")
    (sequence-verifiable-units "record + job-score/job-record + decision before next draft")
    (guard-the-context-window "subagents for draft, eval, and discriminate; parent supervises")
    (laziness-protocol "smallest brief change; revise in place; drop complexity that does not hold the number")
    (make-operations-idempotent "job-trial / job-score converge on resume; finish pending before new draft"))

  (protocol-6-manual-gate
    (note "Web UI and automation wait until this manual loop works end-to-end on the Dostoevsky fixture.")
    (fixture-block ".cursor/skills/eliot/references/examples-dostoevsky.md")
    (fixture-source ".cursor/skills/eliot/assets/dostoevsky-source.txt"))

  (protocol-7-one-command-session
    (trigger ".cursor/commands/hillclimb.md — /hillclimb with source path, URL, pasted text, resume <slug>, or score <slug>")
    (reference "references/one-command.md — scoreboard line, results card, craft-brief-vN retry guidance, cast-aliases intake, best-of-n seeding, register-matched held-out, source resolution")
    (held-out-sibling "references/held-out-sibling.md — post-block brief + Exa + held_out_gate; prefer no held-out over wrong-register")
    (subagents "protocol-2-loop subagent-spawn applies to every iteration; score-only mode skips subagents")
    (defaults "{max_iterations: 3, min_delta: 1.5, early_stop: false, seeds: 3, discrimination_n: 10, drafter: composer-2.5, reviser: composer-2.5, evaluator: composer-2.5}")
    (early-stop-note "when early_stop true with discrimination climb, set min_delta on the 0–1 indistinguishability scale (e.g. 0.05); default 1.5 is legacy total-scale")
    (held-out "after style-block.md: emit held-out-brief.md from DEIXIS/ENV/DNA → Exa 2–3 candidates → held_out_gate.py → write_held_out on first pass; must exist before first job-open; init may precede held-out; Exa failure must not block init; prefer no held-out over wrong-register; forbidden: same-author different book as default genuine")
    (modes
      (new-run "prepare source only → ELIOT block → init when ready → held-out sibling protocol → protocol-2-loop → results card")
      (resume "mandatory order in references/one-command.md: status → job-status → finish in_progress jobs (incl. seed suffixes) → else open missing discrimination → else seed-round → else revise if retry → else results card")
      (score-only "status + results card; no subagents"))
    (topic "neighboring scene in the same register — not a retell of the analyze passage; ask user one line when the derived topic rewrites source beats")
    (brief-priority "when discrimination tells recur, odd-iter briefs prefer those craft tells over the two weakest qualitative axes if they conflict; never chase diagnostic total; even-iter cadence pass only when PatchScope is whole_draft — skip when axis/excerpt scope is set")
    (slug "derive from source filename via prepare.py when omitted")
    (keep-best "status best_* by indistinguishability; total remains diagnostic; regressing last never overwrites best draft pointer")
    (read-seam "eliotapp/application/hillclimb_runs.py — list_runs, run_detail for web UI")))
