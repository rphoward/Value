# Promote vernacular

Promote vernacular drafts Term / `_Avoid_` lines from `CONTEXT.product.md` and optionally merges them into a repo-root `CONTEXT.md` only when `--apply` is passed.

## Sub-features

- `promote-dry-run` prints a draft and writes nothing.
- `promote-apply` merges new terms into run-local `CONTEXT.md`.
- `promote-dry-run-wins` proves `--dry-run` blocks writes even with `--apply`.

## How to get to it (user POV)

- After Values surfaces a promote offer, run `promote_context.py` on the session or seed file.
- Pass `--apply` only after reviewing the dry-run draft.

## Driving it with control-value

Preconditions:

- `CONTEXT.product.md` exists for `verify-demo` (build-pack-seed).
- Run directory is the effective repo root for this drive (helper cwd).

- **Dry-run.** Draft only. Run `python .cursor/skills/verify-value/scripts/control-value.py cli --run-id <RUN_ID> -- promote_context.py workproduct/value-proposition/verify-demo/CONTEXT.product.md --dry-run`. Exit code `0`. Stdout contains `## Language` and at least one `**` term block. File `CONTEXT.md` is still absent in the run directory.
- **Apply.** Merge terms. Run `python .cursor/skills/verify-value/scripts/control-value.py cli --run-id <RUN_ID> -- promote_context.py workproduct/value-proposition/verify-demo/CONTEXT.product.md --apply`. Exit code `0`. File `CONTEXT.md` exists under the run directory and contains `## Language`.
- **Dry-run wins.** Optional regression. Delete or note `CONTEXT.md`, then run with `--dry-run --apply --agents`. Exit code `0`. No new `AGENTS.md` and no CONTEXT write when `--dry-run` is present.
- **Proof.** Keep dry-run and apply transcripts. Re-read `CONTEXT.md` for Term / `_Avoid_` lines.

## Gotchas

- Finding the repo root walks up for a `workproduct/` directory; the verify run dir provides that. Do not run promote against the live monorepo root during verification.
- `--agents` is a separate write gate from `--apply`.
- Duplicate seed bullets are deduped by term name; do not assert exact bullet counts from the seed.
