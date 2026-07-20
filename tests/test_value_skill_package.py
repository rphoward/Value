"""Package contract for .cursor/skills/value/ and skills/value/."""

from __future__ import annotations

import json
import re
import unittest

from tests.value_skill_support import (
    ASSETS_DIR,
    ATOM_FIELDS,
    ATOM_ID_RE,
    BRACKET_TOKEN_RE,
    CANONICAL_SKILL_ROOT,
    MODULE_FILES,
    MODULE_NAMES,
    REFERENCE_FILES,
    REFERENCES_DIR,
    REQUIRED_KB_KEYS,
    REQUIRED_SCHEMA_PROPERTIES,
    SKILL_MD,
    SKILL_ROOT,
    SYNC_IGNORE_NAMES,
    TEMPLATE_FILES,
    atom_field,
    extract_reference_links,
    file_digest,
    frontmatter_field,
    iter_skill_files,
    module_atom_ids,
    parse_frontmatter,
    read_skill_md,
    record_operations,
    split_atoms,
)

class ValueSkillMirrorTests(unittest.TestCase):
    def test_canonical_and_cursor_trees_match(self) -> None:
        mismatches: list[str] = []
        canonical_files = iter_skill_files(CANONICAL_SKILL_ROOT)
        mirror_files = iter_skill_files(SKILL_ROOT)

        for canonical in canonical_files:
            relative = canonical.relative_to(CANONICAL_SKILL_ROOT)
            mirror = SKILL_ROOT / relative
            if not mirror.is_file():
                mismatches.append(f"missing mirror {relative.as_posix()}")
                continue
            if file_digest(canonical) != file_digest(mirror):
                mismatches.append(f"digest mismatch {relative.as_posix()}")

        canonical_relatives = {
            path.relative_to(CANONICAL_SKILL_ROOT) for path in canonical_files
        }
        for mirror in mirror_files:
            relative = mirror.relative_to(SKILL_ROOT)
            if relative not in canonical_relatives:
                mismatches.append(f"extra mirror {relative.as_posix()}")

        self.assertEqual(mismatches, [], "\n".join(mismatches))


class ValueSkillAssetTests(unittest.TestCase):
    def test_knowledge_base_has_required_keys(self) -> None:
        kb = json.loads((ASSETS_DIR / "knowledge-base.json").read_text(encoding="utf-8"))
        missing = [key for key in REQUIRED_KB_KEYS if key not in kb]
        self.assertEqual(missing, [])

    def test_atoms_json_covers_every_module_atom_id(self) -> None:
        expected = module_atom_ids()
        all_expected = {atom for atoms in expected.values() for atom in atoms}
        payload = json.loads((ASSETS_DIR / "atoms.json").read_text(encoding="utf-8"))
        indexed = {atom["id"]: atom for atom in payload["atoms"]}
        missing = sorted(all_expected - set(indexed))
        self.assertEqual(missing, [])
        for module_key, atom_ids in expected.items():
            for atom_id in atom_ids:
                self.assertEqual(indexed[atom_id]["module"], module_key)

    def test_schema_defines_ledger(self) -> None:
        schema = json.loads((ASSETS_DIR / "session.schema.json").read_text(encoding="utf-8"))
        self.assertIn("ledger", schema["required"])
        ledger = schema["$defs"]["ledger"]
        for field in (
            "phase",
            "active_module",
            "completion_pct",
            "validation_milestone",
            "unvalidated_bombs",
        ):
            self.assertIn(field, ledger["required"])

class ValueSkillPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill_text = read_skill_md()
        cls.frontmatter = parse_frontmatter(cls.skill_text)

    def test_skill_md_is_readable(self) -> None:
        self.assertTrue(SKILL_MD.is_file(), f"Expected skill file at {SKILL_MD}")
        self.assertTrue(self.skill_text.strip(), "SKILL.md must not be empty")

    def test_frontmatter_name_is_value(self) -> None:
        name = frontmatter_field(self.frontmatter, "name")
        self.assertEqual(
            name,
            "value",
            f"Expected frontmatter name 'value', got {name!r}",
        )

    def test_frontmatter_description_triggers(self) -> None:
        description = frontmatter_field(self.frontmatter, "description")
        self.assertTrue(
            description.startswith("Use when"),
            f"Description must begin with 'Use when'; got: {description!r}",
        )

        required_phrases = (
            "value proposition",
            "grill",
            "customer profile",
            "UX brief",
        )
        missing = [phrase for phrase in required_phrases if phrase not in description]
        self.assertEqual(
            missing,
            [],
            f"Description missing required phrases {missing}: {description!r}",
        )
        self.assertIn("Not for", description)
        self.assertIn("generic product requirements", description)

    def test_skill_links_all_reference_files(self) -> None:
        linked = set(extract_reference_links(self.skill_text))
        expected = set(REFERENCE_FILES)
        missing = sorted(expected - linked)
        self.assertEqual(
            missing,
            [],
            f"SKILL.md must link all reference files directly; missing: {missing}",
        )

    def test_skill_rejects_nested_reference_links(self) -> None:
        nested = [
            f"references/{path}"
            for path in extract_reference_links(self.skill_text)
            if "/" in path
        ]
        self.assertEqual(
            nested,
            [],
            "Reference links must be one level below references/: "
            + ", ".join(nested),
        )

    def test_modules_define_required_atom_fields(self) -> None:
        for module_name in MODULE_FILES:
            module_path = REFERENCES_DIR / module_name
            self.assertTrue(
                module_path.is_file(),
                f"Missing module reference: {module_path}",
            )
            module_text = module_path.read_text(encoding="utf-8")
            atoms = split_atoms(module_text)
            self.assertTrue(
                atoms,
                f"{module_name} must define at least one atom with (id ...)",
            )

            for atom_index, atom_text in enumerate(atoms, start=1):
                missing_fields = [
                    field
                    for field in ATOM_FIELDS
                    if not re.search(rf"\({field}\s+", atom_text)
                ]
                self.assertEqual(
                    missing_fields,
                    [],
                    f"{module_name} atom {atom_index} missing fields "
                    f"{missing_fields}: {atom_text[:200]!r}",
                )

    def test_atom_ids_are_unique_across_modules(self) -> None:
        seen: dict[str, str] = {}
        duplicates: list[str] = []

        for module_name in MODULE_FILES:
            module_path = REFERENCES_DIR / module_name
            if not module_path.is_file():
                self.fail(f"Missing module reference: {module_path}")
            module_text = module_path.read_text(encoding="utf-8")
            for atom_id in ATOM_ID_RE.findall(module_text):
                if atom_id in seen:
                    duplicates.append(
                        f"{atom_id} in {seen[atom_id]} and {module_name}"
                    )
                else:
                    seen[atom_id] = module_name

        self.assertEqual(
            duplicates,
            [],
            "Atom IDs must be unique across modules: " + "; ".join(duplicates),
        )

    def test_each_atom_asks_contains_one_question_mark(self) -> None:
        for module_name in MODULE_FILES:
            module_text = (REFERENCES_DIR / module_name).read_text(encoding="utf-8")
            for atom_text in split_atoms(module_text):
                atom_id = ATOM_ID_RE.search(atom_text).group(1)
                asks = atom_field(atom_text, "asks")
                self.assertEqual(
                    asks.count("?"),
                    1,
                    f"{atom_id} must contain exactly one question mark in asks: {asks!r}",
                )

    def test_atom_record_writes_use_exact_closed_schema_fields(self) -> None:
        schema = json.loads(
            (ASSETS_DIR / "session.schema.json").read_text(encoding="utf-8")
        )
        record_defs = {
            "answers": "answerRecord",
            "evidence": "evidenceRecord",
            "assumptions": "assumptionRecord",
            "decisions": "decisionRecord",
            "unknowns": "unknownRecord",
            "artifacts": "artifactRecord",
        }

        for module_name in MODULE_FILES:
            module_text = (REFERENCES_DIR / module_name).read_text(encoding="utf-8")
            for atom_text in split_atoms(module_text):
                atom_id = ATOM_ID_RE.search(atom_text).group(1)
                writes = atom_field(atom_text, "writes")
                operations = record_operations(writes)
                declared_operations = re.findall(
                    r"\b(?:append|upsert)\s+([a-z]+)\s+record\b",
                    writes,
                )
                self.assertEqual(
                    len(operations),
                    len(declared_operations),
                    f"{atom_id} record writes must use a braced record block",
                )
                answer_writes = [
                    block
                    for operation, collection, block in operations
                    if operation == "append" and collection == "answers"
                ]
                self.assertEqual(
                    len(answer_writes),
                    1,
                    f"{atom_id} must append exactly one complete answers record",
                )

                for _, collection, block in operations:
                    definition = record_defs[collection]
                    field_tokens = set(
                        re.findall(r"(?:^|,\s*)([a-z_]+)(?=\s)", block)
                    )
                    required = schema["$defs"][definition]["required"]
                    missing = [field for field in required if field not in field_tokens]
                    self.assertEqual(
                        missing,
                        [],
                        f"{atom_id} {collection} write misses exact fields "
                        f"{missing}: {block!r}",
                    )

                for position_field in ("position.module", "position.atom_id", "position.status"):
                    self.assertIn(
                        position_field,
                        writes,
                        f"{atom_id} write must set {position_field}",
                    )
                self.assertIn(
                    "project.updated_at to accepted_at",
                    writes,
                    f"{atom_id} write must refresh project.updated_at",
                )

    def test_scale_constraint_can_remain_blocking_unknown(self) -> None:
        module_text = (REFERENCES_DIR / "business-model.md").read_text(
            encoding="utf-8"
        )
        b06 = next(
            atom for atom in split_atoms(module_text) if "(id B06)" in atom
        )
        accepts = atom_field(b06, "accepts")
        self.assertIn("blocking unknown", accepts)
        self.assertIn("keeps B06 active", accepts)
        writes = atom_field(b06, "writes")
        self.assertIn("append unknowns record", writes)
        self.assertIn("blocking true", writes)
        self.assertIn(
            "when constraint is unknown keep position.module business-model, "
            "position.atom_id B06, position.status in_progress",
            writes,
        )
        self.assertIn(
            "when constraint is accepted set position.module business-model, "
            "position.atom_id B07, position.status in_progress",
            writes,
        )
        self.assertEqual(
            atom_field(b06, "unlocks"),
            "when constraint is unknown keep B06; when constraint is accepted unlock B07",
        )

    def test_test_and_learning_cards_keep_atomic_asks(self) -> None:
        module_text = (REFERENCES_DIR / "experiments.md").read_text(
            encoding="utf-8"
        )
        atoms = {
            ATOM_ID_RE.search(atom).group(1): atom for atom in split_atoms(module_text)
        }
        self.assertEqual(
            atom_field(atoms["E07"], "asks"),
            "Do you accept the assembled test card as written?",
        )
        self.assertEqual(
            atom_field(atoms["E08"], "asks"),
            "What observable result did the test produce?",
        )
        self.assertIn("waits until a test result exists", atom_field(atoms["E08"], "teaches"))
        self.assertIn("blocking unknown", atom_field(atoms["E08"], "teaches"))
        e08_writes = atom_field(atoms["E08"], "writes")
        self.assertIn(
            "when result is absent keep position.module experiments, "
            "position.atom_id E08, position.status in_progress",
            e08_writes,
        )
        self.assertIn(
            "when result is accepted set position.module experiments, "
            "position.atom_id E09, position.status in_progress",
            e08_writes,
        )
        self.assertEqual(
            atom_field(atoms["E08"], "unlocks"),
            "when result is absent keep E08; when result is accepted unlock E09",
        )

    def test_assumption_records_wait_for_accepted_criticality(self) -> None:
        module_text = (REFERENCES_DIR / "experiments.md").read_text(
            encoding="utf-8"
        )
        atoms = {
            ATOM_ID_RE.search(atom).group(1): atom for atom in split_atoms(module_text)
        }
        e01_writes = atom_field(atoms["E01"], "writes")
        self.assertNotIn("append assumptions record", e01_writes)
        self.assertNotIn("medium default", e01_writes)
        self.assertIn("append assumptions record", atom_field(atoms["E02"], "writes"))

        e09_writes = atom_field(atoms["E09"], "writes")
        self.assertIn(
            "when criticality is accepted append assumptions record",
            e09_writes,
        )
        self.assertIn(
            "otherwise append unknowns record",
            e09_writes,
        )
        self.assertIn(
            "position.atom_id E10, position.status in_progress",
            e09_writes,
        )

    def test_boundary_answers_preserve_supported_kind(self) -> None:
        atom_locations = (
            ("profile.md", "P01"),
            ("value-map.md", "V01"),
        )
        for module_name, atom_id in atom_locations:
            module_text = (REFERENCES_DIR / module_name).read_text(encoding="utf-8")
            atom = next(
                candidate
                for candidate in split_atoms(module_text)
                if f"(id {atom_id})" in candidate
            )
            writes = atom_field(atom, "writes")
            self.assertIn(
                "kind decision for an explicit scope choice or the accepted supported kind",
                writes,
            )
            self.assertNotIn("kind fact or unknown", writes)
            self.assertIn("append decisions record", writes)
            self.assertIn("blocking true", writes)
            self.assertIn(
                f"when boundary is unresolved keep position.module {MODULE_NAMES[module_name]}, "
                f"position.atom_id {atom_id}, position.status in_progress",
                writes,
            )
            self.assertIn(
                f"when boundary is accepted set position.module {MODULE_NAMES[module_name]}, "
                f"position.atom_id {atom_id[0]}02, position.status in_progress",
                writes,
            )
            self.assertEqual(
                atom_field(atom, "unlocks"),
                f"when boundary is unresolved keep {atom_id}; "
                f"when boundary is accepted unlock {atom_id[0]}02",
            )

    def test_experiment_gate_requires_the_result_that_e08_blocks_on(self) -> None:
        module_text = (REFERENCES_DIR / "experiments.md").read_text(
            encoding="utf-8"
        )
        atoms = {
            ATOM_ID_RE.search(atom).group(1): atom for atom in split_atoms(module_text)
        }
        self.assertIn("keeps E08 active", atom_field(atoms["E08"], "accepts"))
        e10_accepts = atom_field(atoms["E10"], "accepts")
        self.assertIn("accepted observed result", e10_accepts)
        self.assertNotIn("result or explicit unknown", e10_accepts)

    def test_session_schema_parses_as_json(self) -> None:
        schema_path = ASSETS_DIR / "session.schema.json"
        self.assertTrue(
            schema_path.is_file(),
            f"Missing session schema: {schema_path}",
        )
        try:
            json.loads(schema_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            self.fail(f"session.schema.json is not valid JSON: {exc}")

    def test_session_schema_requires_canonical_fields(self) -> None:
        schema_path = ASSETS_DIR / "session.schema.json"
        self.assertTrue(
            schema_path.is_file(),
            f"Missing session schema: {schema_path}",
        )
        schema = json.loads(schema_path.read_text(encoding="utf-8"))

        required = schema.get("required", [])
        missing = [
            field for field in REQUIRED_SCHEMA_PROPERTIES if field not in required
        ]
        self.assertEqual(
            missing,
            [],
            f"session.schema.json must require {list(REQUIRED_SCHEMA_PROPERTIES)}; "
            f"missing from required: {missing}",
        )

    def test_bracket_token_scanner_ignores_markdown_links_and_images(self) -> None:
        template_text = (
            "# [Project name]\n"
            "Read the [research notes](references/research.md).\n"
            "![Evidence map](assets/evidence-map.png)\n"
        )

        self.assertEqual(BRACKET_TOKEN_RE.findall(template_text), ["[Project name]"])

    def test_templates_exist_without_unfilled_bracket_tokens(self) -> None:
        offenders: list[str] = []

        for template_name in TEMPLATE_FILES:
            template_path = ASSETS_DIR / template_name
            if not template_path.is_file():
                offenders.append(f"missing file: {template_path}")
                continue

            tokens = BRACKET_TOKEN_RE.findall(template_path.read_text(encoding="utf-8"))
            if tokens:
                offenders.append(
                    f"{template_name} contains unfilled bracket tokens: {tokens}"
                )

        self.assertEqual(
            offenders,
            [],
            "Template contract failures:\n" + "\n".join(offenders),
        )


if __name__ == "__main__":
    unittest.main()
