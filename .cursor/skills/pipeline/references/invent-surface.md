(def-ref invent-surface
  (linked-from protocol-0b-invent-session)

  (section path-callouts
    (title "Obvious draft paths")
    (require "After seeds, list repo-relative paths in chat for every draft-v1*.md, content-brief.md, craft-brief-v1.md, style-block.md, and INVENT.md.")
    (forbidden 'burying-paths-only-in-transcript-without-callout))

  (section invent-md
    (path "tools/runs/<slug>/INVENT.md")
    (fields
      (style-block-id "from style-block-id.txt")
      (seeds "bullet list of draft-v1a.md … paths")
      (best "omit or leave unset until the user picks a favorite; then set to that path"))
    (artifact invent-md-template)
    (note "Filename INVENT.md is the durable session index; human-facing chat may say seed drafts / new piece without saying invent."))

  (section cleanup-ask
    (when "tracking/resume sidecars exist in the invent folder (e.g. job-* or scores.json from a later promote)")
    (ask "light: whether to remove resume/tracking sidecars only")
    (never-delete-without-yes
      ["draft-v*.md" "content-brief.md" "craft-brief-v*.md" "style-block.md"
       "style-block-id.txt" "thematic-payload.sexp" "source-excerpt.md" "INVENT.md"
       "discovery.json" "passage-meta.json" "rough-input.md"])
    (note "Invent v1 creates few resume sidecars; skip the ask when none exist."))

;; --- artifacts ---

## invent-md-template

```markdown
# Seed drafts session

- **style-block-id:** <id>
- **run:** tools/runs/<slug>/

## Seeds

- tools/runs/<slug>/draft-v1a.md
- tools/runs/<slug>/draft-v1b.md
- tools/runs/<slug>/draft-v1c.md

## Best

(unset until user picks)
```
)
