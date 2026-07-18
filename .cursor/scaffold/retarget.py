#!/usr/bin/env python3
"""Retarget product slug across a scaffolded repository."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import shutil
import sys
from pathlib import Path

SCAFFOLD_DIR_NAME = "scaffold"


def scaffold_dir(repo_root: Path) -> Path:
    return repo_root / ".cursor" / SCAFFOLD_DIR_NAME


def manifest_path(repo_root: Path) -> Path:
    return scaffold_dir(repo_root) / "manifest.json"


def retarget_paths_config(repo_root: Path) -> Path:
    local = Path(__file__).resolve().parent / "retarget-paths.json"
    if local.is_file():
        return local
    return scaffold_dir(repo_root) / "retarget-paths.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def is_excluded(relative_posix: str, exclude_patterns: list[str]) -> bool:
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(relative_posix, pattern):
            return True
        prefix = pattern.removesuffix("/**")
        if pattern.endswith("/**") and (
            relative_posix == prefix or relative_posix.startswith(prefix + "/")
        ):
            return True
    return False


def collect_replace_files(
    repo_root: Path, replace_patterns: list[str], exclude_patterns: list[str]
) -> list[Path]:
    found: set[Path] = set()
    for pattern in replace_patterns:
        for path in repo_root.glob(pattern):
            if not path.is_file():
                continue
            relative = path.relative_to(repo_root).as_posix()
            if is_excluded(relative, exclude_patterns):
                continue
            found.add(path)
    return sorted(found)


def build_replace_pairs(source_slug: str, target_slug: str) -> list[tuple[str, str]]:
    pairs = [
        (f"src/{source_slug}/", f"src/{target_slug}/"),
        (f"src/{source_slug}", f"src/{target_slug}"),
        (f"{source_slug}.", f"{target_slug}."),
        (f"start-{source_slug}", f"start-{target_slug}"),
    ]
    return sorted(pairs, key=lambda item: len(item[0]), reverse=True)


def apply_text_replacements(
    text: str, pairs: list[tuple[str, str]], source_slug: str, target_slug: str
) -> str:
    for old, new in pairs:
        text = text.replace(old, new)

    bare_patterns = [
        (
            rf'\(product_home "src/{re.escape(source_slug)}/"\)',
            f'(product_home "src/{target_slug}/")',
        ),
        (
            rf'\(import_package "{re.escape(source_slug)}"\)',
            f'(import_package "{target_slug}")',
        ),
        (
            rf'\(repo_folder "{re.escape(source_slug)}"\)',
            f'(repo_folder "{target_slug}")',
        ),
        (rf'\({re.escape(source_slug)}\b', f"({target_slug}"),
        (rf'name = "{re.escape(source_slug)}"', f'name = "{target_slug}"'),
        (rf"import package {re.escape(source_slug)}\b", f"import package {target_slug}"),
        (rf"'{re.escape(source_slug)}\b", f"'{target_slug}"),
    ]
    for pattern, replacement in bare_patterns:
        text = re.sub(pattern, replacement, text)

    text = re.sub(rf"\b{re.escape(source_slug)}\b", target_slug, text)
    return text


def update_repo_layout_protocol(
    repo_root: Path, source_slug: str, target_slug: str
) -> bool:
    path = repo_root / ".cursor" / "rules" / "repo-layout.mdc"
    if not path.is_file():
        return False
    original = path.read_text(encoding="utf-8")
    updated = apply_text_replacements(
        original, build_replace_pairs(source_slug, target_slug), source_slug, target_slug
    )
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def update_manifest(repo_root: Path, target_slug: str, github_remote: str | None = None) -> bool:
    path = manifest_path(repo_root)
    if not path.is_file():
        return False
    manifest = load_json(path)
    original = json.dumps(manifest, indent=2) + "\n"
    manifest["product_slug"] = target_slug
    manifest["import_package"] = target_slug
    manifest["product_home"] = f"src/{target_slug}/"
    manifest["start_script"] = f"tools/start-{target_slug}.ps1"
    manifest["uvicorn_target"] = f"{target_slug}.presentation.app:app"
    if github_remote is not None:
        manifest["github_remote"] = github_remote
    updated = json.dumps(manifest, indent=2) + "\n"
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def rename_product_home(repo_root: Path, source_slug: str, target_slug: str) -> bool:
    source_dir = repo_root / "src" / source_slug
    target_dir = repo_root / "src" / target_slug
    if not source_dir.is_dir():
        return False
    if target_dir.exists():
        if target_dir.resolve() == source_dir.resolve():
            return False
        raise SystemExit(f"target product home already exists: {target_dir}")
    source_dir.rename(target_dir)
    return True


def rename_start_script(repo_root: Path, source_slug: str, target_slug: str) -> bool:
    source_script = repo_root / "tools" / f"start-{source_slug}.ps1"
    target_script = repo_root / "tools" / f"start-{target_slug}.ps1"
    if not source_script.is_file():
        return False
    if target_script.exists() and target_script.resolve() != source_script.resolve():
        raise SystemExit(f"target start script already exists: {target_script}")
    if source_script.resolve() == target_script.resolve():
        return False
    source_script.rename(target_script)
    return True


def retarget(
    repo_root: Path,
    source_slug: str,
    target_slug: str,
    *,
    github_remote: str | None = None,
) -> int:
    if source_slug == target_slug:
        return 0

    product_home = repo_root / "src" / source_slug
    if not product_home.is_dir():
        print(f"error: missing product home {product_home}", file=sys.stderr)
        return 1

    config_path = retarget_paths_config(repo_root)
    config = load_json(config_path)
    files = collect_replace_files(
        repo_root, config.get("replace", []), config.get("exclude", [])
    )
    pairs = build_replace_pairs(source_slug, target_slug)
    changed_files = 0

    for path in files:
        original = path.read_text(encoding="utf-8")
        updated = apply_text_replacements(original, pairs, source_slug, target_slug)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed_files += 1

    if update_repo_layout_protocol(repo_root, source_slug, target_slug):
        changed_files += 1
    if update_manifest(repo_root, target_slug, github_remote):
        changed_files += 1
    if rename_start_script(repo_root, source_slug, target_slug):
        changed_files += 1
    if rename_product_home(repo_root, source_slug, target_slug):
        changed_files += 1

    if changed_files == 0:
        print("error: slug differs but no files changed", file=sys.stderr)
        return 1

    print(f"retargeted {source_slug} -> {target_slug} ({changed_files} changes)")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Retarget scaffold product slug.")
    parser.add_argument("--from", dest="source_slug", required=True)
    parser.add_argument("--to", dest="target_slug", required=True)
    parser.add_argument("--repo-root", default=".", type=Path)
    parser.add_argument("--github-remote", default=None)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = args.repo_root.resolve()
    return retarget(
        repo_root,
        args.source_slug,
        args.target_slug,
        github_remote=args.github_remote,
    )


if __name__ == "__main__":
    raise SystemExit(main())
