(def-ref one-command-session
  (linked-from protocol-7-one-command-session)

  (scoreboard-line-after-each-iteration
    (emit "one compact line in chat after each iteration")
    (artifact scoreboard-line-template)
    (indist-from job-record :climb-metric)
    (total-from record :diagnostic-only)
    (weak "two lowest scores from qualitative-vN.json (eval-audit output)")
    (verdict "stopped when retry is false; else kept"))

  (results-card
    (when "finish, resume when stopped, score-only")
    (artifact results-card-template)
    (best-draft-from status :prefer-higher-indistinguishability :tie-break-total :never-last-iter-if-regressed)
    (genuine "register-matched held-out.txt when present else source.txt")
    (include-best-draft-prose "fenced block when user has not read it yet")
    (score-v2-sidecar "optional; cite when v2-scores.json exists"))

  (retry-brief-when-retry-true
    (craft-language-only)
    (quote "block field prose; never numeric targets bucket counts fingerprint figures score totals")
    (forbidden 'bucket-counts-in-brief 'sentence-length-percentages 'punct-per-100w-targets 'distilled-statistics-from-calibration)
    (discrimination-tells "craft only; promote when recurring; odd-iter prefer tells over two weakest axes when conflict; never chase diagnostic total")
    (alternating-passes
      (odd "recurring discrimination craft tells when present else two weakest qualitative axes from latest qualitative-vN.json; write craft-brief with PatchScope kind axis and those target_axes")
      (even "when PatchScope is whole_draft or absent: read-aloud cadence pass against block PROSODY prose; change nothing else. When PatchScope kind is axis or excerpt: skip whole-draft cadence; stay inside target_axes / span_markers"))
    (patch-scope "eliotapp.application.workflow.draft_inputs.write_craft_brief(..., patch_scope=PatchScope(...)); scope lives in craft-brief frontmatter; drafter must not read scores.json")
    (one-hypothesis-per-iteration)
    (iter-1 "spawn fresh emulate-drafter via Task subagent_type emulate-drafter")
    (iters-2+ "spawn revise-drafter with status.best_draft or last kept draft; never blank-page regenerate"))

  (best-of-n-seeding
    (default-seeds 3)
    (iter-1-only "N independent emulate-drafter Tasks in one message; promote winner by climb_metric only — never qualitative totals")
    (losers "sidecars draft-v1a.md draft-v1b.md; not in scores.json")
    (reference-preference-mode
      (per-pair-job "preference-job-v1{a-vs-b}.json via pref-job-open --left-suffix --right-suffix")
      (per-pair-chain "pref-job-open → reference-preference per pending order → pref-job-order → pref-job-score → pref-job-record (sidecar only)")
      (promote "after all pair scores present: seed-status → seed-promote --record"))
    (legacy-indistinguishability-mode
      (per-seed-job "discrimination-job-v1a.json via job-open --seed-suffix a|b|c")
      (per-seed-chain "eval-audit → qualitative-v1{suffix}.json → job-open --seed-suffix → discriminate all pending → job-trial → job-score → job-record (sidecar only)")
      (promote "after all seed jobs scored: seed-status → seed-promote --record"))
    (forbidden "pick winner from qualitative; record draft-v1 before seed-promote"))

  (seed-round-not-single-iter-loop
    (forbidden "treating best-of-n as one draft-vN loop with a single job-record into scores.json")
    (climb-metric-only "winner = max indistinguishability from discrimination-score-v1{suffix}.json"))

  (cast-aliases-at-prepare
    (write "tools/runs/<slug>/cast-aliases.json before or during prepare")
    (named-cast-only "narrator and author stay qualitative DEIXIS/DNA not in this file")
    (artifact cast-aliases-schema)
    (rules
      (keys "match CAST section names uppercase identifiers")
      (values "alias strings source actually uses")
      (reverent-pronouns "Thou Him when source uses mid-sentence; avoid bare He unless sentence-initial ambiguity accepted")
      (cli "hillclimb_once.py prepare --source <path> [--held-out <path>] [--cast-aliases <path>]"))
    (prepare "passes aliases into calibration; cast_present empty omits CAST from deterministic mean no default 50"))

  (register-matched-held-out
    (protocol "references/held-out-sibling.md")
    (when "after style-block.md; before first job-open; init may precede held-out")
    (brief "held-out-brief.md from DEIXIS ENVIRONMENT DNA — mode is intra-work register not distiller literary/essay/technical")
    (exa "2–3 candidates to .scratch/held-out-cand-*.txt; positives + excludes; no unsliced full-book dumps")
    (gate "python .cursor/skills/workflow/scripts/held_out_gate.py --source … --candidate … [--run-dir …]")
    (length "preferred 800–1200 words; floor 400; hard max 1200 gate-fail")
    (write-on-pass "eliotapp.application.workflow.prepare.write_held_out — never prepare --force just to attach")
    (prefer-no-held-out "over wrong-register; user-supplied still gated; fail → genuine = source.txt")
    (artifacts "held-out-brief.md, held-out-gate.json, held-out.txt on pass")
    (forbidden-as-default-genuine "same-author different book style drift")
    (legacy "runs without held-out.txt discriminate against source.txt")
    (helper "genuine_path(run_dir) returns held-out.txt if present else source.txt"))

  (subagent-loop-required
    (parent-orchestrates-only)
    (steps
      (1 "Task emulate-drafter iter 1 or revise-drafter iters 2+ prior best_draft → draft-vN.md")
      (2 "Task eval-audit → qualitative-vN.json")
      (3 "hillclimb_once.py record --qualitative qualitative-vN.json")
      (4-discrimination-via-job-board
        (not "ad-hoc verdict files")
        (job-open "hillclimb_once.py job-open --run-dir <dir> --iteration N --draft draft-vN.md --genuine <held-out.txt if present else source.txt> --n 10 [--seed-suffix during best-of-n]")
        (discriminate "Task discriminate for each pending_trial_ids from job-status")
        (job-trial "per completed Task --trial-id … --verdict <json>")
        (job-score-then-job-record "attaches indistinguishability; writes discrimination-vN.json"))
      (5 "status → scoreboard line → decision"))
    (forbidden-in-parent
      'writing-draft-prose 'scoring-qualitative-axes 'running-spot-the-real-inline
      'writing-verdicts-by-hand-outside-job-trial 'reading-prior-scores-json-into-emulate-revise-eval-prompts
      'editing-scorer-rubric-calibration-mid-run))

  (source-resolution
    (file-path "hillclimb_once.py prepare --source <path> [--slug <slug>] — without --held-out unless user path already known (still gate later)")
    (url "Exa fetch primary → tools/runs/tmp-<slug>/fetch.txt → prepare --source only; held-out after style-block via held-out-sibling")
    (pasted-text "temp file under tools/runs/tmp-* → prepare --source; held-out after style-block when possible")
    (then "build Dense Style Block from source.txt using ELIOT skill; write style-block.md; init --block when ready"))

  (new-run-sequence
    (1 "parent writes cast-aliases.json when block names characters")
    (2 "prepare --source … → source.txt + calibration.json; calibration.json numeric paragraph stats for scorer only; do not attach held-out yet unless user path known")
    (3 "ELIOT analyze → style-block.md → paragraph_modes per Extensions ParagraphBehavior → init --slug --block --topic when ready (may precede held-out); topic neighboring scene same register not retell; ask user one line if derived topic rewrites source beats; init copies analyzer block unchanged no stamping from calibration")
    (4 "held-out sibling: emit held-out-brief.md → Exa 2–3 candidates → held_out_gate.py per candidate → write_held_out on first pass; prefer no held-out over wrong-register; must finish before first job-open")
    (5-loop-subagents-only
      "iter 1 seeds: N emulate-drafter → per suffix eval-audit → job-open --seed-suffix --genuine <genuine_path> → discriminate all → job-score → job-record (sidecar) → seed-status → seed-promote --record → decision; iters 2+: single draft revise loop per protocol-2 steps 1–7")
    (6 "if retry true write retry brief return to step 5 with revise-drafter")
    (7 "emit results card cite which genuine file was used"))

  (resume-score-only
    (mandatory-resume-order "chat /hillclimb resume and any future driver share this; start with hillclimb_once.py inspect --run-dir <dir>")
    (artifact resume-cli-snippet)
    (steps
      (0 inspect "hillclimb_once.py inspect — follow exactly one next_action")
      (1 status)
      (2 "preference mode: pref-job-status; legacy: job-status")
      (3-preference "if any preference job in_progress → reference-preference per pending order → pref-job-order → pref-job-score → pref-job-record → seed-status → seed-promote --record when ready")
      (3-legacy "if any discrimination job in_progress → discriminate per pending trial → job-trial → job-score → job-record → seed-status → seed-promote --record when ready")
      (4-preference "else if latest iteration draft in scores.json but preference sidecar missing → pref-job-open then full order batch")
      (4-legacy "else if latest iteration draft in scores.json but indistinguishability missing → job-open then full batch")
      (5 "else if iter 1 seed jobs/pairs exist and scores.json has no iteration 1 → seed-status; finish unfinished; seed-promote --record when ready_to_promote")
      (6 "else if retry → revise from best_draft")
      (7 "else results card"))
    (score-only "results card only; no subagents no record no job mutations"))

;; --- artifacts ---

## scoreboard-line-template

```
iter N | indist X.XX | Δind ±X.XX | total XX.X | weak: AXIS1, AXIS2 | verdict kept|stopped
```

## results-card-template

```
## Hillclimb — <slug>
Topic: <topic>
Run: tools/runs/<slug>/

| Iter | Draft | Indist | Δind | Total | Best |
|------|-------|--------|------|-------|------|
| 1 | draft-v1.md | 0.40 | — | 71.8 | |
| 2 | draft-v2.md | 0.80 | +0.40 | 89.24 | ★ |

Best draft: draft-v2.md (indist 0.80, total 89.24, iter 2)
Stopped: max_iterations at iter 3
Genuine: held-out.txt (or source.txt when no held-out)
Calibration: tools/runs/<slug>/calibration.json
score_v2: tools/runs/<slug>/v2-scores.json (if present)

Paths:
- source.txt
- held-out.txt (when present)
- style-block.md
- scores.json
- discrimination-vN.json
- decision.tsv
```

## cast-aliases-schema

```json
{
  "PRODIGAL_SON": ["Prodigal Son", "the prodigal"],
  "GOD": ["God", "the One"]
}
```

## resume-cli-snippet

```powershell
python .cursor/skills/workflow/scripts/hillclimb_once.py status --run-dir tools/runs/<slug>
python .cursor/skills/workflow/scripts/hillclimb_once.py job-status --run-dir tools/runs/<slug>
```

## operator-pitfalls

- **Windows `--run-dir`:** CLI resolves `--run-dir` to an absolute path before any atomic writes. Relative paths such as `tools/runs/<slug>` are fine from repo root; you no longer need an absolute path for `seed-promote --record`.
- **Reserved validation at prepare:** Register `reserved_validation` during `prepare`, not at freeze time. Pass `--reserved-validation-id` and `--reserved-validation-path` together; the path must stay outside the run folder (dev canary: `tools/runs/.scratch/<slug>-reserved-canary.txt`).
- **Preference prompt hash:** `pref-job-open` defaults `--prompt-hash` to SHA-256 of `.cursor/agents/reference-preference.md`. Pin explicitly when needed, or print the default with `hillclimb_once.py prompt-hash`.
- **Held-out length:** Floor is 400 words; preferred band is 800–1200. Longer held-out excerpts run but widen preference windows and slow judging.
