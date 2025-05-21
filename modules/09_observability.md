---
name: "Module_Observability"
version: "1.0"
description: "Monitors and reports performance metrics for Codex Web-Native operations."
inputs: ["audits/performance/", "src/"]
outputs: ["audits/performance/"]
dependencies: []
author: "AI"
last_updated: "2025-05-20"
status: "active"
---

# Observability Module

## Purpose

Provide observability into AI task performance, recording metrics such as runtime, memory usage, and responsiveness.

## Prompt

Collect metrics during task execution and update the dashboards under `audits/performance/`. Alert when thresholds defined in `execution-budget.yaml` are exceeded.
