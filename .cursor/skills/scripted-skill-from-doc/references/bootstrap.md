# Bootstrap with this harness skill

This skill folder is the full pack in standard layout. It travels inside `.cursor/skills/scripted-skill-from-doc/`.

## Checklist

1. Confirm Python 3.10+ is available: `python --version`.
2. From the target repo root (the one that contains `.cursor`), run:

```text
python .cursor/skills/scripted-skill-from-doc/scripts/compile.py check
```

Expect `"ok": true`.

3. Optional: enable pstack in `.cursor/settings.json` if you want poteto-mode:

```json
{
  "plugins": {
    "pstack": {}
  }
}
```

4. Open `references/for-agents.md` and give the agent a source path plus a skill slug (never `value`). Follow `references/curriculum-synthesis.md` for atoms.

More detail: `references/readme.md` and `references/tutorial.md`.
