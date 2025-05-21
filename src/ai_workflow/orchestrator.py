"""Workflow orchestration utilities."""

from __future__ import annotations

import os
from typing import Any, Dict, List

import yaml
from concurrent.futures import ThreadPoolExecutor

from .context_graphs import ContextGraphManager


class WorkflowOrchestrator:
    """Coordinate prompt chains and modules.

    This stub orchestrator provides just enough functionality for the
    command-line interface to execute prompt chains and modules while
    capturing a minimal context graph.
    """

    def __init__(self, registry_path: str = "prompt-registry.yaml") -> None:
        """Initialize the orchestrator with registry and budget data."""

        self._graph_manager = ContextGraphManager()

        try:
            with open(registry_path, "r", encoding="utf-8") as f:
                self._registry = yaml.safe_load(f)
        except OSError:
            self._registry = {}

        try:
            with open("execution-budget.yaml", "r", encoding="utf-8") as f:
                budget = yaml.safe_load(f)
            self._max_parallel = budget.get("task_limits", {}).get(
                "max_parallel_tasks", 3
            )
        except OSError:
            self._max_parallel = 3

    def execute_chain(
        self, chain_name: str, context: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """Execute a prompt chain.

        Parameters
        ----------
        chain_name:
            Name of the chain to execute.
        context:
            Optional execution context passed to the chain.

        Returns
        -------
        dict
            Execution metadata.
        """

        chain_def = None
        for chain in self._registry.get("dependencies", []):
            if chain.get("chain") == chain_name:
                chain_def = chain
                break

        if not chain_def:
            data = {
                "chain": chain_name,
                "context": context or {},
                "status": "executed",
            }
            self._graph_manager.update_from_runtime(data)
            return data

        sequence = chain_def.get("sequence", [])
        executed: List[Dict[str, Any]] = []
        i = 0
        while i < len(sequence):
            step = sequence[i]
            if isinstance(step, dict) and "Module_ParallelAsync" in step:
                modules = step["Module_ParallelAsync"].get("run_parallel", [])
                executed.extend(self._run_parallel(modules, context))
                i += 1
                continue

            if step == "Module_ParallelAsync":
                modules = sequence[i + 1 : i + 1 + self._max_parallel]
                executed.extend(self._run_parallel(modules, context))
                i += 1 + len(modules)
                continue

            executed.append(self.execute_module(step, context))
            i += 1

        data = {
            "chain": chain_name,
            "executed": [m.get("module") for m in executed],
            "status": "completed",
        }
        self._graph_manager.update_from_runtime(data)
        return data

    def execute_module(
        self, module_name: str, context: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """Execute a single prompt module."""

        data: Dict[str, Any] = {
            "module": module_name,
            "context": context or {},
            "status": "executed",
        }
        self._graph_manager.update_from_runtime(data)
        return data

    def _run_parallel(
        self, modules: List[str], context: Dict[str, Any] | None = None
    ) -> List[Dict[str, Any]]:
        """Execute multiple modules in parallel threads."""

        max_workers = min(len(modules), self._max_parallel)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(self.execute_module, m, context) for m in modules
            ]
            return [f.result() for f in futures]

    def export_context_graph(self, output_dir: str = "audits/dashboards") -> str:
        """Export the context graph and return the file path."""

        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "context_graph.html")
        return self._graph_manager.generate_html_visualization(output_path)
