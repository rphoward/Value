# Full-workflow webapp — testing

Back-link: [overview.md](overview.md)

## Static

```powershell
pytest tests/ -q
```

Focus areas as phases land:

- Job store atomic one-job-per-slug
- sdk-climb import fix + spawn wiring
- Presentation canvas / jobs / onboarding routes
- Invent must not create `scores.json`

## Runtime (UI phases)

```powershell
.\tools\start-eliotwf.ps1
```

Then control-ui against `http://127.0.0.1:8000`:

1. Create / open run
2. Studio-lite when empty
3. Stage passage / analyze (job or paste)
4. Invent seeds without scores
5. Improve; JobRail story; sparkline; pause/resume
6. Pick best draft

## Disk ownership proof

After an improve job: HTTP-owned files are job request, ledger events, human revisions, best-draft marker. `scores.json` mtime/content changes only while SDK/CLI runs.
