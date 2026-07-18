(def-ref experiments
  (linked-from protocol-2 protocol-3 protocol-4)
  (purpose "Turn the accepted profile, value map, and business model into one evidence-seeking experiment and a recorded next decision.")
  (evidence-policy "Behavior and commitment are stronger evidence than polite agreement. Keep unsupported claims and absent results labeled hypothesis or unknown.")

  (atom
    (id E01)
    (name "assumption inventory")
    (teaches "An assumption states what must be true for the accepted design to work. Inventorying desirability, feasibility, and viability assumptions first prevents the easiest test from displacing the most important uncertainty.")
    (asks "What must be true about customer demand, delivery capability, and business viability for this design to succeed?")
    (accepts "States at least one falsifiable assumption in each applicable category and labels any category not yet understood unknown.")
    (writes "append one answers record for E01; append each claim to assumptions with criticality, evidence_status, and source_atom E01; append missing required categories to unknowns; set project.updated_at; set position to experiments/E02/in_progress")
    (unlocks E02))

  (atom
    (id E02)
    (name "criticality and evidence")
    (teaches "Criticality describes the harm if an assumption is false, while evidence status describes how well it is supported now. Comparing both makes high-impact, weakly supported claims visible without pretending that a rank is proof.")
    (asks "For each inventoried assumption, how critical is it and what labeled evidence currently supports it?")
    (accepts "Assigns high, medium, or low criticality and supported, partial, unsupported, or unknown evidence status to each assumption, citing evidence records where available.")
    (writes "append one answers record for E02; append revised assumption records carrying source_atom E02; append cited support to evidence and absent support to unknowns; set project.updated_at; set position to experiments/E03/in_progress")
    (unlocks E03))

  (atom
    (id E03)
    (name "highest-risk hypothesis")
    (teaches "The highest-risk hypothesis combines serious consequences with weak evidence. Choosing one now focuses the next experiment on learning that could change the design rather than confirming a comfortable detail.")
    (asks "Which assumption is the highest-risk hypothesis to test next, and why does it outrank the others?")
    (accepts "Selects one inventoried assumption, states the consequence of failure and current evidence gap, and records the choice as a decision.")
    (writes "append one decision-kind answers record for E03; append a decisions record with decision, reason, source_atom E03, and resulting position experiments/E04/in_progress; set project.updated_at; set position to experiments/E04/in_progress")
    (unlocks E04))

  (atom
    (id E04)
    (name "experiment choice")
    (teaches "An experiment creates an observable chance for the selected hypothesis to fail. The method follows the hypothesis so its action, participants, and setting measure the claim rather than general interest.")
    (asks "What smallest ethical experiment could expose the selected hypothesis to observable customer behavior?")
    (accepts "Names participants, setup, action, and observation tied directly to the selected hypothesis; labels unverified access or feasibility as assumptions.")
    (writes "append one answers record for E04; append setup and access assumptions with source_atom E04; set project.updated_at; set position to experiments/E05/in_progress")
    (unlocks E05))

  (atom
    (id E05)
    (name "metric and threshold")
    (teaches "A metric specifies what the experiment observes, and a threshold states the result that would support the hypothesis before data arrives. Defining both now prevents the team from moving the goal after seeing results.")
    (asks "What observable metric and precommitted threshold will distinguish support from insufficient support for this hypothesis?")
    (accepts "Defines one observable metric, a numerical or unambiguous threshold, a time window, and the result classification; records unavailable baseline information as unknown.")
    (writes "append one answers record for E05; append unsupported threshold rationale to assumptions with source_atom E05 and missing baseline data to unknowns; set project.updated_at; set position to experiments/E06/in_progress")
    (unlocks E06))

  (atom
    (id E06)
    (name "evidence-quality defense")
    (teaches "Evidence quality depends on whether the observation could occur without the claimed demand and whether the test explores only one familiar direction. Reviewing those risks now strengthens interpretation before the experiment runs.")
    (visual "Use two checks: a signal filter rejects results explainable by politeness, while a wider-map check asks whether the test merely improves one small hill without comparing another route.")
    (asks "How will this experiment require meaningful behavior or commitment while guarding against a false positive and a narrow local optimum?")
    (accepts "Names the required customer behavior or commitment, at least one alternative explanation, and one credible alternative direction or reason it is out of scope; spoken agreement alone is weak evidence.")
    (writes "append one answers record for E06; append planned evidence claims with source and strength; append unresolved alternative explanations or directions to unknowns; set project.updated_at; set position to experiments/E07/in_progress")
    (unlocks E07))

  (atom
    (id E07)
    (name "test card")
    (teaches "A test card turns prior choices into an executable agreement: hypothesis, method, metric, threshold, owner, and time window. Assembling it now makes responsibility and interpretation explicit before observations begin.")
    (asks "Who owns this test, when will it run, and should the assembled test card be accepted as written?")
    (accepts "Confirms or corrects a card containing title, owner, timing, criticality, hypothesis, method, metric, and threshold; acceptance is an explicit decision.")
    (writes "append one decision-kind answers record for E07; append a decisions record with source_atom E07 and resulting position experiments/E08/in_progress; upsert artifacts record for experiment-plan.md with status draft; set project.updated_at; set position to experiments/E08/in_progress")
    (unlocks E08))

  (atom
    (id E08)
    (name "learning card")
    (teaches "A learning card separates what was believed, what was observed, and what may reasonably be learned. It follows execution so raw results remain distinct from interpretation and missing results remain unknown.")
    (asks "What did the test observably produce, from which source, and what labeled learning does that result support?")
    (accepts "Records the prior hypothesis, raw observation, source, evidence strength, and labeled interpretation; no-run or incomplete results are recorded unknown rather than inferred.")
    (writes "append one answers record for E08; append schema-valid evidence records for raw observations; append interpretations to evidence with kind inference or to assumptions with source_atom E08; append missing results to unknowns; set project.updated_at; set position to experiments/E09/in_progress")
    (unlocks E09))

  (atom
    (id E09)
    (name "next decision")
    (teaches "A result matters when it changes a decision. Choosing to proceed, revise, pivot, stop, or run another test now ties action to the threshold and evidence quality rather than enthusiasm.")
    (asks "Given the threshold and evidence quality, what is the next design decision and why?")
    (accepts "Chooses one concrete next action, cites the accepted result and threshold, explains the reason, and identifies any unresolved assumption that governs further work.")
    (writes "append one decision-kind answers record for E09; append a decisions record with decision, reason, source_atom E09, and resulting position experiments/E10/in_progress; set project.updated_at; set position to experiments/E10/in_progress")
    (unlocks E10))

  (atom
    (id E10)
    (name "experiment gate")
    (teaches "The experiment gate checks that the assumption, test card, observations, evidence quality, learning, and next decision remain traceable. Passing closes this learning cycle while preserving unknowns for the next cycle or final briefs.")
    (asks "Should this experiment cycle pass its gate now, or should one named atom be reopened?")
    (accepts "Records an explicit pass or reopen decision with a reason and target atom; pass requires a selected hypothesis, accepted test card, result or explicit unknown, labeled learning, and next decision.")
    (writes "append one decision-kind answers record for E10; append a decisions record with source_atom E10 and the chosen resulting position; on pass set position to experiments/E10/gate_pending and set experiment-plan.md artifact status pending; on reopen set position to experiments/<chosen-atom>/in_progress; set project.updated_at")
    (unlocks "experiments gate: write experiment-plan.md from accepted experiment state, set its artifact status final, mark experiments completed, then unlock product-design-brief.md and ux-brief.md only when every module is completed or explicitly bypassed")))
