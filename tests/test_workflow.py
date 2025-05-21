import os
import pytest
from ai_workflow import (
    WorkflowOrchestrator,
    ContextGraphManager,
    SemanticDiffAnalyzer,
    PerformanceMonitor,
)


def test_orchestrator_execute_chain(tmp_path):
    orch = WorkflowOrchestrator()
    result = orch.execute_chain("demo", {"foo": "bar"})
    assert result["status"] == "executed"
    path = orch.export_context_graph(output_dir=tmp_path.as_posix())
    assert os.path.exists(path)


def test_parallel_chain(tmp_path):
    orch = WorkflowOrchestrator()
    result = orch.execute_chain("ParallelFeatureDevCycle", {"foo": "bar"})
    assert result["status"] == "completed"
    for mod in [
        "Module_TaskA",
        "Module_TestGenerator",
        "Module_DocWriter",
        "Module_DiffAnalyzerV2",
    ]:
        assert mod in result["executed"]


def test_context_graph_manager(tmp_path):
    manager = ContextGraphManager()
    manager.update_from_runtime({"a": 1})
    json_path = manager.export_graph_json(tmp_path / "cg.json")
    md_path = manager.export_markdown_summary(tmp_path / "cg.md")
    html_path = manager.generate_html_visualization(tmp_path / "cg.html")
    for p in (json_path, md_path, html_path):
        assert os.path.exists(p)


def test_semantic_diff_analyzer(tmp_path):
    analyzer = SemanticDiffAnalyzer()
    old = "a\n"
    new = "a\nb\n"
    analysis = analyzer.analyze_file_diff(old, new, "demo.txt")
    assert analysis["additions"] == 1
    ver = analyzer.verify_marker_compliance([analysis], "feat")
    report = analyzer.generate_diff_report([analysis], "feat", ver)
    assert os.path.exists(report["report_path"])


def test_performance_monitor(tmp_path):
    monitor = PerformanceMonitor()
    metrics = {"inp_ms": 50}
    assert monitor.update_iteration_metrics("123", metrics)
    comp = monitor.check_budget_compliance(metrics)
    dash_files = monitor.generate_performance_dashboard()
    assert isinstance(comp, dict)
    for p in dash_files:
        assert os.path.exists(p)


def test_chain_generates_metrics(tmp_path, monkeypatch):
    import ai_workflow.orchestrator as orch_mod

    def _mon_factory():
        return PerformanceMonitor(metrics_dir=tmp_path / "audits" / "performance")

    monkeypatch.setattr(orch_mod, "PerformanceMonitor", _mon_factory)
    orch = WorkflowOrchestrator()
    orch.execute_chain("demo")
    metrics_path = tmp_path / "audits" / "performance"
    assert any(p.suffix == ".json" for p in metrics_path.glob("*.json"))


@pytest.mark.asyncio
async def test_async_parallel_chain(tmp_path):
    orch = WorkflowOrchestrator()
    result = await orch.execute_chain_async("ParallelFeatureDevCycle", {"foo": "bar"})
    assert result["status"] == "completed"
    for mod in [
        "Module_TaskA",
        "Module_TestGenerator",
        "Module_DocWriter",
        "Module_DiffAnalyzerV2",
    ]:
        assert mod in result["executed"]
