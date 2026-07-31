# Emit the product seed

Emit the product seed writes `CONTEXT.product.md` (and sibling build-pack files) into the session folder so coding agents have a glossary seed.

## Sub-features

- `build-pack-force` writes the pack before all gates pass.
- `seed-present` confirms `CONTEXT.product.md` on disk.

## How to get to it (user POV)

- Pause a Values session or pass a module gate (agent runs `write_build_pack.py`, often via milestone/pause).
- Force a pack mid-session with `--force` when verifying the emitter.

## Driving it with control-value

Preconditions:

- Session exists for `verify-demo` in this run (session-init).
- Prefer at least one accepted answer so the seed is not empty boilerplate only.

- **Force pack.** Write exports. Run `python .cursor/skills/verify-value/scripts/control-value.py cli --run-id <RUN_ID> -- write_build_pack.py workproduct/value-proposition/verify-demo/session.json --force`. Exit code `0`. Stdout lists written paths including `CONTEXT.product.md`.
- **Proof.** File `workproduct/value-proposition/verify-demo/CONTEXT.product.md` exists under the run directory and is non-empty. Keep the CLI transcript.

## Gotchas

- Without `--force`, the script refuses when modules are incomplete. Verification of mid-session emit uses `--force` on purpose.
- Live pause paths also refresh north-star and trail files; this feature only requires the CONTEXT seed.
