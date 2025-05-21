from ai_workflow import ParallelExecutor


def test_parallel_executor_runs_tasks(tmp_path):
    executor = ParallelExecutor(max_tasks=2, log_path=tmp_path / "log.md")
    modules = ["Module_TaskA", "Module_TestGenerator", "Module_DocWriter"]
    results = executor.run_tasks(modules, {"foo": "bar"})
    assert len(results) == len(modules)
    for r in results:
        assert r["status"] == "executed"
    log_path = tmp_path / "log.md"
    assert log_path.exists()
    log_contents = log_path.read_text(encoding="utf-8")
    for module in modules:
        assert module in log_contents
