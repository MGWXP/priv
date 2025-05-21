"""Enhanced diff analyzer for coherence marker validation."""

from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List

from .semantic_diff import SemanticDiffAnalyzer


class DiffAnalyzerV2(SemanticDiffAnalyzer):
    """Provides smarter diff analysis for commit verification."""

    def classify_files(self, analyses: Iterable[Dict[str, Any]]) -> Dict[str, int]:
        """Return counts of file categories in the diff.

        Parameters
        ----------
        analyses:
            Collection of diff metadata dictionaries produced by
            :meth:`SemanticDiffAnalyzer.analyze_file_diff`.
        """

        categories = {"tests": 0, "docs": 0, "code": 0, "others": 0}
        for analysis in analyses:
            path = analysis.get("file_path", "")
            fname = os.path.basename(path)
            if path.startswith("tests") or fname.startswith("test_"):
                categories["tests"] += 1
            elif path.startswith("docs") or path.endswith(".md"):
                categories["docs"] += 1
            elif path.endswith(".py"):
                categories["code"] += 1
            else:
                categories["others"] += 1
        return categories

    def verify_marker_alignment(
        self, analyses: Iterable[Dict[str, Any]], marker: str
    ) -> Dict[str, Any]:
        """Check whether the diff matches the intent implied by the marker."""
        compliance = self.verify_marker_compliance(analyses, marker)
        if not compliance.get("compliant"):
            return compliance

        totals = {
            "additions": sum(a["additions"] for a in analyses),
            "deletions": sum(a["deletions"] for a in analyses),
        }
        classes = self.classify_files(analyses)

        reason = ""
        compliant = True

        if marker == "docs":
            if classes["docs"] != len(list(analyses)):
                compliant = False
                reason = "Non-documentation files changed with docs marker"
        elif marker == "feat":
            if totals["additions"] <= totals["deletions"]:
                compliant = False
                reason = "Feature commits should show net additions"
            elif classes["tests"] == 0:
                compliant = False
                reason = "Feature commits should include tests"
        elif marker == "fix":
            if classes["tests"] == 0:
                compliant = False
                reason = "Bug fixes must modify or add tests"
        elif marker == "test":
            if classes["tests"] != len(list(analyses)):
                compliant = False
                reason = "Test marker should modify only test files"
        return {"compliant": compliant, "reason": reason}

    def check_coding_standards(
        self, analyses: Iterable[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Simple coding standards check for docstrings in Python files."""
        missing_doc: List[str] = []
        trailing_ws: List[str] = []
        for analysis in analyses:
            path = analysis.get("file_path", "")
            diff_lines = analysis.get("diff", "").splitlines()
            if path.endswith(".py"):
                func_added = any(
                    line.startswith("+def ") or line.startswith("+class ")
                    for line in diff_lines
                )
                docstring_added = any(
                    line.startswith('+"')
                    or line.startswith("+'''")
                    or ('"""' in line and line.startswith("+"))
                    for line in diff_lines
                )
                if func_added and not docstring_added:
                    missing_doc.append(path)
            if any(
                line.startswith("+") and line.rstrip() != line for line in diff_lines
            ):
                trailing_ws.append(path)
        reasons = []
        if missing_doc:
            reasons.append(f"Missing docstrings in: {', '.join(missing_doc)}")
        if trailing_ws:
            reasons.append(
                f"Trailing whitespace in: {', '.join(sorted(set(trailing_ws)))}"
            )
        return {"compliant": not reasons, "reason": "; ".join(reasons)}

    def analyze_changeset(
        self, analyses: List[Dict[str, Any]], marker: str, iteration: str | None = None
    ) -> Dict[str, Any]:
        """Analyze diff analyses and generate a detailed report."""
        marker_result = self.verify_marker_alignment(analyses, marker)
        style_result = self.check_coding_standards(analyses)
        combined = {
            "compliant": marker_result["compliant"] and style_result["compliant"],
            "marker_reason": marker_result.get("reason", ""),
            "style_reason": style_result.get("reason", ""),
        }
        report = self.generate_diff_report(analyses, marker, combined, iteration)
        report["file_classes"] = self.classify_files(analyses)
        combined.update(report)
        return combined
