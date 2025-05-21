"""Workflow orchestration utilities."""

from __future__ import annotations

import os
from typing import Any, Dict, List

import yaml

from .context_graphs import ContextGraphManager


class WorkflowOrchestrator:
    """Coordinate prompt chains and modules.

    The orchestrator loads prompt chain definitions from ``prompt-registry.yaml``
    and executes the modules for a given chain sequentially. A shared context
    dictionary is threaded through each module call so data produced by one
    module is available to the next.
    """

    def __init__(self, registry_path: str = "prompt-registry.yaml") -> None:
        self._graph_manager = ContextGraphManager()
        with open(registry_path, "r", encoding="utf-8") as f:
            registry = yaml.safe_load(f) or {}

        self._module_meta: Dict[str, Dict[str, Any]] = {
            mod["name"]: mod for mod in registry.get("modules", [])
        }
        self._chains: Dict[str, List[str]] = {
            dep["chain"]: dep.get("sequence", [])
            for dep in registry.get("dependencies", [])
        }

    def execute_chain(
        self, chain_name: str, context: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """Execute a prompt chain sequentially.

        Parameters
        ----------
        chain_name:
            Name of the chain to execute.
        context:
            Optional execution context passed to the chain.

        Returns
        -------
        dict
            Execution metadata containing the final context and executed modules.
        """

        context = context or {}
        context.setdefault("executed_modules", [])
        modules = self._chains.get(chain_name, [])

        for module in modules:
            self.execute_module(module, context)

        data: Dict[str, Any] = {
            "chain": chain_name,
            "modules": modules,
            "context": context,
            "status": "completed",
        }
        self._graph_manager.update_from_runtime(data)
        return data

    def execute_module(
        self, module_name: str, context: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """Execute a single prompt module.

        The implementation here is a placeholder that simply records the module
        execution in the shared context. Real prompt invocation would be handled
        by the runtime environment.
        """

        context = context or {}
        context.setdefault("executed_modules", []).append(module_name)

        data: Dict[str, Any] = {
            "module": module_name,
            "metadata": self._module_meta.get(module_name, {}),
            "status": "executed",
        }
        self._graph_manager.update_from_runtime({module_name: data})
        return data

    def export_context_graph(self, output_dir: str = "audits/dashboards") -> str:
        """Export the context graph and return the file path."""

        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "context_graph.html")
        return self._graph_manager.generate_html_visualization(output_path)
