(def-ref profile
  (linked-from protocol-2 protocol-3 protocol-4)
  (purpose "Define one customer segment and its accepted jobs, pains, gains, alternatives, evidence, and priority job before describing the offering.")
  (evidence-policy "Keep facts, inferences, hypotheses, decisions, and unknowns labeled. Stop asking why when the next answer would be speculation.")

  (atom
    (id P01)
    (name "segment boundary")
    (teaches "A useful profile describes one recognizable customer segment, not everybody who might benefit. This boundary comes first because later jobs and evidence must belong to the same people.")
    (asks "Which specific customer segment are we profiling, and who is outside that boundary?")
    (accepts "Names a segment using observable role or context and states at least one exclusion; accepts unknown for a boundary not yet established.")
    (writes "append one answers record for P01; append unresolved boundaries to unknowns; set project.updated_at; set position to profile/P02/in_progress")
    (unlocks P02))

  (atom
    (id P02)
    (name "situation and trigger")
    (teaches "Jobs arise in a situation and usually begin with a trigger. Establishing that moment keeps the profile tied to behavior rather than a general persona.")
    (asks "In what concrete situation does this segment begin trying to make progress, and what triggers that effort?")
    (accepts "Describes an observable situation and trigger, or labels either one unknown; distinguishes observed facts from inference.")
    (writes "append one answers record for P02; append supported claims to evidence and missing required details to unknowns; set project.updated_at; set position to profile/P03/in_progress")
    (unlocks P03))

  (atom
    (id P03)
    (name "functional job")
    (teaches "A functional job is the practical progress the customer is trying to make, independent of a proposed product. It follows the trigger so the job can be stated in the customer's actual context; probing why stops before the explanation becomes speculative.")
    (asks "What practical progress is this segment trying to make in that situation?")
    (accepts "States the progress as an action and outcome, with its evidence kind labeled; does not substitute a product feature or unsupported deeper motive.")
    (writes "append one answers record for P03; append any unverified motive to assumptions or unknowns; set project.updated_at; set position to profile/P04/in_progress")
    (unlocks P04))

  (atom
    (id P04)
    (name "social job")
    (teaches "A social job describes how the customer wants to be seen by other people while making progress. It comes after the practical job so status concerns remain connected to a real situation.")
    (asks "How does this segment want relevant other people to see them while they pursue this job?")
    (accepts "Names the audience and desired impression, or records that no social job is established; labels evidence and unknowns.")
    (writes "append one answers record for P04; append missing social evidence to unknowns when relevant; set project.updated_at; set position to profile/P05/in_progress")
    (unlocks P05))

  (atom
    (id P05)
    (name "emotional job")
    (teaches "An emotional job is the feeling the customer seeks or wants to avoid during the work. It follows the social job to separate private experience from public impression.")
    (asks "What does this segment want to feel, or avoid feeling, while making this progress?")
    (accepts "Names a desired or avoided feeling grounded in the situation, or records it unknown; does not present an inferred emotion as fact.")
    (writes "append one answers record for P05; append unsupported emotional claims to assumptions and missing ones to unknowns; set project.updated_at; set position to profile/P06/in_progress")
    (unlocks P06))

  (atom
    (id P06)
    (name "supporting jobs")
    (teaches "Supporting jobs surround the main job when customers compare and buy, contribute feedback, or stop and transfer use. Capturing them now exposes work that can shape adoption without displacing the main job.")
    (asks "Which buying, co-creating, or transferring tasks accompany this segment's main job?")
    (accepts "Names applicable supporting tasks by category, or explicitly records none or unknown; keeps them tied to the accepted segment.")
    (writes "append one answers record for P06; append unresolved supporting tasks to unknowns; set project.updated_at; set position to profile/P07/in_progress")
    (unlocks P07))

  (atom
    (id P07)
    (name "pains")
    (teaches "Pains are bad outcomes, obstacles, and risks encountered while pursuing accepted jobs. Prioritizing them now prevents a long undifferentiated complaint list.")
    (visual "Picture the job as a boat and each pain as an anchor: the anchor that most slows real progress deserves attention first.")
    (asks "Which pains most obstruct the accepted jobs, and how severe is each one?")
    (accepts "Names at least one bad outcome, obstacle, or risk and orders pains using extreme, moderate, or light severity with a stated basis; records absent evidence as unknown.")
    (writes "append one answers record for P07; append pain evidence with kind, source, and strength; append unsupported pain claims to assumptions; set project.updated_at; set position to profile/P08/in_progress")
    (unlocks P08))

  (atom
    (id P08)
    (name "gains")
    (teaches "Gains are outcomes customers require, expect, desire, or would value unexpectedly. They follow pains so positive outcomes are not merely restated fixes for every obstacle.")
    (asks "Which outcomes would count as gains for this segment, and how relevant is each one?")
    (accepts "Names at least one outcome and classifies it as essential, expected, desired, or unexpected with a stated basis; labels missing evidence unknown.")
    (writes "append one answers record for P08; append gain evidence with kind, source, and strength; append unsupported gain claims to assumptions; set project.updated_at; set position to profile/P09/in_progress")
    (unlocks P09))

  (atom
    (id P09)
    (name "current alternatives")
    (teaches "Customers already handle the job somehow, including manual work, delay, or doing nothing. Current alternatives reveal the comparison standard and provide evidence about what remains unsatisfied.")
    (asks "What does this segment do today instead, including workarounds or choosing not to act?")
    (accepts "Names at least one current behavior or explicitly records it unknown, with facts separated from inference.")
    (writes "append one answers record for P09; append observed alternative behavior to evidence and unverified alternatives to assumptions; set project.updated_at; set position to profile/P10/in_progress")
    (unlocks P10))

  (atom
    (id P10)
    (name "evidence and early action")
    (teaches "Evidence becomes stronger as customers move from describing a problem to searching, improvising, budgeting, or committing resources. Qualification comes now because the profile has enough claims to compare against actual action, and polite agreement remains weak evidence.")
    (visual "Use an action ladder: problem mentioned → search begun → workaround built → time or money committed; higher rungs support a claim more strongly.")
    (asks "What observed behavior or commitment supports this profile, and where does it sit on the action ladder?")
    (accepts "Provides a claim, evidence kind, source, and strength for each cited observation; behavior or commitment outranks spoken approval, and missing evidence remains unknown.")
    (writes "append one answers record for P10; append schema-valid evidence records with claim, kind, source, and strength; append unsupported required claims to unknowns; set project.updated_at; set position to profile/P11/in_progress")
    (unlocks P11))

  (atom
    (id P11)
    (name "priority job")
    (teaches "A priority job concentrates design effort on progress that matters, is felt, remains unsatisfied, and can support a viable exchange. The criteria guide discussion rather than automatically declaring the right target.")
    (asks "Which accepted job should be the priority, and what labeled evidence supports that choice?")
    (accepts "Selects one accepted job, gives a reason tied to importance, immediacy, dissatisfaction, or economic behavior, and preserves unsupported criteria as unknown.")
    (writes "append one decision-kind answers record for P11; append a decisions record with source_atom P11 and resulting position profile/P12/in_progress; set project.updated_at; set position to profile/P12/in_progress")
    (unlocks P12))

  (atom
    (id P12)
    (name "profile gate")
    (teaches "The profile gate checks that one segment, its priority job, pains, gains, alternatives, and evidence labels form a usable basis for solution design. Passing the gate records a decision; it does not turn assumptions or unknowns into facts.")
    (asks "Should this customer profile pass its gate now, or should one named atom be reopened?")
    (accepts "Records an explicit pass or reopen decision with a reason and target atom; pass requires a bounded segment, priority job, pains, gains, alternatives, and labeled evidence or explicit unknowns.")
    (writes "append one decision-kind answers record for P12; append a decisions record with source_atom P12 and the chosen resulting position; on pass set position to profile/P12/gate_pending and set customer-profile.md artifact status pending; on reopen set position to profile/<chosen-atom>/in_progress; set project.updated_at")
    (unlocks "profile gate: write customer-profile.md from accepted profile state, set its artifact status final, mark profile completed, then set position to value-map/V01/in_progress")))
