---
name: "Module_Observability"
version: "1.2"
description: "Monitors runtime, memory, and UI latency metrics and validates them against the execution budget."
inputs: ["audits/performance/", "src/"]
outputs: ["audits/performance/"]
dependencies: []
author: "AI"
last_updated: "2025-05-25"
marker: chore
status: "active"
---

# Observability Module

## Purpose

Provide observability into AI task performance, recording metrics such as runtime, memory usage, and responsiveness.

The module exposes a context manager that measures runtime, memory, and optional UI latency metrics for each workflow iteration. Metrics are automatically checked against the limits defined in `execution-budget.yaml`.

## Prompt

Collect metrics during task execution and update the dashboards under `audits/performance/`. Alert when thresholds defined in `execution-budget.yaml` are exceeded. When violations occur, the PerformanceOptimization chain can be triggered to refactor code and run regression tests automatically.
