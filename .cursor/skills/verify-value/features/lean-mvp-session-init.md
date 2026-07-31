# Start a lean-mvp session

Start a lean-mvp session creates a disposable project slug under the run's `workproduct/lean-mvp/` root and shows the lean section strip after init.

## Sub-features

- `lean-prepare` uses the shared verify run.
- `lean-init` writes `session.json` for lean-mvp with the shared verify slug.
- `lean-status` prints the section strip for the active lean module.

## How to get to it (user POV)

- Ask Cursor to run the lean MVP playbook (agent runs lean-mvp `init_session.py`).
- Ask where you are in lean-mvp after init (agent runs lean-mvp `status.py --sections`).

## Driving it with control-value

Preconditions:

- Repo doctor passes without `--run-id`.
- No prior `verify-demo` folder under this run's `workproduct/lean-mvp/`.

- **Prepare run.** Create isolation. Run `python .cursor/skills/verify-value/scripts/control-value.py prepare`. Stdout includes `RUN_ID=` and `WORK_ROOT_LEAN_MVP=`.
- **Doctor run.** Confirm the run. Run `python .cursor/skills/verify-value/scripts/control-value.py doctor --run-id <RUN_ID>`. Stdout includes `doctor ok`.
- **Init session.** Create the project. Run `python .cursor/skills/verify-value/scripts/control-value.py cli --run-id <RUN_ID> --skill lean-mvp -- init_session.py --name "Verify Demo" --slug verify-demo`. Exit code `0`. File `workproduct/lean-mvp/verify-demo/session.json` exists under the run directory.
- **Status strip.** Show progress. Run `python .cursor/skills/verify-value/scripts/control-value.py cli --run-id <RUN_ID> --skill lean-mvp -- status.py workproduct/lean-mvp/verify-demo/session.json --sections`. Exit code `0` and stdout is a non-empty strip line.
- **Proof.** Keep CLI transcripts under `.verify-runs/<RUN_ID>/artifacts/` and confirm `session.json` has `project.slug` of `verify-demo`.

## Gotchas

- Must pass `--skill lean-mvp`.
- Importing Values context (`import_value_context.py`) is a separate path; this feature only proves lean session start.
- Product-Spine done-enough for MVP is mvp-scope gate later; not required here.
