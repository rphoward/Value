(def-ref hillclimb-playbook
  (linked-from protocol-2-loop protocol-6-principles)

  (role
    (own "metric and experiment integrity")
    (supervise-and-review "delegate draft eval discrimination to fresh subagents each iteration")
    (one-change-one-measurement "keep or retry; never stack untested changes; data decides"))

  (metric-and-stop-predicate
    (fixed-before-iteration-1)
    (climb-metric
      "discrimination indistinguishability higher better from hillclimb_once.py job-record wraps record_discrimination after each record"
      (coin-flip "~0.5 maps to 1.0; always caught maps to 0.0"))
    (diagnostic "EvaluatorScore.total from record — stored for UI and history; never keep/stop signal once discrimination attached")
    (stop "Python should_stop in eliotapp/application/workflow/climb_metrics.py — halt at iteration_count == max_iterations; when early_stop true at init also halt when indistinguishability_delta < min_delta after discrimination recorded; use 0-1-scale min_delta with early_stop e.g. 0.05; default 1.5 is legacy total-scale")
    (agree-at-init "max_iterations min_delta early_stop; do not change mid-run"))

  (frozen-harness
    (scores-json-writes-only-via "hillclimb_once.py record / job-record (or legacy record-discrimination)")
    (mid-batch-discrimination-only-via "job-open / job-trial / job-score / job-record; no ad-hoc verdict files")
    (record-evaluate-draft-v2 "when calibration.json exists; qualitative rubric calibration score_draft*.py do not change mid-run; loop agents must not edit; score_fixture.py ad-hoc repro only")
    (baseline "first record + job-record after init establishes iteration 1 totals and indistinguishability"))

  (decision-log-contract
    (path "tools/runs/<slug>/decision.tsv")
    (one-row-per-iteration)
    (artifact decision-tsv-columns)
    (append-via "hillclimb_once.py decision so before/after/delta cannot drift from scores.json")
    (note-column "climb-metric notes indistinguishability weakest axes next brief hint")
    (read-before-each-attempt "search accumulates"))

  (loop-discipline
    (1-one-hypothesis
      (odd-iter-briefs "when discrimination tells recur prefer craft tells over two weakest qualitative axes if conflict; else target two weakest axes craft language only; never chase diagnostic total")
      (even-iters "cadence pass"))
    (2-draft-path "iter 1 emulate-drafter new-run default seeds 3; iters 2+ revise-drafter editing best_draft or last kept; no blank-page regenerate on retries")
    (3-fresh-subagent
      (per "draft eval discriminate trial")
      (no-scores-json-in-drafter-context "no decision.tsv in drafter/reviser; no score history in eval-audit; discriminate sees only blind passages")
      (genuine "register-matched held-out.txt when present else source.txt; --n 10"))
    (4-parent-sequence
      "init → draft agent → eval-audit → record --qualitative → job-open → Task discriminate per pending trial → job-trial → job-score → job-record → status → decision → write next retry brief or stop"
      (on-resume "status then job-status before any new draft"))
    (5-plateau-push "on stall pivot category SURFACE vs ENVIRONMENT vs DNA combine near-misses or radical revise brief before concluding hill climbed")
    (6-stop-rules "do not relax min_delta to declare victory; do not quit while cheap untried hypotheses remain; surface stuck runs instead of spinning")
    (7-neighboring-topic "new scene same register not retell of analyze passage; ask user one line when derived topic rewrites source beats"))

  (principles-one-line-rules
    (artifact principles-table)))

;; --- artifacts ---

## decision-tsv-columns

| Column | Meaning |
|--------|---------|
| `id` | Iteration number (string) |
| `hypothesis` | One-line theory for this attempt |
| `change` | What the drafter did (emulate vs revise, brief focus) |
| `before` | Prior iteration total, or `—` on first |
| `after` | This iteration total from `scores.json` (diagnostic) |
| `delta` | Total delta from `scores.json`, or `—` on first |
| `tests` | Regression gate (`green` when suite passes) |
| `verdict` | `kept`, `reverted`, or `stopped` |
| `note` | Free text (indistinguishability, weakest axes, next brief hint) |

## principles-table

| Name | Rule |
|------|------|
| prove-it-works | Accept only measured indistinguishability movement past noise; total is diagnostic; never claim a win from inspection alone. |
| build-the-lever | Freeze the scorer and rubric before iteration 1; they are the ruler; never edit mid-run. |
| sequence-verifiable-units | Each iteration ends in `record` + `job-record` + `decision` before the next draft begins. |
| guard-the-context-window | Delegate draft, eval, and discriminate to subagents; parent supervises and writes briefs. |
| laziness-protocol | Prefer the smallest revise that moves the weakest axis; revert complexity that does not hold the climb metric. |
