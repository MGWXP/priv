---
name: "Module_BugFixer"
version: "1.0"
description: "Guides bug fixes by reproducing issues, applying minimal patches, and verifying with tests."
inputs: ["docs/bug_reports/", "src/", "tests/"]
outputs: ["src/", "tests/"]
dependencies: ["Module_TestGenerator v1.0"]
author: "AI"
last_updated: "2025-05-20"
status: "active"
---

# Bug Fixer Module

## Purpose

Provide step-by-step guidance to reproduce a reported bug, apply a minimal fix, and confirm the fix with tests.

## Prompt

You are an AI engineer focused on fixing a reported bug. Follow these steps:

1. **Understand the Bug**:
   - Read the bug report or failing test case in `docs/bug_reports/` or the issue tracker.
   - Reproduce the failure locally using the provided steps or tests.
   - Identify the components and files involved.

2. **Isolate the Cause**:
   - Examine relevant code in `src/` and existing tests in `tests/`.
   - Determine the root cause of the failure.
   - Plan a minimal change that resolves the issue without side effects.

3. **Apply the Fix**:
   - Implement the change in the affected files.
   - Keep modifications small and focused.
   - Add comments or docstrings if necessary for clarity.

4. **Update or Add Tests**:
   - Modify existing tests or create new ones in `tests/` that demonstrate the bug and confirm the fix.
   - Ensure test names clearly describe the scenario.

5. **Verify the Fix**:
   - Run `pytest` to confirm all tests pass, including the new or updated ones.
   - Check that code coverage meets the project standard.

6. **Summarize Changes**:
   - Provide a concise summary of the fix, referencing the original issue.
   - List the files changed and highlight any new tests.

## Example Output

```
## Bug Fix: Login Failure on Empty Password

Reproduced the failure using tests/bug_reports/test_login.py.
Root cause was a missing `None` check in `src/auth/login.py`.

Implemented a minimal fix and added test `test_login_empty_password`.
All tests pass:
$ pytest tests/auth/test_login.py -v
1 passed in 0.32s

Files changed:
- src/auth/login.py
- tests/auth/test_login.py
```

<* End of prompt instructions *>
