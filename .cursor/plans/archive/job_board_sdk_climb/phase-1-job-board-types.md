# Phase 1 — Discrimination job types

Back-link: [overview.md](overview.md)

## Goal

Make mid-batch discrimination progress a first-class, loadable artifact under the run folder. No CLI yet.

## Changes

- Add `src/eliotwf_skills/workflow/job_board.py` with open / mark-trial / mark-scored / mark-recorded / load / active-job helpers.
- Persist `tools/runs/<slug>/discrimination-job-v{n}.json` (and seed-suffixed variants when needed).
- Add `tests/test_job_board.py` covering open → partial trials → resume load → score gate while pending → recorded.

Do not touch `hillclimb_once.py` or skill docs in this phase.

## Data structures

`DiscriminationJob` (dict/dataclass written as JSON):

- `kind: "discrimination"`
- `iteration: int`
- `draft`, `genuine` (relative paths)
- `n`, `seed: int`
- `seed_suffix: str | null` (e.g. `"a"` for `trials-v1a.json` during best-of-n; null for normal iters)
- `status: "open" | "in_progress" | "scored" | "recorded" | "failed"`
- `trials_path`, `verdicts_path`, `result_path`
- `completed_trial_ids: list[str]`, `pending_trial_ids: list[str]`
- `updated_at: ISO-8601 UTC`

Illegal states to refuse at the boundary: score while pending nonempty; record while not scored; open when an active non-terminal job already exists for the same iteration+suffix.

`active_discrimination_job` / listing helpers may return **multiple** non-terminal jobs during a seed round (`v1a`/`v1b`/`v1c`). Parent finishes all before promoting a winner.

## Verification

**Static.** `pytest tests/test_job_board.py` green; import smoke for `eliotwf_skills.workflow.job_board`.

**Runtime.** No CLI surface yet. Flag: control-cli deferred to phase 2.
