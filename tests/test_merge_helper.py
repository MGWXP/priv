from src.ai_workflow.orchestrator import WorkflowOrchestrator
from utils.merge_helper import auto_merge_conflict_blocks
import os


def test_auto_merge_conflict_blocks():
    content = """<<<<<<< HEAD
ours
=======
theirs
>>>>>>> main
"""
    result = auto_merge_conflict_blocks(content)
    assert result.strip() == "theirs"


def test_orchestrator_resolve_merge_conflicts(tmp_path, monkeypatch):
    readme = tmp_path / "README.md"
    log = tmp_path / "audits" / "history.log.md"
    log.parent.mkdir()
    readme.write_text(
        """<<<<<<< HEAD\nold\n=======\nnew\n>>>>>>> branch\n""",
        encoding="utf-8",
    )
    log.write_text(
        """<<<<<<< HEAD\na\n=======\nb\n>>>>>>> branch\n""",
        encoding="utf-8",
    )
    cwd = os.getcwd()
    os.chdir(tmp_path)
    orch = WorkflowOrchestrator()
    orch.resolve_merge_conflicts()
    os.chdir(cwd)
    assert readme.read_text().strip() == "new"
    assert log.read_text().strip() == "b"
