---
name: "Module_Observability"
version: "1.1"
description: "Monitors runtime and memory metrics and validates them against the execution budget."
inputs: ["audits/performance/", "src/"]
outputs: ["audits/performance/"]
dependencies: []
author: "AI"
last_updated: "2025-05-24"
status: "active"
---

# Observability Module

## Purpose

Provide observability into AI task performance, recording metrics such as runtime, memory usage, and responsiveness.

The module now exposes a context manager that measures runtime and memory for each
workflow iteration and checks the results against the limits defined in
`execution-budget.yaml`.

## Prompt

Collect metrics during task execution and update the dashboards under `audits/performance/`. Alert when thresholds defined in `execution-budget.yaml` are exceeded.
