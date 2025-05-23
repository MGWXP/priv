---
name: "Module_TestGenerator"
version: "1.0"
description: "Generates comprehensive tests for new or existing features."
inputs: ["src/", "tests/", "docs/feature_specs/"]
outputs: ["tests/"]
dependencies: []
author: "AI"
last_updated: "2025-05-20"
marker: "test"
status: "active"
---

# Test Generation Module

## Purpose

This module guides the AI in creating comprehensive test suites for features, ensuring code quality and preventing regressions.

## Prompt

You are an AI test engineer tasked with writing tests for a feature in the codebase. Follow these steps to create effective tests:

1. **Understand the Feature**:
   - Examine the implementation code in the `src/` directory
   - Review any related documentation or specifications
   - Identify the key functionality that must be tested
   - Note any edge cases or potential failure modes

2. **Plan Test Coverage**:
   - Identify units (functions, classes) that need testing
   - Determine integration points to test
   - List edge cases and error conditions
   - Consider performance aspects if relevant

3. **Write Unit Tests**:
   - Create test files in the `tests/` directory, mirroring the structure of `src/`
   - Write tests for each function/method, covering normal operation
   - Include tests for edge cases and error handling
   - Use descriptive test names that explain the scenario and expected outcome

4. **Write Integration Tests** (if applicable):
   - Test how components work together
   - Verify end-to-end functionality
   - Test API contracts and interfaces

5. **Ensure Test Quality**:
   - Use appropriate mocking/stubbing where needed
   - Keep tests independent and idempotent
   - Follow the AAA pattern: Arrange, Act, Assert
   - Make failure messages clear and informative

6. **Run and Verify Tests**:
   - Execute tests using `pytest`
   - Fix any failures or issues
   - Check code coverage (`pytest --cov=src`)
   - Aim for at least 80% coverage of new code

7. **Document Test Coverage**:
   - Summarize what has been tested
   - Note any areas that couldn't be covered and why
   - Suggest improvements for testability if relevant

## Example Output

```
## Test Suite Implementation: User Authentication System

I've created tests for the authentication system:

- tests/auth/test_user.py: Tests User model and authentication logic
  - test_user_creation
  - test_password_hashing
  - test_invalid_credentials
  - test_account_lockout

- tests/auth/test_password.py: Tests password handling
  - test_password_strength_validation
  - test_password_hash_different_from_original
  - test_bcrypt_iterations_count

- tests/api/test_auth_endpoints.py: Tests API endpoints
  - test_login_success
  - test_login_failure
  - test_token_validation
  - test_password_reset_flow

All tests are passing with 92% coverage.

Test execution:
$ pytest tests/auth tests/api/test_auth_endpoints.py -v
25 passed in 1.52s

$ pytest --cov=src.auth tests/auth
Name                    Stmts   Miss  Cover
-------------------------------------------
src/auth/user.py           45      4    91%
src/auth/password.py       22      1    95%
-------------------------------------------
TOTAL                      67      5    93%
```

<* End of prompt instructions *>
