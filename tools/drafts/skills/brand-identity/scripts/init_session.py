#!/usr/bin/env python3
"""Create a new paced-skill session.json."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _session import (
    SLUG_RE,
    WORKPRODUCT_ROOT,
    default_session,
    default_workproduct_root,
    derive_slug_from_name,
    save_session,
)

PACING_CHOICES = ("standard", "express")


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a paced skill session.")
    parser.add_argument("--name", required=True, help="Display name")
    parser.add_argument(
        "--slug",
        help="Path-safe project slug (derived from --name when omitted)",
    )
    parser.add_argument(
        "--root",
        default=None,
        help=(
            f"Workproduct root for sessions (default: <repo>/{WORKPRODUCT_ROOT} "
            f"when the skill lives under the repo; else {WORKPRODUCT_ROOT})"
        ),
    )
    parser.add_argument(
        "--pacing-mode",
        default="standard",
        choices=PACING_CHOICES,
        help="Interview pacing (default: standard)",
    )
    args = parser.parse_args()
    root = Path(args.root) if args.root else default_workproduct_root()

    slug = args.slug
    if slug is None:
        try:
            slug = derive_slug_from_name(args.name)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1
    elif not SLUG_RE.fullmatch(slug):
        print(f"Invalid slug: {slug!r}", file=sys.stderr)
        return 1

    session_dir = Path(root) / slug
    session_path = session_dir / "session.json"
    if session_path.exists():
        print(f"Session already exists: {session_path}", file=sys.stderr)
        return 1

    session = default_session(slug, args.name, pacing_mode=args.pacing_mode)
    save_session(session_path, session)
    print(f"Created {session_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
