# Gate UX port into prompt-suite-compile (handoff)

Context may compact. This file is the source of truth for the in-flight Feature.

## Goal

Port lean-mvp gate UX into `assets/session-runtime/` in this skill pack so new scaffolds do not re-ship soft-lock / stay-on-gate / missing `--brief` / bulk-on-gate bugs.

Do **not** modify `skills/value/` or `.cursor/skills/value/`.
Do **not** rewrite lean-mvp unless a shared bug remains (lean-mvp already fixed).

## Data shape

Gate ceremony is one transaction helper `prepare_gate_accept(...)` returning `(records_payload, effective_gate_pending, error)`.

- Autofill canonical `decisions[]` on `--gate-pending` or canonical pass phrase.
- Refuse `--stay` on gate atoms.
- Never treat foreign bypass as pass.
- Dedupe via `session_has_gate_pass` on reopen.

Keep template portability: `ENTRY_MODULE`, `WORKPRODUCT_ROOT` / `skill-config.json`. Prefer `resolve_repo_root()` + config relative root when possible.

## Files to change

1. `assets/session-runtime/_session/runtime.py` — port helpers from `.cursor/skills/lean-mvp/scripts/_session/runtime.py` (gate block only; keep template ENTRY_* constants).
2. `assets/session-runtime/_session/__init__.py` — export new symbols.
3. `assets/session-runtime/_session/catalog.py` — optional `resolve_repo_root` + default workproduct from config under repo root.
4. `assets/session-runtime/accept_answer.py` — call `prepare_gate_accept`.
5. `assets/session-runtime/accept_bulk.py` — refuse `atom["gate"]`.
6. `assets/session-runtime/status.py` — `--brief` no-op alias.
7. `assets/session-runtime/init_session.py` — use repo-anchored default when resolvable.
8. `compile.py` generated `session-contract.md` stub — gate autofill paragraph.
9. `FOR_AGENTS.md` — short gate UX paragraph.
10. `smoke.py` — after next_question: seed/accept to first gate if needed OR document minimal path; at least `status --brief` + gate accept on fixture if feasible.
11. `tests/test_prompt_suite_compile_gate_ux.py` — scaffold sample fixture to temp, run gate UX cases against **draft scripts** (mirror `tests/test_lean_mvp_gate_ux.py` spirit).

## Success criteria

```text
python -m pytest tests/test_prompt_suite_compile_gate_ux.py tests/test_prompt_suite_compile.py -v
python .cursor/skills/scripted-skill-from-doc/scripts/selftest.py
```

Both green. No value skill edits.

## Done

- Ported `prepare_gate_accept` and related gate helpers into `assets/session-runtime/_session/runtime.py`.
- Wired `accept_answer.py`, `accept_bulk.py` gate refuse, `status.py --brief`, `init_session.py` repo-anchored default via `default_workproduct_root()`.
- Added `resolve_repo_root` / `default_workproduct_root` to template `catalog.py` (skill-config `workproduct_root`, not lean-mvp hardcode).
- Updated `FOR_AGENTS.md`, `compile.py` session-contract stub, `smoke.py` (brief + gate accept + write_milestone).
- Added `tests/test_prompt_suite_compile_gate_ux.py` against scaffold output.

## Verify order

1. Template code compiles / imports.
2. New gate UX test file green.
3. Existing compile tests green.
4. selftest green.
