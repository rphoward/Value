# Spoke health

Spoke health is the scaffold Starlette app's `/health` endpoint. It proves the optional host spoke starts; it is not the Product-Spine product.

## Sub-features

- `spoke-start` launches uvicorn on an isolated port.
- `spoke-health` returns plain text `ok`.
- `spoke-stop` terminates only the pid this run started.

## How to get to it (user POV)

- Run `tools/start-value.ps1` locally (port 8000) for human smoke.
- For verification, use `control-value spoke-start` on port 8010.

## Driving it with control-value

Preconditions:

- Prepare + doctor for this run.
- Port 8010 is free.

- **Start spoke.** Run `python .cursor/skills/verify-value/scripts/control-value.py spoke-start --run-id <RUN_ID> --port 8010`. Stdout includes `SPOKE_URL=http://127.0.0.1:8010`.
- **Get health.** Run `python .cursor/skills/verify-value/scripts/control-value.py spoke-get --run-id <RUN_ID> --path /health`. Stdout body is `ok`. Transcript saved under artifacts.
- **Stop spoke.** Run `python .cursor/skills/verify-value/scripts/control-value.py spoke-stop --run-id <RUN_ID>`.
- **Proof.** Keep `spoke-get-*.txt` and `spoke.log`. Confirm stop cleared `spoke_pid` in `meta.json`.

## Gotchas

- Do not kill by process name `uvicorn`. Stop via `spoke-stop` using the recorded pid.
- Port 8000 is reserved for the human launcher. Verification uses 8010 by default.
- The spoke has no other routes today. A 404 on `/` is not a product failure.
