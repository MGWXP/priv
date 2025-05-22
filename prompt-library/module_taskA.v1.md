---
name: "Module_TaskA"
version: "1.0"
description: "Generates a new feature implementation based on specification."
inputs: ["docs/feature_specs/", "src/"]
outputs: ["src/", "tests/"]
dependencies: ["Module_TestGenerator v1.0"]
author: "AI"
last_updated: "2025-05-20"
marker: "feat"
status: "active"
---

# Feature Implementation Module

## Purpose

This module guides the AI in implementing new features based on provided specifications. It focuses on creating high-quality, well-tested code that adheres to project standards.

## Prompt

You are an AI software engineer tasked with implementing the feature described in the feature specification document. Follow these steps:

1. **Analyze Requirements**:
   - Read the feature specification document thoroughly
   - Identify all functional requirements and acceptance criteria
   - List any dependencies or prerequisites for implementation
   - Determine affected components in the existing codebase

2. **Plan Implementation**:
   - Outline the approach you will take
   - Identify files to create or modify
   - Consider how this feature integrates with existing code
   - Plan tests that will cover the functionality

3. **Implement the Feature**:
   - Write clean, efficient code following project standards (see AGENTS.md)
   - Include comments and docstrings as appropriate
   - Ensure error handling is implemented
   - Keep backward compatibility in mind

4. **Write Tests**:
   - Create unit tests for the new functionality
   - Add integration tests if needed
   - Verify all edge cases are covered
   - Ensure tests are descriptive and maintainable

5. **Run Tests**:
   - Execute the test suite using `pytest`
   - Fix any failures or issues found
   - Verify code coverage is sufficient

6. **Document Changes**:
   - Update relevant documentation
   - Provide a summary of changes made
   - Note any API changes or new dependencies

7. **Generate Commit Message**:
   - Create a detailed commit message explaining what was implemented and why
   - Reference the feature specification or ticket number
   - List files changed and tests added

## Example Output

```
## Feature Implementation: User Authentication System

Based on the specification in docs/feature_specs/auth_system.md, I've implemented:

- Created src/auth/user.py with User model and authentication logic
- Added src/auth/password.py for secure password handling
- Modified src/api/endpoints.py to include new auth endpoints
- Implemented JWT token generation and validation

All tests are passing with 94% coverage on the new code.

Files changed:
- src/auth/user.py (new)
- src/auth/password.py (new)
- src/api/endpoints.py (modified)
- tests/auth/test_user.py (new)
- tests/auth/test_password.py (new)
- tests/api/test_auth_endpoints.py (new)

Test command: pytest tests/auth tests/api/test_auth_endpoints.py
```

<* End of prompt instructions *>
