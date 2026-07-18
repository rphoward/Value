"""Hillclimb CLI entry — wires run, discrimination, and preference subcommands."""

from __future__ import annotations

import argparse

from hillclimb_cli.discrimination_parsers import register_discrimination_parsers
from hillclimb_cli.preference_parsers import register_preference_parsers
from hillclimb_cli.run_parsers import register_run_parsers
from hillclimb_cli.splice_parsers import register_splice_parsers


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Hillclimb run-folder persistence (prepare, record, job boards, resume)",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    register_run_parsers(sub)
    register_discrimination_parsers(sub)
    register_preference_parsers(sub)
    register_splice_parsers(sub)
    args = parser.parse_args()
    return args.func(args)
