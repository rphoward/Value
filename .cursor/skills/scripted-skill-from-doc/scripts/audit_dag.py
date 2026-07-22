#!/usr/bin/env python3
"""Audit atoms.json DAG coverage (standard / express)."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any


def load_atoms(skill_root: Path) -> list[dict[str, Any]]:
    payload = json.loads((skill_root / "assets" / "atoms.json").read_text(encoding="utf-8"))
    return payload["atoms"]


def load_config(skill_root: Path) -> dict[str, Any]:
    path = skill_root / "assets" / "skill-config.json"
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def structural_issues(atoms: list[dict[str, Any]]) -> list[str]:
    index = {a["id"]: a for a in atoms}
    issues: list[str] = []
    for a in atoms:
        for r in a.get("requires") or []:
            if r not in index:
                issues.append(f"dangling require: {a['id']} -> {r}")
        u = a.get("unlocks")
        if u and u not in index:
            issues.append(f"dangling unlock: {a['id']} -> {u}")

    soft_but_required: list[str] = []
    required_by: dict[str, set[str]] = defaultdict(set)
    for a in atoms:
        for r in a.get("requires") or []:
            required_by[r].add(a["id"])
    for a in atoms:
        if a.get("soft") and required_by[a["id"]]:
            soft_but_required.append(a["id"])
    if soft_but_required:
        issues.append(f"soft_but_required_by_later: {soft_but_required}")
    return issues


def simulate_standard(atoms: list[dict[str, Any]]) -> dict[str, Any]:
    """Greedy readiness walk (requires only). Does not model section ranking."""
    index = {a["id"]: a for a in atoms}
    answered: set[str] = set()
    order: list[str] = []
    for _ in range(len(atoms) * 3 + 1):
        ready = []
        for a in atoms:
            aid = a["id"]
            if aid in answered:
                continue
            reqs = a.get("requires") or []
            if all(r in answered for r in reqs):
                ready.append(aid)
        if not ready:
            break
        # Prefer hard non-gate, then soft, then gate — stable by id
        ready.sort(
            key=lambda i: (
                0 if not index[i].get("soft") and not index[i].get("gate") else 1 if index[i].get("soft") else 2,
                i,
            )
        )
        pick = ready[0]
        answered.add(pick)
        order.append(pick)
    hard = [a["id"] for a in atoms if not a.get("soft") and not a.get("gate")]
    soft = [a["id"] for a in atoms if a.get("soft")]
    gates = [a["id"] for a in atoms if a.get("gate")]
    return {
        "mode": "standard",
        "asked": order,
        "missing_hard": [h for h in hard if h not in answered],
        "missed_soft": [s for s in soft if s not in answered],
        "missing_gates": [g for g in gates if g not in answered],
        "ok": all(h in answered for h in hard) and all(g in answered for g in gates),
    }


def simulate_express(atoms: list[dict[str, Any]], config: dict[str, Any]) -> dict[str, Any]:
    spine: set[str] = set()
    for ids in (config.get("express_spine") or {}).values():
        spine.update(ids)
    if not spine:
        return {"mode": "express", "ok": False, "error": "no express_spine in skill-config.json"}
    requires_map = {
        k: list(v) for k, v in (config.get("express_requires") or {}).items()
    }
    index = {a["id"]: a for a in atoms if a["id"] in spine}
    answered: set[str] = set()
    order: list[str] = []
    for _ in range(len(spine) * 3 + 1):
        ready = []
        for aid, a in index.items():
            if aid in answered:
                continue
            reqs = requires_map.get(aid, a.get("requires") or [])
            if all(r in answered for r in reqs):
                ready.append(aid)
        if not ready:
            break
        ready.sort()
        pick = ready[0]
        answered.add(pick)
        order.append(pick)
    return {
        "mode": "express",
        "asked": order,
        "spine": sorted(spine),
        "missing_spine": sorted(spine - answered),
        "ok": spine <= answered,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit paced-skill atom DAG")
    parser.add_argument("skill_root", type=Path, help="Path to skill package root")
    parser.add_argument(
        "--mode",
        choices=["standard", "express", "both"],
        default="both",
    )
    args = parser.parse_args()
    root = args.skill_root
    if not (root / "assets" / "atoms.json").is_file():
        print(f"Missing atoms.json under {root}", file=sys.stderr)
        return 1
    atoms = load_atoms(root)
    config = load_config(root)
    report: dict[str, Any] = {
        "skill_root": str(root).replace("\\", "/"),
        "atom_count": len(atoms),
        "structural": structural_issues(atoms),
    }
    ok = not any(i.startswith("dangling") for i in report["structural"])
    if args.mode in {"standard", "both"}:
        report["standard"] = simulate_standard(atoms)
        ok = ok and report["standard"]["ok"]
    if args.mode in {"express", "both"}:
        report["express"] = simulate_express(atoms, config)
        if "error" in report["express"]:
            ok = False
        else:
            ok = ok and report["express"]["ok"]
    report["ok"] = ok
    print(json.dumps(report, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
