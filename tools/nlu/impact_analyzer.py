#!/usr/bin/env python3
"""
Documentation Impact Analyzer

This module analyzes the potential impact of changes to documentation by
identifying affected documents and assessing downstream consequences.
"""

import os
import json
import argparse
import logging
import networkx as nx
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('nlu.impact')

class ImpactAnalyzer:
    """Analyzes the impact of changes to documentation."""
    
    def __init__(self, registry_path: str, relationships_path: str):
        """
        Initialize the impact analyzer.
        
        Args:
            registry_path: Path to the document registry JSON file
            relationships_path: Path to the relationship map JSON file
        """
        self.registry_path = Path(registry_path)
        self.relationships_path = Path(relationships_path)
        self.doc_registry = self._load_json(registry_path)
        self.relationship_map = self._load_json(relationships_path)
        self.graph = self._build_graph()
        
    def _load_json(self, path: str) -> Dict:
        """Load JSON file."""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load {path}: {e}")
            return {}
    
    def _build_graph(self) -> nx.DiGraph:
        """Build a directed graph of document relationships."""
        # Create a graph
        G = nx.DiGraph()
        
        # Add nodes
        for doc_id in self.doc_registry:
            G.add_node(doc_id)
        
        # Add edges
        for doc_id, relationships in self.relationship_map.items():
            for rel_type, targets in relationships.items():
                if isinstance(targets, list):
                    for target in targets:
                        if target in self.doc_registry:
                            if rel_type in ["references", "implements", "tests", "documents"]:
                                # Outgoing edge from doc_id to target
                                G.add_edge(doc_id, target, relationship=rel_type)
                            elif rel_type in ["referenced_by", "implemented_by", "tested_by", "documented_by"]:
                                # Incoming edge from target to doc_id
                                G.add_edge(target, doc_id, relationship=rel_type.replace("_by", ""))
        
        return G
    
    def analyze_impact(self, changed_docs: List[str], max_depth: int = 2) -> Dict:
        """
        Analyze the impact of changes to specified documents.
        
        Args:
            changed_docs: List of document IDs that will be changed
            max_depth: Maximum depth to analyze for impact (default: 2)
            
        Returns:
            Dictionary with impact analysis results
        """
        logger.info(f"Analyzing impact of changes to {len(changed_docs)} documents")
        
        # Convert document paths to IDs if needed
        doc_ids = []
        for doc in changed_docs:
            if doc in self.doc_registry:
                doc_ids.append(doc)
            else:
                # Try to find a matching document
                matches = [d for d in self.doc_registry if d.endswith(doc)]
                if len(matches) == 1:
                    doc_ids.append(matches[0])
                elif len(matches) > 1:
                    logger.warning(f"Multiple matches found for '{doc}': {matches}")
                    doc_ids.extend(matches)
                else:
                    logger.warning(f"No matching document found for '{doc}'")
        
        if not doc_ids:
            logger.error("No valid documents specified for impact analysis")
            return {"error": "No valid documents specified"}
        
        # Initialize impact analysis results
        impact = {
            "changed_documents": [],
            "directly_affected": [],
            "indirectly_affected": [],
            "summary": {
                "total_affected": 0,
                "by_layer": {},
                "by_relationship": {}
            }
        }
        
        # Analyze changed documents
        for doc_id in doc_ids:
            doc_metadata = self.doc_registry.get(doc_id, {})
            impact["changed_documents"].append({
                "id": doc_id,
                "title": doc_metadata.get("title", doc_id),
                "layer": doc_metadata.get("taxonomy_layer", "unknown")
            })
        
        # Find directly affected documents (immediate neighbors)
        direct_affected = set()
        for doc_id in doc_ids:
            for successor in self.graph.successors(doc_id):
                direct_affected.add(successor)
        
        # Remove original changed documents from affected
        direct_affected = direct_affected - set(doc_ids)
        
        # Analyze directly affected documents
        for doc_id in direct_affected:
            doc_metadata = self.doc_registry.get(doc_id, {})
            relationships = []
            
            # Find relationships from changed docs to this doc
            for changed_doc in doc_ids:
                for rel_type, targets in self.relationship_map.get(changed_doc, {}).items():
                    if isinstance(targets, list) and doc_id in targets:
                        relationships.append({
                            "from": changed_doc,
                            "type": rel_type,
                            "from_title": self.doc_registry.get(changed_doc, {}).get("title", changed_doc)
                        })
            
            impact["directly_affected"].append({
                "id": doc_id,
                "title": doc_metadata.get("title", doc_id),
                "layer": doc_metadata.get("taxonomy_layer", "unknown"),
                "relationships": relationships
            })
        
        # Find indirectly affected documents (up to max_depth)
        if max_depth > 1:
            indirect_affected = set()
            current_level = direct_affected
            
            for depth in range(2, max_depth + 1):
                next_level = set()
                for doc_id in current_level:
                    for successor in self.graph.successors(doc_id):
                        if successor not in direct_affected and successor not in doc_ids:
                            next_level.add(successor)
                
                indirect_affected.update(next_level)
                current_level = next_level
                
                if not current_level:
                    break
            
            # Analyze indirectly affected documents
            for doc_id in indirect_affected:
                doc_metadata = self.doc_registry.get(doc_id, {})
                impact["indirectly_affected"].append({
                    "id": doc_id,
                    "title": doc_metadata.get("title", doc_id),
                    "layer": doc_metadata.get("taxonomy_layer", "unknown")
                })
        
        # Generate summary statistics
        total_affected = len(direct_affected) + len(impact.get("indirectly_affected", []))
        impact["summary"]["total_affected"] = total_affected
        
        # Count by layer
        layers = {}
        for doc_id in direct_affected.union(set([d["id"] for d in impact.get("indirectly_affected", [])])):
            layer = self.doc_registry.get(doc_id, {}).get("taxonomy_layer", "unknown")
            layers[layer] = layers.get(layer, 0) + 1
        
        impact["summary"]["by_layer"] = layers
        
        # Count by relationship type
        relationships = {}
        for doc in impact["directly_affected"]:
            for rel in doc.get("relationships", []):
                rel_type = rel.get("type", "unknown")
                relationships[rel_type] = relationships.get(rel_type, 0) + 1
        
        impact["summary"]["by_relationship"] = relationships
        
        logger.info(f"Impact analysis complete. {total_affected} documents affected.")
        return impact
    
    def generate_report(self, impact: Dict) -> str:
        """
        Generate a Markdown report of the impact analysis.
        
        Args:
            impact: Impact analysis results
            
        Returns:
            Markdown report
        """
        if "error" in impact:
            return f"# Impact Analysis Error\n\n{impact['error']}"
        
        lines = [
            "# Documentation Change Impact Analysis",
            "",
            "## Summary",
            "",
            f"**Documents Changing**: {len(impact['changed_documents'])}",
            f"**Directly Affected**: {len(impact['directly_affected'])}",
            f"**Indirectly Affected**: {len(impact['indirectly_affected'])}",
            f"**Total Impact**: {impact['summary']['total_affected']} affected documents",
            "",
            "### Impact by Layer",
            ""
        ]
        
        # Impact by layer
        for layer, count in impact['summary']['by_layer'].items():
            lines.append(f"- **{layer.title()}**: {count} documents")
        
        lines.extend([
            "",
            "### Impact by Relationship Type",
            ""
        ])
        
        # Impact by relationship type
        for rel_type, count in impact['summary']['by_relationship'].items():
            lines.append(f"- **{rel_type.replace('_', ' ').title()}**: {count} relationships")
        
        lines.extend([
            "",
            "## Changed Documents",
            ""
        ])
        
        # List changed documents
        for doc in impact['changed_documents']:
            lines.append(f"- **{doc['title']}** (`{doc['id']}`) [{doc['layer']}]")
        
        lines.extend([
            "",
            "## Directly Affected Documents",
            ""
        ])
        
        # List directly affected documents
        for doc in impact['directly_affected']:
            lines.append(f"### {doc['title']} ({doc['layer']})")
            lines.append(f"- **Path**: `{doc['id']}`")
            lines.append("- **Affected by**:")
            
            for rel in doc.get('relationships', []):
                lines.append(f"  - {rel['from_title']} (`{rel['from']}`) via *{rel['type'].replace('_', ' ')}*")
            
            lines.append("")
        
        if impact['indirectly_affected']:
            lines.extend([
                "## Indirectly Affected Documents",
                ""
            ])
            
            # List indirectly affected documents
            for doc in impact['indirectly_affected']:
                lines.append(f"- **{doc['title']}** (`{doc['id']}`) [{doc['layer']}]")
        
        lines.extend([
            "",
            "## Recommendations",
            "",
            "Based on this impact analysis, consider the following recommendations:",
            ""
        ])
        
        # Generate recommendations based on impact
        if len(impact['directly_affected']) > 10:
            lines.append("- **High Impact**: These changes affect many documents. Consider breaking the changes into smaller, more focused updates.")
        
        if any(doc['layer'] == 'config' for doc in impact['directly_affected']):
            lines.append("- **Config Layer Impact**: Changes affect configuration documents. Ensure all dependent systems are updated accordingly.")
        
        if any(doc['layer'] == 'prompts' for doc in impact['directly_affected']):
            lines.append("- **Prompt Module Impact**: Changes affect prompt modules. Verify that AI agents using these prompts will behave as expected.")
        
        if any(doc['layer'] == 'code' for doc in impact['directly_affected']):
            lines.append("- **Code Impact**: Changes affect code files. Run tests to ensure no regressions are introduced.")
        
        if len(impact['indirectly_affected']) > len(impact['directly_affected']):
            lines.append("- **Cascade Effect**: These changes have a significant cascade effect. Review indirectly affected documents carefully.")
        
        return "\n".join(lines)


def main():
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description="Analyze the impact of changes to documentation")
    parser.add_argument("--registry", default="docs/nlu/document_registry.json", 
                        help="Path to document registry JSON file")
    parser.add_argument("--relationships", default="docs/nlu/relationship_map.json", 
                        help="Path to relationship map JSON file")
    parser.add_argument("--documents", nargs="+", required=True,
                        help="List of documents to analyze")
    parser.add_argument("--max-depth", type=int, default=2,
                        help="Maximum depth for impact analysis")
    parser.add_argument("--output", 
                        help="Output path for impact report")
    parser.add_argument("--json", action="store_true",
                        help="Output results in JSON format")
    
    args = parser.parse_args()
    
    analyzer = ImpactAnalyzer(args.registry, args.relationships)
    impact = analyzer.analyze_impact(args.documents, args.max_depth)
    
    if args.json:
        # Output JSON results
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(impact, f, indent=2)
        else:
            print(json.dumps(impact, indent=2))
    else:
        # Generate and output report
        report = analyzer.generate_report(impact)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            logger.info(f"Impact report saved to {args.output}")
        else:
            print(report)
    
    return 0


if __name__ == "__main__":
    exit(main())