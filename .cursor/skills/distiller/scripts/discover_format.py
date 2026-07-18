#!/usr/bin/env python3
"""Validate and format distiller discovery JSON."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from eliotapp.core.distiller.payload import validate_thematic_payload
from eliotapp.core.distiller.shapes import (
    discovery_result_to_dict,
    parse_discovery_result,
    validate_discovery_result,
)


def _cmd_validate(args: argparse.Namespace) -> int:
    raw = args.json.read_text(encoding="utf-8")
    data = json.loads(raw)
    if args.payload is not None:
        payload_text = args.payload.read_text(encoding="utf-8")
        errors = validate_thematic_payload(payload_text)
        if errors:
            for err in errors:
                print(err, file=sys.stderr)
            return 1
    errors = validate_discovery_result(data)
    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        return 1
    result = parse_discovery_result(data)
    print(json.dumps(discovery_result_to_dict(result), indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Distiller discovery JSON tools")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="Validate discovery JSON")
    validate.add_argument("--json", type=Path, required=True)
    validate.add_argument("--payload", type=Path, help="Optional ThematicPayload file")
    validate.set_defaults(func=_cmd_validate)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
