"""Argparse registration for span-splice crossover subcommand."""

from __future__ import annotations

import argparse
from pathlib import Path

from hillclimb_cli.common import resolve_run_dir_arg
from hillclimb_cli.splice import cmd_splice


def register_splice_parsers(sub: argparse._SubParsersAction) -> None:
    splice = sub.add_parser(
        "splice",
        help="Span-splice two parent drafts into draft-v{N}.md + splice-v{N}.json",
    )
    splice.add_argument("--run-dir", type=resolve_run_dir_arg, required=True)
    splice.add_argument(
        "--parent-a",
        type=Path,
        required=True,
        help="First parent draft (path under run-dir or absolute)",
    )
    splice.add_argument(
        "--parent-b",
        type=Path,
        required=True,
        help="Second parent draft (path under run-dir or absolute)",
    )
    splice.add_argument(
        "--span-map",
        required=True,
        help="JSON array file path or inline span_map JSON",
    )
    splice.add_argument(
        "--record",
        action="store_true",
        help="After splice, call record_iteration on the merged draft",
    )
    splice.add_argument(
        "--qualitative",
        type=Path,
        default=None,
        help="Qualitative JSON file for --record (optional)",
    )
    splice.set_defaults(func=cmd_splice)
