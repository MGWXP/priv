---
name: "Module_DiffAnalyzerV2"
version: "1.1"
description: "Analyzes code changes to ensure coherence marker compliance and perform semantic diff verification."
inputs: ["audits/diffs/"]
outputs: ["audits/diffs/"]
dependencies: []
author: "AI"
last_updated: "2025-05-21"
marker: chore
status: "active"
---

# Diff Analyzer V2 Module

## Purpose

Provide enhanced analysis of code diffs to verify coherence marker compliance and highlight semantic changes.

## Prompt
Analyze the provided diff and confirm that the changes align with the commit's
coherence marker and description.

### Checklist

1. **Parse Diff**
   - Count additions and deletions per file.
   - Classify files as documentation, tests, or code.
   - Detect trailing whitespace and missing docstrings.

2. **Verify Marker Alignment**
   - `[feat]` → net additions should outnumber deletions and a test must be present.
   - `[fix]` → requires a test file that demonstrates the fix.
   - `[docs]` → only documentation files may be modified.
   - `[test]` → only test files should change.

3. **Check Coding Standards**
   - New Python functions or classes must include docstrings.
   - Flag obvious style issues such as trailing whitespace or large commented blocks.

4. **Produce Verdict**
   - Output a summary stating whether the diff matches the marker.
   - Save a YAML report in `audits/diffs/` with totals and the compliance status.

Record any mismatches as warnings so CI can fail when the changeset does not respect the coherence rules.
