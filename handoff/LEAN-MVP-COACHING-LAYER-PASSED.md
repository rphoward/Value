(def-sop lean-mvp-coaching-layer
  (context
    (target "agent-resuming-or-reviewing-the-lean-mvp-coaching-layer")
    (optimization "durable-record-of-what-shipped-and-what-the-source-plan-got-wrong"))

  <central_idea>
  (center-of-gravity
    (invariant "Every lean-mvp atom now ships a coaching entry that next_question.py resolves into the turn payload: why the turn matters, definition text pulled from knowledge-base.json, what a complete answer contains, a worked example, the common miss, and a board of the prior answers with a clause naming what each contributes. The interview never stops when an entry is absent."))
  </central_idea>

  (section outcome
    (result PASS)
    (evidence "python -m pytest tests -q")
    (measured "125 passed, 0 failed")
    (baseline "15 failed, 108 passed before _session import isolation and kb_refs fill")
    (note "tests/skill_session_loader.py loads each skill _session under a hashed module name so value, lean-mvp, and compile scaffolds no longer race on sys.modules['_session']. Eight atoms now ship kb_refs into knowledge-base.json.")
    (next "None for this follow-up; keep coaching tests subprocess-only and use load_skill_session for any new in-process _session access."))

  (section what-shipped
    (asset "assets/atom-coaching.json — 32 entries, one per atom, six fields each")
    (entry-fields why_it_matters kb_refs reads-with-why complete_when worked_example common_miss)
    (module "scripts/_session/coaching.py — load_atom_coaching, flatten_kb_value, resolve_kb_ref, coaching_for_atom")
    (payload "next_question.py gains one key, coaching, which is null when the atom has no entry")
    (deleted "MATCH_BOARD_ATOMS and match_board_for_atom, dead in lean-mvp and still speaking the value skill's V02/V03 vocabulary")
    (knowledge-base "invest_user_story_rubric widened from bare words to definition and check per letter, restored from docs/lean-product-playbook-prompt-suite.md")
    (skill-body "protocol-3-turn-recipe gained a coaching delivery order; assets block registers atom-coaching.json")
    (test "tests/test_lean_mvp_coaching.py — 8 cases, no _session import, drives next_question.py as a subprocess")
    (mirrored "every file byte-identical across skills/lean-mvp/ and .cursor/skills/lean-mvp/"))

  (section invariants-a-future-change-must-not-break
    (no-gate-in-reads "A coaching entry's reads may not name a gate atom. is_ceremony_answer only filters text holding both bypass and gate, so the canonical answer pass <module> gate would reach the human as evidence they never supplied.")
    (priors-may-be-absent "EXPRESS_SPINE skips most atoms, so a listed prior is often unanswered. Unanswered priors are marked missing and the agent skips them without narrating the gap.")
    (soft-fail "A missing entry or unreadable atom-coaching.json yields coaching null; next_question.py still exits 0")
    (dotted-refs "kb_refs are dotted paths into knowledge-base.json. A top-level ref where a child would do drags sibling content into the payload as noise.")
    (no-session-import "tests/test_lean_mvp_coaching.py must never import _session; four existing test files race for that name on sys.path."))

  (section source-plan-audit
    (plan ".cursor/plans/lean-mvp_coaching_layer_a9e65afa.plan.md — third attempt, outside this workspace so not edited")
    (record "tools/drafts/lean-mvp-coaching/plan-audit.md")
    (verified-claims "the ten-field payload, the 32-atom split, the dead board machinery, the bare INVEST rubric, the 35-file mirror, the 15-failure baseline, the two all-pass INVEST strings, the stale story-elements line")
    (corrected-claims
      (dangling-pointer "the plan credited a story-generation-prompt test with catching unregistered lean-mvp assets; that test is scoped to its own skill and lean-mvp had no equivalent, so one was added")
      (invest-widening "the plan treated widening INVEST as authoring; docs/lean-product-playbook-prompt-suite.md lines 78-85 already held the definitions the shipped asset had truncated, so it was restoration")
      (reads-shape "a flat list of atom ids cannot produce the board the plan promised; each prior carries a why clause and a human label")
      (kb-refs-shape "top-level keys were too coarse; refs are dotted paths")
      (gate-atoms "five of the 32 atoms are review turns and the plan never mentioned them")
      (express-pacing "the plan's test would have been flaky because express pacing leaves listed priors unanswered")))

  (section evidence-a-reviewer-can-rerun
    (harness "tools/drafts/lean-mvp-coaching/demo_turn.py <ATOM_ID> — seeds through MT01 (UX gate included); any atom id is a valid target, e.g. MT02")
    (baselines "tools/drafts/lean-mvp-coaching/baseline-C01.json, baseline-MS05.json, baseline-MS12.json — the ten-key payload before the change")
    (trail "tools/drafts/lean-mvp-coaching/decisions.tsv")
    (design "tools/drafts/lean-mvp-coaching/synthesis.md plus candidate-1, candidate-2, candidate-3")))
