"""Package contract for .cursor/skills/value/."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


def repo_root() -> Path:
    """Locate the repository root from this test module."""
    here = Path(__file__).resolve()
    for candidate in (here.parent, *here.parents):
        if (candidate / "pyproject.toml").is_file():
            return candidate
    raise RuntimeError(
        "Could not locate repository root from tests/test_value_skill_package.py"
    )


ROOT = repo_root()
SKILL_ROOT = ROOT / ".cursor" / "skills" / "value"
SKILL_MD = SKILL_ROOT / "SKILL.md"
REFERENCES_DIR = SKILL_ROOT / "references"
ASSETS_DIR = SKILL_ROOT / "assets"

REFERENCE_FILES = (
    "profile.md",
    "value-map.md",
    "business-model.md",
    "experiments.md",
    "session-contract.md",
)

MODULE_FILES = (
    "profile.md",
    "value-map.md",
    "business-model.md",
    "experiments.md",
)

TEMPLATE_FILES = (
    "customer-profile.template.md",
    "value-map.template.md",
    "business-model.template.md",
    "experiment-plan.template.md",
    "product-design-brief.template.md",
    "ux-brief.template.md",
)

REQUIRED_SCHEMA_PROPERTIES = (
    "schema_version",
    "project",
    "position",
    "answers",
    "evidence",
    "assumptions",
    "decisions",
    "unknowns",
    "artifacts",
)

ATOM_FIELDS = ("id", "teaches", "asks", "accepts", "writes", "unlocks")

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
REFERENCE_LINK_RE = re.compile(r"references/([^\s\"')\]]+)")
ATOM_ID_RE = re.compile(r"\(id\s+([^)\s]+)\)")
BRACKET_TOKEN_RE = re.compile(r"\[[^\]\r\n]+\](?!\s*\()")


def read_skill_md() -> str:
    if not SKILL_MD.is_file():
        raise FileNotFoundError(f"Missing skill entrypoint: {SKILL_MD}")
    return SKILL_MD.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> str:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return ""
    return match.group(1)


def frontmatter_field(block: str, field: str) -> str:
    folded = re.search(rf"^{field}:\s*>\s*\n((?:  .+\n?)+)", block, re.MULTILINE)
    if folded:
        lines = folded.group(1).splitlines()
        return " ".join(
            line[2:] if line.startswith("  ") else line.strip() for line in lines
        ).strip()

    inline = re.search(rf"^{field}:\s*(.+)$", block, re.MULTILINE)
    if not inline:
        return ""

    value = inline.group(1).strip()
    if value == ">":
        return ""
    return value.strip("\"'")


def extract_reference_links(text: str) -> list[str]:
    return REFERENCE_LINK_RE.findall(text)


def split_atoms(text: str) -> list[str]:
    matches = list(ATOM_ID_RE.finditer(text))
    if not matches:
        return []

    atoms: list[str] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        atoms.append(text[start:end])
    return atoms


def atom_field(atom_text: str, field: str) -> str:
    match = re.search(rf'\({field}\s+"([^"]*)"\)', atom_text)
    return match.group(1) if match else ""


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
            '(ask-first "project slug and display name only")',
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

    def test_briefs_require_every_module_gate_outcome(self) -> None:
        self.assertIn(
            '(gate-prerequisite "profile, value-map, business-model, and experiments '
            'must each be completed or explicitly bypassed")',
            self.skill_text,
        )

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

    def test_each_atom_asks_exactly_one_question(self) -> None:
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

    def test_atom_record_appends_include_closed_schema_fields(self) -> None:
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
                self.assertIn(
                    "append answers record",
                    writes,
                    f"{atom_id} must append a complete answers record",
                )

                for clause in writes.split(";"):
                    if "append" not in clause and "upsert" not in clause:
                        continue
                    for collection, definition in record_defs.items():
                        operations = (
                            f"append {collection} record",
                            f"upsert {collection} record",
                        )
                        if not any(operation in clause for operation in operations):
                            continue
                        required = schema["$defs"][definition]["required"]
                        missing = [field for field in required if field not in clause]
                        self.assertEqual(
                            missing,
                            [],
                            f"{atom_id} {collection} write misses {missing}: {clause!r}",
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
        self.assertIn("constraint unknown", atom_field(b06, "accepts"))
        writes = atom_field(b06, "writes")
        self.assertIn("append unknowns record", writes)
        self.assertIn("blocking true", writes)

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
