"""Diff analysis utilities."""

from __future__ import annotations

import difflib
import os
from datetime import datetime
from typing import Any, Dict, Iterable, List

import yaml


class SemanticDiffAnalyzer:
    """Perform simple semantic diff analysis."""

    def analyze_file_diff(
        self, old_content: str, new_content: str, file_path: str
    ) -> Dict[str, Any]:
        """Return diff statistics for a single file."""

        diff_lines = list(
            difflib.unified_diff(
                old_content.splitlines(),
                new_content.splitlines(),
                fromfile=file_path,
                tofile=file_path,
                lineterm="",
            )
        )

        additions = sum(
            1
            for line in diff_lines
            if line.startswith("+") and not line.startswith("+++")
        )
        deletions = sum(
            1
            for line in diff_lines
            if line.startswith("-") and not line.startswith("---")
        )

        return {
            "file_path": file_path,
            "diff": "\n".join(diff_lines),
            "additions": additions,
            "deletions": deletions,
        }

    def verify_marker_compliance(
        self, analyses: Iterable[Dict[str, Any]], marker: str
    ) -> Dict[str, Any]:
        """Verify that a given coherence marker is valid."""

        with open("execution-budget.yaml", "r", encoding="utf-8") as f:
            budget = yaml.safe_load(f)

        valid_markers = budget.get("coherence_markers", {}).get("valid_markers", [])
        if marker not in valid_markers:
            return {"compliant": False, "reason": "Invalid coherence marker"}

        return {"compliant": True}

    def generate_diff_report(
        self,
        analyses: List[Dict[str, Any]],
        marker: str,
        verification: Dict[str, Any],
        iteration: str | None = None,
    ) -> Dict[str, Any]:
        """Generate a YAML report summarizing diff statistics."""

        iteration = iteration or datetime.now().strftime("%Y%m%d%H%M%S")
        os.makedirs(os.path.join("audits", "diffs"), exist_ok=True)
        report_path = os.path.join("audits", "diffs", f"{iteration}_diff_report.yaml")

        totals = {"files_changed": len(analyses), "additions": 0, "deletions": 0}
        for analysis in analyses:
            totals["additions"] += analysis["additions"]
            totals["deletions"] += analysis["deletions"]

        report_data = {
            "marker": marker,
            "compliant": verification.get("compliant", False),
            **totals,
            "report_path": report_path,
        }

        with open(report_path, "w", encoding="utf-8") as f:
            yaml.dump(report_data, f)

        return report_data
