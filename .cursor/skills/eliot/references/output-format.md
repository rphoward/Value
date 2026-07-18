(def-ref output-format
  (linked-from protocol-3-output)

  (dense-style-block-format (artifact dense-style-block-template))

  (OutputInstructions
    (purpose "ensure style block renders as standalone artifact")

    (Compactness
      (principle "style block = spec not essay; density IS fidelity")
      (FieldBudget "one line default; 2-3 ONLY where voice depends on it")
      (Notation "spec-phrases not sentences; semicolon-chained; use Extensions :compact forms")
      (CastBudget "full entry only for voices speaking at length; minor voices = one line")
      (BlockBudget "core (all sections except CAST) <= ~120 lines; add ~15 per full CAST entry + 1 per minor voice — block length scales with enumerated voices, nothing else; if over: demote borderline voices per CastBudget first, THEN compress SURFACE + WORLDVIEW")
      (Test "delete a word — emulation unchanged? then delete it"))

    (AnalysisOutput
      (structure "two parts — explanation THEN style block")
      (Part1
        (label "BRIEF explanation (2-4 sentences max)")
        (content "summary of what was analyzed and key observations")
        (format "plain prose, no code fence"))
      (Part2
        (label "DENSE STYLE BLOCK as standalone code block")
        (format "MUST be wrapped in triple backticks as single fenced code block")
        (content "complete style block following DENSE STYLE BLOCK FORMAT")
        (purpose "copy-pasteable style guide for AI emulation"))
      (example "Here is the style analysis for [Author]: [2-4 sentence summary] [TRIPLE BACKTICKS — open fence] [complete style block per DENSE STYLE BLOCK FORMAT] [TRIPLE BACKTICKS — close fence]"))

    (EmulationOutput
      (structure "style block reference THEN generated content")
      (Part1
        (label "Style block being used (if not already visible)")
        (format "code block if showing reference; omit if already present"))
      (Part2
        (label "Generated content in author's voice")
        (format "prose, no code fence")
        (content "text written following the style block specifications")))

    (CriticalRule
      (always "the Dense Style Block MUST be inside triple backticks")
      (never "do NOT embed style block in prose or mix with explanation")
      (why "style block must be extractable as standalone document"))))

;; --- artifacts ---

## dense-style-block-template

```
[AUTHOR] ([Work/Period])
--------------------------------------------------------------------------------
OCEAN:
+---+-------+------------------------------------------+
| O | ##    | I:## Aes:## Em:## Adv:## Int:## Lib:##   |
| C | ##    | SE:## Ord:## Dt:## AS:## SD:## Cau:##    |
| E | ##    | W:## G:## A:## AL:## ES:## Ch:##         |
| A | ##    | Tr:## SF:## Alt:## Comp:## Mod:## TM:##  |
| N | ##    | Anx:## Ang:## Dep:## SC:## Imm:## V:##   |
+---+-------+------------------------------------------+

SURFACE: [prose texture, sentence patterns, register, paragraph behavior]

ENVIRONMENT:
  function: [backdrop / witness / pressure / fragile container]
  scale_contrast: [smallness vs. vastness]
  objects: [symbolic weight carriers]
  intrusions: [measuring/interrupting sounds or events]
  trajectory: [change or static-by-design; what shifts mark; tempo]

DEIXIS: [POV, person, spatial orientation, temporal orientation, drift]
  narrator: [frequency; function; timing]
  tempo: [scene/summary/ellipsis/pause/stretch — dominant; what earns scene; skip marking]

PROSODY: [rhythm patterns, cadence sources, stress patterns]
  sentences: [length, variation, departure function, internal structure]
  fingerprint: [%short/%med/%long; punct per-100w , ; — ? !; dialogue:narration]
  paragraph_modes: [qualitative paragraph shapes — length + internal rhythm + job;
    prose only; NO dist …% shares; short declaratives are sentence-level departures inside
    paragraphs, not a stack of one-line paragraphs; never one template only when source shapes differ]

DNA:
  signature: [distinctive moves, recurring techniques]
  voice_sample: [2-3 characteristic narration constructions — Tier1 clause-level anchor]
  tension: [productive oppositions]
  avoids: [what this author never does]
  commits: [authorial vices — faults author reliably makes: editor-cut repetitions,
    lopsided sentences, pet constructions, digressive habits.
    DOSAGE (mandatory): source frequency, never amplified; noticed on first read = overdosed]
  images:
    inventory: [recurring image clusters]
    deployment: [how images enter — as-argument / as-eruption / as-accumulation /
      as-contrast / as-refrain / as-bridge; what work they DO]
  dwells: [expansion targets] | compresses: [abbreviation targets] | tone=[register]
  detail: [type, level, scope]
  intertextual: [sources; mode; density]

WORLDVIEW:
  metaphysics: [nature of reality]
  epistemology: [how knowledge works]
  axiology: [value hierarchies]
  cultural: [traditions engaged]
  anthropology: [theory of human nature]

ARCHETYPE MAPPING:
  primary: [Duality / Cycle / Connection / Inquiry]
  active_bindings: [specific operations]
  crystallization_targets: [Physics manifestations]

ARC:
  shape: [family + variant — heros-journey only if demonstrated]
  movement: [what actually moves]
  resolution: [closed / open / refused / ironic / deferred / cyclic]
  scale: [whole-work vs. scene arcs, if they differ]

DIALOGUE DYNAMICS:
  dominance: [pattern]
  secondary_function: [role of non-dominant voices]
  must_land: [yes/no]
  response_style: [rhetorical strategy]
  response_type: [structural form]
  response_weight: [what it weighs against]

CAST:
  [CHARACTER]:
    OCEAN_delta:
    +---+-----+------------------------------------------+
    | O | +/- | [only facets that diverge significantly] |
    | C | +/- | ...                                      |
    | E | +/- | ...                                      |
    | A | +/- | ...                                      |
    | N | +/- | ...                                      |
    +---+-----+------------------------------------------+
    worldview: [character beliefs — may contradict author]
    stance: [derived from archetype + worldview]
    rhetoric: [argument patterns]
    idiolect: [vocabulary tics register]
    voice_sample: [2-3 characteristic constructions]
    function: [role in orchestration]
  [MINOR-VOICE]: delta=[facets]; idiolect=[one marker]; function=[role]

orchestration: [how CAST members embody ideas; author's relationship to opposition]

(Nonfiction sources: remap fields per GenreAdaptation; omit fields that remap to nothing.)
```
