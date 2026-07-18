(def-ref emulation-prompts
  (linked-from protocol-2-phases phase-4)

  (step 4 emulation-prompts
    (goal "Numbered ready-to-use prompts for new seed drafts or ELIOT emulate. One prompt per style candidate from phase 3.")
    (posture "Default toward payload + craft direction → new seed drafts under the chosen voice — not pastiche or lost-chapter unless the user asks for that."))

  (section per-prompt-structure
    (artifact per-prompt-template))

  (section rules
    (rule 1 "NEVER use source text vocabulary in the prompt.")
    (rule 2 "Each prompt must produce recognizably DIFFERENT output from the others.")
    (rule 3 "Prompts must be usable even if the user has not yet analyzed the suggested work.")
    (rule 4 "Reference payload facets (thesis, tensions, dwell targets), not style texture from a passage.")
    (rule 5 "Prefer new-piece framing (seed drafts carrying the payload) over lost-chapter pastiche unless the user asked for pastiche.")
    (rule 6 "After the numbered list, note: The Thematic Payload below is also compatible with IRIS for image generation if you reach that stage."))

  (section optional-sidecar
    (write "emulation-prompts.json in the distiller run folder when recording a session")
    (artifact emulation-prompts-schema)
    (note "No Python validator in this gate; prose output is authoritative."))

;; --- artifacts ---

## per-prompt-template

```
Write a new [NarrativeShape] in [Author]'s voice (style block), carrying this thematic payload — not a lost chapter of [Work] unless asked.
[SceneSeed mapped to this author's specific affordances].
Dwell on [DwellTargets mapped to author].
Compress [CompressionTargets].
The governing tension is [payload tension mapped to author's tension].
[Archetype binding instruction if relevant].
For best results, first analyze [Work/Location] with ELIOT (or reuse a named style block).
```

## emulation-prompts-schema

```json
{
  "prompts": [
    { "author": "...", "work": "...", "location": "...", "text": "..." }
  ]
}
```
