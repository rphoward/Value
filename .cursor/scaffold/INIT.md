# Scaffold init (`.cursor/`-first workflow)

Start a new repo from the Twins layout without copying the full codebase.

**This repository (EliotWF):** Eliot code lives at root `eliotapp/` and data at
`workproduct/` — not under `src/`. Scaffold init still fills `src/<slug>/` for **non-Eliot**
products copied from this layout. Do not retarget Eliot into `src/`.

## Workflow

1. Copy `.cursor/` into an empty folder (exclude `.cursor/plans/` if you do not need plan files).
2. Ask AI to scaffold `src/twins/`, `tests/`, and `pyproject.toml` using `.cursor/rules/repo-layout.mdc` and layer rules. Paths will still say `twins` — that is expected; init retargets later.
3. Run init (pass `-ProductSlug`; no need to edit the manifest first):

```powershell
.\.cursor\scaffold\scaffold-init.ps1 -ProductSlug myapp
```

Optional flags:

| Flag | Purpose |
|------|---------|
| `-GitHubRemote URL` | `git remote add origin` when none exists |
| `-InitGit` | `git init` (requires `.gitignore`) |
| `-SkipVerify` | Skip `pip install -e .` and unittest |
| `-UseGh` | `gh repo create` when `gh` is available |

4. Verify:

```powershell
pip install -e .
$env:PYTHONPATH = 'src'
python -m unittest discover -s tests -v
```

## Manifest during scaffold

`.cursor/scaffold/manifest.json` in the copied folder still has `twins` values. That is correct for the AI scaffold phase. `scaffold-init.ps1` reads the manifest, retargets paths and globs to your slug, and rewrites the manifest. You can pass `-ProductSlug` instead of editing the file by hand.

## What `.cursor/` does not include

Copy `.cursor/` only. AI (or you) must still create:

| Item | Notes |
|------|--------|
| `src/<slug>/` | Four layers: `core/`, `application/`, `infrastructure/`, `presentation/` plus `presentation/routes/`, `templates/`, `browser_assets/` |
| `tests/` | At least one passing unittest; optional portable `test_scaffold.py` from Twins |
| `pyproject.toml` | Editable install; package under `src/` |
| `tools/start-<slug>.ps1` | Local dev launcher; retarget renames from `start-twins.ps1` |
| `AGENTS.md` | Repo map for agents (Twins template links to this scaffold doc) |
| `CONTEXT.md` | Domain glossary at repo root |
| `.gitignore` | Required if you pass `-InitGit` |
| `docs/adr/` | Optional; `domain-context.mdc` globs expect it when present |

Rules, skills, and scaffold tooling travel inside `.cursor/` (including `README.md` and this file). No `tools/scaffold*`, root `scaffold.manifest.json`, or `docs/SCAFFOLD-*` needed.

## What retarget does

`.cursor/scaffold/retarget.py` scans paths listed in `.cursor/scaffold/retarget-paths.json` (longest-token-first replaces, explicit exclude list). It renames `src/<old>/`, `tools/start-<old>.ps1`, updates `repo-layout.mdc` protocol-1, and rewrites `.cursor/scaffold/manifest.json`.

Do not hand-edit rule globs for a new slug. Use retarget or init.

Excluded from text scan: `conduct.mdc`, `safety.mdc`, authoring rules, `grillwithdocs/**`, and scaffold tooling itself.

## Manual dry-run (no AI)

Use the fixture tree as a minimal repo:

```powershell
$dest = Join-Path $env:TEMP "scaffold-dry-run"
Remove-Item $dest -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item -Recurse tests\fixtures\retarget_mini $dest
Copy-Item -Recurse .cursor\scaffold (Join-Path $dest ".cursor\scaffold")
Set-Location $dest
python .cursor\scaffold\retarget.py --from twins --to myapp --repo-root .
```

Inspect globs in `.cursor/rules/`, `.cursor/scaffold/manifest.json`, and `src/myapp/`.

## Twins maintainers only

`maintainer-refresh-template.ps1` refreshes a CHANGEME manifest template inside Twins after rule or skill changes. It is **not** part of the copy workflow — never run it before copying `.cursor/` out.

