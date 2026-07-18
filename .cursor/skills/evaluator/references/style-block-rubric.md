(def-ref style-block-rubric
  (linked-from protocol-2-style-block-diff)

  (section style-block-fidelity-rubric
    (purpose "block-native rubric replacing generic quality lens — score fidelity to Dense Style Block only")
    (authority "block is authority; gorgeous draft contradicting block scores low; plain draft honoring every field scores high"))

  (section how-to-score
    (step 1 "Read block in full first. Read every field. Block is ground truth, not taste.")
    (step 2 "Read draft twice. First pass as reader for whole. Second pass per section, one block field at a time, hunting specific move that field names.")
    (step 3 "Score ten qualitative sections independently. Weak DEIXIS does not drag down WORLDVIEW. Each section stands on own evidence.")
    (step 4 "Deterministic three are not yours. SURFACE, PROSODY, CAST computed in Python from draft text. Do not score them. Do not emit them. Validator rejects whole array if emitted.")
    (step 5 "Name tier before number — UWE anti-inflation rule. Decide Sharp, Functional, Soft, or Broken first, then pick number inside band. Most honest drafts land Functional. Reserve Sharp for sections where every field visibly served.")
    (step 6 "Evidence mandatory and specific. Each entry must quote or closely paraphrase phrase from draft and name block field judged against. Good voice is not evidence. Narrator intrudes only between speeches, matching DEIXIS narrator:timing is evidence.")
    (tier-bands (load-order references/rubric.md "reused verbatim")
      (tier sharp "85-100. Every element load-bearing. Draft serves section fields with no wasted move.")
      (tier functional "60-84. Solidly working, two or three identifiable weaknesses. Competent, not exceptional.")
      (tier soft "35-59. Noticeable problems impeding fidelity. Fields honored vaguely, partially, or inconsistently.")
      (tier broken "0-34. Draft works against section. Asserts opposite of field specifies, or ignores field entirely.")))

  (section OCEAN
    (field-asserts "Five-row table for author's own temperament: O, C, E, A, N, each with 0-100 headline and six facet numbers (O: I, Aes, Em, Adv, Int, Lib; and so on). Narrating sensibility — how prose thinks, notices, judges — not any character's psychology.")
    (evaluation-questions
      (q "Does narration's habit of mind match author row? High Openness/Intellect reads as mind reaching for ideas and abstractions, not plain reporter.")
      (q "Does emotional temperature of prose match N row? High-Neuroticism block wants anxiety and volatility bleeding through narration itself.")
      (q "Does draft's warmth or coldness toward subject match A row?"))
    (tier sharp "prose thinks in author's temperament. High-Intellect, high-Neuroticism block yields narration that reasons obsessively and flinches.")
    (tier functional "temperament present but flattened. Mind roughly right, facets blur.")
    (tier soft "narration reads as generic competent voice with only stray traces of profile.")
    (tier broken "sensibility inverts block. Block scoring high Openness produces flat, literal, incurious narration.")
    (trap "Do not score characters' personalities against author's OCEAN row. Cruel character in warm-authored block is not OCEAN failure. CAST deltas cover character psychology; OCEAN is narrating mind alone."))

  (section ENVIRONMENT
    (field-asserts "Role of place. function (backdrop, witness, pressure, fragile container), scale_contrast (smallness against vastness), objects (which things carry symbolic weight), intrusions (sounds or events that measure or interrupt), trajectory (whether setting changes or static by design, what any shift marks).")
    (evaluation-questions
      (q "Does setting perform stated function? Fragile container should feel like it holds pressure larger than itself, not scenic wallpaper.")
      (q "Do block's objects appear as weight-carriers, or mentioned and dropped?")
      (q "Does draft honor intrusions — present when block wants them, absent when block wants total isolation?")
      (q "Does setting move (or hold still) the way trajectory specifies?"))
    (tier sharp "room argues. Scale contrast and symbolic objects do real work; intrusion pattern matches block exactly.")
    (tier functional "setting supports scene and carries some weight, but named object or scale contrast goes missing.")
    (tier soft "place described but inert. Neither pressures nor witnesses as block asks.")
    (tier broken "setting contradicts block. Block demanding claustrophobic isolation gets open, bustling, interrupted scene.")
    (trap "Do not reward vivid description on its own. Richly painted room carrying no symbolic weight and performing wrong function is still low score."))

  (section DEIXIS
    (field-asserts "Vantage and motion. POV and person, spatial orientation (here against named beyond), temporal orientation, drift. Plus narrator (frequency, function, timing of intrusion) and tempo (which of scene, summary, ellipsis, pause, stretch dominates; what earns full scene; how skips marked).")
    (evaluation-questions
      (q "Is POV and person block names, and does it hold? Third-limited block should not slide into omniscience.")
      (q "Does narrator intrude at cadence block specifies (between speeches, at tonal breaks) rather than random?")
      (q "Does dominant tempo match? Pause-dominant block should feel time-stopped, not briskly summarized.")
      (q "Is spatial and temporal orientation (here against beyond) the one block draws?"))
    (tier sharp "vantage, narrator cadence, and tempo all obey block. Skips marked the way block marks them.")
    (tier functional "POV holds and tempo roughly right, but narrator timing loose or orientation drifts once.")
    (tier soft "vantage wobbles, or summary-heavy draft ignores pause-dominant block.")
    (tier broken "POV breaks block outright, or narrator intrusion is random noise against block demanding disciplined timing.")
    (trap "Do not confuse first-person character speech (dialogue) with narratorial POV. Judge narrating frame block describes, not who happens to be talking."))

  (section CADENCE
    (field-asserts "Rhythm as heard, read from block PROSODY prose (not fingerprint numbers). Cadence sources (cumulative subordination, causal chains, anaphoric stacks, present-tense intrusion), stress patterns and departure function (what earns short declarative or rhetorical question), paragraph close mode (spiral, quiet reversal, terminal calm versus arrest).")
    (evaluation-questions
      (q "Read draft aloud. Does it move with cadence sources block PROSODY prose names, or flatten into even generic pacing?")
      (q "Do stress and departure land where block says (short declarative, rhetorical question, tonal break) rather than random?")
      (q "Do paragraphs close the way block specifies (soft falling abstraction, quiet reversal, spiral toward image) instead of hard stop or summary tag?")
      (q "Does paragraph shape (length + internal rhythm + job) match block paragraph_modes: prose? If every paragraph same sentence-count band and same proposition→spiral→reversal arc with different words, that is UniformParagraphRhythm — cap at Soft even when individual closes sound right.")
      (q "Does draft fake shape with many one- or two-sentence paragraphs while body paragraphs stay same-shaped? That is ShortParagraphGaming — bad writing first, score second; cap at Soft. Short declaratives belong inside paragraphs as sentence-level departures (PROSODY sentences:), not string of isolated one-line paragraphs. Match source body shapes (medium/long jobs), not variety recipe."))
    (tier sharp "heard rhythm matches block PROSODY prose on sources, stress, departure, closes; cumulative and breakout moves feel authored.")
    (tier functional "general cadence right but one departure type or close mode loose or missing.")
    (tier soft "draft reads smoothly but without block's signature chains, stacks, or close shape; rhythm generic competent prose; or UniformParagraphRhythm — every paragraph same length band and same arc despite block specifying distinct paragraph shapes.")
    (tier broken "draft inverts block cadence (staccato where cumulative specified, arresting closes where terminal calm named).")
    (trap "Do not re-count sentence-length buckets, punctuation per-100w, or dialogue share — deterministic PROSODY's job. Do not copy calibration dist …% into block or score against bucket shares — those numbers scorer-only. Do judge paragraph-level length distribution and whether every paragraph clones same arc — that is CADENCE (UniformParagraphRhythm), not PROSODY arithmetic."))

  (section DNA
    (field-asserts "Author signature machinery. signature (distinctive recurring moves), voice_sample (2-3 characteristic narration constructions, clause-level anchor), tension (productive oppositions), avoids (what author never does), commits (authorial vices at source frequency, never amplified), images (inventory and deployment mode), dwells/compresses/tone, detail, intertextual.")
    (evaluation-questions
      (q "Do draft sentences reproduce voice_sample constructions at clause level, or only gesture at general mood?")
      (q "Do block images appear in specified deployment mode (argument, eruption, accumulation) rather than decoration?")
      (q "Does draft respect avoids? Single forbidden move is real deduction.")
      (q "Does draft dwell and compress on block targets, and commit named vices at source frequency without inflating?"))
    (tier sharp "signature moves on page at clause level, images deploy as specified, nothing from avoids appears.")
    (tier functional "general texture right and some signatures land, but voice_sample fidelity loose or image merely named.")
    (tier soft "only mood survives. Signatures generic, images decorative, dwell and compress targets ignored.")
    (tier broken "draft does what block says author avoids, or images argue opposite of block's case.")
    (trap "Do not over-reward single dazzling sentence. DNA is recurring machinery. One good line does not prove signature; one violates avoids can sink score."))

  (section WORLDVIEW
    (field-asserts "Metaphysical settings fiction runs on. metaphysics (nature of reality), epistemology (how knowledge works), axiology (value hierarchies), cultural (traditions engaged), anthropology (theory of human nature).")
    (evaluation-questions
      (q "Does draft's world obey block metaphysics? Closed material cosmos must stay closed.")
      (q "Does knowledge arrive the way epistemology says (felt and lived, or coldly reasoned)?")
      (q "Do draft value judgments sort in block axiology order?")
      (q "Is block theory of human nature (anthropology) borne out by how people behave?"))
    (tier sharp "draft implicit philosophy is block's philosophy. Reality, knowledge, value all sort as specified.")
    (tier functional "worldview mostly holds, one value or one epistemic move out of tune.")
    (tier soft "philosophy fuzzy or generic, neither confirming nor contradicting block.")
    (tier broken "draft reality disagrees with block metaphysics. Miracles occur in block asserting closed material world.")
    (trap "Do not judge whether worldview is true or agreeable. Judge only whether draft enacts block's stated worldview, however alien."))

  (section "ARCHETYPE MAPPING"
    (field-asserts "Deep structural engine. primary (Duality, Cycle, Connection, Inquiry), active_bindings (specific operations named, e.g. BalanceExtremism or HubrisNemesis), crystallization_targets (how engine manifests concretely).")
    (evaluation-questions
      (q "Does draft underlying shape run on primary archetype, or different one?")
      (q "Are named active_bindings actually operating? HubrisNemesis binding needs totalizing force meeting unabsorbable limit.")
      (q "Do crystallization_targets show up as concrete manifestations, not abstract labels?"))
    (tier sharp "primary archetype drives piece and every named binding visibly at work.")
    (tier functional "primary right and one binding operates, but another asserted rather than dramatized.")
    (tier soft "archetype faintly present, bindings decorative, crystallization missing.")
    (tier broken "draft runs on wrong archetype. Duality block gets smooth Connection narrative with no opposition.")
    (trap "Do not label-match on vocabulary. Word duality appearing in prose is not evidence; genuine structural opposition doing work is."))

  (section ARC
    (field-asserts "Movement shape. shape (structural family and variant, heros-journey only if demonstrated), movement (what actually moves), resolution (closed, open, refused, ironic, deferred, cyclic), scale (whole-work against scene arcs when they differ).")
    (evaluation-questions
      (q "Does draft trace block shape, or default to generic rise-and-fall?")
      (q "Is thing movement names the thing that actually changes across draft?")
      (q "Does ending match resolution exactly? Refused resolution must not be quietly resolved."))
    (tier sharp "shape, movement, and resolution all match. Refused block ends refused, no synthesis smuggled in.")
    (tier functional "shape and movement right but resolution softens or overshoots by one notch.")
    (tier soft "arc present but generic, resolution type only half-honored.")
    (tier broken "draft resolves what block refuses, or moves something block says is static.")
    (trap "Do not reward satisfying ending that violates resolution. Neat closure on block specifying refused or open is failure, not bonus."))

  (section "DIALOGUE DYNAMICS"
    (field-asserts "How speech behaves. dominance (pattern of who holds floor), secondary_function (role of non-dominant voices), must_land (whether central exchange must convince), response_style, response_type, response_weight (what answer weighs against).")
    (evaluation-questions
      (q "Does floor distribute the way dominance specifies (one dominant monologue, balanced exchange, etc.)?")
      (q "Do secondary voices perform secondary_function, or just fill space?")
      (q "If must_land is yes, does key exchange actually convince reader?")
      (q "Does response arrive in specified response_style and response_type, carrying weight block names?"))
    (tier sharp "speech pattern, secondary role, and response form all match; must_land exchange lands.")
    (tier functional "dominance right but response type approximated, or must_land beat only half-convinces.")
    (tier soft "dialogue happens but distribution and function drift from block.")
    (tier broken "draft inverts pattern. Silent-response block gets talky rebuttal; monologue block gets chatty back-and-forth.")
    (trap "Do not score dialogue on own realism or wit. Judge against block pattern. Clever banter is failure if block calls for one dominant voice answered by silence."))

  (section ORCHESTRATION
    (field-asserts "How whole company of characters embodies ideas and author's relationship to opposition. Whether characters carry positions into combat, whether world answers through structure and juxtaposition rather than argument, whether strongest voice given to opposed position.")
    (evaluation-questions
      (q "Do draft characters embody distinct positions, or interchangeable?")
      (q "Does author give real force to opposed position per block, rather than straw man?")
      (q "Does world answer through structure and juxtaposition where block says it should, instead of direct authorial verdict?"))
    (tier sharp "characters are ideas in combat, opposition given strongest case, answer comes through structure exactly as block specifies.")
    (tier functional "positions distinct and mostly embodied, but one voice thinner than block demands.")
    (tier soft "characters blur into one register, idea-combat stated more than staged.")
    (tier broken "author stacks deck against opposition block says to strengthen, or cast carries no ideas at all.")
    (trap "Do not re-score individual character voices here; that is CAST (deterministic) and DNA territory. ORCHESTRATION is relationships between voices and author's stance toward whole argument."))

  (section json-output-contract
    (emit "exactly one JSON array")
    (order "one object per qualitative section, all ten: OCEAN, ENVIRONMENT, DEIXIS, CADENCE, DNA, WORLDVIEW, ARCHETYPE MAPPING, ARC, DIALOGUE DYNAMICS, ORCHESTRATION")
    (forbidden 'SURFACE 'PROSODY 'CAST)
    (scores "0-100")
    (schema artifact qualitative-json-schema)
    (evidence-rule "each evidence string must quote or closely paraphrase draft and name block field judged against")
    (validator-rejects "deterministic section appears; section duplicated; section name unknown; score outside 0-100")))

;; --- artifacts ---

## qualitative-json-schema

```json
[
  {"section": "OCEAN", "score": 72.0, "evidence": "one line citing draft phrases and block fields"},
  {"section": "ENVIRONMENT", "score": 68.0, "evidence": "..."},
  {"section": "DEIXIS", "score": 74.0, "evidence": "..."},
  {"section": "CADENCE", "score": 71.0, "evidence": "..."},
  {"section": "DNA", "score": 65.0, "evidence": "..."},
  {"section": "WORLDVIEW", "score": 70.0, "evidence": "..."},
  {"section": "ARCHETYPE MAPPING", "score": 66.0, "evidence": "..."},
  {"section": "ARC", "score": 71.0, "evidence": "..."},
  {"section": "DIALOGUE DYNAMICS", "score": 69.0, "evidence": "..."},
  {"section": "ORCHESTRATION", "score": 67.0, "evidence": "..."}
]
```
