# How to use “prompt suite → skill” (human tutorial)

This note sits next to the technical plan. The complete standalone toolkit and its docs live in `tools/prompt-suite-compile/`. Prefer that folder’s `README.md`, `TUTORIAL.md`, and `bootstrap.md` when you copy the pack to another repo.

## What this is

You already built paced skills by hand (`value`, then `lean-mvp`). The toolbox under `tools/prompt-suite-compile/` scaffolds the next book-shaped doc into a draft skill. You (with poteto-mode) fill in real questions before promote.

`value` and Values stay protected. The compiler refuses the slug `value`.

## Run it in this repo (today)

### 1. Scaffold a draft

In PowerShell from the repo root:

```powershell
python tools/prompt-suite-compile/compile.py scaffold `
  --source "docs/lean-product-playbook-prompt-suite.md" `
  --slug my-new-skill `
  --out tools/drafts/skills
```

That creates `tools/drafts/skills/my-new-skill/` with:

- extracted `knowledge-base.json`
- session scripts (portable runtime)
- stub atoms (`S01`/`G01` …) so scripts already run
- draft `SKILL.md` and module references

### 2. Check the question tree

```powershell
python tools/prompt-suite-compile/audit_dag.py tools/drafts/skills/my-new-skill
```

You want `"ok": true` for standard mode.

### 3. Expand the curriculum (agent + you)

Open `tools/prompt-suite-compile/FOR_AGENTS.md` in Cursor. Turn on `/poteto-mode`. Tell the agent the draft path. Ask it to replace stub atoms with real questions from the source doc. Re-run the audit until green.

You can also say you want the **scripted-skill-from-doc** skill. It points at the same runbook.

### 4. Smoke without chatting

```powershell
.\tools\prompt-suite-compile\smoke.ps1 -Draft tools/drafts/skills/my-new-skill
```

### 5. Promote only when you say so

```powershell
python tools/prompt-suite-compile/promote.py tools/drafts/skills/my-new-skill
```

That copies into `.cursor/skills/my-new-skill/`. Add `--also-skills` only if you also want `skills/my-new-skill/`.

## Run an existing skill (unchanged)

- **Value:** ask to grill a value proposition. Sessions under `workproduct/value-proposition/`.
- **Lean MVP:** ask for the lean product playbook. Sessions under `workproduct/lean-mvp/`. May import from a matching value session.

Those skills do not need the toolbox to run.

## Fresh / other repo

1. Copy `tools/prompt-suite-compile/` into that repo.
2. Optionally enable pstack in `.cursor/settings.json` (see `bootstrap.md`).
3. Drop your suite markdown under `docs/`.
4. Open `FOR_AGENTS.md`, give source path + slug, use poteto-mode.
5. Scaffold → audit → expand → smoke → promote with consent.

## Honest limits

- Stub atoms are placeholders. A shippable curriculum still needs the poteto pass.
- Express pacing skips material on purpose. Prefer standard for full coverage.
- A weak source doc still yields a weak skill.

## Where things live

| Path | Role |
|------|------|
| `tools/prompt-suite-compile/README.md` | Operator commands |
| `tools/prompt-suite-compile/FOR_AGENTS.md` | Agent runbook |
| `tools/prompt-suite-compile/bootstrap.md` | Other-repo install |
| `.cursor/skills/scripted-skill-from-doc/` | Meta-skill entry |
| `.cursor/plans/prompt-suite-to-skill/overview.md` | Design plan |

## One-line summary

Scaffold with `compile.py`, finish atoms under poteto-mode via `FOR_AGENTS.md`, promote only after you consent. Never overwrites `value`.
