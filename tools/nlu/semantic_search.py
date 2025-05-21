#!/usr/bin/env python3
"""
Documentation Semantic Search Tool

This module provides semantic search capabilities for repository documentation,
enabling developers to find relevant documents based on natural language queries.
"""

import os
import json
import numpy as np
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('nlu.search')

class SemanticSearch:
    """Provides semantic search capabilities for repository documentation."""
    
    def __init__(self, registry_path: str, embeddings_path: str):
        """
        Initialize the semantic search tool.
        
        Args:
            registry_path: Path to the document registry JSON file
            embeddings_path: Path to the document embeddings JSON file
        """
        self.registry_path = Path(registry_path)
        self.embeddings_path = Path(embeddings_path)
        self.doc_registry = self._load_json(registry_path)
        self.embeddings = self._load_embeddings(embeddings_path)
        
    def _load_json(self, path: str) -> Dict:
        """Load JSON file."""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load {path}: {e}")
            return {}
            
    def _load_embeddings(self, path: str) -> Dict[str, np.ndarray]:
        """Load document embeddings."""
        try:
            with open(path, 'r') as f:
                embeddings_data = json.load(f)
                
            # Convert lists back to numpy arrays
            embeddings = {}
            for doc_id, embedding in embeddings_data.items():
                embeddings[doc_id] = np.array(embedding)
                
            return embeddings
        except Exception as e:
            logger.error(f"Failed to load embeddings: {e}")
            return {}
    
    def search(self, query: str, num_results: int = 5, filter_layer: Optional[str] = None) -> List[Dict]:
        """
        Search for documents that match the query.
        
        Args:
            query: Search query
            num_results: Maximum number of results to return
            filter_layer: Optional taxonomy layer to filter results
            
        Returns:
            List of matching documents with scores
        """
        logger.info(f"Searching for: '{query}'")
        
        # Generate query embedding (in a real system, this would use the same model as the document embedder)
        query_embedding = self._generate_query_embedding(query)
        
        # Calculate cosine similarity for all documents
        similarities = {}
        for doc_id, embedding in self.embeddings.items():
            # Filter by layer if specified
            if filter_layer and self.doc_registry.get(doc_id, {}).get("taxonomy_layer") != filter_layer:
                continue
                
            similarity = self._cosine_similarity(query_embedding, embedding)
            similarities[doc_id] = similarity
        
        # Sort by similarity (descending)
        sorted_docs = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
        
        # Prepare results
        results = []
        for doc_id, score in sorted_docs[:num_results]:
            doc_metadata = self.doc_registry.get(doc_id, {})
            result = {
                "id": doc_id,
                "title": doc_metadata.get("title", doc_id),
                "score": float(score),  # Convert from numpy to float for JSON serialization
                "layer": doc_metadata.get("taxonomy_layer", "unknown"),
                "snippet": self._extract_snippet(doc_metadata, query),
                "type": doc_metadata.get("file_type", "unknown")
            }
            results.append(result)
            
        logger.info(f"Found {len(results)} results")
        return results
    
    def _generate_query_embedding(self, query: str) -> np.ndarray:
        """
        Generate embedding for a search query.
        
        In a real system, this would use the same model as the document embedder.
        Here we're using a mock implementation for demonstration.
        """
        # Create a deterministic but unique vector based on the query
        query_hash = hash(query) % 10000
        np.random.seed(query_hash)
        return np.random.rand(384)  # Same dimensions as document embeddings
    
    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    def _extract_snippet(self, doc_metadata: Dict, query: str) -> str:
        """Extract a relevant snippet from the document based on the query."""
        # In a real implementation, this would extract text near query terms
        # Here we'll just return a simplified snippet based on available metadata
        
        if "docstring" in doc_metadata:
            return doc_metadata["docstring"][:150] + "..." if len(doc_metadata["docstring"]) > 150 else doc_metadata["docstring"]
            
        if "front_matter" in doc_metadata and "description" in doc_metadata["front_matter"]:
            return doc_metadata["front_matter"]["description"]
            
        if "headers" in doc_metadata and len(doc_metadata["headers"]) > 1:
            return f"{doc_metadata['headers'][0]['text']} - {doc_metadata['headers'][1]['text']}"
            
        return f"File: {doc_metadata.get('file_path', 'Unknown path')}"
    
    def search_interactive(self) -> None:
        """Run interactive search mode."""
        print("\nDocumentation Semantic Search")
        print("============================")
        print("Type 'exit' or 'quit' to end the session.\n")
        
        while True:
            query = input("Search query: ").strip()
            if query.lower() in ['exit', 'quit', 'q']:
                break
                
            if not query:
                continue
                
            layer_filter = input("Filter by layer (config, prompts, code, docs, audit) [optional]: ").strip()
            if not layer_filter:
                layer_filter = None
                
            num_results = 5
            try:
                num_input = input(f"Number of results [default: {num_results}]: ").strip()
                if num_input:
                    num_results = int(num_input)
            except ValueError:
                pass
                
            results = self.search(query, num_results, layer_filter)
            
            if not results:
                print("\nNo results found. Try a different query or remove the layer filter.\n")
                continue
                
            print(f"\nFound {len(results)} results:")
            for i, result in enumerate(results):
                print(f"\n{i+1}. {result['title']} [{result['layer']}]")
                print(f"   Path: {result['id']}")
                print(f"   Score: {result['score']:.2f}")
                print(f"   {result['snippet']}")
                
            print("\n" + "-" * 40 + "\n")


def main():
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description="Search repository documentation semantically")
    parser.add_argument("--registry", default="docs/nlu/document_registry.json", 
                        help="Path to document registry JSON file")
    parser.add_argument("--embeddings", default="docs/nlu/embeddings/document_embeddings.json", 
                        help="Path to document embeddings JSON file")
    parser.add_argument("--query", 
                        help="Search query (if not provided, runs in interactive mode)")
    parser.add_argument("--num-results", type=int, default=5, 
                        help="Number of results to return")
    parser.add_argument("--layer", 
                        help="Filter results by taxonomy layer")
    parser.add_argument("--json", action="store_true", 
                        help="Output results in JSON format")
    
    args = parser.parse_args()
    
    searcher = SemanticSearch(args.registry, args.embeddings)
    
    if args.query:
        # Single query mode
        results = searcher.search(args.query, args.num_results, args.layer)
        
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(f"Search results for '{args.query}':")
            for i, result in enumerate(results):
                print(f"\n{i+1}. {result['title']} [{result['layer']}]")
                print(f"   Path: {result['id']}")
                print(f"   Score: {result['score']:.2f}")
                print(f"   {result['snippet']}")
    else:
        # Interactive mode
        searcher.search_interactive()
    
    return 0


if __name__ == "__main__":
    exit(main())