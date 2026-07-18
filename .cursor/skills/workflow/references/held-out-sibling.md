(def-ref held-out-sibling
  (linked-from protocol-7-one-command-session)

  (when
    (after "style-block.md exists")
    (before "first discrimination job-open")
    (note "init may precede held-out; Exa failure must not block init"))

  (vocabulary
    (mode "exposition | memoir | dialogue | lyric — intra-work register from SURFACE/DEIXIS tempo")
    (not "distiller literary/essay/technical register")
    (forbidden 'conflating-brief-mode-with-distiller-register))

  (brief-card
    (emit "tools/runs/<slug>/held-out-brief.md")
    (fields-from "DEIXIS ENVIRONMENT DNA only — do not dump the whole block")
    (artifact brief-card-template))

  (exa-query
    (positives "work + chapter/mode cues + want line")
    (excludes "opposite POV, wrong mode, named chapters to avoid")
    (prefer "continuous public-domain prose pages")
    (fetch "2–3 candidates into tools/runs/<slug>/.scratch/held-out-cand-*.txt")
    (forbidden "full-book dumps that open on wrong-register chapters without slicing"))

  (gate
    (cli "python .cursor/skills/workflow/scripts/held_out_gate.py --source tools/runs/<slug>/source.txt --candidate <path> [--run-dir tools/runs/<slug>] — run-dir defaults to source parent when source is source.txt; always writes held-out-gate.json")
    (order "first pass wins; prefer no held-out over wrong-register held-out")
    (user-supplied "still run gate; on fail refuse as genuine — fall back to source.txt and print reasons")
    (overlap "reject near-duplicates of source.txt")
    (write-on-pass "eliotapp.application.workflow.prepare.write_held_out(run_dir, text) → held-out.txt")
    (forbidden "prepare --force just to attach held-out"))

  (artifacts
    (always "held-out-brief.md")
    (always "held-out-gate.json — chosen candidate or last failure summary")
    (on-pass "held-out.txt"))

  (length
    (preferred "800–1200 words")
    (floor 400)
    (hard-max 1200 :gate-fail)))

;; --- artifacts ---

## brief-card-template

```
work: <from source / discovery>
want: <one line from DNA signature + ENVIRONMENT function>
pov: <we | I | mixed — from DEIXIS>
mode: <exposition | memoir | dialogue | lyric — from SURFACE/DEIXIS tempo>
exclude: <opposite POV, wrong mode, named chapters to avoid>
length: 800–1200 words
```
