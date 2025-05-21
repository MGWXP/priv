#!/usr/bin/env python3
"""
Documentation Dashboard Generator

This script generates a documentation health dashboard based on analysis results.
It provides a visual overview of documentation quality metrics and key insights.
"""

import os
import json
import yaml
import argparse
import logging
from pathlib import Path
from datetime import datetime
import re
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("nlu.dashboard")


class DashboardGenerator:
    """Generates a documentation health dashboard from analysis results."""

    def __init__(
        self,
        registry_path: str,
        relationships_path: str,
        validation_report_path: str,
        template_path: str,
    ):
        """Initialize the dashboard generator."""
        self.registry_path = Path(registry_path)
        self.relationships_path = Path(relationships_path)
        self.validation_report_path = Path(validation_report_path)
        self.template_path = Path(template_path)

        self.doc_registry = self._load_json(registry_path)
        self.relationship_map = self._load_json(relationships_path)
        self.template = self._load_template(template_path)
        self.metrics = self._calculate_metrics()

    def _load_json(self, path: str) -> Dict:
        """Load JSON file."""
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load {path}: {e}")
            return {}

    def _load_template(self, path: str) -> str:
        """Load dashboard template."""
        try:
            with open(path, "r") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to load template {path}: {e}")
            return ""

    def _calculate_metrics(self) -> Dict:
        """Calculate documentation health metrics."""
        # Count files by type
        total_src_files = sum(
            1 for doc_id in self.doc_registry if doc_id.startswith("src/")
        )
        total_prompt_modules = sum(
            1
            for doc_id in self.doc_registry
            if doc_id.startswith(("prompt-library/", "modules/"))
        )

        # Count documented files
        documented_src_files = sum(
            1
            for doc_id in self.doc_registry
            if doc_id.startswith("src/") and self.doc_registry[doc_id].get("docstring")
        )

        # Count complete prompt modules (assume they're complete if they have front_matter)
        complete_prompt_modules = sum(
            1
            for doc_id in self.doc_registry
            if doc_id.startswith(("prompt-library/", "modules/"))
            and self.doc_registry[doc_id].get("front_matter")
        )

        # Count tested files
        tested_src_files = sum(
            1
            for doc_id in self.doc_registry
            if doc_id.startswith("src/")
            and any(
                rel_type == "tested_by" and len(rels) > 0
                for rel_type, rels in self.relationship_map.get(doc_id, {}).items()
            )
        )

        # Count orphaned documents
        orphaned_count = sum(
            1
            for doc_id, relationships in self.relationship_map.items()
            if all(len(rels) == 0 for rel_type, rels in relationships.items())
        )

        # Calculate percentages
        code_coverage = (
            (documented_src_files / total_src_files * 100) if total_src_files > 0 else 0
        )
        prompt_completeness = (
            (complete_prompt_modules / total_prompt_modules * 100)
            if total_prompt_modules > 0
            else 0
        )
        test_coverage = (
            (tested_src_files / total_src_files * 100) if total_src_files > 0 else 0
        )

        # Calculate overall score (weighted average)
        weights = {
            "code_coverage": 0.4,
            "prompt_completeness": 0.3,
            "test_coverage": 0.2,
            "orphaned": 0.1,
        }
        orphaned_score = (
            100 if orphaned_count < 5 else max(0, 100 - (orphaned_count - 5) * 10)
        )

        overall_score = (
            weights["code_coverage"] * code_coverage
            + weights["prompt_completeness"] * prompt_completeness
            + weights["test_coverage"] * test_coverage
            + weights["orphaned"] * orphaned_score
        )

        return {
            "overall_score": round(overall_score),
            "code_coverage": round(code_coverage),
            "prompt_completeness": round(prompt_completeness),
            "test_coverage": round(test_coverage),
            "orphaned_count": orphaned_count,
        }

    def _extract_critical_issues(self) -> List[Dict]:
        """Extract critical issues from validation report."""
        if not self.validation_report_path.exists():
            return []

        try:
            with open(self.validation_report_path, "r") as f:
                report_content = f.read()

            # Extract core document issues
            core_issues = []
            core_section_match = re.search(
                r"## Core Document Issues(.*?)(?=##|\Z)", report_content, re.DOTALL
            )

            if core_section_match:
                core_section = core_section_match.group(1)
                issue_blocks = re.finditer(
                    r"### (.*?)\n.*?- \*\*Path\*\*: `(.*?)`.*?- \*\*Issues\*\*:(.*?)(?=###|\Z)",
                    core_section,
                    re.DOTALL,
                )

                for match in issue_blocks:
                    name = match.group(1).strip()
                    location = match.group(2).strip()
                    issues_text = match.group(3).strip()

                    issues = re.findall(r"- (.*?)$", issues_text, re.MULTILINE)
                    for issue in issues:
                        if "required" in issue.lower():
                            core_issues.append(
                                {
                                    "description": f"Missing required content in {name}",
                                    "location": location,
                                }
                            )

            # Extract prompt module issues
            prompt_issues = []
            prompt_section_match = re.search(
                r"## Prompt Module Issues(.*?)(?=##|\Z)", report_content, re.DOTALL
            )

            if prompt_section_match:
                prompt_section = prompt_section_match.group(1)
                issue_blocks = re.finditer(
                    r"### (.*?)\n.*?- \*\*Path\*\*: `(.*?)`.*?- \*\*Issues\*\*:(.*?)(?=###|\Z)",
                    prompt_section,
                    re.DOTALL,
                )

                for match in issue_blocks:
                    name = match.group(1).strip()
                    location = match.group(2).strip()
                    issues_text = match.group(3).strip()

                    issues = re.findall(r"- (.*?)$", issues_text, re.MULTILINE)
                    for issue in issues:
                        if (
                            "required" in issue.lower()
                            and "front matter" in issue.lower()
                        ):
                            prompt_issues.append(
                                {
                                    "description": f"Missing required front matter in {name}",
                                    "location": location,
                                }
                            )

            # Return combined issues, prioritizing core issues
            return core_issues + prompt_issues
        except Exception as e:
            logger.error(f"Failed to extract critical issues: {e}")
            return []

    def _generate_recommendations(self) -> List[Dict]:
        """Generate recommendations based on metrics and issues."""
        recommendations = []

        # Core document completion recommendation
        if len(self._extract_critical_issues()) > 0:
            recommendations.append(
                {
                    "priority": 1,
                    "description": "Complete all required fields in core documents and prompt modules",
                }
            )

        # Code documentation recommendation
        if self.metrics["code_coverage"] < 80:
            recommendations.append(
                {
                    "priority": (
                        2 if len(recommendations) == 0 else len(recommendations) + 1
                    ),
                    "description": f"Improve code documentation coverage from {self.metrics['code_coverage']}% to at least 80%",
                }
            )

        # Test coverage recommendation
        if self.metrics["test_coverage"] < 80:
            recommendations.append(
                {
                    "priority": (
                        2 if len(recommendations) == 0 else len(recommendations) + 1
                    ),
                    "description": f"Increase test coverage from {self.metrics['test_coverage']}% to at least 80%",
                }
            )

        # Orphaned documents recommendation
        if self.metrics["orphaned_count"] > 5:
            recommendations.append(
                {
                    "priority": (
                        2 if len(recommendations) == 0 else len(recommendations) + 1
                    ),
                    "description": f"Address {self.metrics['orphaned_count']} orphaned documents by connecting them to related components",
                }
            )

        # If no specific recommendations, add a general one
        if len(recommendations) == 0:
            recommendations.append(
                {
                    "priority": 1,
                    "description": "Maintain current documentation quality and expand coverage as new features are added",
                }
            )

        return recommendations

    def _generate_ascii_graph(self) -> str:
        """Generate ASCII chart of metrics."""
        # Very simple ASCII bar chart
        metrics = self.metrics
        max_width = 50

        chart = []
        chart.append("Documentation Metrics:")
        chart.append("---------------------")

        for metric, value in [
            ("Overall Score", metrics["overall_score"]),
            ("Code Coverage", metrics["code_coverage"]),
            ("Prompt Completeness", metrics["prompt_completeness"]),
            ("Test Coverage", metrics["test_coverage"]),
        ]:
            bar_width = int((value / 100) * max_width)
            bar = "█" * bar_width
            chart.append(f"{metric:20} [{bar:<{max_width}}] {value}%")

        return "\n".join(chart)

    def _generate_recent_changes(self) -> List[Dict]:
        """Generate list of recent documentation changes."""
        # In a real implementation, this would extract data from git history
        # For this example, we'll create a mock entry
        return [
            {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "description": "Initial documentation analysis setup",
                "impact": "Baseline established",
            }
        ]

    def generate_dashboard(self) -> str:
        """Generate the documentation dashboard."""
        logger.info("Generating documentation dashboard")

        # Prepare template variables
        template_vars = {
            "metrics": self.metrics,
            "current_date": datetime.now().strftime("%Y-%m-%d"),
            "graph": self._generate_ascii_graph(),
            "recent_changes": self._generate_recent_changes(),
            "critical_issues": self._extract_critical_issues(),
            "recommendations": self._generate_recommendations(),
        }

        # Apply template variables
        dashboard = self.template

        # Replace conditionals
        for condition_match in re.finditer(
            r"<% if ([^%]+) %>(.*?)(?:<% else %>(.*?))?<% endif %>",
            dashboard,
            re.DOTALL,
        ):
            condition = condition_match.group(1).strip()
            if_content = condition_match.group(2)
            else_content = condition_match.group(3) if condition_match.group(3) else ""

            # Evaluate condition (very simple evaluation)
            parts = condition.split(">=")
            if len(parts) == 2:
                left = parts[0].strip()
                right = float(parts[1].strip())

                # Get left value from template_vars
                path = left.split(".")
                value = template_vars
                for key in path:
                    value = value.get(key, 0)

                result = if_content if value >= right else else_content
                dashboard = dashboard.replace(condition_match.group(0), result)

        # Replace elseif conditions
        for condition_match in re.finditer(r"<% elseif ([^%]+) %>", dashboard):
            condition = condition_match.group(0)
            dashboard = dashboard.replace(condition, "<% else %>")

        # Replace loops
        for loop_match in re.finditer(
            r"<% for (\w+) in ([^%]+) %>(.*?)<% endfor %>", dashboard, re.DOTALL
        ):
            var_name = loop_match.group(1)
            collection_name = loop_match.group(2).strip()
            content_template = loop_match.group(3)

            # Get collection from template_vars
            path = collection_name.split(".")
            collection = template_vars
            for key in path:
                collection = collection.get(key, [])

            # Generate content for each item
            generated_content = ""
            for item in collection:
                item_content = content_template

                # Replace variable references
                for var_match in re.finditer(
                    r"<%= " + var_name + r"\.([^%]+) %>", item_content
                ):
                    var_path = var_match.group(1).strip()
                    var_value = str(item.get(var_path, ""))
                    item_content = item_content.replace(var_match.group(0), var_value)

                generated_content += item_content

            dashboard = dashboard.replace(loop_match.group(0), generated_content)

        # Replace simple variable references
        for var_match in re.finditer(r"<%= ([^%]+) %>", dashboard):
            var_path = var_match.group(1).strip()

            # Handle ternary expressions
            if "?" in var_path and ":" in var_path:
                ternary_parts = var_path.split("?")
                condition = ternary_parts[0].strip()
                values = ternary_parts[1].split(":")
                true_value = values[0].strip().strip("\"'")
                false_value = values[1].strip().strip("\"'")

                # Evaluate condition
                condition_parts = condition.split(">=")
                if len(condition_parts) == 2:
                    left = condition_parts[0].strip()
                    right = float(condition_parts[1].strip())

                    # Get left value from template_vars
                    path = left.split(".")
                    value = template_vars
                    for key in path:
                        value = value.get(key, 0)

                    var_value = true_value if value >= right else false_value
                    dashboard = dashboard.replace(var_match.group(0), var_value)
                continue

            # Handle regular variables
            var_parts = var_path.split(".")
            var_value = template_vars
            for part in var_parts:
                if isinstance(var_value, dict):
                    var_value = var_value.get(part, "")
                else:
                    var_value = ""
                    break

            dashboard = dashboard.replace(var_match.group(0), str(var_value))

        return dashboard

    def save_dashboard(self, output_path: str) -> None:
        """Save the dashboard to a file."""
        dashboard = self.generate_dashboard()

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w") as f:
            f.write(dashboard)

        logger.info(f"Dashboard saved to {output_path}")


def main():
    """Command-line entry point."""
    parser = argparse.ArgumentParser(
        description="Generate documentation health dashboard"
    )
    parser.add_argument(
        "--registry",
        default="docs/nlu/document_registry.json",
        help="Path to document registry JSON file",
    )
    parser.add_argument(
        "--relationships",
        default="docs/nlu/relationship_map.json",
        help="Path to relationship map JSON file",
    )
    parser.add_argument(
        "--validation-report",
        default="docs/synthesis/reports/validation_report.md",
        help="Path to validation report",
    )
    parser.add_argument(
        "--template",
        default="docs/nlu/dashboard_template.md",
        help="Path to dashboard template",
    )
    parser.add_argument(
        "--output",
        default="docs/synthesis/reports/documentation_dashboard.md",
        help="Output path for the dashboard",
    )

    args = parser.parse_args()

    generator = DashboardGenerator(
        args.registry, args.relationships, args.validation_report, args.template
    )
    generator.save_dashboard(args.output)

    return 0


if __name__ == "__main__":
    exit(main())
