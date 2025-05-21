#!/usr/bin/env python3
"""
Documentation Validator - Verify documentation completeness against criteria.

This module validates the repository documentation against completeness criteria
and generates a report of any gaps or issues found.
"""

import os
import json
import yaml
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('nlu.validator')


class DocumentationValidator:
    """Validates documentation against completeness criteria."""
    
    def __init__(self, registry_path: str, criteria_path: str):
        """
        Initialize the documentation validator.
        
        Args:
            registry_path: Path to the document registry JSON file
            criteria_path: Path to the completeness criteria YAML file
        """
        self.registry_path = Path(registry_path)
        self.criteria_path = Path(criteria_path)
        self.doc_registry = self._load_json(registry_path)
        self.criteria = self._load_yaml(criteria_path)
        self.validation_results = {
            "core_documents": [],
            "prompt_modules": [],
            "code_files": [],
            "coverage_metrics": {}
        }
        
    def _load_json(self, path: str) -> Dict:
        """Load JSON file."""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load {path}: {e}")
            return {}
            
    def _load_yaml(self, path: str) -> Dict:
        """Load YAML file."""
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load {path}: {e}")
            return {}
    
    def validate_documentation(self) -> Dict:
        """
        Validate documentation against completeness criteria.
        
        Returns:
            Dictionary with validation results
        """
        logger.info("Validating documentation against criteria")
        
        # Validate core documents
        self._validate_core_documents()
        
        # Validate prompt modules
        self._validate_prompt_modules()
        
        # Validate code files
        self._validate_code_files()
        
        # Calculate coverage metrics
        self._calculate_coverage_metrics()
        
        return self.validation_results
    
    def _validate_core_documents(self) -> None:
        """Validate core documents against criteria."""
        core_criteria = self.criteria.get("core_criteria", [])
        
        for criterion in core_criteria:
            path = criterion["path"]
            
            # Check if document exists
            exists = path in self.doc_registry
            
            result = {
                "name": criterion["name"],
                "path": path,
                "exists": exists,
                "required": criterion.get("required", False),
                "issues": []
            }
            
            if exists:
                # Check must_contain requirements
                if "must_contain" in criterion:
                    content_targets = criterion["must_contain"]
                    document = self.doc_registry[path]
                    
                    # Check if document contains required sections
                    if "headers" in document:
                        headers = [h["text"].lower() for h in document["headers"]]
                        
                        for target in content_targets:
                            found = any(target.lower() in header for header in headers)
                            if not found:
                                result["issues"].append(f"Missing required section: '{target}'")
            else:
                if criterion.get("required", False):
                    result["issues"].append("Required document is missing")
                    
            self.validation_results["core_documents"].append(result)
    
    def _validate_prompt_modules(self) -> None:
        """Validate prompt modules against criteria."""
        prompt_criteria = self.criteria.get("prompt_modules", {})
        required_fields = prompt_criteria.get("front_matter_fields", {}).get("required", [])
        recommended_fields = prompt_criteria.get("front_matter_fields", {}).get("recommended", [])
        required_sections = prompt_criteria.get("sections", {}).get("required", [])
        
        for doc_id, metadata in self.doc_registry.items():
            if doc_id.startswith(("prompt-library/", "modules/")):
                result = {
                    "name": metadata.get("front_matter", {}).get("name", doc_id),
                    "path": doc_id,
                    "issues": []
                }
                
                # Check required front matter fields
                if "front_matter" in metadata:
                    front_matter = metadata["front_matter"]
                    for field in required_fields:
                        if field not in front_matter:
                            result["issues"].append(f"Missing required front matter field: '{field}'")
                    
                    # Check recommended front matter fields
                    for field in recommended_fields:
                        if field not in front_matter:
                            result["issues"].append(f"Missing recommended front matter field: '{field}' (warning)")
                else:
                    result["issues"].append("Missing front matter completely")
                
                # Check required sections
                if "headers" in metadata:
                    headers = [h["text"].lower() for h in metadata["headers"]]
                    
                    for section in required_sections:
                        found = any(section.lower() in header for header in headers)
                        if not found:
                            result["issues"].append(f"Missing required section: '{section}'")
                
                self.validation_results["prompt_modules"].append(result)
    
    def _validate_code_files(self) -> None:
        """Validate code files against criteria."""
        code_criteria = self.criteria.get("code", {})
        
        for doc_id, metadata in self.doc_registry.items():
            if doc_id.startswith("src/") and metadata.get("file_type") in ["py", "js", "ts"]:
                file_type = metadata["file_type"]
                type_criteria = code_criteria.get(file_type, {}) if file_type in ["py", "js"] else code_criteria.get("javascript", {})
                
                result = {
                    "name": metadata.get("title", doc_id),
                    "path": doc_id,
                    "issues": []
                }
                
                # Check for docstrings
                if "docstring" in type_criteria.get("required", []):
                    if not metadata.get("docstring"):
                        result["issues"].append("Missing required docstring")
                
                # Check for tests
                if "tests" in type_criteria.get("required", []) or "tests" in type_criteria.get("recommended", []):
                    is_required = "tests" in type_criteria.get("required", [])
                    # Construct potential test paths
                    test_path = doc_id.replace("src/", "tests/")
                    test_path_with_test = test_path.replace(".py", "_test.py").replace(".js", "_test.js").replace(".ts", "_test.ts")
                    test_path_prefix = "tests/test_" + Path(doc_id).name
                    
                    if not any(p in self.doc_registry for p in [test_path, test_path_with_test, test_path_prefix]):
                        if is_required:
                            result["issues"].append("Missing required tests")
                        else:
                            result["issues"].append("Missing recommended tests (warning)")
                
                # Check type hints for Python
                if file_type == "py" and "type_hints" in type_criteria.get("required", []):
                    # This would require more sophisticated parsing
                    pass
                
                self.validation_results["code_files"].append(result)
    
    def _calculate_coverage_metrics(self) -> None:
        """Calculate documentation coverage metrics."""
        coverage_thresholds = self.criteria.get("coverage_thresholds", {})
        
        # Count files by type
        total_src_files = sum(1 for doc_id in self.doc_registry if doc_id.startswith("src/"))
        total_prompt_modules = sum(1 for doc_id in self.doc_registry if doc_id.startswith(("prompt-library/", "modules/")))
        
        # Count documented files
        documented_src_files = sum(1 for doc_id in self.doc_registry 
                                  if doc_id.startswith("src/") and 
                                  self.doc_registry[doc_id].get("docstring"))
        
        complete_prompt_modules = sum(1 for result in self.validation_results["prompt_modules"] 
                                     if not result["issues"])
        
        # Count tested files
        tested_src_files = sum(1 for doc_id in self.doc_registry 
                               if doc_id.startswith("src/") and 
                               any(rel.startswith("tests/") 
                                   for rel in self.doc_registry.get(doc_id, {})
                                              .get("relationships", {})
                                              .get("tested_by", [])))
        
        # Calculate percentages
        src_doc_percentage = (documented_src_files / total_src_files * 100) if total_src_files > 0 else 0
        prompt_doc_percentage = (complete_prompt_modules / total_prompt_modules * 100) if total_prompt_modules > 0 else 0
        src_test_percentage = (tested_src_files / total_src_files * 100) if total_src_files > 0 else 0
        
        # Store metrics
        self.validation_results["coverage_metrics"] = {
            "src_files": {
                "total": total_src_files,
                "documented": documented_src_files,
                "percentage": src_doc_percentage,
                "threshold": coverage_thresholds.get("documentation", {}).get("src", 0),
                "pass": src_doc_percentage >= coverage_thresholds.get("documentation", {}).get("src", 0)
            },
            "prompt_modules": {
                "total": total_prompt_modules,
                "complete": complete_prompt_modules,
                "percentage": prompt_doc_percentage,
                "threshold": coverage_thresholds.get("documentation", {}).get("modules", 0),
                "pass": prompt_doc_percentage >= coverage_thresholds.get("documentation", {}).get("modules", 0)
            },
            "test_coverage": {
                "total": total_src_files,
                "tested": tested_src_files,
                "percentage": src_test_percentage,
                "threshold": coverage_thresholds.get("tests", {}).get("src", 0),
                "pass": src_test_percentage >= coverage_thresholds.get("tests", {}).get("src", 0)
            }
        }
    
    def generate_validation_report(self) -> str:
        """
        Generate a markdown report of validation results.
        
        Returns:
            Markdown string with validation report
        """
        logger.info("Generating validation report")
        
        # Build markdown document
        lines = [
            "# Documentation Validation Report",
            "",
            f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
            "",
            "## Summary",
            ""
        ]
        
        # Add coverage metrics summary
        coverage_metrics = self.validation_results["coverage_metrics"]
        src_files = coverage_metrics.get("src_files", {})
        prompt_modules = coverage_metrics.get("prompt_modules", {})
        test_coverage = coverage_metrics.get("test_coverage", {})
        
        lines.extend([
            "### Documentation Coverage",
            "",
            f"- **Source Files**: {src_files.get('documented', 0)}/{src_files.get('total', 0)} " +
            f"({src_files.get('percentage', 0):.1f}%) " +
            f"{'✅' if src_files.get('pass', False) else '❌'}",
            
            f"- **Prompt Modules**: {prompt_modules.get('complete', 0)}/{prompt_modules.get('total', 0)} " +
            f"({prompt_modules.get('percentage', 0):.1f}%) " +
            f"{'✅' if prompt_modules.get('pass', False) else '❌'}",
            
            f"- **Test Coverage**: {test_coverage.get('tested', 0)}/{test_coverage.get('total', 0)} " +
            f"({test_coverage.get('percentage', 0):.1f}%) " +
            f"{'✅' if test_coverage.get('pass', False) else '❌'}",
            ""
        ])
        
        # Add core document issues
        core_issues = [doc for doc in self.validation_results["core_documents"] if doc["issues"]]
        if core_issues:
            lines.extend([
                "## Core Document Issues",
                ""
            ])
            
            for doc in core_issues:
                lines.extend([
                    f"### {doc['name']}",
                    f"- **Path**: `{doc['path']}`",
                    f"- **Exists**: {'Yes' if doc['exists'] else 'No'}"
                ])
                
                if doc["issues"]:
                    lines.append("- **Issues**:")
                    for issue in doc["issues"]:
                        lines.append(f"  - {issue}")
                
                lines.append("")
        
        # Add prompt module issues
        prompt_issues = [doc for doc in self.validation_results["prompt_modules"] if doc["issues"]]
        if prompt_issues:
            lines.extend([
                "## Prompt Module Issues",
                ""
            ])
            
            for doc in prompt_issues:
                lines.extend([
                    f"### {doc['name']}",
                    f"- **Path**: `{doc['path']}`",
                    "- **Issues**:"
                ])
                
                for issue in doc["issues"]:
                    lines.append(f"  - {issue}")
                
                lines.append("")
        
        # Add code file issues
        code_issues = [doc for doc in self.validation_results["code_files"] if doc["issues"]]
        if code_issues:
            lines.extend([
                "## Code File Issues",
                ""
            ])
            
            for doc in code_issues:
                lines.extend([
                    f"### {doc['name']}",
                    f"- **Path**: `{doc['path']}`",
                    "- **Issues**:"
                ])
                
                for issue in doc["issues"]:
                    lines.append(f"  - {issue}")
                
                lines.append("")
        
        # Add recommendations
        lines.extend([
            "## Recommendations",
            ""
        ])
        
        if not core_issues and not prompt_issues and not code_issues:
            lines.append("✅ Documentation is in excellent shape! No significant issues found.")
        else:
            # Prioritize recommendations
            if any(doc["required"] and not doc["exists"] for doc in self.validation_results["core_documents"]):
                lines.append("1. Create missing required core documents.")
                
            if any("Missing required front matter field" in issue 
                  for doc in self.validation_results["prompt_modules"] 
                  for issue in doc["issues"]):
                lines.append("2. Add missing required front matter fields to prompt modules.")
                
            if any("Missing required docstring" in issue 
                  for doc in self.validation_results["code_files"] 
                  for issue in doc["issues"]):
                lines.append("3. Add docstrings to code files.")
                
            if any("Missing required tests" in issue 
                  for doc in self.validation_results["code_files"] 
                  for issue in doc["issues"]):
                lines.append("4. Add tests for code files.")
        
        return "\n".join(lines)
    
    def validate_and_report(self, report_path: str) -> None:
        """
        Validate documentation and generate a report.
        
        Args:
            report_path: Path to save the validation report
        """
        self.validate_documentation()
        report = self.generate_validation_report()
        
        # Save report
        report_dir = Path(report_path).parent
        report_dir.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w') as f:
            f.write(report)
            
        logger.info(f"Validation report saved to {report_path}")


def main():
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description="Validate documentation completeness")
    parser.add_argument("--registry", default="docs/nlu/document_registry.json", 
                        help="Path to document registry JSON file")
    parser.add_argument("--criteria", default="docs/nlu/schemas/completeness_criteria.yaml", 
                        help="Path to completeness criteria YAML file")
    parser.add_argument("--report", default="docs/synthesis/reports/validation_report.md", 
                        help="Path to save the validation report")
    
    args = parser.parse_args()
    
    validator = DocumentationValidator(args.registry, args.criteria)
    validator.validate_and_report(args.report)
    
    return 0


if __name__ == "__main__":
    exit(main())
