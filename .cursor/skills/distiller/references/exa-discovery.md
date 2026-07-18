(def-ref exa-discovery
  (linked-from protocol-2-phases phase-3 protocol-4-contracts)

  (section exa-mcp
    (title "exa MCP — author and passage discovery")
    (use "plugin-exa-exa tools")
    (note "Python does not call exa; the agent does at phase 3."))

  (section tool-selection
    (confirm-work-exists
      (tool web_search_exa)
      (query "Natural language: ideal page describing the chapter or scene"))
    (pull-excerpt
      (tool web_fetch_exa)
      (url "From search result with substantive prose")))

  (section originating-constraints
    (rule "Originating prompt constraints win over default Exa query templates.")
    (example "first chapter of All the Pretty Horses by Cormac McCarthy → Exa query and PassageCandidate must use that author/work/location")
    (recommend "Name one best match; list a few probables when search returns options; user may override."))

  (section search-pattern
    (step 1 "Pick the best author from phase 3 prose list (highest thematic overlap + accessible passage), unless the originating prompt already named author/work/location.")
    (step 2 "web_search_exa with query shaped by originating constraints, else: [Author] [Work] [chapter or scene] full text excerpt public domain")
    (step 3 "From results, choose a URL with continuous prose (Project Gutenberg, Wikisource, or reputable excerpt).")
    (step 4 "web_fetch_exa on that URL. Extract 200–2000 words suitable for ELIOT analyze. Target 800–1200 words. Never default to ~5000-word pulls.")
    (step 5 "Record PassageCandidate: author, work, location, source_url, excerpt_hint (first sentence or scene label), provenance: web, optional word_count."))

  (section public-domain-preference
    (preferred "Exa on public-domain sources")
    (not-required "Technical and modern registers often need owned corpus.")
    (when-weak-truncated-paywalled
      (step 1 "Still record the best author/work/location in discovery.json.")
      (step 2 "Set passage_resolution: needs_owned_corpus in session notes (or distiller run README).")
      (step 3 "Proceed to resolve_passage catalog lookup, file ref, or paste per resolve-passage.")))

  (section resolve-passage
    (after Exa)
    (step 1 "If the user gave an explicit file path (in or outside the repo), read it; slice to 200–2000 words; set provenance: owned or manual as appropriate; copy into source-excerpt.md.")
    (step 2 "Else if Exa succeeded, slice fetch to 200–2000 words (prefer 800–1200); set provenance: web.")
    (step 3 "Else lookup sources/catalog.json by author/work/location label.")
    (step 4 "Read local_path; slice to bounds; set provenance: owned, catalog_id, word_count.")
    (step 5 "If no usable open text, ask in plain language for a markdown paste into the run folder (provenance: manual).")
    (validate "eliotapp/core/distiller/passage_bounds.py"))

  (section held-out-sibling
    (note "Distiller owns author/passage discovery for analyze. Hillclimb owns a second Exa pull for register-matched discrimination genuine.")
    (protocol ".cursor/skills/workflow/references/held-out-sibling.md")
    (when "after style-block.md; before first job-open")
    (forbidden "using this ref as the held-out protocol — stay on author-discovery here"))

  (section smoke-gate
    (minimum-deliverable "author + passage candidate JSON — no ELIOT analyze yet")
    (artifact smoke-gate-json)
    (validate-cmd (artifact validate-command))
    (forbidden "Do NOT run ELIOT analyze in the distiller smoke gate."))

;; --- artifacts ---

## smoke-gate-json

```json
{
  "topic": "...",
  "authors": [ { "author": "...", "work": "...", "location": "...", ... } ],
  "passage": {
    "author": "...",
    "work": "...",
    "location": "...",
    "source_url": "...",
    "excerpt_hint": "...",
    "provenance": "web",
    "word_count": 950
  }
}
```

## validate-command

```bash
python .cursor/skills/distiller/scripts/discover_format.py validate --json <file>
```
