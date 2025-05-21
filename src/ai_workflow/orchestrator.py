"""Workflow orchestration utilities."""

from __future__ import annotations

import os
import time
from typing import Any, Dict

from .context_graphs import ContextGraphManager
from .performance_monitor import PerformanceMonitor


class WorkflowOrchestrator:
    """Coordinate prompt chains and modules.

    This stub orchestrator provides just enough functionality for the
    command-line interface to execute prompt chains and modules while
    capturing a minimal context graph.
    """

    def __init__(self) -> None:
        self._graph_manager = ContextGraphManager()
        self._monitor = PerformanceMonitor()

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

        with self._monitor.capture_metrics() as metrics:
            data: Dict[str, Any] = {
                "chain": chain_name,
                "context": context or {},
                "status": "executed",
            }
            self._graph_manager.update_from_runtime(data)

        iteration = str(int(time.time()))
        self._monitor.update_iteration_metrics(iteration, metrics)
        data["performance_metrics"] = metrics
        compliance = self._monitor.check_budget_compliance(metrics)
        if not compliance["compliant"]:
            data["performance_alerts"] = compliance["violations"]
        return data

    def execute_module(
        self, module_name: str, context: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """Execute a single prompt module."""

        with self._monitor.capture_metrics() as metrics:
            data: Dict[str, Any] = {
                "module": module_name,
                "context": context or {},
                "status": "executed",
            }
            self._graph_manager.update_from_runtime(data)

        iteration = str(int(time.time()))
        self._monitor.update_iteration_metrics(iteration, metrics)
        data["performance_metrics"] = metrics
        compliance = self._monitor.check_budget_compliance(metrics)
        if not compliance["compliant"]:
            data["performance_alerts"] = compliance["violations"]
        return data

    def export_context_graph(self, output_dir: str = "audits/dashboards") -> str:
        """Export the context graph and return the file path."""

        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "context_graph.html")
        return self._graph_manager.generate_html_visualization(output_path)
