# Documentation CLI Tool Guide

This guide explains how to use the Documentation CLI Tool to interact with the NLU documentation pipeline, generate reports, search documentation, and analyze the impact of changes.

## Installation

1. Ensure the NLU documentation pipeline is installed:
   ```bash
   # Make the CLI tool executable
   chmod +x tools/nlu/docs-cli

   # Create a symlink in a directory that's in your PATH (optional)
   ln -s $(pwd)/tools/nlu/docs-cli /usr/local/bin/docs-cli
   ```

## Commands Overview

The Documentation CLI Tool provides the following commands:

- `process`: Process repository and extract metadata
- `embed`: Generate embeddings for repository documents
- `synthesize`: Generate synthesis reports
- `validate`: Validate documentation completeness
- `dashboard`: Generate documentation dashboard
- `search`: Search documentation semantically
- `impact`: Analyze impact of changes to documentation
- `run-all`: Run the entire documentation pipeline
- `open-dashboard`: Open the documentation dashboard in the default browser

## Usage Examples

### Run the Entire Pipeline

Process the entire repository, generate embeddings, synthesis reports, validate documentation, and create a dashboard:

```bash
./tools/nlu/docs-cli run-all
```

### Process Repository

Extract metadata and build relationships between documents:

```bash
./tools/nlu/docs-cli process

# Specify custom configuration
./tools/nlu/docs-cli process --config custom_config.yaml --output-dir custom_output/
```

### Generate Embeddings

Create vector embeddings for all documents in the repository:

```bash
./tools/nlu/docs-cli embed

# Specify custom model
./tools/nlu/docs-cli embed --model different-embedding-model
```

### Generate Synthesis Reports

Create reports based on document analysis:

```bash
./tools/nlu/docs-cli synthesize
```

### Validate Documentation

Check documentation completeness against criteria:

```bash
./tools/nlu/docs-cli validate
```

### Generate Dashboard

Create a documentation health dashboard:

```bash
./tools/nlu/docs-cli dashboard
```

### Search Documentation

Search the repository documentation semantically:

```bash
# Interactive search mode
./tools/nlu/docs-cli search

# Single query search
./tools/nlu/docs-cli search --query "prompt modules"

# Filter by layer
./tools/nlu/docs-cli search --query "configuration" --layer config

# Output results as JSON
./tools/nlu/docs-cli search --query "testing" --json
```

### Analyze Impact of Changes

Analyze the potential impact of changing specific documents:

```bash
# Analyze impact of changes to README.md
./tools/nlu/docs-cli impact --documents README.md

# Analyze impact of changes to multiple documents
./tools/nlu/docs-cli impact --documents README.md AGENTS.md execution-budget.yaml

# Specify depth of impact analysis
./tools/nlu/docs-cli impact --documents README.md --max-depth 3

# Save impact report to file
./tools/nlu/docs-cli impact --documents README.md --output impact_report.md
```

### Open Dashboard

Open the documentation dashboard in your default browser:

```bash
./tools/nlu/docs-cli open-dashboard
```

## Default File Paths

The CLI tool uses default paths for its input and output files:

- Document Registry: `docs/nlu/document_registry.json`
- Relationship Map: `docs/nlu/relationship_map.json`
- Embeddings: `docs/nlu/embeddings/document_embeddings.json`
- Validation Report: `docs/synthesis/reports/validation_report.md`
- Dashboard: `docs/synthesis/reports/documentation_dashboard.md`
- Processor Config: `docs/nlu/schemas/processor_config.yaml`
- Completeness Criteria: `docs/nlu/schemas/completeness_criteria.yaml`

You can specify custom paths for any of these files using the appropriate command-line arguments.

## Integration with Development Workflow

### Pre-Commit Hook

You can set up a pre-commit hook to validate documentation before committing changes:

```bash
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
./tools/nlu/docs-cli validate
if [ $? -ne 0 ]; then
  echo "Documentation validation failed. Please fix issues before committing."
  exit 1
fi
EOF
chmod +x .git/hooks/pre-commit
```

### CI/CD Integration

The NLU documentation pipeline can be integrated into your CI/CD workflow using the `.github/workflows/nlu-pipeline.yml` file, which automatically runs the pipeline on repository changes.

## Troubleshooting

### Missing Dependencies

If you encounter errors about missing dependencies, ensure all required Python packages are installed:

```bash
pip install pyyaml numpy networkx matplotlib
```

### Document Registry Not Found

If you see "Document registry not found" errors, run the `process` command first:

```bash
./tools/nlu/docs-cli process
```

### Embeddings Not Found

If you see "Embeddings not found" errors, run the `embed` command:

```bash
./tools/nlu/docs-cli embed
```

### Permission Denied

If you encounter permission denied errors when running the CLI tool, make it executable:

```bash
chmod +x tools/nlu/docs-cli
```

## Further Reading

- [NLU Documentation Pipeline Overview](../README.md)
- [Integration Guide](integration_guide.md)
- [Knowledge Graph Visualization](../synthesis/visualizations/README.md)
