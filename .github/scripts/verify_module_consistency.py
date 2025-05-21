#!/usr/bin/env python3
"""
Script to verify consistency between prompt modules and the registry.
This script verifies that all modules in the registry have consistent information
with their corresponding module files, and vice versa.
"""
import os
import re
import sys
import yaml
import glob
from pathlib import Path


def extract_frontmatter(file_path):
    """Extract YAML frontmatter from markdown file."""
    with open(file_path, "r") as f:
        content = f.read()

    match = re.search(r"---\n(.*?)\n---", content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError as e:
            print(f"❌ ERROR: Invalid YAML frontmatter in {file_path}: {e}")
            return None
    return None


def load_registry():
    """Load the prompt registry data."""
    repo_root = Path(__file__).resolve().parents[2]
    registry_path = repo_root / "prompt-registry.yaml"
    if not os.path.exists(registry_path):
        print("❌ ERROR: prompt-registry.yaml not found")
        return None

    try:
        with open(registry_path, "r") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"❌ ERROR: Invalid YAML in prompt-registry.yaml: {e}")
        return None


def find_all_modules():
    """Find all module files in the project."""
    repo_root = Path(__file__).resolve().parents[2]
    module_files = []

    # Check prompt-library directory
    prompt_library = repo_root / "prompt-library"
    if prompt_library.exists():
        module_files.extend(glob.glob(str(prompt_library / "*.md")))

    # Check modules directory
    modules_dir = repo_root / "modules"
    if modules_dir.exists():
        module_files.extend(glob.glob(str(modules_dir / "*.md")))

    return module_files


def verify_coherence_markers(registry_data):
    """Verify that all modules have valid coherence markers."""
    if not registry_data:
        return False

    valid_markers = set(item["name"] for item in registry_data.get("markers", []))
    if not valid_markers:
        print("⚠️ WARNING: No valid markers defined in registry")
        return True

    all_valid = True
    for module in registry_data.get("modules", []):
        marker = module.get("marker")
        if not marker:
            print(f"❌ ERROR: Module {module.get('name')} has no marker defined")
            all_valid = False
            continue

        if marker not in valid_markers:
            print(f"❌ ERROR: Module {module.get('name')} has invalid marker: {marker}")
            print(f"  Valid markers are: {', '.join(sorted(valid_markers))}")
            all_valid = False

    return all_valid


def main():
    """Main verification function."""
    registry_data = load_registry()
    if not registry_data:
        return 1

    registry_modules = {}
    for module in registry_data.get("modules", []):
        name = module.get("name")
        if name:
            registry_modules[name] = module

    # Check module files
    all_valid = True
    module_files = find_all_modules()

    # Track which modules we've seen in files
    found_modules = set()

    # Verify each module file
    for file_path in module_files:
        frontmatter = extract_frontmatter(file_path)
        if not frontmatter:
            print(f"❌ ERROR: Missing or invalid frontmatter in {file_path}")
            all_valid = False
            continue

        module_name = frontmatter.get("name")
        if not module_name:
            print(f"❌ ERROR: Module in {file_path} has no name defined")
            all_valid = False
            continue

        found_modules.add(module_name)

        # Check if module exists in registry
        if module_name not in registry_modules:
            print(f"❌ ERROR: Module {module_name} ({file_path}) not found in registry")
            all_valid = False
            continue

        # Verify required fields
        required_fields = [
            "name",
            "version",
            "marker",
            "description",
            "inputs",
            "outputs",
            "last_updated",
            "status",
        ]
        for field in required_fields:
            if field not in frontmatter:
                print(f"❌ ERROR: Module {module_name} missing required field: {field}")
                all_valid = False

        # Verify consistency with registry
        registry_module = registry_modules[module_name]

        # Check version
        if frontmatter.get("version") != registry_module.get("version"):
            print(f"❌ ERROR: Version mismatch for {module_name}")
            print(
                f"  File: {frontmatter.get('version')}, Registry: {registry_module.get('version')}"
            )
            all_valid = False

        # Check marker
        if frontmatter.get("marker") != registry_module.get("marker"):
            print(f"❌ ERROR: Marker mismatch for {module_name}")
            print(
                f"  File: {frontmatter.get('marker')}, Registry: {registry_module.get('marker')}"
            )
            all_valid = False

        # Check inputs
        if set(frontmatter.get("inputs", [])) != set(registry_module.get("inputs", [])):
            print(f"❌ ERROR: Inputs mismatch for {module_name}")
            print(f"  File: {frontmatter.get('inputs')}")
            print(f"  Registry: {registry_module.get('inputs')}")
            all_valid = False

        # Check outputs
        if set(frontmatter.get("outputs", [])) != set(
            registry_module.get("outputs", [])
        ):
            print(f"❌ ERROR: Outputs mismatch for {module_name}")
            print(f"  File: {frontmatter.get('outputs')}")
            print(f"  Registry: {registry_module.get('outputs')}")
            all_valid = False

    # Check for modules in registry that don't exist in files
    for module_name in registry_modules:
        if module_name not in found_modules:
            print(
                f"❌ ERROR: Module {module_name} in registry has no corresponding file"
            )
            all_valid = False

    # Verify coherence markers
    if not verify_coherence_markers(registry_data):
        all_valid = False

    if all_valid:
        print("✅ SUCCESS: All modules are consistent with the registry!")
        return 0
    else:
        print("❌ ERROR: Module verification failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
