"""Performance monitoring utilities."""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Generator

from contextlib import contextmanager
import time
import tracemalloc

import yaml


class PerformanceMonitor:
    """Store and evaluate iteration performance metrics."""

    def __init__(self) -> None:
        self.metrics_dir = os.path.join("audits", "performance")
        os.makedirs(self.metrics_dir, exist_ok=True)

        with open("execution-budget.yaml", "r", encoding="utf-8") as f:
            budget = yaml.safe_load(f)
        self.budgets = budget.get("performance_budgets", {})

    @contextmanager
    def capture_metrics(self) -> Generator[Dict[str, float], None, None]:
        """Capture runtime and memory usage for a code block."""

        start = time.perf_counter()
        tracemalloc.start()
        metrics: Dict[str, float] = {}
        try:
            yield metrics
        finally:
            end = time.perf_counter()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            metrics["runtime_ms"] = (end - start) * 1000
            metrics["memory_peak_kb"] = peak / 1024

    def update_iteration_metrics(self, iteration: str, metrics: Dict[str, Any]) -> bool:
        """Persist metrics for a given iteration and return success status."""

        try:
            path = os.path.join(self.metrics_dir, f"{iteration}.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(metrics, f, indent=2)
            return True
        except OSError:
            return False

    def check_budget_compliance(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate metrics against the configured performance budget."""

        violations: List[Dict[str, str]] = []
        compliant = True

        chat_budget = self.budgets.get("chat_ui", {})
        if "inp_ms" in metrics and metrics["inp_ms"] > chat_budget.get(
            "max_inp_ms", float("inf")
        ):
            compliant = False
            violations.append({"metric": "inp_ms", "message": "INP exceeds budget"})

        test_budget = self.budgets.get("test_suite", {})
        if (
            "runtime_ms" in metrics
            and metrics["runtime_ms"]
            > test_budget.get("max_runtime_seconds", float("inf")) * 1000
        ):
            compliant = False
            violations.append(
                {"metric": "runtime_ms", "message": "Test runtime exceeds budget"}
            )

        if (
            "memory_peak_kb" in metrics
            and metrics["memory_peak_kb"]
            > test_budget.get("max_memory_mb", float("inf")) * 1024
        ):
            compliant = False
            violations.append(
                {"metric": "memory_peak_kb", "message": "Memory usage exceeds budget"}
            )

        return {"compliant": compliant, "violations": violations}

    def generate_performance_dashboard(self) -> List[str]:
        """Create a simple dashboard listing recorded iterations."""

        dashboard_path = os.path.join(self.metrics_dir, "dashboard.md")
        with open(dashboard_path, "w", encoding="utf-8") as f:
            f.write("# Performance Dashboard\n\n")
            for file in sorted(os.listdir(self.metrics_dir)):
                if file.endswith(".json"):
                    f.write(f"- {file}\n")
        return [dashboard_path]
