#!/usr/bin/env python3
"""Import accepted answers from a value-proposition session into lean-mvp."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from _session import (
    atom_by_id,
    answered_atom_ids,
    atom_requires,
    load_atoms,
    load_json,
    load_session,
    recompute_ledger,
    save_session,
    schedule_next_atom,
    utc_now_iso,
)

SKILL_ROOT = Path(__file__).resolve().parent.parent
BRIDGE_PATH = SKILL_ROOT / "assets" / "value-bridge-map.json"


def latest_answer_by_atom(session: dict) -> dict[str, dict]:
    latest: dict[str, dict] = {}
    for record in session.get("answers", []):
        atom_id = record["atom_id"]
        prior = latest.get(atom_id)
        if prior is None or record["accepted_at"] >= prior["accepted_at"]:
            latest[atom_id] = record
    return latest


def lean_answer_exists(session: dict, atom_id: str) -> bool:
    return any(record["atom_id"] == atom_id for record in session.get("answers", []))


def import_from_value(
    lean_session: dict,
    value_session: dict,
    bridge: dict,
    atoms: list[dict],
) -> tuple[dict, list[str]]:
    atom_map: dict[str, str] = bridge.get("atom_map", {})
    value_answers = latest_answer_by_atom(value_session)
    imported: list[str] = []
    timestamp = utc_now_iso()
    index = atom_by_id(atoms)
    pending: list[tuple[str, str, dict]] = []

    for value_atom_id, lean_atom_id in atom_map.items():
        if lean_atom_id not in index:
            continue
        if lean_answer_exists(lean_session, lean_atom_id):
            continue
        source = value_answers.get(value_atom_id)
        if source is None:
            continue
        pending.append((value_atom_id, lean_atom_id, source))

    changed = True
    while changed and pending:
        changed = False
        answered = answered_atom_ids(lean_session)
        still_pending: list[tuple[str, str, dict]] = []
        for value_atom_id, lean_atom_id, source in pending:
            atom = index[lean_atom_id]
            if not all(req in answered for req in atom_requires(atom)):
                still_pending.append((value_atom_id, lean_atom_id, source))
                continue
            lean_session["answers"].append(
                {
                    "atom_id": lean_atom_id,
                    "answer": source["answer"],
                    "kind": source.get("kind", "fact"),
                    "accepted_at": timestamp,
                    "provenance": "value-import",
                    "source_atom": value_atom_id,
                }
            )
            imported.append(lean_atom_id)
            answered.add(lean_atom_id)
            changed = True
        pending = still_pending

    if imported:
        lean_session["project"]["updated_at"] = timestamp
        lean_session["value_import"] = {
            "source_session": bridge.get("_resolved_value_session", ""),
            "imported_at": timestamp,
            "mapped_atoms": sorted(set(imported)),
        }
        next_atom = schedule_next_atom(lean_session, atoms)
        if next_atom is not None:
            lean_session["position"] = {
                "module": next_atom["module"],
                "atom_id": next_atom["id"],
                "status": "in_progress",
            }
        lean_session["ledger"] = recompute_ledger(lean_session)

    return lean_session, imported


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Import value-proposition session answers into lean-mvp."
    )
    parser.add_argument("session", type=Path, help="Path to lean-mvp session.json")
    parser.add_argument(
        "--value-root",
        default="workproduct/value-proposition",
        help="Value workproduct root (default: workproduct/value-proposition)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print import plan without writing session.json",
    )
    args = parser.parse_args()

    if not args.session.is_file():
        print(f"Missing session: {args.session}", file=sys.stderr)
        return 1
    if not BRIDGE_PATH.is_file():
        print(f"Missing bridge map: {BRIDGE_PATH}", file=sys.stderr)
        return 1

    bridge = load_json(BRIDGE_PATH)
    lean_session = load_session(args.session)
    slug = lean_session["project"]["slug"]
    value_path = Path(args.value_root) / slug / "session.json"
    bridge["_resolved_value_session"] = str(value_path).replace("\\", "/")

    if not value_path.is_file():
        print(json.dumps({"imported": [], "reason": "no value session", "path": str(value_path)}))
        return 0

    value_session = load_session(value_path)
    atoms = load_atoms()
    updated, imported = import_from_value(lean_session, value_session, bridge, atoms)

    payload = {"imported": imported, "path": str(value_path)}
    if args.dry_run:
        print(json.dumps(payload, indent=2))
        return 0

    if imported:
        save_session(args.session, updated)
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
