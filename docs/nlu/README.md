# NLU Documentation Pipeline

## Overview

This documentation pipeline provides automated Natural Language Understanding (NLU) capabilities for the Codex Web-Native repository. The pipeline extracts structured metadata from documentation, builds semantic relationships between documents, and generates insights to improve documentation quality and completeness.

## Architecture

The NLU pipeline consists of the following components:

1. **Document Processor**: Extracts metadata and relationships from repository files
2. **Document Embedder**: Generates semantic vector embeddings for similarity analysis
3. **Document Synthesizer**: Creates reports and visualizations based on document analysis
4. **Documentation Validator**: Verifies documentation completeness against criteria

## Key Features

- **Semantic Understanding**: Analyzes document content to extract meaning, not just keywords
- **Cross-Document Relationships**: Identifies connections between different documents
- **Documentation Gap Analysis**: Automatically detects missing or incomplete documentation
- **Visualization**: Generates knowledge graphs for visual exploration of relationships
- **CI/CD Integration**: Runs automatically on repository changes

## Usage

The NLU pipeline is automatically executed by the GitHub Actions workflow on repository changes. You can also run it manually:

```bash
# Process documents and extract metadata
python tools/nlu/processor.py --base-path . --output-dir docs/nlu

# Generate embeddings
python tools/nlu/embedder.py --registry docs/nlu/document_registry.json --output docs/nlu/embeddings/document_embeddings.json

# Generate reports
python tools/nlu/synthesizer.py --registry docs/nlu/document_registry.json --relationships docs/nlu/relationship_map.json --output-dir docs/synthesis/reports

# Validate documentation
python tools/nlu/validator.py --registry docs/nlu/document_registry.json --criteria docs/nlu/schemas/completeness_criteria.yaml --report docs/synthesis/reports/validation_report.md
```

## Taxonomy Integration

The NLU pipeline integrates with the repository's existing taxonomy layers:

- **Layer 0 (Config)**: Validates core configuration files
- **Layer 1 (Prompts)**: Analyzes prompt modules for completeness
- **Layer 2 (Code)**: Checks code documentation and test coverage
- **Layer 3 (Docs)**: Ensures documentation completeness
- **Layer 4 (Audit)**: Integrates with existing audit mechanisms

## Reports

The NLU pipeline generates the following reports:

- **System Overview**: High-level summary of repository structure and relationships
- **Documentation Gaps**: Analysis of missing or incomplete documentation
- **Cross-Reference Index**: Detailed cross-references between documents
- **Knowledge Graph**: Visual representation of document relationships

## Configuration

The pipeline behavior can be customized through the following configuration files:

- `docs/nlu/schemas/processor_config.yaml`: Document processing rules
- `docs/nlu/schemas/completeness_criteria.yaml`: Documentation validation criteria