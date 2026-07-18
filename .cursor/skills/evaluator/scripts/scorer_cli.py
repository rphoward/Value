#!/usr/bin/env python3
"""Unified evaluator CLI with subcommands delegating to existing scorer scripts."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

_COMMAND_MODULES: dict[str, str] = {
    "score": "score_fixture",
    "score-v2": "score_v2",
    "gate": "gate_v2",
    "pairwise": "pairwise_v2",
    "discrimination": "discrimination_v2",
    "authorprint": "authorprint_v2",
}


def _dispatch(command: str) -> int:
    module_name = _COMMAND_MODULES.get(command)
    if module_name is None:
        names = ", ".join(sorted(_COMMAND_MODULES))
        print(f"unknown subcommand: {command}\nchoices: {names}", file=sys.stderr)
        return 2
    sys.argv = [f"{module_name}.py", *sys.argv[2:]]
    module = importlib.import_module(module_name)
    return int(module.main())


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        names = ", ".join(sorted(_COMMAND_MODULES))
        print(f"usage: scorer_cli.py <{names}> [args...]", file=sys.stderr)
        return 2 if len(sys.argv) < 2 else 0
    return _dispatch(sys.argv[1])


if __name__ == "__main__":
    raise SystemExit(main())
