---
name: "Module_RegressionSuite"
version: "1.0"
description: "Manages comprehensive regression testing to prevent performance and functional regressions."
inputs: ["tests/", "src/"]
outputs: ["tests/"]
dependencies: []
author: "AI"
last_updated: "2025-05-20"
marker: test
status: "active"
---

# Regression Test Suite Module

## Purpose

This module runs and maintains a suite of regression tests to catch regressions in functionality and performance.

## Prompt

Execute the full regression test suite using `pytest`. Ensure coverage meets the target specified in `execution-budget.yaml` and report results.
