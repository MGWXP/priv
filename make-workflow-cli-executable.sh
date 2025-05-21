#!/bin/bash
# Make the AI workflow CLI executable

chmod +x scripts/ai_workflow_cli.py

echo "✅ AI workflow CLI is now executable"
echo "Usage: ./scripts/ai_workflow_cli.py [command] [options]"
echo "Available commands:"
echo "  execute-chain       Execute a prompt chain"
echo "  execute-module      Execute a single prompt module"
echo "  analyze-diff        Analyze a diff between two files"
echo "  visualize-context   Visualize context graph"
echo "  monitor-performance Monitor performance metrics"
echo ""
echo "For more details, run: ./scripts/ai_workflow_cli.py --help"
