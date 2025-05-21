# Codex Web-Native Repository

## Overview

This repository implements a modern application development workflow optimized for use with the ChatGPT Codex Web Interface. It provides a structured, transparent environment where AI agents and human developers can collaborate efficiently in building and maintaining software.

## Key Features

- Modular prompt system with versioning and lifecycle management
- Transparent audit trail of all AI contributions
- Parallel task support and semantic prompt chaining
- Comprehensive testing and performance tracking
- AI-friendly project structure with clear guidance
- Lightweight workflow orchestration utilities (CLI-driven)

## Getting Started

1. Review `AGENTS.md` to understand the AI orchestration guidelines
2. Explore the `prompt-library/` to see available AI instruction modules
3. Check `prompt-registry.yaml` for the index of all prompt modules
4. Run tests with `pytest` to verify everything is working
5. Ensure the `ai_workflow` package is installed or available on your `PYTHONPATH`.

## Development Workflow

This project follows the Iterative Deep Research Loop:

1. **Re-ingest**: The AI reviews the current state of the codebase
2. **Focus**: Define specific task goals and select appropriate prompt modules
3. **Synthesize**: Execute the task and create/modify code
4. **Commit**: Integrate changes and record them in the audit trail
5. **Refine**: Review results and plan improvements

Each iteration (LOOP) is documented in `audits/` with performance metrics and semantic diffs.

## Using the AI Workflow System

### Running Prompt Chains

The repository includes a CLI utility for working with the AI workflow system:

```bash
# Make the CLI executable
./make-workflow-cli-executable.sh

# Execute a prompt chain
./scripts/ai_workflow_cli.py execute-chain FeatureDevCycle --context '{"feature": "user-authentication"}'

# Execute a single module
./scripts/ai_workflow_cli.py execute-module Module_TaskA
```

### Parallel Execution

For parallel execution of tasks, use the ParallelFeatureDevCycle chain:

```bash
./scripts/ai_workflow_cli.py execute-chain ParallelFeatureDevCycle
```

This utilizes the Module_ParallelAsync to coordinate multiple tasks running concurrently.

### Analyzing Diffs

To analyze semantic diffs and verify coherence marker compliance:

```bash
./scripts/ai_workflow_cli.py analyze-diff --old-file src/old.py --new-file src/new.py --marker feat
```

### Monitoring Performance

To update performance metrics and generate dashboards:

```bash
# Update metrics for the current iteration
./scripts/ai_workflow_cli.py monitor-performance --update --metrics '{"test_count": 42, "code_coverage": 85}'

# Generate performance dashboard
./scripts/ai_workflow_cli.py monitor-performance --generate-dashboard
```

### Visualizing Context Graphs

To visualize the relationships between modules and their input/output contexts:

```bash
./scripts/ai_workflow_cli.py visualize-context --format html
```

## Project Structure

```
/  (Project Root)
├── AGENTS.md                   # Project-level AI orchestration guidelines
├── README.md                   # This file - human-readable project overview
├── scripts/ai_workflow_cli.py  # CLI utility for AI workflow
├── execution-budget.yaml       # Resource limits and performance targets
├── prompt-chains.graphml       # Visual representation of prompt relationships
├── prompt-registry.yaml        # Index of prompt modules, versions, and metadata
├── module_taskA.v1.md          # Example prompt module
├── module_test_generator.v1.md # Example prompt module
├── scripts/                    # Utility scripts
├── tools/                      # NLU tools and helpers
├── docs/                       # Documentation
├── run.sh                      # Launch script
├── src/                        # Application source code
│   ├── app.py                  # Application entry point
│   ├── auth/                   # Authentication package
│   └── ai_workflow/            # AI workflow modules
└── (additional files and stubs)
```

## Contributing

To contribute to this project:

1. Review `AGENTS.md` for guidelines and conventions
2. Use appropriate prompts from the prompt library for AI assistance
3. Ensure all tests pass before submitting changes
4. Update the audit trail with meaningful diffs and logs
5. Follow semantic linking rules when creating new components
