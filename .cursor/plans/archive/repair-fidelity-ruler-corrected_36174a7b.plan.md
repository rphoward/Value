---
name: repair-fidelity-ruler-corrected
overview: Replace spot-the-genuine as the controlling metric with a calibrated, reference-conditioned comparison between generated candidates. Pin every judge run explicitly, prevent reference-copying from winning, preserve legacy artifacts, and require calibration before workflow wiring.
todos:
  - id: correct-record
    content: Record the metric root cause and mark affected conclusions inconclusive without changing frozen artifacts
    status: completed
  - id: build-calibrate
    content: Implement and calibrate the pinned reference-preference evaluator with overlap, self-pair, degraded-control, side-swap, and repeatability checks
    status: completed
  - id: wire-workflow
    content: Make preference outcomes control new hillclimbs with deterministic tournament, tie, and legacy behavior
    status: completed
  - id: rescore-contracts
    content: Re-evaluate existing drafts, update workflow and UI contracts, and run the complete test suite
    status: completed
isProject: false
---

# Repair the Fidelity Ruler — Corrected

**Status:** shipped 2026-07-10 — see `handoff/REFERENCE-PREFERENCE-SHIPPED.md`, `handoff/PREFERENCE-ORCHESTRATION-PASSED.md`.

## 1. Correct the record
- Add [`handoff/DISCRIMINATION-METRIC-ROOT-CAUSE.md`](handoff/DISCRIMINATION-METRIC-ROOT-CAUSE.md) and update [`handoff/STATE.md`](handoff/STATE.md). Mark floor-bound StyleBlock conclusions **inconclusive under an unstable ruler** without changing frozen reports or manifests.
- Record the demonstrated causes: unpinned judge drift, source recognition, misstated five- and ten-trial resolution, and staged expansion that could not trigger under its configured boundary.

## 2. Build and calibrate reference preference
- Add [`src/eliotwf_skills/evaluator/reference_preference.py`](src/eliotwf_skills/evaluator/reference_preference.py), [`.cursor/agents/reference-preference.md`](.cursor/agents/reference-preference.md), a thin evaluator CLI, and [`tests/test_reference_preference.py`](tests/test_reference_preference.py).
- Compare two same-brief generated candidates against authentic reference windows. The authentic passage is never a selectable candidate. Reject candidates that exceed the existing held-out overlap limits so quotation or copying cannot win.
- Require every run manifest to name an explicit available judge model; reject `inherit`. Keep the model configurable rather than hard-coding `composer-2.5-fast`, and record model, prompt, reference, candidate, and policy hashes.
- For each of three reference windows, judge both A/B orders. A valid pair keeps the winning candidate identity constant while the displayed A/B label flips; an inconsistent pair becomes a window tie. Aggregate the three windows to a winner only when one candidate wins at least two windows; otherwise return `TIE`.
- Calibrate before workflow changes with two repeated batches of: identical self-pairs, a deterministic degraded-text control, and side-swapped packets. Self-pairs must aggregate to ties, degraded controls must lose, and repeated batches must preserve the aggregate candidate outcome; individual verdicts need not be identical. Use historical Sample I/IV only as secondary evidence, not ground truth.

## 3. Make preference control new hillclimbs
- Add versioned `climb_metric: reference_preference_v1` handling in [`src/eliotwf_skills/workflow/loop.py`](src/eliotwf_skills/workflow/loop.py), [`src/eliotwf_skills/workflow/run_state.py`](src/eliotwf_skills/workflow/run_state.py), [`src/eliotwf_skills/workflow/job_board.py`](src/eliotwf_skills/workflow/job_board.py), and [`.cursor/skills/workflow/scripts/hillclimb_once.py`](.cursor/skills/workflow/scripts/hillclimb_once.py). Runs without this field retain legacy behavior.
- Select initial seeds by full round robin. Use pairwise wins and ties to choose a unique leader; if a cycle or score tie remains, use the earliest deterministic seed ID as the incumbent and record `unresolved_tournament: true` rather than claiming a style winner.
- Later iterations compare the challenger directly with the incumbent. A win promotes the challenger; a loss retains the incumbent; a tie retains the incumbent and stops cleanly. Remove `min_delta` from this relative path.
- Keep spot-the-genuine readable as an optional final diagnostic only. It cannot select seeds, stop iterations, freeze finalists, or decide PASS/FAIL.
- Extend the existing hillclimb, run-state, job-board, and validation-freeze tests for the new decisions and legacy compatibility.

## 4. Re-evaluate existing evidence and update contracts
- Only after calibration passes, compare existing drafts in `tools/runs/styleblock-content-match-001/` and `tools/runs/styleblock-aa-source-probe-001/`; generate no new prose.
- Add versioned preference outcomes with legacy fallback in [`src/eliotwf_skills/workflow/benchmark.py`](src/eliotwf_skills/workflow/benchmark.py). Do not rewrite historical staged-replay traces.
- Update evaluator/workflow skill references, [` .cursor/commands/hillclimb.md`](.cursor/commands/hillclimb.md), and the run UI so reference preference is the climb decision and indistinguishability is diagnostic.
- Run focused tests, then `$env:PYTHONPATH="src"; python -m pytest tests/ -q`. Publish one short handoff with calibration evidence, legacy compatibility, and the recovered StyleBlock comparison outcome.