# Scaffold a new repo (quick start)

Start a new project from the Twins layout without copying the full codebase.

## What you copy

Copy only `.cursor/` into an empty folder. You do not copy `src/`, `tests/`, or `pyproject.toml` — AI scaffolds those next.

Optionally skip `.cursor/plans/` if you do not need plan files.

The copied `.cursor/scaffold/manifest.json` will still say `twins` — that is correct until init retargets your slug.

## Steps

1. **Copy** `.cursor/` into your empty repo folder (optionally skip `plans/`).
2. **Scaffold the code tree** — paste the [suggested AI prompt](#suggested-ai-prompt) below. AI creates `src/twins/`, `tests/`, `pyproject.toml`, and supporting files using `.cursor/rules/repo-layout.mdc` and the layer rules. Paths will still say `twins` until init runs.
3. **Run init** when the tree is ready (pass your slug; no need to edit the manifest first):

```powershell
.\.cursor\scaffold\scaffold-init.ps1 -ProductSlug myapp
```

Optional flags: `-InitGit`, `-GitHubRemote URL`, `-UseGh`, `-SkipVerify`. See [INIT.md](INIT.md) for details.

## Verify

```powershell
pip install -e .
$env:PYTHONPATH = 'src'
python -m unittest discover -s tests -v
```

Init runs these by default unless you pass `-SkipVerify`.

## Suggested AI prompt

After copying `.cursor/` into an empty folder, paste this:

```
Scaffold a minimal Python repo from the copied .cursor/ rules.

Create:
- src/twins/ with core/, application/, infrastructure/, presentation/ (empty __init__.py where needed; presentation/routes/, templates/, browser_assets/)
- tests/ with one passing unittest
- pyproject.toml (editable install, package under src/)
- tools/start-twins.ps1, AGENTS.md, CONTEXT.md, .gitignore

Follow .cursor/rules/repo-layout.mdc and the layer rules (core, application, infrastructure, presentation). Use twins paths and import name for now — scaffold-init will retarget the slug later.

When done, run: .\.cursor\scaffold\scaffold-init.ps1 -ProductSlug <yourslug>

Do not hand-edit rule globs. Do not copy Twins product logic.
```

## Full detail

See [INIT.md](INIT.md) for retarget behavior, init flags, and dry-run fixture.

