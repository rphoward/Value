# Testing

Back-link: [overview.md](./overview.md)

## Harness

New tests under `tests/test_prompt_suite_*.py` (or pack-local `tools/prompt-suite-compile/tests/` if kept self-contained for foreign repos). Prefer pack-local tests so the lever travels.

## Cases (minimum)

1. Parse value suite → IR has four modules + KB keys.
2. Parse lean-product suite → IR has four subskills + KB keys.
3. Scaffold writes required paths and never touches `skills/value/`.
4. Session runtime toy curriculum. init/accept/milestone.
5. `audit_dag` value standard. missing_hard empty.
6. `audit_dag` value express. missing_hard equals known skip set.
7. `audit_dag` soft-but-required detection on a planted fixture.
8. Promote fail-closed without gate atom.
9. Standalone smoke script exits 0 in a temp dir.

## Patterns to reuse from this repo

Mirror digests (`iter_skill_files` / `file_digest`), atom DAG cycle checks, SKILL↔reference linkage, temp `session.json` + subprocess `run_script` goldens, adversarial “no atom-id leakage” cases. See `tests/value_skill_support.py`, `tests/test_value_skill_package.py`, `tests/test_value_skill_dag.py`, `tests/test_value_session_integrity.py`.

## Surfaces

- CLI. compile, audit, promote, smoke (`control-cli`).
- Agent. FOR_AGENTS dry-run stop at human gate (manual once per release).

## Non-goals for automated tests

- Full live agent curriculum quality.
- Pixel/UI.
- Values GitHub publish.
