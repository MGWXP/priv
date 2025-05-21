---
name: "Module_RegressionSuite"
version: "1.1"
description: "Manages comprehensive regression testing to prevent performance and functional regressions."
inputs: ["tests/", "src/"]
outputs: ["tests/"]
dependencies: []
author: "AI"
last_updated: "2025-05-20"
status: "active"
---

# Regression Test Suite Module

## Purpose

This module runs and maintains a suite of regression tests to catch regressions in functionality and performance.

## Prompt

Execute the full regression test suite using `pytest`. Parse the output to determine success or failure and return the summary. If any tests fail, trigger the appropriate fix cycle before proceeding. Integrate with Observability and DiffAnalyzer modules to run automatically after risky changes or major refactors.
