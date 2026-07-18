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
BRACKET_TOKEN_RE = re.compile(r"\[[^\]]+\]")


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
