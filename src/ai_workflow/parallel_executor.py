"""Parallel task execution utilities."""

from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Any, Dict, Iterable, List

import yaml

from .orchestrator import WorkflowOrchestrator


class ParallelExecutor:
    """Execute multiple workflow modules concurrently."""

    def __init__(
        self, max_tasks: int | None = None, log_path: str | None = None
    ) -> None:
        with open("execution-budget.yaml", "r", encoding="utf-8") as f:
            budget = yaml.safe_load(f)
        default_tasks = budget.get("task_limits", {}).get("max_parallel_tasks", 1)
        self.max_tasks = max_tasks or default_tasks
        self.log_path = log_path or os.path.join("audits", "parallel_execution.log.md")

    def _run_module(
        self, module: str, context: Dict[str, Any] | None
    ) -> Dict[str, Any]:
        orch = WorkflowOrchestrator()
        return orch.execute_module(module, context)

    def run_tasks(
        self, modules: Iterable[str], context: Dict[str, Any] | None = None
    ) -> List[Dict[str, Any]]:
        """Run modules concurrently and return execution results."""

        results: List[Dict[str, Any]] = []
        with ThreadPoolExecutor(max_workers=self.max_tasks) as executor:
            futures = {
                executor.submit(self._run_module, m, context): m for m in modules
            }
            for future in as_completed(futures):
                results.append(future.result())
        self._log_results(modules, results)
        return results

    def _log_results(
        self, modules: Iterable[str], results: List[Dict[str, Any]]
    ) -> None:
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(f"## Execution {datetime.now().isoformat()}\n")
            for module, result in zip(modules, results):
                status = result.get("status", "unknown")
                f.write(f"- {module}: {status}\n")
            f.write("\n")
