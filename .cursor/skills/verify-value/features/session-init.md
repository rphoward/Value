# Start a Values session

Start a Values session creates a disposable project slug under an isolated workproduct root and shows a one-line progress strip the human would see after init.

## Sub-features

- `session-prepare` creates a verify run directory.
- `session-init` writes `session.json` for a named project.
- `session-status` prints the section strip for the active module.

## How to get to it (user POV)

- Ask Cursor to start Values for a new idea (agent runs `init_session.py`).
- Ask where you are in Values after init (agent runs `status.py --sections`).

## Driving it with control-value

Preconditions:

- Repo doctor passes without `--run-id`.
- No prior `verify-demo` folder under this run's work root.

- **Prepare run.** Create isolation. Run `python .cursor/skills/verify-value/scripts/control-value.py prepare`. Stdout includes `RUN_ID=` and `WORK_ROOT=`.
- **Doctor run.** Confirm the run. Run `python .cursor/skills/verify-value/scripts/control-value.py doctor --run-id <RUN_ID>`. Stdout includes `doctor ok`.
- **Init session.** Create the project. Run `python .cursor/skills/verify-value/scripts/control-value.py cli --run-id <RUN_ID> -- init_session.py --name "Verify Demo" --slug verify-demo`. Exit code `0`. File `workproduct/value-proposition/verify-demo/session.json` exists under the run directory.
- **Status strip.** Show progress. Run `python .cursor/skills/verify-value/scripts/control-value.py cli --run-id <RUN_ID> -- status.py workproduct/value-proposition/verify-demo/session.json --sections`. Exit code `0` and stdout is a non-empty strip line.
- **Proof.** Keep both CLI transcripts under `.verify-runs/<RUN_ID>/artifacts/` and confirm `session.json` has `project.slug` of `verify-demo`.

## Gotchas

- Omitting `--slug` derives a slug from `--name`; recipes that assert paths must pass `--slug verify-demo`.
- Running `init_session.py` without `control-value` can write into the live repo workproduct root. Always use the helper.
- `--operator` status is for telemetry. Prefer `--sections` for the human-facing strip.
- Canonical slug field is `project.slug`, not a top-level `"slug"` key.
