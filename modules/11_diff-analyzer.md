---
name: "Module_DiffAnalyzerV2"
version: "1.0"
description: "Analyzes code changes to ensure coherence marker compliance and perform semantic diff verification."
inputs: ["audits/diffs/"]
outputs: ["audits/diffs/"]
dependencies: []
author: "AI"
last_updated: "2025-05-20"
status: "active"
---

# Diff Analyzer V2 Module

## Purpose

Provide enhanced analysis of code diffs to verify coherence marker compliance and highlight semantic changes.

## Prompt

Analyze provided diffs, ensure commit messages match the changes, and record findings in the audits directory.
