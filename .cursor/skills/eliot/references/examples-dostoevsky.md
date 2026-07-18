(def-ref examples-dostoevsky
  (linked-from protocol-4-fixture)
  (input assets/dostoevsky-source.txt)
  (note "INPUT passage pinned in assets/; block below is EXPECTED SHAPE gold from v5.7")
  (pinned-source "assets/dostoevsky-source.txt (Garnett, Grand Inquisitor excerpt)")
  (expected-shape "v5.7 gold — Run C canonical, CAST order per workflows step 7")
  (artifact expected-shape-gold))

;; --- artifacts ---

## expected-shape-gold

```
DOSTOEVSKY (Brothers Karamazov, Grand Inquisitor)
--------------------------------------------------------------------------------
OCEAN:
+---+----+------------------------------------------+
| O | 75 | I:85 Aes:70 Em:80 Adv:60 Int:90 Lib:65   |
| C | 70 | SE:75 Ord:60 Dt:65 AS:80 SD:55 Cau:50    |
| E | 65 | W:70 G:60 A:70 AL:75 ES:80 Ch:40         |
| A | 60 | Tr:55 SF:70 Alt:75 Comp:45 Mod:50 TM:85  |
| N | 70 | Anx:65 Ang:60 Dep:70 SC:75 Imm:65 V:80   |
+---+----+------------------------------------------+

SURFACE: Long periodic sentences (35-55 words avg), em-dash interruption
mid-thought, accumulative syntax. Elevated register grounded in visceral
imagery. Paragraph spirals with intensification toward climax. Heavy use
of rhetorical questions as structural device.

ENVIRONMENT:
  function: fragile container — prison cell holding cosmic argument
  scale_contrast: cramped vault vs. fifteen centuries of human history
  objects: flaming brand (only light source), iron door (isolation),
    silence (presence not absence)
  intrusions: none — total isolation amplifies monologue weight;
    the world is locked out
  trajectory: static-by-design — cell fixed while argument sweeps centuries;
    stasis = the Inquisitor's frozen system; ONE event (door opens,
    prisoner released) carries the resolution

DEIXIS: Third limited (Ivan as frame narrator), shifts to first/second
in Inquisitor's monologue (I/You address to silent Christ). Spatial
axis: "here on earth" vs. abstract celestial beyond. Temporal sweep:
"fifteen centuries" as recurring measure. Drift toward confrontation —
every scene narrows to two figures facing each other.
  narrator: moderate; physical+emotional; between speeches+tonal breaks
  tempo: pause-dominant — time stops inside the monologue while argument sweeps
    centuries in clauses; frame = scene; ellipsis absorbed into rhetoric, unmarked

PROSODY: Anapestic surge -> spondaic arrest (long build, hard stop).
Biblical parallelism and sermon cadence. Folk-tale rhythms in frame
("In those times..."). Terminal stress on monosyllables after long
builds ("Dixi." / "That is so."). Load-bearing rhythm — meaning
carried by sound pattern as much as semantics.
  sentences: long(35-55), moderate variation, departure=punctuation
    and emphasis, periodic+cumulative
  fingerprint: 15/35/50 %short/med/long; per-100w: ,9 ;0.8 —1.5 ?1.2 !0.6;
    dialogue:narration 70:30 (monologue-weighted)
  paragraph_modes: shapes as jobs — frame continuation / long swell to climax / medium
    compress; open assertion or question; close on image or monosyllabic stop; not every
    paragraph spirals to climax; short declaratives land inside paragraphs as departures,
    not as isolated one-line paragraphs

DNA:
  signature: concrete atrocity as philosophical argument; rhetorical
    trap questions; emotional escalation through listing/accumulation;
    tonal breaks (irony->anguish->irony); direct address implicating
    listener; strongest voice given to opposed position
  voice_sample: narration piles subordinate clauses then arrests on a short
    declarative; "and" as accumulation-engine not conjunction; abstract sweep
    suddenly grounded in a body ("fifteen centuries" -> "a bit of bread")
  tension: freedom/happiness; love/pity; articulation/comprehension;
    passion/system
  avoids: ironic distance from suffering; resolution or synthesis;
    aesthetic detachment from moral stakes; straw men
  commits: obsessive word-repetition (same key term 3-4x where an editor would vary);
    stacked intensifiers ("positively", "utterly" piled on one noun); digressive asides
    mid-argument that wander then snap back
  images:
    inventory: bread(earthly), stones(transformation), fire(judgment),
      blood/tears/bodies, kiss(wordless response), children(innocence
      that indicts)
    deployment: as-argument + as-accumulation; images ARE the
      philosophical case not decoration; "bread" weaponized as proof
      freedom=cruelty; tortured children pile until weight unanswerable;
      kiss arrives as only non-propositional response to propositional trap
  dwells: suffering, moral crisis, philosophical argument |
    compresses: nature, physical action, scenic description |
    tone=anguished underneath irony
  detail: psychological+symbolic+social-contextual, maximal, extends
    to minor elements
  intertextual: Scripture(Temptations Revelation Job), Church Fathers,
    Russian poets(Tyutchev); mode=argument+allusion; density=saturated

WORLDVIEW:
  metaphysics: morally structured cosmos — rebellion confirms structure;
    irreducible consciousness; innocent suffering as scandal requiring response
  epistemology: ideas must be lived not thought; felt facts > logic;
    understanding through suffering
  axiology: justice > harmony; individual > collective; this world matters
  cultural: Russian Orthodox (sobornost kenosis) — engaged even when
    rejected; Western rationalism as antagonist
  anthropology: human cruelty uniquely artistic; children as innocent
    species; humans crave authority yet resent it; freedom=burden

ARCHETYPE MAPPING:
  primary: Duality (Freedom/Happiness; Truth/Peace)
  active_bindings:
    - BalanceExtremism (Inquisitor=reasonable center; Christ's freedom=cruel extremism)
    - HubrisNemesis (totalized system meets unabsorbable limit)
    - PatternAnomaly (Christ persists without refuting)
  crystallization_targets:
    - Embeddings->ConceptualNeighborhoods (Scripture as habitat)
    - RelationalVectors->AnalogicalReasoning (Temptations->argument structure)
    - ContextualAttention->Disambiguation ("freedom" and "love" shift under pressure)

ARC:
  shape: rise-to-limit (HubrisNemesis) in Tragic(fate-driven) frame;
    NOT heros-journey — nothing overcome, no return
  movement: the argument's authority — accumulates, totalizes, breaks on the kiss
  resolution: refused — no synthesis; kiss glows, old man adheres to his idea
  scale: frame(Ivan/Alyosha) = spiral, return transformed

DIALOGUE DYNAMICS:
  dominance: one dominant (Inquisitor monologue)
  secondary_function: silent opposition-embodiment
  must_land: yes — reader must feel Inquisitor may be right
  response_style: silence
  response_type: wordless act (kiss)
  response_weight: nothing propositional — testifies what system cannot absorb

CAST:
  INQUISITOR:
    OCEAN_delta:
    +---+-----+------------------------------------------+
    | O | +10 | Int:+10                                  |
    | A | -20 | TM:-20                                   |
    | N | +15 | SC:+15                                   |
    +---+-----+------------------------------------------+
    idiolect: ecclesiastical register; direct "You" address; em-dash self-interruption
    voice_sample: "And did You not know...?" as trap; pivots we->You mid-clause
      shifting blame; stacks accusations as single mounting sentence; declaratives
      containing their own rhetorical question
    function: opposition-embodiment — strongest voice for opposed position
    worldview: materialist compassion — humans weak, freedom=cruelty, bread>truth
    stance: [BalanceExtremism] claims center; Christ's gift=extremist cruelty
    rhetoric: trap questions; listing as escalation; "You know this" implicating listener

  CHRIST:
    OCEAN_delta:
    +---+-----+------------------------------------------+
    | A | +40 | TM:+40                                   |
    | E | -30 | ES:-30 — stillness as presence           |
    +---+-----+------------------------------------------+
    idiolect: none — kiss substitutes for speech
    voice_sample: [n/a — rendered through narrator: stillness, dark eyes, gentle silence]
    function: silent opposition; system limit
    worldview: [silent-inferred] freedom as gift despite cost; love without coercion
    stance: [PatternAnomaly] persists without refuting; unabsorbable exception
    rhetoric: none — silence as rhetoric

  IVAN:
    OCEAN_delta:
    +---+-----+------------------------------------------+
    | O | +5  | Int:+5                                   |
    | N | +10 | Anx:+10                                  |
    +---+-----+------------------------------------------+
    idiolect: literary register; parenthetical qualification; questions to Alyosha
    voice_sample: opens with deflection then can't stop ("Well of course it's
      absurd but—"); parenthetical self-correction mid-sentence; questions aimed
      at Alyosha really aimed at self
    function: frame narrator; needs the tale told
    worldview: performs atheism, cannot commit; returns ticket but cannot stop caring
    stance: ironic distance that cannot hold; frames but is implicated
    rhetoric: self-deprecation as shield; "just a poem" as escape hatch

  ALYOSHA:
    OCEAN_delta:
    +---+-----+------------------------------------------+
    | Ag| +25 | TM:+25 SF:+15                            |
    | N | -15 | Anx:-15                                  |
    +---+-----+------------------------------------------+
    idiolect: simpler syntax; emotional directness; exclamation
    voice_sample: short exclamatory bursts ("But that's—!"); questions that
      are pleas; simple declaratives carrying conviction that doesn't argue
    function: witness; receives tale and must respond
    worldview: Orthodox belief — tested not naive; feels Ivan's weight
    stance: [PatternAnomaly] will not refute but will not concede; mirrors Christ's kiss
    rhetoric: direct questions; refusal of ironic distance

orchestration: Characters embody ideas in combat. Author gives strongest
voice to opposed positions — Inquisitor MORE convincing than most real
defenses of authoritarianism. World answers through structure/juxtaposition
(kiss) not counter-argument. Ivan frames but cannot escape; Alyosha
witnesses and mirrors.
```
