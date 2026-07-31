# Start a BMG session

Start a BMG session creates a disposable project slug under the run's `workproduct/bmg/` root and shows the Canvas Mapper section strip after init.

## Sub-features

- `bmg-prepare` uses the shared verify run (all skill work areas already created).
- `bmg-init` writes `session.json` for BMG with the shared verify slug.
- `bmg-status` prints the section strip for canvas-mapper.

## How to get to it (user POV)

- Ask Cursor for a Business Model Canvas / BMG (agent runs BMG `init_session.py`).
- Ask where you are in BMG after init (agent runs BMG `status.py --sections`).

## Driving it with control-value

Preconditions:

- Repo doctor passes without `--run-id`.
- No prior `verify-demo` folder under this run's `workproduct/bmg/`.

- **Prepare run.** Create isolation. Run `python .cursor/skills/verify-value/scripts/control-value.py prepare`. Stdout includes `RUN_ID=` and `WORK_ROOT_BMG=`.
- **Doctor run.** Confirm the run. Run `python .cursor/skills/verify-value/scripts/control-value.py doctor --run-id <RUN_ID>`. Stdout includes `doctor ok`.
- **Init session.** Create the project. Run `python .cursor/skills/verify-value/scripts/control-value.py cli --run-id <RUN_ID> --skill bmg -- init_session.py --name "Verify Demo" --slug verify-demo`. Exit code `0`. File `workproduct/bmg/verify-demo/session.json` exists under the run directory.
- **Status strip.** Show progress. Run `python .cursor/skills/verify-value/scripts/control-value.py cli --run-id <RUN_ID> --skill bmg -- status.py workproduct/bmg/verify-demo/session.json --sections`. Exit code `0` and stdout is a non-empty strip line.
- **Proof.** Keep CLI transcripts under `.verify-runs/<RUN_ID>/artifacts/` and confirm `session.json` has `project.slug` of `verify-demo`.

## Gotchas

- Must pass `--skill bmg`. Default skill is Values and will write the wrong work area.
- Same slug as Values/Teams/lean when verifying a shared journey project; recipes use `verify-demo`.
- Done-enough for Product-Spine business is canvas-mapper gate later; this feature only proves session start.
