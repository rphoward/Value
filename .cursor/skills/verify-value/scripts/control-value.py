#!/usr/bin/env python3
"""Drive journey skill scripts and the spoke /health endpoint for verification."""

from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
RUNS_ROOT = REPO_ROOT / ".verify-runs"
DEFAULT_SPOKE_PORT = 8010

# skill slug -> scripts dir relative to .cursor/skills, workproduct area, required CLIs
SKILL_PACKS: dict[str, dict[str, object]] = {
    "value": {
        "dir": "value",
        "work_area": "value-proposition",
        "required": (
            "init_session.py",
            "status.py",
            "next_question.py",
            "accept_answer.py",
            "write_build_pack.py",
            "promote_context.py",
        ),
    },
    "bmg": {
        "dir": "bmg",
        "work_area": "bmg",
        "required": (
            "init_session.py",
            "status.py",
            "next_question.py",
            "accept_answer.py",
            "write_milestone.py",
        ),
    },
    "teams": {
        "dir": "teams",
        "work_area": "teams",
        "required": (
            "init_session.py",
            "status.py",
            "next_question.py",
            "accept_answer.py",
            "write_milestone.py",
        ),
    },
    "lean-mvp": {
        "dir": "lean-mvp",
        "work_area": "lean-mvp",
        "required": (
            "init_session.py",
            "status.py",
            "next_question.py",
            "accept_answer.py",
            "import_value_context.py",
        ),
    },
}


def skill_scripts(skill: str) -> Path:
    pack = SKILL_PACKS[skill]
    return REPO_ROOT / ".cursor" / "skills" / str(pack["dir"]) / "scripts"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def run_dir(run_id: str) -> Path:
    return RUNS_ROOT / run_id


def meta_path(run_id: str) -> Path:
    return run_dir(run_id) / "meta.json"


def load_meta(run_id: str) -> dict:
    path = meta_path(run_id)
    if not path.is_file():
        raise SystemExit(f"missing run meta: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def save_meta(run_id: str, meta: dict) -> None:
    meta_path(run_id).write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")


def work_root_for(meta: dict, skill: str) -> Path:
    roots = meta.get("work_roots") or {}
    if skill in roots:
        return Path(roots[skill])
    if skill == "value" and meta.get("work_root"):
        return Path(meta["work_root"])
    raise SystemExit(
        f"no work root for skill {skill!r} in run meta; re-run prepare"
    )


def cmd_prepare(args: argparse.Namespace) -> int:
    run_id = args.run_id or f"verify-{utc_now()}"
    root = run_dir(run_id)
    artifacts = root / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    work_roots: dict[str, str] = {}
    for skill, pack in SKILL_PACKS.items():
        work = root / "workproduct" / str(pack["work_area"])
        work.mkdir(parents=True, exist_ok=True)
        work_roots[skill] = str(work)
    meta = {
        "run_id": run_id,
        "created_at": utc_now(),
        "repo_root": str(REPO_ROOT),
        "work_root": work_roots["value"],
        "work_roots": work_roots,
        "artifacts": str(artifacts),
        "spoke_pid": None,
        "spoke_port": None,
        "spoke_url": None,
    }
    save_meta(run_id, meta)
    print(f"RUN_ID={run_id}")
    print(f"RUN_DIR={root}")
    print(f"WORK_ROOT={work_roots['value']}")
    for skill, path in work_roots.items():
        print(f"WORK_ROOT_{skill.upper().replace('-', '_')}={path}")
    print(f"ARTIFACTS={artifacts}")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    problems: list[str] = []
    if not (REPO_ROOT / "pyproject.toml").is_file():
        problems.append("missing pyproject.toml")
    for skill, pack in SKILL_PACKS.items():
        scripts = skill_scripts(skill)
        if not scripts.is_dir():
            problems.append(f"missing skill scripts: {scripts}")
            continue
        for name in pack["required"]:  # type: ignore[union-attr]
            if not (scripts / str(name)).is_file():
                problems.append(f"missing {skill}/{name}")
    try:
        import value  # noqa: F401
    except Exception as exc:  # pragma: no cover - environment probe
        problems.append(f"import value failed: {exc}")

    if args.run_id:
        meta = load_meta(args.run_id)
        root = run_dir(args.run_id)
        if not root.is_dir():
            problems.append(f"missing run dir {root}")
        roots = meta.get("work_roots") or {"value": meta.get("work_root")}
        for skill, path in roots.items():
            if path and not Path(path).is_dir():
                problems.append(f"missing work root for {skill}: {path}")
        if meta.get("spoke_pid"):
            port = meta.get("spoke_port")
            url = meta.get("spoke_url")
            try:
                with urllib.request.urlopen(f"{url}/health", timeout=2) as resp:
                    body = resp.read().decode("utf-8")
                if body.strip() != "ok":
                    problems.append(f"spoke /health returned {body!r}")
                else:
                    print(f"spoke healthy at {url} port={port} pid={meta['spoke_pid']}")
            except Exception as exc:
                problems.append(f"spoke not reachable: {exc}")

    if problems:
        for item in problems:
            print(f"FAIL {item}", file=sys.stderr)
        return 1
    print("doctor ok")
    print(f"REPO_ROOT={REPO_ROOT}")
    print(f"SKILLS={','.join(SKILL_PACKS)}")
    if args.run_id:
        print(f"RUN_ID={args.run_id}")
        meta = load_meta(args.run_id)
        print(f"WORK_ROOT={meta.get('work_root')}")
    return 0


def cmd_cli(args: argparse.Namespace) -> int:
    if not args.script_args:
        raise SystemExit(
            "usage: control-value.py cli --run-id <id> [--skill value|bmg|teams|lean-mvp] "
            "-- <script.py> [args...]"
        )
    skill = args.skill
    if skill not in SKILL_PACKS:
        raise SystemExit(f"unknown skill {skill!r}; choose {', '.join(SKILL_PACKS)}")
    meta = load_meta(args.run_id)
    script_name = args.script_args[0]
    script_args = list(args.script_args[1:])
    scripts = skill_scripts(skill)
    script_path = scripts / script_name
    if not script_path.is_file():
        raise SystemExit(f"unknown {skill} script: {script_name}")

    if script_name == "init_session.py" and "--root" not in script_args:
        script_args.extend(["--root", str(work_root_for(meta, skill))])

    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT / "src") + os.pathsep + env.get("PYTHONPATH", "")
    cwd = run_dir(args.run_id)
    cmd = [sys.executable, str(script_path), *script_args]
    print("CMD", " ".join(cmd))
    print("CWD", cwd)
    print(f"SKILL={skill}")
    result = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    stamp = utc_now()
    transcript = Path(meta["artifacts"]) / f"cli-{skill}-{script_name}-{stamp}.txt"
    transcript.write_text(
        "\n".join(
            [
                f"skill: {skill}",
                f"cmd: {' '.join(cmd)}",
                f"cwd: {cwd}",
                f"exit: {result.returncode}",
                "--- stdout ---",
                result.stdout,
                "--- stderr ---",
                result.stderr,
            ]
        ),
        encoding="utf-8",
    )
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    print(f"TRANSCRIPT={transcript}")
    return result.returncode


def cmd_spoke_start(args: argparse.Namespace) -> int:
    run_id = args.run_id
    meta = load_meta(run_id)
    if meta.get("spoke_pid"):
        print(f"spoke already recorded pid={meta['spoke_pid']} url={meta['spoke_url']}")
        return 0
    port = args.port or DEFAULT_SPOKE_PORT
    log_path = Path(meta["artifacts"]) / "spoke.log"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT / "src") + os.pathsep + env.get("PYTHONPATH", "")
    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "value.presentation.app:app",
        "--host",
        "127.0.0.1",
        "--port",
        str(port),
    ]
    log_file = log_path.open("w", encoding="utf-8")
    proc = subprocess.Popen(
        cmd,
        cwd=REPO_ROOT,
        env=env,
        stdout=log_file,
        stderr=subprocess.STDOUT,
    )
    url = f"http://127.0.0.1:{port}"
    deadline = time.time() + 15
    while time.time() < deadline:
        if proc.poll() is not None:
            log_file.close()
            raise SystemExit(f"spoke exited early; see {log_path}")
        try:
            with urllib.request.urlopen(f"{url}/health", timeout=1) as resp:
                if resp.read().decode("utf-8").strip() == "ok":
                    break
        except (urllib.error.URLError, TimeoutError):
            time.sleep(0.2)
    else:
        proc.terminate()
        log_file.close()
        raise SystemExit(f"spoke did not become ready at {url}")
    meta["spoke_pid"] = proc.pid
    meta["spoke_port"] = port
    meta["spoke_url"] = url
    meta["spoke_log"] = str(log_path)
    save_meta(run_id, meta)
    print(f"SPOKE_PID={proc.pid}")
    print(f"SPOKE_URL={url}")
    print(f"SPOKE_LOG={log_path}")
    return 0


def cmd_spoke_stop(args: argparse.Namespace) -> int:
    meta = load_meta(args.run_id)
    pid = meta.get("spoke_pid")
    if not pid:
        print("no spoke pid recorded")
        return 0
    try:
        os.kill(pid, signal.SIGTERM)
    except OSError as exc:
        print(f"kill {pid}: {exc}")
    meta["spoke_pid"] = None
    meta["spoke_port"] = None
    meta["spoke_url"] = None
    save_meta(args.run_id, meta)
    print(f"stopped spoke pid={pid}")
    return 0


def cmd_spoke_get(args: argparse.Namespace) -> int:
    meta = load_meta(args.run_id)
    url = meta.get("spoke_url")
    if not url:
        raise SystemExit("spoke not started for this run")
    path = args.path if args.path.startswith("/") else f"/{args.path}"
    full = f"{url}{path}"
    with urllib.request.urlopen(full, timeout=5) as resp:
        body = resp.read().decode("utf-8")
        code = resp.status
    stamp = utc_now()
    out = Path(meta["artifacts"]) / f"spoke-get-{stamp}.txt"
    out.write_text(f"GET {full}\nstatus: {code}\n--- body ---\n{body}\n", encoding="utf-8")
    print(body)
    print(f"TRANSCRIPT={out}")
    return 0 if code == 200 else 1


def cmd_cleanup(args: argparse.Namespace) -> int:
    run_id = args.run_id
    meta = load_meta(run_id)
    if meta.get("spoke_pid"):
        cmd_spoke_stop(args)
    workproduct = run_dir(run_id) / "workproduct"
    if workproduct.exists():
        for path in sorted(workproduct.rglob("*"), reverse=True):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                path.rmdir()
        if workproduct.is_dir() and not any(workproduct.iterdir()):
            workproduct.rmdir()
    print(f"cleaned workproduct for {run_id}")
    print(f"ARTIFACTS_KEPT={meta['artifacts']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    prepare = sub.add_parser("prepare", help="Create an isolated verification run directory")
    prepare.add_argument("--run-id", default=None)
    prepare.set_defaults(func=cmd_prepare)

    doctor = sub.add_parser("doctor", help="Read-only readiness check")
    doctor.add_argument("--run-id", default=None)
    doctor.set_defaults(func=cmd_doctor)

    cli = sub.add_parser("cli", help="Run a journey skill script inside a run directory")
    cli.add_argument("--run-id", required=True)
    cli.add_argument(
        "--skill",
        default="value",
        choices=sorted(SKILL_PACKS.keys()),
        help="Which .cursor/skills/<name> scripts to run (default: value)",
    )
    cli.add_argument("script_args", nargs=argparse.REMAINDER)
    cli.set_defaults(func=cmd_cli)

    spoke_start = sub.add_parser("spoke-start", help="Start spoke /health on an isolated port")
    spoke_start.add_argument("--run-id", required=True)
    spoke_start.add_argument("--port", type=int, default=DEFAULT_SPOKE_PORT)
    spoke_start.set_defaults(func=cmd_spoke_start)

    spoke_stop = sub.add_parser("spoke-stop", help="Stop spoke started for this run")
    spoke_stop.add_argument("--run-id", required=True)
    spoke_stop.set_defaults(func=cmd_spoke_stop)

    spoke_get = sub.add_parser("spoke-get", help="GET a spoke path and save transcript")
    spoke_get.add_argument("--run-id", required=True)
    spoke_get.add_argument("--path", default="/health")
    spoke_get.set_defaults(func=cmd_spoke_get)

    cleanup = sub.add_parser("cleanup", help="Remove run workproduct; keep artifacts")
    cleanup.add_argument("--run-id", required=True)
    cleanup.set_defaults(func=cmd_cleanup)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "cli" and args.script_args and args.script_args[0] == "--":
        args.script_args = args.script_args[1:]
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
