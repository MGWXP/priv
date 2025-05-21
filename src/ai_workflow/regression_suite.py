"""Utilities for running regression tests programmatically."""

from __future__ import annotations

import os
import re
import subprocess
from typing import Any, Dict


class RegressionSuiteRunner:
    """Run the repository's regression test suite using pytest."""

    def __init__(self, tests_path: str = "tests") -> None:
        self.tests_path = tests_path

    def run(self) -> Dict[str, Any]:
        """Execute pytest and return parsed results.

        Returns
        -------
        dict
            A dictionary containing the return code, test summary line and
            complete pytest output.
        """

        env = os.environ.copy()
        command = ["pytest", self.tests_path, "-q"]
        result = subprocess.run(command, capture_output=True, text=True, env=env)
        summary_line = self._extract_summary(result.stdout)
        return {
            "returncode": result.returncode,
            "summary": summary_line,
            "output": result.stdout,
        }

    @staticmethod
    def _extract_summary(output: str) -> str:
        """Return the final summary line from pytest output."""

        for line in reversed(output.splitlines()):
            if re.search(r"\bpassed\b|\bfailed\b", line):
                return line.strip()
        return ""
