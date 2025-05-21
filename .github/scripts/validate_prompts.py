#!/usr/bin/env python3
"""Validate prompt modules and registry.

This script checks markdown files in `prompt-library/` for required YAML
frontmatter fields and ensures corresponding entries exist in
`prompt-registry.yaml` with required metadata.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Any

import yaml

REQUIRED_FRONTMATTER_FIELDS = [
    "name",
    "version",
    "description",
    "inputs",
    "outputs",
    "author",
    "last_updated",
    "status",
]

REQUIRED_REGISTRY_FIELDS = [
    "name",
    "file",
    "version",
    "description",
    "status",
    "last_update",
    "marker",
]


def extract_frontmatter(path: Path) -> dict[str, Any] | None:
    """Return the parsed YAML frontmatter from a markdown file."""
    content = path.read_text()
    match = re.search(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None


def load_registry(registry_path: Path) -> dict[str, Any] | None:
    """Load registry YAML data."""
    if not registry_path.exists():
        print(f"❌ ERROR: Registry file not found: {registry_path}")
        return None
    try:
        with registry_path.open() as fh:
            return yaml.safe_load(fh)
    except yaml.YAMLError as exc:
        print(f"❌ ERROR: Invalid YAML in registry: {exc}")
        return None


def validate_prompt_file(path: Path, registry_modules: dict[str, Any]) -> list[str]:
    """Validate a single prompt file against the registry."""
    errors: list[str] = []
    frontmatter = extract_frontmatter(path)
    if not frontmatter:
        errors.append(f"{path} missing or invalid frontmatter")
        return errors

    for field in REQUIRED_FRONTMATTER_FIELDS:
        if field not in frontmatter:
            errors.append(f"{path} missing required field '{field}'")

    name = frontmatter.get("name")
    if name and name in registry_modules:
        reg = registry_modules[name]
        if str(path).replace(os.sep, "/") != reg.get("file"):
            errors.append(f"{name} file path mismatch with registry")
        if str(frontmatter.get("version")) != str(reg.get("version")):
            errors.append(f"{name} version mismatch with registry")
    elif name:
        errors.append(f"{name} not found in registry")

    return errors


def validate_registry_entries(
    registry_data: dict[str, Any], repo_root: Path
) -> tuple[dict[str, Any], list[str]]:
    """Validate registry modules and return mapping of name to data."""
    errors: list[str] = []
    modules: dict[str, Any] = {}
    for item in registry_data.get("modules", []):
        for field in REQUIRED_REGISTRY_FIELDS:
            if field not in item:
                errors.append(
                    f"Registry module '{item.get('name')}' missing field '{field}'"
                )
        name = item.get("name")
        if name:
            modules[name] = item
            file_path = repo_root / item.get("file", "")
            if not file_path.exists():
                errors.append(
                    f"Registry file not found for module '{name}': {file_path}"
                )
    return modules, errors


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    registry_path = repo_root / "prompt-registry.yaml"
    registry_data = load_registry(registry_path)
    if registry_data is None:
        return 1

    registry_modules, errors = validate_registry_entries(registry_data, repo_root)

    prompt_dir = repo_root / "prompt-library"
    for path in sorted(prompt_dir.glob("*.md")):
        errors.extend(validate_prompt_file(path, registry_modules))

    if errors:
        for err in errors:
            print(f"❌ ERROR: {err}")
        return 1

    print("✅ SUCCESS: Prompts and registry validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
