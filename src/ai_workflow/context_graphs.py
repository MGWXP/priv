"""Runtime context graph utilities."""

from __future__ import annotations

import html
import json
import os
from typing import Any, Dict


class ContextGraphManager:
    """Manage a simple context graph for prompt execution."""

    def __init__(self) -> None:
        self.graph: Dict[str, Any] = {}

    def update_from_runtime(self, context: Dict[str, Any]) -> None:
        """Update the internal graph with runtime context."""

        self.graph.update(context)

    def export_graph_json(self, output_path: str | None = None) -> str:
        """Export the graph to JSON."""

        path = output_path or os.path.join("audits", "dashboards", "context_graph.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.graph, f, indent=2)
        return path

    def export_markdown_summary(self, output_path: str | None = None) -> str:
        """Export a Markdown summary of the graph."""

        path = output_path or os.path.join("audits", "dashboards", "context_graph.md")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            lines = ["# Context Graph\n", "\n"]
            lines.extend(f"- **{key}**: {value}\n" for key, value in self.graph.items())
            f.writelines(lines)
        return path

    def generate_html_visualization(self, output_path: str | None = None) -> str:
        """Generate a basic HTML visualization of the graph."""

        path = output_path or os.path.join("audits", "dashboards", "context_graph.html")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("<html><body><h1>Context Graph</h1><pre>")
            f.write(html.escape(json.dumps(self.graph, indent=2)))
            f.write("</pre></body></html>")
        return path
