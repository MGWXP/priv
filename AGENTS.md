# AI Agent Guidelines

## Project Overview

This repository implements a Codex Web-Native application that follows the standardized schema for AI-assisted development. It is designed to maximize compatibility with ChatGPT Codex's multi-agent, asynchronous workflow within the browser-based environment.

## Repository Structure

- `/` (Project Root)
  - `AGENTS.md`: This file - Project-level AI orchestration guidelines
  - `README.md`: Human-readable project overview
  - `prompt-library/`: Modular prompt definitions
  - `prompt-registry.yaml`: Index of prompt modules, versions, and metadata
  - `modules/`: Core modules for parallel execution, observability, and governance
  - `workflows/`: CI/CD and governance workflows
  - `audits/`: Logs, diffs, and performance audit data
    - `diffs/`: Recorded semantic diffs for each iteration or PR
    - `performance/`: Performance metrics and benchmarks
    - `dashboards/`: Markdown-based visualization dashboards
    - `analysis/`: Semantic diff analysis reports
    - `history.log.md`: Chronological log of AI agent actions/outputs
  - `execution-budget.yaml`: Resource limits and performance targets
  - `tests/`: Test suite for validating implementations
  - `src/`: Source code of the application
  - `docs/`: Documentation for the project

## Development Practices

### Coding Standards

- **Python**: Follow PEP 8 style guide
  - Use snake_case for functions and variable names
  - Use CamelCase for class names
  - 4 spaces for indentation (no tabs)
  - Maximum line length of 88 characters (Black formatter compatible)

- **JavaScript/TypeScript**:
  - Use camelCase for functions and variable names
  - Use PascalCase for class and component names
  - 2 spaces for indentation
  - Semicolons at the end of statements
  - Prefer const over let, avoid var

- **Markdown**:
  - Use ATX headings (# for headings, not underlines)
  - Proper nesting of headings (# → ## → ###)
  - Include front-matter in prompt modules

### Coherence Marker System

- Every commit must have a coherence marker prefix in square brackets
- Valid markers: [feat], [fix], [docs], [style], [refactor], [perf], [test], [chore]
- Marker must match the nature of the change (enforced by CI)
- Include descriptive message after the marker

### Documentation Requirements

- Every function and class must include docstrings
- README.md must be kept updated with new features
- All prompts must include their purpose, inputs, and outputs clearly
- Update history.log.md with details of all significant changes

### Performance Requirements

- All changes must adhere to performance budgets in execution-budget.yaml
- UI operations must maintain INP < 200ms
- Test suite execution must complete within budget
- Resource usage must stay within defined limits

## Testing Instructions

- **Run tests**: Execute `pytest` in the repository root
- **Run linting**: Use `flake8` for Python, `eslint` for JavaScript
- **Run formatting**: Use `black` for Python, `prettier` for JavaScript

## Build/Run Instructions

- Setup virtual environment: `python -m venv venv`
- Activate environment: `. venv/bin/activate` (Unix) or `venv\Scripts\activate` (Windows)
- Install dependencies: `pip install -r requirements.txt`
- Run application: `python src/main.py`

## Agent Roles

### FeatureBuilder
Responsible for implementing new features based on specifications. Works primarily with code in the `src/` directory and adds appropriate tests. Uses Module_TaskA prompt.

### TestWriter
Focuses on creating comprehensive test suites for existing features. Ensures test coverage meets project standards. Uses Module_TestGenerator prompt.

### Refactor
Improves existing code without changing functionality. Focuses on performance, readability, and maintainability. Uses Module_Refactor prompt.

### DocumentationWriter
Creates and updates documentation to match current implementations. Ensures README, docstrings, and other docs stay in sync with code. Uses Module_DocWriter prompt.

### DiffAnalyzer
Reviews changes to ensure they meet project standards and implement requirements correctly. Works with the audit system to track changes over time. Uses Module_DiffAnalyzer prompt.

### BugFixer
Replicates and resolves reported bugs with minimal changes. Uses Module_BugFixer and ensures tests reflect the fix. Typically run via the BugFixCycle chain.

### ParallelExecutor
Manages parallel task execution and resource allocation. Ensures that multiple AI agents can work simultaneously without conflicts. Uses Module_ParallelAsync.

### ObservabilityManager
Tracks performance metrics and generates dashboards. Ensures the project meets performance targets. Uses Module_Observability.

## Constraints

- Never add or edit license files (LICENSE, LICENSE.md, etc.)
- Do not modify files in the prompt-library/ without explicit instruction
- Ensure all tests pass before considering a task complete
- Always create appropriate documentation for new features
- Keep the audit trail updated with meaningful diffs and logs
- Follow the semantic linking rules when creating new components or modules
- Only create what's needed - avoid speculative or unused code
- Adhere to the execution budget constraints defined in execution-budget.yaml
- Never bypass coherence marker validation

## Parallel Execution

- Coordinate multiple AI tasks via Module_ParallelAsync
- Use file-level isolation to prevent conflicts
- Respect max_parallel_tasks setting in execution-budget.yaml
- Report progress in sidebar only to maintain UI responsiveness
- Generate detailed logs in audits/parallel_execution.log.md

## Taxonomy Layers

This repository follows a strict taxonomy to organize artifacts:

- Layer 0: Project configuration (README.md, AGENTS.md, execution-budget.yaml)
- Layer 1: AI prompts and modules (prompt-library/, modules/)
- Layer 2: Source code and tests (src/, tests/)
- Layer 3: Documentation (docs/)
- Layer 4: Audit and governance (audits/, workflows/)

Follow this taxonomy when organizing new files and components.
