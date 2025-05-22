# History Log

## 2025-05-21
- Initialized audit directory structure and updated GitHub integration paths.
- Renamed `gitignore` to `.gitignore` for Git compatibility.

## 2025-05-21
- Added `IntegrationsConfig` utility for server environment variables.
- Updated README with environment configuration instructions.
- Introduced `PrivDashboardPreview` React component for dashboard previews.

## 2025-05-21
- Cached valid markers during diff analyzer initialization
- Batched line writing in context graph export for improved I/O
- Expanded documentation with NLU pipeline instructions and audit directory details

## 2025-05-21
- Implemented threaded execution in `WorkflowOrchestrator` for true parallel task
  orchestration.
- Added test coverage for the parallel chain and documented the new scheduler in
  the README.

## Loop N — Merge parallel-orchestration upgrade (2025-05-21)
* Integrated parallel executor, DiffAnalyzer V2 gate, BugFix cycle.
* Tag: v1.0.0

## 2025-05-22
- Expanded `DiffAnalyzerV2` with marker alignment checks and coding standard validation.
- Updated module documentation and README with new analyzer capabilities.

## 2025-05-23
- Added dedicated `Module_BugFixer` for handling `[fix]` tasks.
- Introduced `BugFixCycle` chain and updated prompt registry and README.

## 2025-05-24
- Upgraded Module_Observability to v1.1 with automatic runtime and memory tracking.
- Orchestrator now records metrics for each chain execution.
- Updated README and module documentation accordingly.

## 2025-05-25
- Expanded Module_Observability to v1.2 with UI latency metrics and budget alerts.
- Updated orchestrator to pass INP, CLS, and TBT values from the execution context.
- Tests and documentation updated to reflect new observability capabilities.

## 2025-05-26
- Added marker fields to all module front-matter for CI compatibility.
- Synced Module_DiffAnalyzerV2 metadata in prompt registry.

## 2025-05-22
- Documented custom instructions profile for ChatGPT integration.
- Added README section on using custom instructions.
