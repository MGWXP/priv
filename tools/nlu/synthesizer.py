#!/usr/bin/env python3
"""
Document Synthesizer - Generate cross-document insights and visualizations.

This module analyzes relationships between documents to generate insights,
reports, and visualizations for better understanding the repository structure.
"""

import os
import json
import argparse
import logging
import networkx as nx
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('nlu.synthesizer')


class DocumentSynthesizer:
    """Generates insights and visualizations from document relationships."""
    
    def __init__(self, registry_path: str, relationships_path: str):
        """
        Initialize the document synthesizer.
        
        Args:
            registry_path: Path to the document registry JSON file
            relationships_path: Path to the relationship map JSON file
        """
        self.registry_path = Path(registry_path)
        self.relationships_path = Path(relationships_path)
        self.doc_registry = self._load_json(registry_path)
        self.relationship_map = self._load_json(relationships_path)
        
    def _load_json(self, path: str) -> Dict:
        """Load JSON file."""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load {path}: {e}")
            return {}
    
    def generate_system_overview(self) -> str:
        """
        Generate a system overview markdown document.
        
        Returns:
            Markdown string with system overview
        """
        logger.info("Generating system overview")
        
        # Count documents by taxonomy layer
        layer_counts = {}
        for doc_id, metadata in self.doc_registry.items():
            layer = metadata.get("taxonomy_layer", "unknown")
            layer_counts[layer] = layer_counts.get(layer, 0) + 1
            
        # Count relationship types
        relationship_counts = {}
        for doc_id, relationships in self.relationship_map.items():
            for rel_type, rel_targets in relationships.items():
                if isinstance(rel_targets, list):
                    relationship_counts[rel_type] = relationship_counts.get(rel_type, 0) + len(rel_targets)
        
        # Build markdown document
        lines = [
            "# System Overview",
            "",
            f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
            "",
            "## Repository Statistics",
            "",
            f"Total documents: {len(self.doc_registry)}",
            "",
            "### Documents by Taxonomy Layer",
            ""
        ]
        
        for layer, count in sorted(layer_counts.items()):
            lines.append(f"- **{layer.title()}**: {count} documents")
            
        lines.extend([
            "",
            "### Relationship Statistics",
            ""
        ])
        
        for rel_type, count in sorted(relationship_counts.items()):
            lines.append(f"- **{rel_type.replace('_', ' ').title()}**: {count} connections")
            
        # Add key documents section
        lines.extend([
            "",
            "## Key Documents",
            ""
        ])
        
        # Find most referenced documents
        doc_references = {}
        for doc_id, relationships in self.relationship_map.items():
            doc_references[doc_id] = len(relationships.get("referenced_by", []))
            
        top_docs = sorted(doc_references.items(), key=lambda x: x[1], reverse=True)[:10]
        
        for doc_id, ref_count in top_docs:
            if ref_count > 0:
                doc_title = self.doc_registry.get(doc_id, {}).get("title", doc_id)
                lines.append(f"- **{doc_title}** (`{doc_id}`): Referenced {ref_count} times")
                
        # Add orphaned documents section
        orphans = []
        for doc_id, relationships in self.relationship_map.items():
            if (len(relationships.get("references", [])) == 0 and 
                len(relationships.get("referenced_by", [])) == 0):
                orphans.append(doc_id)
                
        if orphans:
            lines.extend([
                "",
                "## Potential Issues",
                "",
                "### Orphaned Documents",
                "",
                "These documents have no relationships with other documents and may need attention:",
                ""
            ])
            
            for orphan in sorted(orphans):
                doc_title = self.doc_registry.get(orphan, {}).get("title", orphan)
                lines.append(f"- **{doc_title}** (`{orphan}`)") 
                
        return "\n".join(lines)
    
    def generate_knowledge_graph(self) -> Dict:
        """
        Generate a knowledge graph representation.
        
        Returns:
            Dictionary with nodes and edges for visualization
        """
        logger.info("Generating knowledge graph")
        
        # Create networkx graph
        G = nx.DiGraph()
        
        # Add nodes
        for doc_id, metadata in self.doc_registry.items():
            G.add_node(doc_id, 
                      title=metadata.get("title", doc_id),
                      layer=metadata.get("taxonomy_layer", "unknown"),
                      file_type=metadata.get("file_type", ""))
            
        # Add edges
        for doc_id, relationships in self.relationship_map.items():
            for rel_type, targets in relationships.items():
                if isinstance(targets, list) and rel_type in ["references", "implements", "tests", "documents"]:
                    for target in targets:
                        if target in self.doc_registry:  # Ensure target exists
                            G.add_edge(doc_id, target, relationship=rel_type)
        
        # Convert to visualization format
        nodes = []
        for node, attrs in G.nodes(data=True):
            nodes.append({
                "id": node,
                "label": attrs.get("title", node),
                "group": attrs.get("layer", "unknown"),
                "type": attrs.get("file_type", "")
            })
            
        edges = []
        for source, target, attrs in G.edges(data=True):
            edges.append({
                "from": source,
                "to": target,
                "label": attrs.get("relationship", ""),
                "type": attrs.get("relationship", "")
            })
            
        return {
            "nodes": nodes,
            "edges": edges
        }
    
    def generate_documentation_gaps(self) -> str:
        """
        Generate a report of documentation gaps.
        
        Returns:
            Markdown string with documentation gaps report
        """
        logger.info("Analyzing documentation gaps")
        
        # Find code files without documentation
        undocumented_code = []
        for doc_id, metadata in self.doc_registry.items():
            if (metadata.get("taxonomy_layer") == "code" and 
                not self.relationship_map.get(doc_id, {}).get("documented_by")):
                undocumented_code.append(doc_id)
                
        # Find code files without tests
        untested_code = []
        for doc_id, metadata in self.doc_registry.items():
            if (metadata.get("taxonomy_layer") == "code" and 
                doc_id.startswith("src/") and
                not self.relationship_map.get(doc_id, {}).get("tested_by")):
                untested_code.append(doc_id)
                
        # Find prompt modules without implementation
        unimplemented_prompts = []
        for doc_id, metadata in self.doc_registry.items():
            if (doc_id.startswith(("prompt-library/", "modules/")) and 
                not self.relationship_map.get(doc_id, {}).get("implemented_by")):
                unimplemented_prompts.append(doc_id)
        
        # Build markdown document
        lines = [
            "# Documentation Gap Analysis",
            "",
            f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
            ""
        ]
        
        if undocumented_code:
            lines.extend([
                "## Undocumented Code",
                "",
                "The following code files have no associated documentation:",
                ""
            ])
            
            for code_file in sorted(undocumented_code):
                doc_title = self.doc_registry.get(code_file, {}).get("title", code_file)
                lines.append(f"- **{doc_title}** (`{code_file}`)") 
                
        if untested_code:
            lines.extend([
                "",
                "## Untested Code",
                "",
                "The following code files have no associated tests:",
                ""
            ])
            
            for code_file in sorted(untested_code):
                doc_title = self.doc_registry.get(code_file, {}).get("title", code_file)
                lines.append(f"- **{doc_title}** (`{code_file}`)") 
                
        if unimplemented_prompts:
            lines.extend([
                "",
                "## Unimplemented Prompt Modules",
                "",
                "The following prompt modules have no associated implementation:",
                ""
            ])
            
            for prompt_file in sorted(unimplemented_prompts):
                doc_title = self.doc_registry.get(prompt_file, {}).get("title", prompt_file)
                lines.append(f"- **{doc_title}** (`{prompt_file}`)") 
                
        if not (undocumented_code or untested_code or unimplemented_prompts):
            lines.extend([
                "## No Significant Gaps Found",
                "",
                "No major documentation or testing gaps were identified in the repository.",
                "",
                "Congratulations on maintaining good documentation and test coverage!"
            ])
            
        return "\n".join(lines)
    
    def generate_cross_references(self) -> str:
        """
        Generate a cross-reference index for all documents.
        
        Returns:
            Markdown string with cross-reference index
        """
        logger.info("Generating cross-reference index")
        
        # Group documents by taxonomy layer
        layers = {}
        for doc_id, metadata in self.doc_registry.items():
            layer = metadata.get("taxonomy_layer", "unknown")
            if layer not in layers:
                layers[layer] = {}
            layers[layer][doc_id] = metadata
            
        # Build markdown document
        lines = [
            "# Document Cross-Reference Index",
            "",
            f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
            "",
            "This index provides a cross-reference of all documents in the repository, organized by taxonomy layer.",
            ""
        ]
        
        for layer, docs in sorted(layers.items()):
            lines.extend([
                f"## {layer.title()} Layer",
                ""
            ])
            
            for doc_id, metadata in sorted(docs.items()):
                doc_title = metadata.get("title", doc_id)
                lines.extend([
                    f"### {doc_title}",
                    "",
                    f"- **Path**: `{doc_id}`",
                    f"- **Type**: {metadata.get('file_type', 'unknown')}"
                ])
                
                # Add relationships
                relationships = self.relationship_map.get(doc_id, {})
                
                # References
                if relationships.get("references"):
                    lines.append("- **References**:")
                    for ref in sorted(relationships["references"]):
                        ref_title = self.doc_registry.get(ref, {}).get("title", ref)
                        lines.append(f"  - {ref_title} (`{ref}`)")
                        
                # Referenced by
                if relationships.get("referenced_by"):
                    lines.append("- **Referenced by**:")
                    for ref in sorted(relationships["referenced_by"]):
                        ref_title = self.doc_registry.get(ref, {}).get("title", ref)
                        lines.append(f"  - {ref_title} (`{ref}`)")
                        
                # Other relationships
                for rel_type in ["implements", "implemented_by", "tests", "tested_by", "documents", "documented_by"]:
                    if relationships.get(rel_type):
                        rel_title = rel_type.replace("_", " ").title()
                        lines.append(f"- **{rel_title}**:")
                        for rel in sorted(relationships[rel_type]):
                            rel_title = self.doc_registry.get(rel, {}).get("title", rel)
                            lines.append(f"  - {rel_title} (`{rel}`)")
                            
                lines.append("")
                
        return "\n".join(lines)
    
    def generate_all_reports(self, output_dir: str) -> None:
        """
        Generate all reports and save them to the output directory.
        
        Args:
            output_dir: Directory to save the reports
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate system overview
        overview = self.generate_system_overview()
        with open(output_path / "system_overview.md", 'w') as f:
            f.write(overview)
            
        # Generate knowledge graph
        knowledge_graph = self.generate_knowledge_graph()
        with open(output_path.parent / "visualizations" / "knowledge_graph.json", 'w') as f:
            json.dump(knowledge_graph, f, indent=2)
            
        # Generate documentation gaps report
        gaps = self.generate_documentation_gaps()
        with open(output_path / "documentation_gaps.md", 'w') as f:
            f.write(gaps)
            
        # Generate cross-reference index
        xref = self.generate_cross_references()
        with open(output_path / "cross_reference_index.md", 'w') as f:
            f.write(xref)
            
        logger.info(f"Generated all reports in {output_dir}")


def main():
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description="Generate document synthesis reports")
    parser.add_argument("--registry", default="docs/nlu/document_registry.json", 
                        help="Path to document registry JSON file")
    parser.add_argument("--relationships", default="docs/nlu/relationship_map.json", 
                        help="Path to relationship map JSON file")
    parser.add_argument("--output-dir", default="docs/synthesis/reports", 
                        help="Directory to save the reports")
    parser.add_argument("--report", choices=["all", "overview", "gaps", "xref"], default="all",
                        help="Which report to generate")
    
    args = parser.parse_args()
    
    synthesizer = DocumentSynthesizer(args.registry, args.relationships)
    
    if args.report == "all":
        synthesizer.generate_all_reports(args.output_dir)
    elif args.report == "overview":
        overview = synthesizer.generate_system_overview()
        with open(Path(args.output_dir) / "system_overview.md", 'w') as f:
            f.write(overview)
    elif args.report == "gaps":
        gaps = synthesizer.generate_documentation_gaps()
        with open(Path(args.output_dir) / "documentation_gaps.md", 'w') as f:
            f.write(gaps)
    elif args.report == "xref":
        xref = synthesizer.generate_cross_references()
        with open(Path(args.output_dir) / "cross_reference_index.md", 'w') as f:
            f.write(xref)
    
    return 0


if __name__ == "__main__":
    exit(main())
