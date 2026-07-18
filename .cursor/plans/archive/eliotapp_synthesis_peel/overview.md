# Eliotapp SYNTHESIS peel — overview

Back-link: [eliotapp_synthesis_peel.plan.md](../eliotapp_synthesis_peel.plan.md)

## Context

Evacuate into `eliotapp/` + `workproduct/` is closed on `master` (PR #1). The SYNTHESIS peel still owns locator-first inspect, kill `loop.py`, Path out of core, real `eliotapp/cli`, and catalog under `workproduct/`.

After evacuate, the repo root still shows multiple Eliot-named entries. Observed:

| Path | Role |
|------|------|
| `eliotapp/` | Intentional sole code home |
| `workproduct/` | Intentional sole data home |
| `eliotworkflow/` | Intentional reference markdown (not importable product) |
| `EliotWF/` | Accidental orphan gitlink (`160000`, no `.gitmodules`) |
| `eliotwf.egg-info/` | Accidental setuptools residue |

The nesting intuition (one umbrella folder holding code + data) fights ADR 005, packaging (`include = ["eliotapp*"]`), and the handoff ban on reopening homes. Clarity comes from deleting residue and keeping the two intentional homes as siblings.

## Scope

**In**

1. Root hygiene (gitlink + egg-info).
2. All eight handoff must-plan peel items (inspect split, kill loop, list vs deep, Path peel, real CLI, catalog home, locator authority, optional HTTP boundary).
3. Docs/STATE closeout for this track.

**Out**

- Re-evacuating or moving code back under `src/`.
- Nesting `eliotapp/` layers under a new parent folder.
- Renaming `workproduct/` → `eliot-workproduct` (open preference; not this plan).
- Day-one `Protocol` ports.
- HTTP hillclimb mutation.
- Permanent `loop.py` shim.
- Product draft-merge (crossover) work.

## Constraints

- ADR 005 + `repo-layout.mdc`: sibling `eliotapp/` + `workproduct/`.
- Migrate callers then delete legacy API in one wave.
- Verify each phase with `pytest`; UI phases smoke GET `/` and `/runs/<slug>`; CLI phases use `control-cli` or existing hillclimb_cli smoke.
- Dual-read of `tools/runs` stays inside the locator/store only until catalog/runs migrate complete.

## Alternatives (folder shape)

| Option | Verdict |
|--------|---------|
| A. Keep siblings; delete residue (chosen) | Matches ADR; smallest diff; fixes the visual mess |
| B. Nest `eliotapp/` + `workproduct/` under one root umbrella | Rejected: breaks import package layout, reopens locked homes, large rename for optics |
| C. Rename `workproduct/` → `eliot-workproduct` only | Deferred preference: needs ADR + locator + rules; optional later if sibling clarity is still insufficient after phase 0 |
| D. Collapse data under `eliotapp/workproduct/` | Rejected: mixes package tree with durable artifacts |

Arena candidate-3 (hygiene-first) agreed on A and argued catalog + locator before inspect. This plan keeps handoff order (inspect early) so the densest seam lands soon. Pull phases 05–06 forward only if dual-read confusion blocks the inspect migrate.

## Applicable skills / non-negotiables

- **how** over each subsystem before editing it.
- **migrate-callers-then-delete-legacy-apis** on `loop.py` and Path-in-core APIs.
- **boundary-discipline** (Path at store; pure decide in core).
- **prove-it-works** (pytest + surface smoke per phase).
- `/deslop` before each commit; **unslop** on prose.
- **babysit** after opening the PR.
- **control-cli** / **control-ui** for CLI and browser surfaces.

## Phases

Authoritative body: [../eliotapp_synthesis_peel.plan.md](../eliotapp_synthesis_peel.plan.md). Detail files below may lag; prefer the `.plan.md`.

1. [phase-00-root-hygiene.md](phase-00-root-hygiene.md)
2. [phase-01-inspect-split.md](phase-01-inspect-split.md)
3. [phase-03-kill-loop.md](phase-03-kill-loop.md) — **order note:** kill-loop is plan phase 02 (before list)
4. [phase-02-list-vs-deep.md](phase-02-list-vs-deep.md) — **order note:** list-vs-deep is plan phase 03 (after loop kill)
5. [phase-04-path-peel-core.md](phase-04-path-peel-core.md)
6. [phase-05-locator-authority.md](phase-05-locator-authority.md)
7. [phase-06-catalog-home.md](phase-06-catalog-home.md)
8. [phase-07-real-cli.md](phase-07-real-cli.md)
9. [phase-08-http-boundary.md](phase-08-http-boundary.md)
10. [phase-09-closeout.md](phase-09-closeout.md)

See also [testing.md](testing.md).

## Verification (project-level)

```powershell
$env:PYTHONPATH="."
python -m pytest tests/ -q
```

Expect full suite green (currently ~481 passed, 1 skipped on master after evacuate).

## Open questions (human)

1. Is orphan `EliotWF/` safe to delete after a quick content check, or do you need anything recovered from that nested tree first?
2. After phase 00, do you still want `workproduct/` renamed to include `eliot`, or is sibling clarity enough?
3. How short should the catalog dual-read window be once `workproduct/catalog.json` exists?
4. Should a later cleanup rename or relocate `eliotworkflow/` (reference tree only), or leave it at root forever?

## Implementation guidance

Implement one phase at a time. Do not start phase N+1 until phase N verification is green. Prefer eight-to-ten small phases over one fat peel. Keep a decision trail if the wave spans multiple PRs (`show-me-your-work`).
