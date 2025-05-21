---
name: "Module_Observability"
version: "1.1"
description: "Monitors runtime and memory metrics for Codex Web-Native operations."
inputs: ["audits/performance/", "src/"]
outputs: ["audits/performance/"]
dependencies: []
author: "AI"
last_updated: "2025-05-21"
status: "active"
---

# Observability Module

## Purpose

Provide observability into AI task performance, recording metrics such as runtime, memory usage, and responsiveness.

## Prompt

Collect runtime and peak memory metrics during task execution and update the
dashboards under `audits/performance/`. Alert when thresholds defined in
`execution-budget.yaml` are exceeded.
