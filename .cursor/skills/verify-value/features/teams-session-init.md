# Start a Teams session

Start a Teams session creates a disposable project slug under the run's `workproduct/teams/` root and shows the TAM Planner section strip after init.

## Sub-features

- `teams-prepare` uses the shared verify run.
- `teams-init` writes `session.json` for Teams with the shared verify slug.
- `teams-status` prints the section strip for tam-planner.

## How to get to it (user POV)

- Ask Cursor for team alignment / TAM / team friction help (agent runs Teams `init_session.py`).
- Ask where you are in Teams after init (agent runs Teams `status.py --sections`).

## Driving it with control-value

Preconditions:

- Repo doctor passes without `--run-id`.
- No prior `verify-demo` folder under this run's `workproduct/teams/`.

- **Prepare run.** Create isolation. Run `python .cursor/skills/verify-value/scripts/control-value.py prepare`. Stdout includes `RUN_ID=` and `WORK_ROOT_TEAMS=`.
- **Doctor run.** Confirm the run. Run `python .cursor/skills/verify-value/scripts/control-value.py doctor --run-id <RUN_ID>`. Stdout includes `doctor ok`.
- **Init session.** Create the project. Run `python .cursor/skills/verify-value/scripts/control-value.py cli --run-id <RUN_ID> --skill teams -- init_session.py --name "Verify Demo" --slug verify-demo`. Exit code `0`. File `workproduct/teams/verify-demo/session.json` exists under the run directory.
- **Status strip.** Show progress. Run `python .cursor/skills/verify-value/scripts/control-value.py cli --run-id <RUN_ID> --skill teams -- status.py workproduct/teams/verify-demo/session.json --sections`. Exit code `0` and stdout mentions tam-planner / Mission and Period (or equivalent section strip).
- **Proof.** Keep CLI transcripts under `.verify-runs/<RUN_ID>/artifacts/` and confirm `session.json` has `project.slug` of `verify-demo`.

## Gotchas

- Must pass `--skill teams`.
- Product-Spine done-enough for teams is the tam-planner gate later; this feature only proves session start.
- Deeper modules (assessor, contract, conflict) are not required for this proof.
