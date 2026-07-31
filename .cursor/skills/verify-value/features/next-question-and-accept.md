# Ask and accept the next atom

Ask and accept advances one Values coaching atom: fetch the next question, then accept a human answer so the session ledger moves.

## Sub-features

- `next-question` prints the current atom payload.
- `accept-answer` records an answer and advances position.
- `status-after-accept` shows the strip after the accept.

## How to get to it (user POV)

- Continue a Values session (agent runs `next_question.py`, then `accept_answer.py` with the human's words).

## Driving it with control-value

Preconditions:

- Session-init completed for slug `verify-demo` in this run.
- Doctor passes for the run id.

- **Next question.** Fetch the atom. Run `python .cursor/skills/verify-value/scripts/control-value.py cli --run-id <RUN_ID> -- next_question.py workproduct/value-proposition/verify-demo/session.json`. Exit code `0`. Stdout JSON includes an `atom_id` (or equivalent ask payload).
- **Accept answer.** Record a fact. Run `python .cursor/skills/verify-value/scripts/control-value.py cli --run-id <RUN_ID> -- accept_answer.py workproduct/value-proposition/verify-demo/session.json --atom-id <ATOM_ID> --answer "Verification segment for servers trading a shift tonight" --kind fact`. Exit code `0`.
- **Status after.** Confirm movement. Run `python .cursor/skills/verify-value/scripts/control-value.py cli --run-id <RUN_ID> -- status.py workproduct/value-proposition/verify-demo/session.json --sections`. Exit code `0`.
- **Proof.** Transcripts exist for next and accept. `session.json` answers array contains the accepted text.

## Gotchas

- Atom ids change with curriculum; always copy `atom_id` from the latest `next_question.py` stdout for this run.
- Do not invent atom ids from memory.
- Gate atoms may need `--gate-pending`; ordinary profile atoms do not.
