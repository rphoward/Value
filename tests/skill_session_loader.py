"""Load skill scripts/_session without registering sys.modules['_session']."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path
from types import ModuleType

_CACHE: dict[str, ModuleType] = {}


def _module_name(scripts_dir: Path) -> str:
    digest = hashlib.sha256(str(scripts_dir.resolve()).encode()).hexdigest()[:16]
    return f"_skill_session_{digest}"


def load_skill_session(scripts_dir: Path) -> ModuleType:
    """Import the ``scripts/_session`` package under a unique module name per scripts_dir."""
    scripts_dir = scripts_dir.resolve()
    session_dir = scripts_dir / "_session"
    init_path = session_dir / "__init__.py"
    if not init_path.is_file():
        raise FileNotFoundError(f"Missing _session package: {init_path}")

    cache_key = str(scripts_dir)
    if cache_key in _CACHE:
        mod = _CACHE[cache_key]
        mod.reset_atom_indexes()
        return mod

    name = _module_name(scripts_dir)
    spec = importlib.util.spec_from_file_location(
        name,
        init_path,
        submodule_search_locations=[str(session_dir)],
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load _session from {scripts_dir}")

    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    _CACHE[cache_key] = mod
    mod.reset_atom_indexes()
    return mod
