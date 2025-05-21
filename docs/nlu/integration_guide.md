# NLU Documentation Pipeline Integration Guide

## Overview

This guide explains how to integrate the NLU Documentation Pipeline into your development workflow and interpret its analysis results. The pipeline provides automated documentation quality assessment, relationship mapping, and visualization tools to ensure comprehensive documentation coverage across the repository.

## 🔄 Pipeline Integration Points

### 1. CI/CD Integration

The NLU Documentation Pipeline runs automatically on GitHub Actions when changes are pushed to the repository. You can also trigger it manually:

- **Automatic Trigger**: Occurs on any push to `main` branch that affects documentation, code, or configuration files
- **Manual Trigger**: Available in GitHub Actions tab under "NLU Documentation Pipeline" workflow

### 2. Pre-Commit Integration

To analyze documentation locally before committing:

```bash
# Setup pre-commit hook (one-time)
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
python tools/nlu/processor.py --base-path . --output-dir docs/nlu
python tools/nlu/validator.py --registry docs/nlu/document_registry.json --criteria docs/nlu/schemas/completeness_criteria.yaml --report docs/synthesis/reports/validation_report.md
EOF
chmod +x .git/hooks/pre-commit
```

## 📈 Interpreting Analysis Results

### Documentation Validation Report

The validation report (`docs/synthesis/reports/validation_report.md`) provides:

- **Documentation Coverage**: Percentage of source files and prompt modules with complete documentation
- **Test Coverage**: Percentage of source files with associated tests
- **Issue Reports**: Lists of specific documentation issues across different components
- **Recommendations**: Prioritized list of suggested improvements

### System Overview

The system overview report (`docs/synthesis/reports/system_overview.md`) includes:

- **Repository Statistics**: Document counts by taxonomy layer
- **Relationship Statistics**: Connection counts by relationship type
- **Key Documents**: Most referenced documents in the codebase
- **Potential Issues**: Orphaned documents with no connections

### Knowledge Graph

The knowledge graph visualization (`docs/synthesis/visualizations/knowledge_graph_viewer.html`) allows you to:

- **Filter by Layer**: Focus on specific taxonomy layers (config, prompts, code, docs, audit)
- **Filter by Relationship**: View specific relationship types (references, implements, tests, documents)
- **Explore Connections**: Click on nodes to see detailed relationships for each document
- **Navigate Structure**: Understand the overall repository architecture visually

### Cross-Reference Index

The cross-reference index (`docs/synthesis/reports/cross_reference_index.md`) provides:

- **Detailed Directory**: Every document organized by taxonomy layer
- **Relationship Listings**: All connections between documents, grouped by relationship type
- **Search Support**: Easily searchable format for finding relationships

## 🔖 Documentation Quality Standards

The pipeline validates documentation against the following standards:

### For Core Configuration Files:
- README.md: Must include overview, purpose, and layers sections
- AGENTS.md: Must include standards, roles, and constraints sections
- execution-budget.yaml: Must include version, task_limits, and performance_budgets

### For Prompt Modules:
- Required front matter: name, version, marker, description, inputs, outputs, status
- Recommended front matter: dependencies, author, last_updated
- Required sections: purpose, prompt
- Recommended sections: example

### For Code Files:
- Python: Required docstrings and type hints; recommended tests and examples
- JavaScript: Required JSDoc; recommended tests and TypeScript

## 💡 Improving Documentation Quality

To improve documentation quality based on pipeline reports:

1. **Address Critical Gaps First**: Focus on missing required content
2. **Improve Relationship Coverage**: Connect orphaned documents to related components
3. **Enhance Module Metadata**: Ensure prompt modules have complete front-matter
4. **Add Missing Tests**: Write tests for untested code files
5. **Follow Layer Guidelines**: Organize documentation according to the taxonomy layer structure

## 🛠️ Customizing the Pipeline

The pipeline can be customized by modifying these configuration files:

- `docs/nlu/schemas/processor_config.yaml`: Extraction rules and taxonomy structure
- `docs/nlu/schemas/completeness_criteria.yaml`: Documentation quality criteria

The key components can also be extended:

- `tools/nlu/processor.py`: Document processing and relationship extraction
- `tools/nlu/embedder.py`: Semantic embedding generation
- `tools/nlu/synthesizer.py`: Report generation
- `tools/nlu/validator.py`: Documentation validation

## 🏆 Best Practices

1. **Write Documentation As You Code**: Maintain documentation alongside code changes
2. **Include Relationship References**: Cross-reference related documents explicitly
3. **Use Consistent Taxonomy**: Follow the established layer structure
4. **Review Validation Reports**: Check documentation coverage after each significant change
5. **Visualize Impacts**: Use the knowledge graph to understand how changes affect documentation structure