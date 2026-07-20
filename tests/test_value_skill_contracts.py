"""Value skill review contract tests."""

from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

from tests.value_skill_support import (
    ASSETS_DIR,
    ATOM_FIELDS,
    ATOM_ID_RE,
    BRACKET_TOKEN_RE,
    MODULE_FILES,
    MODULE_NAMES,
    REFERENCE_FILES,
    REFERENCES_DIR,
    REQUIRED_KB_KEYS,
    REQUIRED_SCHEMA_PROPERTIES,
    ROOT,
    SCRIPTS_DIR,
    SKILL_MD,
    SKILL_ROOT,
    TEMPLATE_FILES,
    atom_field,
    extract_reference_links,
    file_digest,
    frontmatter_field,
    import_session_helper,
    module_atom_ids,
    parse_frontmatter,
    read_skill_md,
    record_operations,
    run_script,
    split_atoms,
)

class ValueSkillReviewContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill_text = read_skill_md()
        cls.frontmatter = parse_frontmatter(cls.skill_text)
        cls.contract_text = (
            REFERENCES_DIR / "session-contract.md"
        ).read_text(encoding="utf-8")
        cls.schema = json.loads(
            (ASSETS_DIR / "session.schema.json").read_text(encoding="utf-8")
        )

    def test_intent_skill_is_discoverable_repo_wide(self) -> None:
        self.assertIsNone(
            re.search(r"^paths\s*:", self.frontmatter, re.MULTILINE),
            "Intent-discovered value skill must omit paths so fresh prompts can load it",
        )

    def test_missing_session_creation_is_one_question_then_consent(self) -> None:
        required_contract = (
            '(ask-first "what the user is working on — display name only; derive slug silently from name")',
            '(wait-for "explicit consent before creating session.json")',
            '(initial-position profile P01 in_progress)',
            '(initial-arrays answers evidence assumptions decisions unknowns artifacts :empty t)',
            '(initial-timestamps created_at updated_at :rfc3339 t :same-value t)',
            '(write "complete schema-valid session.json immediately after consent")',
        )
        missing = [
            statement
            for statement in required_contract
            if statement not in self.contract_text
        ]
        self.assertEqual(
            missing,
            [],
            "Missing-session creation contract is incomplete: " + ", ".join(missing),
        )

    def test_skill_declares_voice_recipe(self) -> None:
        for needle in (
            "voice-recipe",
            "known",
            "edge",
            "never paste JSON",
            "scripts-silent",
            "match-board",
            "post-fix",
            "revise <area>",
            "prefix-notification-every-turn",
        ):
            self.assertIn(needle, self.skill_text)

    def test_value_map_gate_presentation_contract(self) -> None:
        value_map = (REFERENCES_DIR / "value-map.md").read_text(encoding="utf-8")
        for needle in (
            "value-map-gate-review",
            "user-language",
            "Fit links",
            "Differentiation",
            "expand-fit-links",
            "expand-differentiation",
            "indirect, conditional, or weak",
            "never fake direct",
            "forbidden-at-gate",
            "'mermaid-diagrams",
            "'tables",
            "ad-lib-on-ask",
            "never at gate open",
            "atom-ids-or-internal-codes-to-user",
            "cryptic-drill-triggers",
            "mermaid-or-tables-at-value-map-gate",
            "ad-lib-wall-at-value-map-gate-open",
            "human-artifacts",
            "never atom IDs, source_atom codes, or curriculum numbers",
        ):
            self.assertIn(needle, self.skill_text)
        banned = (
            "user says links or diff",
            "say links or diff",
        )
        for phrase in banned:
            self.assertNotIn(phrase, self.skill_text)
        for needle in (
            "(presentation",
            "gate-open",
            "split stickies",
            "expand-fit-links",
            "expand-differentiation",
            "ad-lib-on-ask",
            "ad-lib-pitch-on-ask",
            "never at gate open",
            "indirect, conditional, or weak",
        ):
            self.assertIn(needle, value_map)
        self.assertIn(
            "value-map-gate-review",
            self.contract_text,
        )
        self.assertIn("Fit links", self.contract_text)
        self.assertIn("Differentiation", self.contract_text)
        self.assertIn("ad-lib pitch on-ask only", self.contract_text)
        self.assertNotIn("links or diff", self.contract_text)

    def test_adr_provenance_uses_section_names(self) -> None:
        session_mod = import_session_helper()
        session = session_mod.default_session("demo", "Demo")
        session["decisions"].append(
            {
                "decision": "accepted segment boundary",
                "reason": "Scope locked for design.",
                "source_atom": "P01",
                "resulting_module": "profile",
                "resulting_atom": "P02",
                "resulting_status": "in_progress",
            }
        )
        planned = session_mod.plan_hard_decision_adrs(
            session, Path("workproduct/value-proposition/demo")
        )
        self.assertTrue(planned)
        _path, body = planned[0]
        self.assertIn("Customer profile — Segment", body)
        self.assertNotIn("Source atom: P01", body)
        self.assertNotIn("_Source atom:", body)
        self.assertNotIn("P01", body)

    def test_export_lenses_forbid_atom_ids_to_user(self) -> None:
        export_lenses = (REFERENCES_DIR / "export-lenses.md").read_text(encoding="utf-8")
        self.assertIn("never atom IDs", export_lenses)
        self.assertIn("quote-atom-ids-in-user-facing-copy", export_lenses)
        self.assertNotIn("who P01", export_lenses)
        self.assertNotIn("V08 three ad-libs", export_lenses)

    def test_drop_in_decision_mode_uses_accepted_alternatives(self) -> None:
        for needle in (
            "drop-in-decision-mode",
            "if segment is satisfied do not restart at segment",
            "accepted alternatives when present",
            "never hardcode fixed alternative names",
            "serves outward value / park as orphan / record unknown",
            "never treat Values as an autonomy or creativity coach for the product",
        ):
            self.assertIn(needle, self.skill_text)

    def test_autonomy_guardrail_allows_profile_parks_offering(self) -> None:
        self.assertIn("profile may hold autonomy", self.skill_text)
        self.assertIn("park autonomy-as-offering", self.skill_text)
        self.assertIn(
            "autonomy-as-offering-without-reopen-offering-boundary",
            self.contract_text,
        )

    def test_pause_refreshes_build_pack_with_one_endurance_sentence(self) -> None:
        for needle in (
            '(run "scripts/status.py --sections then scripts/write_build_pack.py --force")',
            "one human sentence naming what endured",
            "show the one --sections strip line",
            "north-star-blurb.md",
            "quote ## Blurb and ## Install",
            "value-trail section titles grew",
            "do not paste the entire trail",
            "requiring-a-canvas-to-see-the-blurb",
        ):
            self.assertIn(needle, self.skill_text)

    def test_north_star_surfaces_in_chat_not_path_only(self) -> None:
        for needle in (
            "surface-north-star",
            "on-ask \"when user asks for discord, blurb, pitch, north star, or paste",
            "only-mentioning-file-path-without-quoting-body",
        ):
            self.assertIn(needle, self.skill_text)

    def test_value_trail_lens_and_on_ask_triggers(self) -> None:
        export_lenses = (REFERENCES_DIR / "export-lenses.md").read_text(encoding="utf-8")
        for needle in (
            "Value_Trail_Lens",
            "value-trail.md",
            "cognitive_murder",
            "pregnant_man_trap",
            "fit_check_rules",
            "spreadsheet_mirage",
            "North_Star_Lens",
            "Discord_Update_Blurb",
            "ai-slop-pitch-voice",
            "feature-semicolon-laundry-list",
            "Peer Discord",
        ):
            self.assertIn(needle, export_lenses)
        for needle in (
            "value-trail",
            "trail, breadcrumbs, value record, marketing, or ads",
            "path-only-without-quoting-trail",
            "value-trail.md",
            "ai-slop-pitch-voice",
            "Discord_Update_Blurb",
        ):
            self.assertIn(needle, self.skill_text)

    def test_skill_declares_script_orchestration(self) -> None:
        for needle in (
            "scripts/status.py",
            "scripts/next_question.py",
            "scripts/accept_answer.py",
            "scripts/write_design_briefs.py",
            "scripts/write_build_pack.py",
            "references/export-lenses.md",
            "assets/knowledge-base.json",
            "assets/atoms.json",
        ):
            self.assertIn(needle, self.skill_text)

    def test_briefs_require_every_module_gate_outcome(self) -> None:
        self.assertIn(
            '(gate-prerequisite "profile, value-map, business-model, and experiments '
            'must each be completed or explicitly bypassed")',
            self.skill_text,
        )
        self.assertIn("app-design-brief.md", self.skill_text)

    def test_bypass_records_exact_resulting_position(self) -> None:
        decision = self.schema["$defs"]["decisionRecord"]
        resulting_fields = {
            "resulting_module",
            "resulting_atom",
            "resulting_status",
        }
        self.assertTrue(resulting_fields.issubset(decision["properties"]))
        self.assertTrue(resulting_fields.issubset(decision["required"]))
        self.assertIn(
            "(resulting-position resulting_module resulting_atom resulting_status)",
            self.contract_text,
        )
        self.assertIn(
            '(resulting_module "requested target phase")',
            self.contract_text,
        )
        self.assertIn(
            '(resulting_atom "first atom id in the target module")',
            self.contract_text,
        )
        self.assertIn("(resulting_status in_progress)", self.contract_text)
        self.assertIn(
            '(position-update "set position.module, position.atom_id, and '
            "position.status exactly to the decision's resulting_module, "
            'resulting_atom, and resulting_status")',
            self.contract_text,
        )

    def test_schema_timestamp_patterns_enforce_rfc3339(self) -> None:
        timestamp_schemas = (
            self.schema["$defs"]["project"]["properties"]["created_at"],
            self.schema["$defs"]["project"]["properties"]["updated_at"],
            self.schema["$defs"]["answerRecord"]["properties"]["accepted_at"],
        )
        for timestamp_schema in timestamp_schemas:
            pattern = timestamp_schema.get("pattern")
            self.assertTrue(pattern, "RFC 3339 timestamp fields must define a pattern")
            valid_timestamps = (
                "2026-07-18T12:34:56Z",
                "2024-02-29T23:59:59+14:00",
                "2026-01-01T00:00:00.123-05:30",
            )
            invalid_timestamps = (
                "2023-02-29T12:34:56Z",
                "2026-02-31T12:34:56Z",
                "2026-04-31T12:34:56Z",
                "2026-07-18T12:34:56",
                "2026-07-18T12:34:56+1400",
                "2026-07-18T12:34:56+24:00",
                "2026-07-18T12:34:56+12:60",
            )
            for timestamp in valid_timestamps:
                with self.subTest(timestamp=timestamp):
                    self.assertIsNotNone(re.fullmatch(pattern, timestamp))
            for timestamp in invalid_timestamps:
                with self.subTest(timestamp=timestamp):
                    self.assertIsNone(re.fullmatch(pattern, timestamp))

    def test_conflicts_and_assumptions_have_schema_valid_sources(self) -> None:
        assumption = self.schema["$defs"]["assumptionRecord"]
        self.assertIn("source_atom", assumption["properties"])
        self.assertIn("source_atom", assumption["required"])
        self.assertIn(
            '(on-conflict "append a blocking unknown with the conflicting statements; '
            'preserve both accepted answers")',
            self.contract_text,
        )
        self.assertIn(
            '(resolution "append a decision naming the governing statement, reason, '
            'source_atom, and resulting position; remove the blocking unknown")',
            self.contract_text,
        )

    def test_accepted_answer_refreshes_project_updated_at(self) -> None:
        self.assertIn(
            '(refresh "project.updated_at to the accepted_at RFC 3339 timestamp")',
            self.skill_text,
        )

    def test_project_slug_is_path_safe(self) -> None:
        slug_schema = self.schema["$defs"]["project"]["properties"]["slug"]
        self.assertEqual(slug_schema.get("pattern"), r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        pattern = slug_schema["pattern"]
        for slug in ("value", "cleaner-scheduler", "v2"):
            with self.subTest(slug=slug):
                self.assertIsNotNone(re.fullmatch(pattern, slug))
        for slug in ("../escape", "a/b", r"a\b", "/absolute", "Two Words", "-bad"):
            with self.subTest(slug=slug):
                self.assertIsNone(re.fullmatch(pattern, slug))
        self.assertIn(
            '(slug-format "lowercase ASCII letters, digits, and single hyphens only; '
            'must match ^[a-z0-9]+(?:-[a-z0-9]+)*$")',
            self.contract_text,
        )

    def test_schema_pairs_each_module_with_its_atoms(self) -> None:
        expected = module_atom_ids()
        position_pairs = {
            branch["properties"]["module"]["const"]: set(
                branch["properties"]["atom_id"]["enum"]
            )
            for branch in self.schema["$defs"]["position"]["oneOf"]
        }
        self.assertEqual(position_pairs, {key: set(value) for key, value in expected.items()})

        decision = self.schema["$defs"]["decisionRecord"]
        resulting_pairs = {
            branch["properties"]["resulting_module"]["const"]: set(
                branch["properties"]["resulting_atom"]["enum"]
            )
            for branch in decision["oneOf"]
        }
        self.assertEqual(resulting_pairs, {key: set(value) for key, value in expected.items()})

        all_atoms = {atom for atoms in expected.values() for atom in atoms}
        answer_atoms = set(
            self.schema["$defs"]["answerRecord"]["properties"]["atom_id"]["enum"]
        )
        source_atoms = set(decision["properties"]["source_atom"]["enum"])
        self.assertEqual(answer_atoms, all_atoms)
        self.assertEqual(source_atoms, all_atoms)

    def test_module_outcomes_are_derived_from_durable_records(self) -> None:
        required_contract = (
            '(position-only "position is only the current active atom; it is not module history")',
            '(completed "latest gate decision for the module is pass and its milestone artifact status is final")',
            '(bypassed "latest applicable decision uses decision bypass <module> gate and names the waived module")',
            '(pending "neither completed nor bypassed by the durable records")',
        )
        for statement in required_contract:
            self.assertIn(statement, self.contract_text)

    def test_pressure_test_checklist_names_live_scenarios(self) -> None:
        pressure_text = (ROOT / "docs" / "value-skill-pressure-tests.md").read_text(
            encoding="utf-8"
        )
        scenarios = (
            "session creation write",
            "accepted-answer persistence",
            "resume from valid state",
            "post-session bypass",
            "gate artifact write",
            "product, UX, and app brief generation",
        )
        for scenario in scenarios:
            with self.subTest(scenario=scenario):
                self.assertRegex(
                    pressure_text,
                    rf"(?:PENDING live|Live) — {re.escape(scenario)}\. Success: [^\n]+",
                )



if __name__ == "__main__":
    unittest.main()
