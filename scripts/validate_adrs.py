#!/usr/bin/env python3
"""Validate Architecture Decision Records (ADRs).

This script checks the ADR directory for the presence of ADR markdown files and
verifies basic formatting requirements.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


HEADER_REGEX = re.compile(r"^#\s*ADR[- ]?(\d+):?\s+.+")
STATUS_REGEX = re.compile(r"^Status:\s*")


def find_adr_files(adr_dir: Path) -> list[Path]:
    """Return a sorted list of ADR markdown files."""
    return sorted(adr_dir.glob("*.md"))


def validate_adr(file_path: Path) -> list[str]:
    """Validate a single ADR file and return a list of errors."""
    errors = []
    lines = file_path.read_text().splitlines()
    if not lines:
        errors.append(f"{file_path} is empty")
        return errors

    if not HEADER_REGEX.match(lines[0]):
        errors.append(f"{file_path} missing ADR header")

    if not any(STATUS_REGEX.match(line) for line in lines):
        errors.append(f"{file_path} missing Status line")

    return errors


def validate_adrs(adr_dir: Path) -> int:
    """Validate all ADRs in the given directory."""
    if not adr_dir.exists():
        print(f"❌ ERROR: ADR directory not found: {adr_dir}")
        return 1

    adrs = find_adr_files(adr_dir)
    if not adrs:
        print(f"❌ ERROR: No ADR files found in {adr_dir}")
        return 1

    all_errors = []
    for adr in adrs:
        all_errors.extend(validate_adr(adr))

    if all_errors:
        for err in all_errors:
            print(f"❌ ERROR: {err}")
        return 1

    print(f"✅ SUCCESS: {len(adrs)} ADR files validated")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate ADR files")
    parser.add_argument(
        "adr_dir",
        nargs="?",
        default="docs/adr",
        help="Path to the ADR directory (default: docs/adr)",
    )
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    adr_path = repo_root / args.adr_dir
    return validate_adrs(adr_path)


if __name__ == "__main__":
    sys.exit(main())
