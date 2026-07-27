(def-ref curriculum-synthesis
  (linked-from protocol-2 for-agents tutorial)

  (section purpose
    (note "Judgment path for expanding seeded draft atoms into a shippable paced curriculum without pstack or poteto-mode."))

  (section habits
    (build-the-lever "Prefer scripts (audit_dag, status) over hand-waving progress")
    (encode-in-structure "Put unlocks, requires, and gate flags in atoms.json — not prose reminders")
    (prove-it-works "Run audit_dag --mode both before offering promote")
    (one-question "One primary human question per atom")
    (prose-that-changes-decisions "Each ask must force a concrete answer or explicit unknown")
    (never-invent-beyond-suite "Ground asks in module cargo in references/<module>.md"))

  (section workflow
    1 "Read seeded assets/atoms.json and references for each module")
    2 "Replace stub asks (What is the first concrete fact for ...) with suite-grounded questions")
    3 "Tune soft labels only when express mode should skip non-spine atoms; never leave soft atoms in a later requires chain")
    4 "Align section-map.json milestones and templates with module voice")
    5 "Re-run audit_dag --mode both; promote only after human consent")

  (section optional-poteto
    (note "If poteto-mode or pstack is already installed, you may use it for voice and review. It is not required.")))
