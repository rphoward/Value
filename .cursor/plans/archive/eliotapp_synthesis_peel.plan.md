---
name: Eliotapp SYNTHESIS peel
overview: "Post-evacuate peel: root hygiene first, then inspect split, kill loop.py, Path out of core, real CLI, catalog under workproduct. Keeps ADR 005 sibling homes; does not nest under one eliot* umbrella."
todos:
  - id: phase-00-hygiene
    content: "Delete orphan EliotWF/ gitlink + eliotwf.egg-info; scrub skill prose still citing src/eliotwf_skills"
    status: completed
  - id: phase-01-inspect-split
    content: "Create core.progression.decide (new); store load → InspectedRun/RunSnapshot; callers pass run_id + locator"
    status: completed
  - id: phase-02-kill-loop
    content: "Migrate every loop.py importer (~19); delete eliotapp/application/workflow/loop.py in the same wave"
    status: completed
  - id: phase-03-list-vs-deep
    content: "Cheap RunCard list path after loop is gone; deep load once for decisions"
    status: completed
  - id: phase-04-path-peel-core
    content: "Move Path I/O out of eliotapp/core/ into infrastructure (or application compose)"
    status: completed
  - id: phase-05-locator-authority
    content: "Presentation dual-read helpers call locator only; delete parallel path math in routes"
    status: completed
  - id: phase-06-catalog-home
    content: "workproduct/catalog.json locked home; shrink dual-read; fix UI copy still saying tools/runs"
    status: completed
  - id: phase-07-real-cli
    content: "eliotapp/cli hillclimb + inspect operators; skill scripts become thin wrappers"
    status: completed
  - id: phase-08-http-boundary
    content: "Optional import-linter: presentation ↛ application hillclimb writers"
    status: cancelled
  - id: phase-09-closeout
    content: "Update STATE/AGENTS/plans index; gate record; archive this plan when green"
    status: completed
isProject: false
---

# Eliotapp SYNTHESIS peel

**Plan only until human gate.** Do not implement until accepted.

Sources: `handoff/ELIOTAPP-SYNTHESIS-PEEL-HANDOFF.md`, `tools/drafts/architect-eliotapp/SYNTHESIS.md`, ADR 005.

Phase detail files (optional depth): [eliotapp_synthesis_peel/](eliotapp_synthesis_peel/overview.md).

## Locked folder decision

Keep ADR 005 **sibling** homes:

```text
eliotapp/       # sole Eliot code (import eliotapp)
workproduct/    # sole Eliot data
eliotworkflow/  # reference engine markdown — not a product home
```

Do **not** nest under one root `eliot*` umbrella. Do **not** rename `workproduct/` in this plan.

The “four Eliot folders” look is mostly residue (`EliotWF/` orphan gitlink + `eliotwf.egg-info/`) plus the intentional `eliotworkflow/` reference tree. Phase 00 removes the residue.

| Path | Role |
|------|------|
| `eliotapp/` | Intentional sole code home |
| `workproduct/` | Intentional sole data home |
| `eliotworkflow/` | Intentional reference markdown |
| `EliotWF/` | Accidental orphan gitlink (`160000`, no `.gitmodules`) |
| `eliotwf.egg-info/` | Accidental setuptools residue |

## Scope

**In:** root hygiene; inspect split; list vs deep; kill `loop.py`; Path peel from core; locator authority in presentation; catalog home + UI copy; real `eliotapp/cli`; optional import-linter; docs closeout.

**Out:** re-evacuate / move under `src/`; umbrella nesting; `workproduct` rename; day-one Protocols; HTTP hillclimb mutation; permanent `loop.py` shim; draft-merge product work.

## Alternatives (folder)

| Option | Verdict |
|--------|---------|
| A. Keep siblings; delete residue | **Chosen** |
| B. Nest under one `eliot*` umbrella | Rejected (ADR + packaging churn) |
| C. Rename `workproduct/` → `eliot-*` | Deferred preference after hygiene |
| D. Data under `eliotapp/workproduct/` | Rejected |

## Phase 00 — Root hygiene

**Goal.** Clear fake Eliot roots and scrub agent prose that still teaches `src/eliotwf_skills`.

**Changes.** After human OK on content check: remove `EliotWF/` gitlink + nested tree; delete `eliotwf.egg-info/` and `src/eliotwf.egg-info/`; scrub `.cursor/skills/**` stale import homes; keep `eliotworkflow/` as reference-only.

**Verify.** `git ls-files -s EliotWF` empty; no egg-info residue; pytest green.

## Phase 01 — Inspect split

**Goal.** Callers pass `run_id` + locator. Store loads. Core decides. No public `inspect_run(run_dir: Path)`.

**Today.** `eliotapp/application/workflow/run_state.py` `inspect_run(run_dir: Path)`. SDK: `tools/sdk_climb_lib.py`. There is **no** `eliotapp/core/progression.py` yet — create it in this phase (do not hunt for an existing module).

**Changes.** Store → `InspectedRun`/`RunSnapshot`; extract pure decide into new `core.progression`; rewrite compose + SDK. Optional: `RunHandle` (validated slug) only via locator (SYNTHESIS c3 graft).

**Verify.** Pytest inspect/run_state/SDK paths; CLI/SDK smoke on a fixture run.

## Phase 02 — Kill loop.py

**Goal.** Delete `eliotapp/application/workflow/loop.py` in the same wave as every importer rewrite. No permanent shim.

**Why before list-vs-deep.** `run_index` / hillclimb list paths still import `loop.run_status`. Kill the facade first so list work does not rewrite the same imports twice.

**Callers (19 files, verified).** App: `run_index.py`, `hillclimb_runs.py`. CLI: hillclimb_cli `{run,run_parsers,discrimination,preference}.py`. Hook: `validate_skills_module.py`. Tools: `audit_runs.py`, `rescore_run.py`, `prepare_sdk_live_probe.py`. Tests: 9 under `tests/`.

**Verify.** `rg workflow.loop` empty on active tree (ignore nested `EliotWF/`); full pytest; one hillclimb_cli smoke.

## Phase 03 — List vs deep

**Goal.** Cheap `RunCard` (or projected `IndexedRun`) for list; deep snapshot once for decisions.

**Changes.** `run_index.py` / dashboard must not force full inspect per row. `run_status` becomes a projection over loaded facts (owning module after phase 02), not a second filesystem crawler.

**Verify.** Pytest run_index / presentation list; TestClient GET runs index.

## Phase 04 — Path peel from core

**Goal.** No Path I/O under `eliotapp/core/`.

**Files.** `core/eliot/scorecard.py`, `core/distiller/style_blocks.py`, `core/evaluator/{calibration,cast_aliases,content_adherence}.py` → move file helpers to infrastructure / application compose.

**Verify.** Grep Path under core clean; pytest those modules; score/adherence write still lands.

## Phase 05 — Locator authority

**Goal.** Routes call `WorkProductLocator.resolve_run_dir` / `iter_run_dirs` only.

**Changes.** Delete `_extra_run_bases` / `_resolve_run_dir` parallel math in `presentation/routes/runs.py`.

**Verify.** Pytest presentation runs; TestClient GET `/` and `/runs/<slug>` still dual-read `tools/runs` via locator.

## Phase 06 — Catalog home + UI copy

**Goal.** `workproduct/catalog.json` is the locked catalog home. UI stops teaching `tools/runs/` as the only home.

**Facts.** Neither `workproduct/catalog.json` nor `sources/catalog.json` exists on disk yet. Live runs still under `tools/runs/`; `workproduct/runs/` is essentially empty. Dual-read stays until a deliberate run migrate.

**Changes.** Create/prefer catalog under workproduct; shrink dual-read inside locator; update templates (`wizard.html`, `_done_stub.html`, `runs/index.html`, etc.).

**Verify.** Pytest catalog/wizard; TestClient or control-ui smoke.

## Phase 07 — Real eliotapp/cli

**Goal.** `python -m eliotapp.cli …` runs hillclimb + inspect. Skill scripts become thin wrappers.

**Today.** `eliotapp/cli/__main__.py` is a stub pointing at `.cursor/skills/workflow/scripts/hillclimb_cli`.

**Verify.** `python -m eliotapp.cli --help` + one non-mutating inspect; pytest green.

## Phase 08 — HTTP boundary (optional)

**Goal.** Import-linter (or equivalent): presentation ↛ hillclimb writers. Skip if tooling cost exceeds value.

**Verify.** Contract fails on forbidden import; pytest still green.

## Phase 09 — Closeout

**Goal.** STATE + gate record + archive this plan when green.

**Verify.** Full pytest; docs match reality.

## Verification (every phase)

```powershell
$env:PYTHONPATH="."
python -m pytest tests/ -q
```

Expect ~481 passed, 1 skipped (current master baseline).

## Open questions (human)

1. Is orphan `EliotWF/` safe to delete after a quick content check?
2. After phase 00, still want `workproduct/` renamed to include `eliot`?
3. How short is the catalog dual-read window once `workproduct/catalog.json` exists?
4. Later cleanup for `eliotworkflow/` name/location, or leave at root?

## Phase order note (vs handoff protocol-2)

Handoff listed inspect → kill-loop → list. This plan matches that for those three. Locator is before catalog (boundary first). Real CLI is late (wrap finished seams). Hygiene is phase 00 (handoff optional → promoted).

## Definition of done

- `loop.py` gone; no Path I/O in core; catalog under `workproduct/`; presentation uses locator only; real CLI; root no longer shows orphan `EliotWF/` / egg-info as extra Eliot homes.
