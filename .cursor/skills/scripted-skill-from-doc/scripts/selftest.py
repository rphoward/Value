#!/usr/bin/env python3
"""Standalone self-test for the scripted-skill-from-doc pack."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from _paths import SAMPLE_FIXTURE, SCRIPTS_DIR


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=SCRIPTS_DIR,
        capture_output=True,
        text=True,
        check=False,
    )


def main() -> int:
    check = run([str(SCRIPTS_DIR / "compile.py"), "check"])
    print(check.stdout)
    if check.returncode != 0:
        print(check.stderr, file=sys.stderr)
        print("selftest: check failed", file=sys.stderr)
        return check.returncode

    sample = SAMPLE_FIXTURE
    tmp = Path(tempfile.mkdtemp(prefix="psc-selftest-"))
    try:
        out = tmp / "drafts"
        scaffold = run(
            [
                str(SCRIPTS_DIR / "compile.py"),
                "scaffold",
                "--source",
                str(sample),
                "--slug",
                "demo-selftest",
                "--out",
                str(out),
            ]
        )
        print(scaffold.stdout)
        if scaffold.returncode != 0:
            print(scaffold.stderr, file=sys.stderr)
            print("selftest: scaffold failed", file=sys.stderr)
            return scaffold.returncode
        draft = out / "demo-selftest"
        if not (draft / "SKILL.md").is_file():
            print("selftest: draft SKILL.md missing", file=sys.stderr)
            return 1

        audit = run(
            [str(SCRIPTS_DIR / "audit_dag.py"), str(draft), "--mode", "standard"]
        )
        print(audit.stdout)
        if audit.returncode != 0:
            print(audit.stderr, file=sys.stderr)
            print("selftest: audit failed", file=sys.stderr)
            return audit.returncode
        report = json.loads(audit.stdout)
        if not report.get("ok"):
            print("selftest: audit report not ok", file=sys.stderr)
            return 1

        smoke = run([str(SCRIPTS_DIR / "smoke.py"), str(draft)])
        print(smoke.stdout)
        if smoke.returncode != 0:
            print(smoke.stderr, file=sys.stderr)
            print("selftest: smoke failed", file=sys.stderr)
            return smoke.returncode

        bad = run(
            [
                str(SCRIPTS_DIR / "compile.py"),
                "scaffold",
                "--source",
                str(sample),
                "--slug",
                "value",
                "--out",
                str(out),
            ]
        )
        if bad.returncode == 0:
            print("selftest: slug value should be refused", file=sys.stderr)
            return 1

        print("selftest ok")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
