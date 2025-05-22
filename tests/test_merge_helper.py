import builtins
from src.utils.merge_helper import auto_merge_conflict_blocks


def test_auto_merge_conflict_blocks_prefers_incoming():
    content = (
        "first\n"
        "<<<<<<< HEAD\nold\n=======\nnew\n>>>>>>> branch\n"
        "last\n"
    )
    result = auto_merge_conflict_blocks(content)
    assert "new" in result
    assert "old" not in result
    assert "first" in result and "last" in result


def test_resolve_merge_conflicts_updates_files(tmp_path, monkeypatch):
    readme = tmp_path / "README.md"
    history_dir = tmp_path / "audits"
    history_dir.mkdir()
    history = history_dir / "history.log.md"
    readme.write_text(
        "upstream\n<<<<<<< HEAD\nold\n=======\nnew\n>>>>>>> branch\n"
    )
    history.write_text(
        "log\n<<<<<<< HEAD\nA\n=======\nB\n>>>>>>> branch\n"
    )

    def open_patch(path, mode="r", encoding="utf-8"):
        if path == "README.md":
            return builtins.open(readme, mode, encoding=encoding)
        if path == "audits/history.log.md":
            return builtins.open(history, mode, encoding=encoding)
        return original_open(path, mode, encoding=encoding)

    original_open = builtins.open
    monkeypatch.setattr(builtins, "open", open_patch)

    from src.ai_workflow.orchestrator import WorkflowOrchestrator

    orch = WorkflowOrchestrator()
    orch.resolve_merge_conflicts()

    assert "<<<<" not in readme.read_text()
    assert "B" in history.read_text()
