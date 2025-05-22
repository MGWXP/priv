---
name: "Module_BugFixer"
version: "1.0"
description: "Guides the AI in reproducing and fixing bugs with minimal changes."
inputs: ["tests/", "src/", "docs/issue_specs/"]
outputs: ["src/", "tests/"]
dependencies: ["Module_TestGenerator v1.0"]
author: "AI"
last_updated: "2025-05-21"
marker: "fix"
status: "active"
---

# Bug Fix Module

## Purpose

This module instructs the AI in addressing bugs reported via issue tickets or failing tests. It emphasizes reproducing the problem, applying the smallest viable change, and verifying the fix with tests.

## Prompt

You are an AI engineer tasked with fixing a bug in the project. Follow these steps:

1. **Understand the Issue**
   - Review the issue description or failing test output.
   - Identify the expected vs actual behavior.
   - Determine affected components and recent changes.

2. **Reproduce the Bug**
   - Run the failing test or replicate the steps outlined in the ticket.
   - Confirm you can reliably trigger the problem.

3. **Isolate the Cause**
   - Inspect relevant code paths and recent commits.
   - Narrow down the exact source of the bug.

4. **Apply the Fix**
   - Make the minimal code change necessary to resolve the issue.
   - Add comments or docstrings if the fix needs clarification.

5. **Write/Update Tests**
   - Modify existing tests or create new ones that prove the bug is fixed.
   - Ensure the test would fail without the fix and pass with it.

6. **Run Tests**
   - Execute `pytest` to confirm all tests pass.
   - Address any new failures that arise.

7. **Document the Fix**
   - Update relevant documentation or issue references.
   - Summarize what was changed and why.

8. **Generate Commit Message**
   - Craft a commit message beginning with `[fix]` describing the bug and resolution.
   - List files changed and reference the issue/ticket number if available.

## Example Output

```markdown
## Bug Fix: Incorrect Token Expiration

- Reproduced failing test in `tests/auth/test_tokens.py::test_token_expiry`.
- Cause: Expiration time calculated in minutes instead of seconds.
- Fixed by adjusting `expiry_seconds` multiplication in `src/auth/tokens.py`.
- Added regression test `test_token_expiry_correct`.
- All tests pass (26 total).
```

<* End of prompt instructions *>
