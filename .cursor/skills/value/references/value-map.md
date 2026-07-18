(def-ref value-map
  (linked-from protocol-2 protocol-3 protocol-4)
  (purpose "Define how one offering serves the accepted profile and park unmatched features for explicit decisions.")
  (evidence-policy "Use only accepted profile state as the fit baseline. Preserve every inference, hypothesis, decision, and unknown label.")

  (atom
    (id V01)
    (name "offering boundary")
    (teaches "A value map covers one offering for the accepted segment and priority job. Setting that boundary prevents unrelated products and customers from hiding weak fit.")
    (asks "Which single offering are we mapping for the accepted segment and priority job, and what is outside its boundary?")
    (accepts "Names one offering and at least one boundary exclusion; records an unresolved boundary as unknown rather than broadening it silently.")
    (writes "append one answers record for V01; append unresolved offering boundaries to unknowns; set project.updated_at; set position to value-map/V02/in_progress")
    (unlocks V02))

  (atom
    (id V02)
    (name "products and services")
    (teaches "Products and services are the concrete things the customer can receive or use, whether physical, service-based, digital, or financial. Listing them now establishes the parts whose effects must be justified next.")
    (asks "What products or services are actually included in this offering?")
    (accepts "Lists concrete included items and distinguishes established scope from hypotheses; avoids claiming benefits in place of deliverables.")
    (writes "append one answers record for V02; append unconfirmed included items to assumptions; set project.updated_at; set position to value-map/V03/in_progress")
    (unlocks V03))

  (atom
    (id V03)
    (name "pain relievers")
    (teaches "A pain reliever states how an included item reduces a specific accepted pain. It follows the offering list so relief claims can be traced to something the offering actually does.")
    (asks "How does each relevant part of the offering reduce a specific accepted customer pain?")
    (accepts "Links each proposed relief to an included item and an accepted pain, states the expected reduction, and labels unsupported effects as hypotheses.")
    (writes "append one answers record for V03; append unsupported relief claims to assumptions with source_atom V03; set project.updated_at; set position to value-map/V04/in_progress")
    (unlocks V04))

  (atom
    (id V04)
    (name "gain creators")
    (teaches "A gain creator states how the offering produces an accepted essential, expected, desired, or unexpected outcome. Separating creation from pain relief prevents the same claim from doing double duty without evidence.")
    (asks "How does each relevant part of the offering create a specific accepted customer gain?")
    (accepts "Links each proposed effect to an included item and accepted gain, states the expected outcome, and labels unsupported effects as hypotheses.")
    (writes "append one answers record for V04; append unsupported gain-creation claims to assumptions with source_atom V04; set project.updated_at; set position to value-map/V05/in_progress")
    (unlocks V05))

  (atom
    (id V05)
    (name "job alignment")
    (teaches "Fit requires traceable links from offering items and effects to accepted jobs, pains, or gains. Checking alignment now reveals both supported value and claims that have no profile basis.")
    (asks "Which accepted job, pain, or gain does each offering item, pain reliever, and gain creator serve?")
    (accepts "Provides a traceable match for every listed item or marks it unmatched; does not invent a profile claim to manufacture fit.")
    (writes "append one answers record for V05; append unsupported alignment claims to assumptions and missing profile links to unknowns; set project.updated_at; set position to value-map/V06/in_progress")
    (unlocks V06))

  (atom
    (id V06)
    (name "orphan candidates")
    (teaches "An unmatched item is an orphan candidate, not automatic waste. Parking it preserves the idea while forcing an explicit later decision to support, test, change, or remove it.")
    (asks "Which unmatched items should be parked as orphan candidates, and what decision is deferred for each?")
    (accepts "Names every unmatched item and records a deferred support, test, change, or remove decision; an empty list is accepted only when V05 matched every item.")
    (writes "append one answers record for V06; append each parked candidate to assumptions with evidence_status unknown and source_atom V06; append explicit disposition choices to decisions with resulting position value-map/V07/in_progress; set project.updated_at; set position to value-map/V07/in_progress")
    (unlocks V07))

  (atom
    (id V07)
    (name "alternative distinction")
    (teaches "Value is relative to what the customer does today, including workarounds and inaction. Comparing against accepted alternatives now tests whether the mapped effects create a meaningful difference.")
    (asks "What meaningful difference does this offering provide over the accepted current alternatives for the priority job?")
    (accepts "States at least one specific difference tied to an accepted job, pain, or gain and labels its evidence; records no established difference as unknown.")
    (writes "append one answers record for V07; append supported distinctions to evidence and unsupported distinctions to assumptions; set project.updated_at; set position to value-map/V08/in_progress")
    (unlocks V08))

  (atom
    (id V08)
    (name "value-map gate")
    (teaches "The value-map gate checks that the offering boundary, effects, fit links, alternatives, and orphan decisions are explicit. Passing confirms a coherent design hypothesis, not proven customer demand.")
    (asks "Should this value map pass its gate now, or should one named atom be reopened?")
    (accepts "Records an explicit pass or reopen decision with a reason and target atom; pass requires offering scope, mapped effects, fit links, alternative distinction, and parked orphan candidates or an explicit empty set.")
    (writes "append one decision-kind answers record for V08; append a decisions record with source_atom V08 and the chosen resulting position; on pass set position to value-map/V08/gate_pending and set value-map.md artifact status pending; on reopen set position to value-map/<chosen-atom>/in_progress; set project.updated_at")
    (unlocks "value-map gate: write value-map.md from accepted value-map state, set its artifact status final, mark value-map completed, then set position to business-model/B01/in_progress")))
