#!/usr/bin/env python3
"""
Document Embedder - Generate semantic embeddings for repository documents.

This module creates vector embeddings for all documents in the repository,
enabling semantic search and similarity analysis.
"""

import os
import json
import numpy as np
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('nlu.embedder')

# Mock embeddings for demonstration
# In production, you would use a proper embedding model
def generate_mock_embedding(text: str, dim: int = 384) -> np.ndarray:
    """Generate a mock embedding vector for demonstration purposes."""
    # Create a deterministic but unique vector based on the text
    text_hash = hash(text) % 10000
    np.random.seed(text_hash)
    return np.random.rand(dim)


class DocumentEmbedder:
    """Generates semantic embeddings for repository documents."""
    
    def __init__(self, registry_path: str, model_name: str = "text-embedding-3-large"):
        """
        Initialize the document embedder.
        
        Args:
            registry_path: Path to the document registry JSON file
            model_name: Name of the embedding model to use
        """
        self.registry_path = Path(registry_path)
        self.model_name = model_name
        self.doc_registry = self._load_registry()
        self.embeddings = {}
        
    def _load_registry(self) -> Dict:
        """Load document registry from JSON file."""
        try:
            with open(self.registry_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load document registry: {e}")
            return {}
    
    def generate_embeddings(self) -> Dict[str, np.ndarray]:
        """
        Generate embeddings for all documents in the registry.
        
        Returns:
            Dictionary mapping document IDs to embedding vectors
        """
        logger.info(f"Generating embeddings using model: {self.model_name}")
        
        for doc_id, metadata in self.doc_registry.items():
            # Prepare text for embedding
            document_text = self._extract_text_for_embedding(metadata)
            
            # Generate embedding
            try:
                # In production, you would use a proper embedding model API here
                embedding = generate_mock_embedding(document_text)
                self.embeddings[doc_id] = embedding
                logger.info(f"Generated embedding for {doc_id}")
            except Exception as e:
                logger.error(f"Failed to generate embedding for {doc_id}: {e}")
        
        logger.info(f"Generated {len(self.embeddings)} embeddings")
        return self.embeddings
    
    def _extract_text_for_embedding(self, metadata: Dict) -> str:
        """
        Extract relevant text from document metadata for embedding.
        
        Args:
            metadata: Document metadata dictionary
            
        Returns:
            Extracted text for embedding
        """
        text_parts = []
        
        # Add title if available
        if "title" in metadata:
            text_parts.append(f"Title: {metadata['title']}")
            
        # Add front matter fields
        if "front_matter" in metadata:
            front_matter = metadata["front_matter"]
            for key, value in front_matter.items():
                if isinstance(value, str):
                    text_parts.append(f"{key}: {value}")
                elif isinstance(value, list) and all(isinstance(item, str) for item in value):
                    text_parts.append(f"{key}: {', '.join(value)}")
            
        # Add headers
        if "headers" in metadata:
            headers = metadata["headers"]
            for header in headers:
                text_parts.append(f"H{header['level']}: {header['text']}")
                
        # Add docstring
        if "docstring" in metadata:
            text_parts.append(metadata["docstring"])
            
        # Add classes and functions
        if "classes" in metadata:
            text_parts.append(f"Classes: {', '.join(metadata['classes'])}")
            
        if "functions" in metadata:
            text_parts.append(f"Functions: {', '.join(metadata['functions'])}")
            
        # Add file path for context
        text_parts.append(f"Path: {metadata['file_path']}")
        
        # Add taxonomy layer
        if "taxonomy_layer" in metadata:
            text_parts.append(f"Layer: {metadata['taxonomy_layer']}")
            
        # Join all parts
        return "\n".join(text_parts)
    
    def save_embeddings(self, output_path: str) -> None:
        """
        Save embeddings to a binary file.
        
        Args:
            output_path: Path to save the embeddings
        """
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save embeddings as numpy array
        embeddings_array = {}
        for doc_id, embedding in self.embeddings.items():
            embeddings_array[doc_id] = embedding.tolist()
            
        with open(output_path, 'w') as f:
            json.dump(embeddings_array, f)
            
        logger.info(f"Saved embeddings to {output_path}")
        
        # Save document IDs mapping
        ids_path = Path(output_path).with_suffix('.ids.json')
        with open(ids_path, 'w') as f:
            json.dump(list(self.embeddings.keys()), f, indent=2)
            
        logger.info(f"Saved document IDs to {ids_path}")
    
    def process_and_save(self, output_path: str) -> None:
        """
        Generate embeddings and save them.
        
        Args:
            output_path: Path to save the embeddings
        """
        self.generate_embeddings()
        self.save_embeddings(output_path)


def main():
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description="Generate embeddings for repository documents")
    parser.add_argument("--registry", default="docs/nlu/document_registry.json", 
                        help="Path to document registry JSON file")
    parser.add_argument("--model", default="text-embedding-3-large", 
                        help="Embedding model to use")
    parser.add_argument("--output", default="docs/nlu/embeddings/document_embeddings.json", 
                        help="Output path for embeddings")
    
    args = parser.parse_args()
    
    embedder = DocumentEmbedder(args.registry, args.model)
    embedder.process_and_save(args.output)
    
    return 0


if __name__ == "__main__":
    exit(main())
