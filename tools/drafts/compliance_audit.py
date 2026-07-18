#!/usr/bin/env python3
"""One-off compliance audit: plan, suite, non-native cargo."""
from __future__ import annotations

import json
import re
from pathlib import Path

VALUE_ROOT = Path(r"c:\Projects\value\skills\value")
VALUES_ROOT = Path(r"c:\Projects\Values\skills\value")
SUITE_PATH = Path(r"c:\Projects\value\docs\value-proposition-prompt-suite (1).md")


def read_tree(root: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            rel = path.relative_to(root).as_posix()
            files[rel] = path.read_text(encoding="utf-8", errors="replace")
    return files


def digest_tree(root: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    for rel in sorted(read_tree(root)):
        h.update(rel.encode())
        h.update(read_tree(root)[rel].encode())
    return h.hexdigest()[:16]


def flatten(obj, prefix: str = "") -> dict[str, object]:
    out: dict[str, object] = {}
    if isinstance(obj, dict):
        for key, value in obj.items():
            path = f"{prefix}.{key}" if prefix else key
            out.update(flatten(value, path))
    else:
        out[prefix] = obj
    return out


def main() -> None:
    value_files = read_tree(VALUE_ROOT)
    values_files = read_tree(VALUES_ROOT)
    all_text = "\n".join(value_files.values()).lower()
    skill_text = value_files["SKILL.md"].lower()

    print("=== Values GitHub vs value monorepo ===")
    only_value = sorted(set(value_files) - set(values_files))
    only_values = sorted(set(values_files) - set(value_files))
    diffs = [rel for rel in sorted(set(value_files) & set(values_files)) if value_files[rel] != values_files[rel]]
    print(f"value files: {len(value_files)} | Values files: {len(values_files)}")
    print(f"only in value: {only_value or 'none'}")
    print(f"only in Values: {only_values or 'none'}")
    print(f"content diffs: {len(diffs)}")
    print(f"digest match: {digest_tree(VALUE_ROOT) == digest_tree(VALUES_ROOT)}")

    plan_checks = {
        "skill_name_value": "name: value" in value_files["SKILL.md"],
        "description_triggers": all(
            token in value_files["SKILL.md"].lower()
            for token in ("use when", "value proposition", "grilled", "customer profile", "ux brief")
        )
        or all(
            token in value_files["SKILL.md"].lower()
            for token in ("use when", "value proposition", "grill", "customer profile", "ux brief")
        ),
        "five_reference_links": all(
            link in value_files["SKILL.md"]
            for link in (
                "references/profile.md",
                "references/value-map.md",
                "references/business-model.md",
                "references/experiments.md",
                "references/session-contract.md",
            )
        ),
        "no_nested_refs": not re.search(r"references/[^/\s]+/", value_files["SKILL.md"]),
        "session_schema": "assets/session.schema.json" in value_files,
        "six_original_templates": all(
            rel in value_files
            for rel in (
                "assets/customer-profile.template.md",
                "assets/value-map.template.md",
                "assets/business-model.template.md",
                "assets/experiment-plan.template.md",
                "assets/product-design-brief.template.md",
                "assets/ux-brief.template.md",
            )
        ),
        "workflow_deleted": "references/workflow.md" not in value_files,
        "atom_fields": all(
            re.search(r"\(id\s+" + atom_id, value_files.get(f"references/{module}.md", ""))
            for atom_id, module in (("P01", "profile"), ("V01", "value-map"), ("B01", "business-model"), ("E01", "experiments"))
        ),
        "atom_ids_present": len(set(re.findall(r"\(id\s+([A-Z]\d{2})", "\n".join(value_files.values())))) >= 38,
        "pressure_tests_doc": Path(r"c:\Projects\value\docs\value-skill-pressure-tests.md").exists(),
    }
    recovery_extras = {
        "knowledge_base_json": "assets/knowledge-base.json" in value_files,
        "atoms_json": "assets/atoms.json" in value_files,
        "scripts_present": all(
            rel in value_files
            for rel in (
                "scripts/init_session.py",
                "scripts/status.py",
                "scripts/next_question.py",
                "scripts/accept_answer.py",
                "scripts/write_milestone.py",
                "scripts/write_design_briefs.py",
                "scripts/_session.py",
            )
        ),
        "ledger_in_schema": "completion_pct" in value_files["assets/session.schema.json"],
        "app_design_brief": "assets/app-design-brief.template.md" in value_files,
        "test_learning_cards": "assets/test-card.template.md" in value_files and "assets/learning-card.template.md" in value_files,
    }

    plan_pass = sum(plan_checks.values())
    plan_total = len(plan_checks)
    print("\n=== vs superpowers plan (2026-07-18) ===")
    print(f"Original plan contract: {plan_pass}/{plan_total} = {100 * plan_pass / plan_total:.0f}%")
    for key, ok in plan_checks.items():
        if not ok:
            print(f"  MISS: {key}")
    print(f"Recovery extras beyond plan: {sum(recovery_extras.values())}/{len(recovery_extras)}")

    kb = json.loads(value_files["assets/knowledge-base.json"])
    kb_text = json.dumps(kb).lower()

    suite_layers = {
        "knowledge_base_json": {
            "weight": 0.18,
            "items": [
                "visual_grounding_analogies",
                "customer_profile_triggers",
                "high_value_job_rubric",
                "value_map_categories",
                "osterwalder_7_bm_questions",
                "experiment_library",
            ],
            "source": "kb",
        },
        "orchestrator_philosophy": {
            "weight": 0.12,
            "items": [
                "spreadsheet mirage",
                "cognitive murder",
                "state ledger",
                "completion",
                "unvalidated",
                "next-step nudge",
                "forbid premature",
            ],
            "source": "text",
        },
        "profile_subskill": {
            "weight": 0.15,
            "items": [
                "sticky note",
                "functional",
                "social",
                "emotional",
                "supporting",
                "buyer_of_value",
                "pain_severity",
                "gain_relevance",
                "high-value job",
                "at least 2",
                "earlyvangelist",
                "five whys",
                "outlier",
            ],
            "source": "text",
        },
        "value_map_subskill": {
            "weight": 0.13,
            "items": [
                "physical",
                "intangible",
                "digital",
                "financial",
                "checkmark",
                "orphan",
                "steve blank",
                "ad-lib",
                "waste rule",
            ],
            "source": "text",
        },
        "bm_subskill": {
            "weight": 0.12,
            "items": [
                "front stage",
                "backstage",
                "switching_costs",
                "recurring_revenues",
                "earning_versus_spending",
                "game_changing",
                "others_do_the_work",
                "scalability",
                "protection_from_competition",
                "medtech",
                "hilti",
            ],
            "source": "text",
        },
        "experiment_subskill": {
            "weight": 0.15,
            "items": [
                "test card",
                "learning card",
                "false-positive",
                "false-negative",
                "local maximum",
                "exhausted maximum",
                "wrong data",
                "validation funnel",
                "willingness to pay",
                "lit fuse",
                "desirability",
                "feasibility",
                "viability",
            ],
            "source": "text",
        },
        "state_progress": {
            "weight": 0.15,
            "items": [
                "session.json",
                "ledger",
                "completion_pct",
                "atoms.json",
                "status.py",
                "next_question.py",
                "accept_answer.py",
                "write_milestone",
                "write_design_briefs",
                "--reopen",
            ],
            "source": "text",
        },
    }

    weighted = 0.0
    layer_scores: dict[str, float] = {}
    print("\n=== vs prompt suite (your original doc) ===")
    for name, layer in suite_layers.items():
        hits = 0
        misses: list[str] = []
        for item in layer["items"]:
            if layer.get("source") == "kb":
                ok = item in kb_text
            else:
                needle = item.lower()
                ok = needle in all_text or needle in skill_text
                if not ok and needle == "spreadsheet mirage":
                    ok = "spreadsheet_mirage" in all_text or "spreadsheet-mirage" in all_text
                if not ok and needle == "cognitive murder":
                    ok = "cognitive_murder" in all_text or "cognitive-murder" in all_text
                if not ok and needle == "state ledger":
                    ok = "ledger" in skill_text and "status.py" in skill_text
                if not ok and needle == "next-step nudge":
                    ok = "end-nudge" in skill_text or "next-step" in all_text
                if not ok and needle == "high-value job":
                    ok = "high_value_job" in all_text or "high-value" in all_text
                if not ok and needle == "at least 2":
                    ok = any(token in all_text for token in ("at least 2", "≥2", ">=2", "two of"))
                if not ok and needle == "five whys":
                    ok = "five why" in all_text or "5 why" in all_text
                if not ok and needle == "waste rule":
                    ok = "orphan" in all_text and "waste" in all_text
                if not ok and needle == "intangible":
                    ok = "intagible" in all_text or "intangible" in all_text
            hits += int(ok)
            if not ok:
                misses.append(item)
        pct = hits / len(layer["items"]) if layer["items"] else 0.0
        layer_scores[name] = pct * 100
        weighted += pct * layer["weight"]
        print(f"  {name}: {pct * 100:.0f}% ({hits}/{len(layer['items'])})")
        if misses:
            print(f"    missing: {', '.join(misses)}")

    print(f"Weighted suite compliance NOW: {weighted * 100:.1f}%")

    non_native = {
        "supporting_job_banks": all(token in kb_text for token in ("buyer_of_value", "cocreator_of_value", "transferrer_of_value")),
        "scales_mandatory": all(token in kb_text for token in ("job_importance_scale", "pain_severity_scale", "gain_relevance_scale")),
        "high_value_gate": "high_value_job_rubric" in kb_text and any(token in all_text for token in ("at least 2", "≥2", ">=2", "two of")),
        "checkmark_orphan_matrix": "checkmark" in all_text and "orphan" in all_text,
        "ad_lib_x3": "ad-lib" in all_text or "ad lib" in all_text,
        "seven_bm_anchors": "osterwalder_7_bm_questions" in kb_text and "switching_costs" in all_text,
        "medtech_hilti": "medtech" in all_text and "hilti" in all_text,
        "experiment_library_table": "experiment_library" in kb_text and "google adwords" in kb_text,
        "test_learning_templates": "assets/test-card.template.md" in value_files and "assets/learning-card.template.md" in value_files,
        "five_data_traps": sum(1 for token in ("false-positive", "false-negative", "local maximum", "exhausted maximum", "wrong data") if token in all_text) >= 4,
        "validation_funnel_order": "validation funnel" in all_text or ("interest validated" in all_text and "willingness to pay" in all_text),
        "named_analogies_actions": len(kb.get("visual_grounding_analogies", {})) >= 6,
        "visible_ledger_each_turn": "status.py" in value_files["SKILL.md"] and "completion_pct" in value_files["assets/session.schema.json"],
        "script_backed_progress": all(rel in value_files for rel in ("scripts/next_question.py", "scripts/accept_answer.py")),
    }
    nn_pass = sum(non_native.values())
    print("\n=== non-native cargo (not reliable in model training) ===")
    print(f"NOW: {nn_pass}/{len(non_native)} = {100 * nn_pass / len(non_native):.0f}%")
    for key, ok in non_native.items():
        if not ok:
            print(f"  MISS: {key}")

    prior = {
        "suite_weighted": 22.5,
        "plan_contract": 95.0,
        "non_native_cargo": 8.0,
        "knowledge_base_json": 10.0,
        "state_progress": 15.0,
        "orchestrator": 35.0,
    }
    now = {
        "suite_weighted": weighted * 100,
        "plan_contract": 100 * plan_pass / plan_total,
        "non_native_cargo": 100 * nn_pass / len(non_native),
        "knowledge_base_json": layer_scores["knowledge_base_json"],
        "state_progress": layer_scores["state_progress"],
        "orchestrator": layer_scores["orchestrator_philosophy"],
    }
    print("\n=== DELTAS (pre-recovery estimate -> now) ===")
    for key in prior:
        print(f"  {key}: {prior[key]:.1f}% -> {now[key]:.1f}%  (Δ {now[key] - prior[key]:+.1f}pp)")

    suite_text = SUITE_PATH.read_text(encoding="utf-8", errors="replace")
    suite_json_match = re.search(r"```json\n(\{.*?\})\n```", suite_text, re.S)
    if suite_json_match:
        suite_kb = json.loads(suite_json_match.group(1))
        suite_flat = flatten(suite_kb)
        kb_flat = flatten(kb)
        same = sum(1 for key in suite_flat if key in kb_flat and suite_flat[key] == kb_flat[key])
        print(f"\nKB leaf-path fidelity vs suite §1: {same}/{len(suite_flat)} = {100 * same / len(suite_flat):.0f}%")

    model_native_share = 42.5
    non_native_share = 57.5
    cargo_in_skill = now["non_native_cargo"]
    delta_still_missing = non_native_share * (1 - cargo_in_skill / 100)
    print("\n=== three-way split (substance) ===")
    print(f"Model-native canvas vocabulary (~{model_native_share}% of suite): mostly redundant in prompts")
    print(f"Non-native operational cargo (~{non_native_share}% of suite): {cargo_in_skill:.0f}% now in skill")
    print(f"Non-native still missing from skill: ~{delta_still_missing:.0f}% of total suite substance")


if __name__ == "__main__":
    main()
