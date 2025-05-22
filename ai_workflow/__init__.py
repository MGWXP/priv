from importlib import import_module

_base = import_module("src.ai_workflow")
for attr in _base.__all__:
    globals()[attr] = getattr(_base, attr)

# Expose submodules for fully-qualified imports
submodules = [
    "orchestrator",
    "context_graphs",
    "semantic_diff",
    "scheduler",
    "diff_analyzer_v2",
    "performance_monitor",
]
for name in submodules:
    module = import_module(f"src.ai_workflow.{name}")
    globals()[name] = module
    import_module = __import__  # to use same name
    import sys

    sys.modules[f"{__name__}.{name}"] = module
