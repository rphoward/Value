---
name: verify-value
description: >
  Drive the Value monorepo journey skills the way a user does: Values, BMG,
  Teams, and lean-mvp session scripts (init, status, next, accept, build pack,
  promote_context, milestones) in an isolated .verify-runs/ root, plus the
  optional spoke /health smoke. Use when proving a skill-script behavior
  change, sibling workproduct isolation, promote_context write gates, or spoke
  scaffold health — not for Cursor slash-command grilling itself
  (/product-spine, /value, /bmg, /teams, /lean-mvp).
---

# Verify Value

Agent-facing control surface for this monorepo's **journey skill CLIs**. Primary surfaces are the paced skills under `.cursor/skills/{value,bmg,teams,lean-mvp}/scripts/`. Secondary is the Starlette spoke at `value.presentation.app:app` (`/health` only). Product-Spine and other slash sessions are not driveable here; prove sibling script side effects instead.

Read `features/README.md` before driving. Pick one feature file and follow it literally.

## Launch

There is no long-lived Values server for skill grilling. Launch means prepare an isolated run directory, then run skill scripts through the helper.

```powershell
pip install -e .
$env:PYTHONPATH = 'src'
python .cursor/skills/verify-value/scripts/control-value.py prepare
```

Ready when stdout prints `RUN_ID=...`, `WORK_ROOT=...` (Values area), per-skill `WORK_ROOT_*=...`, and `ARTIFACTS=...`. Export `RUN_ID` for the rest of the run.

Spoke (optional, secondary features only):

```powershell
python .cursor/skills/verify-value/scripts/control-value.py spoke-start --run-id <RUN_ID> --port 8010
```

Ready when `SPOKE_URL=http://127.0.0.1:8010` prints and `GET /health` returns `ok`. Default verify port is **8010** so it does not collide with the human launcher on **8000** (`tools/start-value.ps1`).

Teardown: `cleanup` (and `spoke-stop` if you started a spoke).

## Doctor

```powershell
python .cursor/skills/verify-value/scripts/control-value.py doctor
python .cursor/skills/verify-value/scripts/control-value.py doctor --run-id <RUN_ID>
```

Must print `doctor ok`. With `--run-id`, also checks disposable work roots and, if a spoke was started for that run, `/health`.

Refuse to drive a live `workproduct/` session that this run did not create. Refuse to drive spoke port 8000 unless this run started it (helper defaults to 8010).

## Drive

```powershell
python .cursor/skills/verify-value/scripts/control-value.py cli --run-id <RUN_ID> [--skill value|bmg|teams|lean-mvp] -- <script.py> [args...]
```

Default `--skill` is `value`. Examples:

```powershell
python .cursor/skills/verify-value/scripts/control-value.py cli --run-id <RUN_ID> -- init_session.py --name "Verify Demo" --slug verify-demo
python .cursor/skills/verify-value/scripts/control-value.py cli --run-id <RUN_ID> --skill teams -- init_session.py --name "Verify Demo" --slug verify-demo
python .cursor/skills/verify-value/scripts/control-value.py cli --run-id <RUN_ID> --skill bmg -- status.py workproduct/bmg/verify-demo/session.json --sections
python .cursor/skills/verify-value/scripts/control-value.py cli --run-id <RUN_ID> -- promote_context.py workproduct/value-proposition/verify-demo/CONTEXT.product.md --dry-run
```

`init_session.py` automatically receives `--root` for the chosen skill's work area under the run. Session-relative paths are relative to the run directory (cwd).

Spoke:

```powershell
python .cursor/skills/verify-value/scripts/control-value.py spoke-get --run-id <RUN_ID> --path /health
```

## Evidence

Store under `.verify-runs/<RUN_ID>/artifacts/`. The helper writes CLI and spoke transcripts automatically (`cli-<skill>-*.txt`, `spoke-get-*.txt`, `spoke.log`).

Proof standards:

- Exercise the real skill scripts a journey agent would run, not private `_session` imports alone.
- Capture command, exit code, stdout/stderr, and resulting files (`session.json`, milestones, `CONTEXT.product.md`, run-local `CONTEXT.md` when `--apply` is used).
- For dry-run, prove no write by asserting the target file is absent or unchanged after the command.
- Do not treat unit tests as a substitute for a mapped feature drive.

## Cleanup

```powershell
python .cursor/skills/verify-value/scripts/control-value.py cleanup --run-id <RUN_ID>
```

Stops a spoke this run started, deletes disposable `workproduct/` under the run dir (all skill areas), **keeps** `artifacts/` and `meta.json`. Never delete `.verify-runs/<RUN_ID>/artifacts/`.

## Helpers

| Command | Purpose |
|---------|---------|
| `control-value.py prepare` | Create isolated run with value/bmg/teams/lean-mvp work areas |
| `control-value.py doctor [--run-id]` | Readiness for all journey skill packs |
| `control-value.py cli --run-id … [--skill …] -- <script> …` | Drive skill scripts |
| `control-value.py spoke-start/stop/get` | Optional spoke smoke |
| `control-value.py cleanup --run-id …` | Tear down scratch; keep evidence |

Invocation root: repo root of Value. Scripts live at `.cursor/skills/verify-value/scripts/control-value.py`.
