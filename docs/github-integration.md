# GitHub Integration Guide

This document provides guidelines for using GitHub with the Codex Web-Native framework, covering repository organization, workflows, and best practices for continuous integration.

## Repository Organization

The Codex Web-Native repository follows a structured taxonomy:

- **Layer 0: Configuration** - Root-level files (`README.md`, `AGENTS.md`, `execution-budget.yaml`)
- **Layer 1: Prompts and Modules** - `prompt-library/` and `modules/` directories
- **Layer 2: Code and Tests** - `src/` and `tests/` directories
- **Layer 3: Documentation** - `docs/` directory (including `adr/` for architecture decisions)
- **Layer 4: Audit & CI** - `audits/` and `.github/workflows/` directories

## GitHub Workflow

### Feature Development Workflow

1. **Create a Feature Branch**
   ```bash
   ./scripts/github_integration.py feature "Feature name"
   ```

2. **Implement Changes**
   - Follow the guidelines in `AGENTS.md`
   - Ensure all prompt modules have proper front-matter
   - Add tests for new functionality

3. **Verify Changes**
   ```bash
   ./run.sh
   ```

4. **Commit Changes**
   ```bash
   ./scripts/github_integration.py commit "[feat] Implement new feature"
   ```

5. **Generate Diff Report**
   ```bash
   ./scripts/github_integration.py diff
   ```

6. **Create Pull Request**
   ```bash
   ./scripts/github_integration.py pr "[feat] Implement new feature" "Detailed description"
   ```

### Coherence Markers

All commits must include a coherence marker prefix in square brackets:

- `[feat]` - New feature or functionality
- `[fix]` - Bug fix
- `[docs]` - Documentation changes only
- `[style]` - Formatting, whitespace changes
- `[refactor]` - Code restructuring without behavior change
- `[perf]` - Performance improvements
- `[test]` - Adding or modifying tests
- `[chore]` - Maintenance tasks, build changes

Example:
```
[feat] Add user authentication module
```

## Continuous Integration

The repository is configured with GitHub Actions workflows for continuous integration:

### Main CI Workflow

The `codex-web-native-ci.yml` workflow is triggered on:
- Push to the `main` branch
- Any pull request to the `main` branch
- Manual workflow dispatch

It performs the following steps:
1. **Validation**
   - Verifies module consistency
   - Validates prompt module schemas
   - Validates architecture decision records
   - Runs linting

2. **Testing**
   - Runs all tests with coverage reporting
   - Uploads coverage report as an artifact

3. **Semantic Diff Analysis** (for PRs)
   - Generates a diff report
   - Verifies coherence marker compliance
   - Uploads diff report as an artifact

4. **Dashboard Update** (when merged to main)
   - Updates the project dashboard with latest metrics
   - Commits the updated dashboard

### Prompt Validation Workflow

The `validate-prompts.yml` workflow is triggered when files in the prompt directories or registry are changed. It ensures:
- All prompt modules have required metadata
- Registry entries match module implementations
- Module dependencies are valid

## GitHub Integration Utils

The `scripts/github_integration.py` utility provides several commands:

- `verify` - Check if Git is properly configured
- `commit` - Stage and commit changes with coherence marker verification
- `push` - Push changes to GitHub
- `feature` - Create a feature branch
- `pr` - Create a pull request
- `diff` - Generate a diff report

## Branch Protection Rules

Configure the following branch protection rules for the `main` branch:

1. **Require Pull Request Reviews**
   - Require at least one approval
   - Dismiss stale pull request approvals when new commits are pushed

2. **Require Status Checks to Pass**
   - Require the `validate`, `test`, and `semantic-diff` jobs to pass

3. **Require Conversation Resolution**
   - All conversations must be resolved before merging

4. **Include Administrators**
   - Apply these rules to repository administrators

5. **Restrict Who Can Push**
   - Limit push access to administrators, requiring all others to use pull requests

## Best Practices

1. **Frequent Small Commits**
   - Make small, focused commits with clear coherence markers
   - Push changes regularly to benefit from continuous integration

2. **Comprehensive Testing**
   - Write tests for all new features and bug fixes
   - Aim for high code coverage (80%+)

3. **Semantic Versioning**
   - Use [SemVer](https://semver.org/) for releases
   - Tag releases with appropriate version numbers

4. **Descriptive PRs**
   - Use clear titles with proper coherence markers
   - Include detailed descriptions explaining the changes
   - Reference any issues being addressed

5. **Audit Trail**
   - Maintain the audit trail through proper diff reports
   - Update the history log when making significant changes

By following these guidelines, you'll ensure smooth collaboration and maintain the integrity of the Codex Web-Native framework.