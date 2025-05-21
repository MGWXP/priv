#!/usr/bin/env python3
"""
AI Workflow CLI Utility

Command-line interface for interacting with the AI workflow components
of the Codex Web-Native repository.
"""

import os
import sys
import argparse
import json
import yaml
from datetime import datetime

# Add the repository root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from ai_workflow import WorkflowOrchestrator, ContextGraphManager, SemanticDiffAnalyzer, PerformanceMonitor
except ImportError:
    print("Error: Unable to import AI workflow modules. Make sure you're running this script from the repository root.")
    sys.exit(1)

def execute_chain(args):
    """Execute a prompt chain."""
    orchestrator = WorkflowOrchestrator()
    
    # Parse context if provided
    context = {}
    if args.context:
        try:
            context = json.loads(args.context)
        except json.JSONDecodeError:
            print("Error: Invalid JSON context. Please provide context as a valid JSON string.")
            sys.exit(1)
            
    print(f"Executing chain: {args.chain}")
    result = orchestrator.execute_chain(args.chain, context)
    
    print("\nExecution Result:")
    print(json.dumps(result, indent=2))
    
    # Export context graph if requested
    if args.export_graph:
        graph_path = orchestrator.export_context_graph()
        print(f"Context graph exported to: {graph_path}")

def execute_module(args):
    """Execute a single prompt module."""
    orchestrator = WorkflowOrchestrator()
    
    # Parse context if provided
    context = {}
    if args.context:
        try:
            context = json.loads(args.context)
        except json.JSONDecodeError:
            print("Error: Invalid JSON context. Please provide context as a valid JSON string.")
            sys.exit(1)
            
    print(f"Executing module: {args.module}")
    result = orchestrator.execute_module(args.module, context)
    
    print("\nExecution Result:")
    print(json.dumps(result, indent=2))
    
    # Export context graph if requested
    if args.export_graph:
        graph_path = orchestrator.export_context_graph()
        print(f"Context graph exported to: {graph_path}")

def analyze_diff(args):
    """Analyze a diff between two files or content."""
    analyzer = SemanticDiffAnalyzer()
    
    # Get file content
    if args.old_file and args.new_file:
        try:
            with open(args.old_file, 'r') as f:
                old_content = f.read()
            with open(args.new_file, 'r') as f:
                new_content = f.read()
        except FileNotFoundError as e:
            print(f"Error: File not found - {e}")
            sys.exit(1)
    elif args.old_content and args.new_content:
        old_content = args.old_content
        new_content = args.new_content
    else:
        print("Error: You must provide either file paths or content strings.")
        sys.exit(1)
        
    # Set file path for analysis
    file_path = args.file_path or args.old_file or "unknown.file"
    
    # Analyze diff
    analysis = analyzer.analyze_file_diff(old_content, new_content, file_path)
    
    # Verify marker compliance
    verification = analyzer.verify_marker_compliance([analysis], args.marker)
    
    # Generate report
    report = analyzer.generate_diff_report([analysis], args.marker, verification, args.iteration)
    
    print(f"Diff analysis report generated: {report['report_path']}")
    print(f"Marker compliance: {'✅ Yes' if report['compliant'] else '❌ No'}")
    
    if not report['compliant']:
        print(f"Reason: {verification['reason']}")
        
    # Print summary
    print("\nSummary of changes:")
    print(f"  Files: {report['files_changed']}")
    print(f"  Additions: {report['additions']}")
    print(f"  Deletions: {report['deletions']}")

def visualize_context(args):
    """Visualize context graph."""
    manager = ContextGraphManager()
    
    # Load runtime context if provided
    if args.runtime_context:
        try:
            with open(args.runtime_context, 'r') as f:
                runtime_context = json.load(f)
            manager.update_from_runtime(runtime_context)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading runtime context: {e}")
            sys.exit(1)
            
    # Generate outputs
    if args.format == 'json':
        output_path = manager.export_graph_json(args.output)
        print(f"Context graph exported to JSON: {output_path}")
    elif args.format == 'markdown':
        output_path = manager.export_markdown_summary(args.output)
        print(f"Context graph summary exported to Markdown: {output_path}")
    elif args.format == 'html':
        output_path = manager.generate_html_visualization(args.output)
        print(f"Context graph visualization exported to HTML: {output_path}")
    else:
        print(f"Error: Unsupported format '{args.format}'")
        sys.exit(1)

def monitor_performance(args):
    """Monitor performance metrics."""
    monitor = PerformanceMonitor()
    
    if args.update:
        # Parse metrics if provided
        metrics = {}
        if args.metrics:
            try:
                metrics = json.loads(args.metrics)
            except json.JSONDecodeError:
                print("Error: Invalid JSON metrics. Please provide metrics as a valid JSON string.")
                sys.exit(1)
                
        # Load metrics from file if provided
        if args.metrics_file:
            try:
                with open(args.metrics_file, 'r') as f:
                    file_metrics = json.load(f)
                metrics.update(file_metrics)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error loading metrics file: {e}")
                sys.exit(1)
                
        # Update metrics for the specified iteration
        success = monitor.update_iteration_metrics(args.iteration, metrics)
        if success:
            print(f"Metrics updated for iteration {args.iteration}")
        else:
            print("Error updating metrics")
            sys.exit(1)
            
        # Check compliance if requested
        if args.check_compliance:
            compliance = monitor.check_budget_compliance(metrics)
            print(f"Compliance status: {'✅ Compliant' if compliance['compliant'] else '❌ Non-Compliant'}")
            
            if compliance["violations"]:
                print("\nViolations:")
                for violation in compliance["violations"]:
                    print(f"- {violation['message']}")
    
    if args.generate_dashboard:
        dashboard_files = monitor.generate_performance_dashboard()
        print(f"Dashboard generated with {len(dashboard_files)} files:")
        for file_path in dashboard_files:
            print(f"- {file_path}")

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="AI Workflow CLI Utility")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Execute chain command
    chain_parser = subparsers.add_parser("execute-chain", help="Execute a prompt chain")
    chain_parser.add_argument("chain", help="Name of the chain to execute")
    chain_parser.add_argument("--context", help="JSON string with context data")
    chain_parser.add_argument("--export-graph", action="store_true", help="Export context graph after execution")
    
    # Execute module command
    module_parser = subparsers.add_parser("execute-module", help="Execute a single prompt module")
    module_parser.add_argument("module", help="Name of the module to execute")
    module_parser.add_argument("--context", help="JSON string with context data")
    module_parser.add_argument("--export-graph", action="store_true", help="Export context graph after execution")
    
    # Analyze diff command
    diff_parser = subparsers.add_parser("analyze-diff", help="Analyze a diff between two files")
    diff_parser.add_argument("--old-file", help="Path to the old file version")
    diff_parser.add_argument("--new-file", help="Path to the new file version")
    diff_parser.add_argument("--old-content", help="Old content string")
    diff_parser.add_argument("--new-content", help="New content string")
    diff_parser.add_argument("--file-path", help="Path to use for the file in analysis")
    diff_parser.add_argument("--marker", required=True, help="Coherence marker to verify")
    diff_parser.add_argument("--iteration", help="Iteration identifier")
    
    # Visualize context command
    viz_parser = subparsers.add_parser("visualize-context", help="Visualize context graph")
    viz_parser.add_argument("--runtime-context", help="Path to runtime context JSON file")
    viz_parser.add_argument("--format", default="html", choices=["json", "markdown", "html"], help="Output format")
    viz_parser.add_argument("--output", help="Output file path")
    
    # Monitor performance command
    monitor_parser = subparsers.add_parser("monitor-performance", help="Monitor performance metrics")
    monitor_parser.add_argument("--update", action="store_true", help="Update performance metrics")
    monitor_parser.add_argument("--iteration", default=str(int(datetime.now().timestamp())), help="Iteration identifier")
    monitor_parser.add_argument("--metrics", help="JSON string with metrics data")
    monitor_parser.add_argument("--metrics-file", help="Path to metrics JSON file")
    monitor_parser.add_argument("--check-compliance", action="store_true", help="Check budget compliance")
    monitor_parser.add_argument("--generate-dashboard", action="store_true", help="Generate performance dashboard")
    
    args = parser.parse_args()
    
    # Execute the appropriate command
    if args.command == "execute-chain":
        execute_chain(args)
    elif args.command == "execute-module":
        execute_module(args)
    elif args.command == "analyze-diff":
        analyze_diff(args)
    elif args.command == "visualize-context":
        visualize_context(args)
    elif args.command == "monitor-performance":
        monitor_performance(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
