#!/usr/bin/env python3
"""
NLU Document Processor - Core component for extracting metadata and building relationships.

This module processes documentation files across the repository to extract structured
metadata and build semantic relationships between documents.
"""

import os
import json
import yaml
import re
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set, Any
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('nlu.processor')

class DocumentProcessor:
    """Processes documentation files to extract structured metadata and relationships."""
    
    def __init__(self, base_path: str, config_path: str = "docs/nlu/schemas/processor_config.yaml"):
        """
        Initialize the document processor with the repository base path.
        
        Args:
            base_path: Root path of the repository
            config_path: Path to configuration file
        """
        self.base_path = Path(base_path)
        self.config = self._load_config(config_path)
        self.doc_registry = {}
        self.relationship_map = {}
        
    def _load_config(self, config_path: str) -> Dict:
        """Load processor configuration."""
        config_file = self.base_path / config_path
        if not config_file.exists():
            logger.warning(f"Config file not found at {config_path}, using defaults")
            return {
                "file_patterns": [".md", ".py", ".yaml", ".yml"],
                "extraction_rules": {
                    "md": {
                        "front_matter": r"---\n(.*?)\n---",
                        "headers": r"^(#{1,6})\s+(.*?)$"
                    },
                    "py": {
                        "docstring": r'"""(.*?)"""',
                        "class": r"class\s+(\w+)",
                        "function": r"def\s+(\w+)"
                    }
                },
                "relationship_types": [
                    "references",
                    "implements",
                    "tests",
                    "documents",
                    "depends_on"
                ],
                "taxonomy_layers": [
                    {"name": "config", "paths": ["README.md", "AGENTS.md", "execution-budget.yaml"]},
                    {"name": "prompts", "paths": ["prompt-library/", "modules/"]},
                    {"name": "code", "paths": ["src/", "tests/"]},
                    {"name": "docs", "paths": ["docs/"]},
                    {"name": "audit", "paths": ["audits/", ".github/workflows/"]}
                ]
            }
        
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def process_repository(self) -> Tuple[Dict, Dict]:
        """
        Process all documentation in the repository.
        
        Returns:
            Tuple of (document_registry, relationship_map)
        """
        # Scan repository for relevant files
        file_paths = self._find_files()
        
        # Process each file to extract metadata
        for file_path in file_paths:
            doc_metadata = self._extract_metadata(file_path)
            if doc_metadata:
                doc_id = str(file_path.relative_to(self.base_path))
                self.doc_registry[doc_id] = doc_metadata
        
        # Build relationships between documents
        self._build_relationships()
        
        # Add taxonomy layer information
        self._annotate_taxonomy_layers()
        
        return self.doc_registry, self.relationship_map
    
    def _find_files(self) -> List[Path]:
        """Find all relevant files in the repository."""
        patterns = self.config.get("file_patterns", [".md", ".py", ".yaml", ".yml"])
        
        file_paths = []
        for pattern in patterns:
            for path in self.base_path.glob(f"**/*{pattern}"):
                if not self._should_ignore(path):
                    file_paths.append(path)
        
        logger.info(f"Found {len(file_paths)} files to process")
        return file_paths
    
    def _should_ignore(self, path: Path) -> bool:
        """Check if a file should be ignored based on path."""
        ignore_patterns = [
            ".git", 
            "__pycache__", 
            "venv", 
            "node_modules",
            "docs/nlu/embeddings",  # Don't process the embeddings themselves
            ".DS_Store"
        ]
        
        str_path = str(path)
        return any(pattern in str_path for pattern in ignore_patterns)
    
    def _extract_metadata(self, file_path: Path) -> Optional[Dict]:
        """
        Extract metadata from a file based on its type.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary of extracted metadata or None if extraction failed
        """
        file_ext = file_path.suffix.lstrip('.')
        
        # Get extraction rules based on file extension
        rules = self.config.get("extraction_rules", {}).get(file_ext)
        
        if not rules:
            # Use generic extraction for unknown file types
            return self._extract_generic_metadata(file_path)
        
        # Create base metadata
        metadata = {
            "file_path": str(file_path.relative_to(self.base_path)),
            "file_type": file_ext,
            "last_modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            "size_bytes": file_path.stat().st_size
        }
        
        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Failed to read {file_path}: {e}")
            return None
            
        # Extract based on file type
        if file_ext == 'md':
            self._extract_markdown_metadata(content, metadata)
        elif file_ext in ('py', 'js', 'ts'):
            self._extract_code_metadata(content, metadata, file_ext)
        elif file_ext in ('yaml', 'yml'):
            self._extract_yaml_metadata(content, metadata)
            
        # Extract references to other files
        metadata["references"] = self._extract_references(content, file_path)
            
        return metadata
    
    def _extract_markdown_metadata(self, content: str, metadata: Dict) -> None:
        """Extract metadata from markdown files."""
        # Extract front matter
        front_matter_match = re.search(r"---\n(.*?)\n---", content, re.DOTALL)
        if front_matter_match:
            try:
                front_matter = yaml.safe_load(front_matter_match.group(1))
                metadata["front_matter"] = front_matter
            except Exception as e:
                logger.warning(f"Failed to parse front matter: {e}")
        
        # Extract headers structure
        headers = []
        for line in content.split('\n'):
            header_match = re.match(r"^(#{1,6})\s+(.*?)$", line)
            if header_match:
                level = len(header_match.group(1))
                text = header_match.group(2).strip()
                headers.append({"level": level, "text": text})
        
        metadata["headers"] = headers
        
        # Extract title from first h1 or front matter
        if headers and headers[0]["level"] == 1:
            metadata["title"] = headers[0]["text"]
        elif metadata.get("front_matter", {}).get("title"):
            metadata["title"] = metadata["front_matter"]["title"]
        else:
            # Use filename as fallback title
            metadata["title"] = Path(metadata["file_path"]).stem.replace('_', ' ').title()
            
    def _extract_code_metadata(self, content: str, metadata: Dict, lang: str) -> None:
        """Extract metadata from code files."""
        # Extract module docstring
        docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
        if docstring_match:
            metadata["docstring"] = docstring_match.group(1).strip()
            
        # Extract classes
        classes = []
        for class_match in re.finditer(r"class\s+(\w+)", content):
            class_name = class_match.group(1)
            classes.append(class_name)
        
        metadata["classes"] = classes
        
        # Extract functions
        functions = []
        for func_match in re.finditer(r"def\s+(\w+)", content):
            func_name = func_match.group(1)
            functions.append(func_name)
        
        metadata["functions"] = functions
        
        # Use filename as title
        metadata["title"] = Path(metadata["file_path"]).stem.replace('_', ' ').title()
            
    def _extract_yaml_metadata(self, content: str, metadata: Dict) -> None:
        """Extract metadata from YAML files."""
        try:
            yaml_content = yaml.safe_load(content)
            # Extract key top-level fields
            if isinstance(yaml_content, dict):
                # Get first 5 top-level keys as a summary
                top_keys = list(yaml_content.keys())[:5]
                metadata["top_level_keys"] = top_keys
                
                # If it has a name or title field, use it
                if "name" in yaml_content:
                    metadata["title"] = yaml_content["name"]
                elif "title" in yaml_content:
                    metadata["title"] = yaml_content["title"]
                else:
                    # Use filename as title
                    metadata["title"] = Path(metadata["file_path"]).stem.replace('_', ' ').title()
        except Exception as e:
            logger.warning(f"Failed to parse YAML content: {e}")
            metadata["title"] = Path(metadata["file_path"]).stem.replace('_', ' ').title()
    
    def _extract_generic_metadata(self, file_path: Path) -> Dict:
        """Extract basic metadata for unknown file types."""
        return {
            "file_path": str(file_path.relative_to(self.base_path)),
            "file_type": file_path.suffix.lstrip('.'),
            "last_modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            "size_bytes": file_path.stat().st_size,
            "title": file_path.name
        }
    
    def _extract_references(self, content: str, file_path: Path) -> List[str]:
        """Extract references to other files in the repository."""
        references = []
        
        # Look for markdown links
        for link_match in re.finditer(r'\[.*?\]\((.*?)\)', content):
            link = link_match.group(1).split('#')[0]  # Remove anchor
            if not link.startswith(('http://', 'https://', 'mailto:')):
                # This is a relative link
                references.append(link)
        
        # Look for import statements in code
        for import_match in re.finditer(r'(?:import|from)\s+([.\w]+)', content):
            module = import_match.group(1)
            references.append(module)
            
        # Look for file paths in strings
        for path_match in re.finditer(r'["\'](?:\.{0,2}/)?(?:[\w-]+/)*[\w.-]+\.\w+["\']', content):
            path = path_match.group(0).strip('"\'')
            references.append(path)
            
        return references
    
    def _build_relationships(self) -> None:
        """Build relationships between documents based on references and other heuristics."""
        # Initialize relationship map
        for doc_id in self.doc_registry:
            self.relationship_map[doc_id] = {
                "references": [],
                "referenced_by": [],
                "implements": [],
                "implemented_by": [],
                "tests": [],
                "tested_by": [],
                "documents": [],
                "documented_by": []
            }
        
        # Process references to build basic relationships
        for doc_id, metadata in self.doc_registry.items():
            references = metadata.get("references", [])
            for ref in references:
                # Normalize the reference
                ref_path = self._normalize_reference(ref, doc_id)
                if ref_path in self.doc_registry:
                    # Add to relationship map
                    self.relationship_map[doc_id]["references"].append(ref_path)
                    self.relationship_map[ref_path]["referenced_by"].append(doc_id)
        
        # Infer more complex relationships
        self._infer_advanced_relationships()
        
    def _normalize_reference(self, ref: str, source_doc_id: str) -> str:
        """
        Normalize a reference to match a document ID in the registry.
        
        Args:
            ref: The reference string from the source document
            source_doc_id: The ID of the document containing the reference
            
        Returns:
            Normalized reference path that might match a document ID
        """
        # Handle import-style references
        if '.' in ref and not ref.startswith('.') and not ref.endswith(('.md', '.py', '.js', '.ts', '.yaml', '.yml')):
            # Convert "module.submodule" to potential file paths
            ref = ref.replace('.', '/') + '.py'
            
        # Handle relative paths
        if ref.startswith(('./')) or not '/' in ref:
            # Get directory of source document
            source_dir = Path(source_doc_id).parent
            ref_path = (source_dir / ref).resolve().relative_to(self.base_path)
            return str(ref_path)
            
        return ref
    
    def _infer_advanced_relationships(self) -> None:
        """Infer advanced relationships beyond direct references."""
        # Infer test relationships
        for doc_id in self.doc_registry:
            if 'tests/' in doc_id or 'test_' in doc_id:
                # This is likely a test file
                # Try to find what it tests
                implementation_path = self._infer_tested_implementation(doc_id)
                if implementation_path:
                    self.relationship_map[doc_id]["tests"].append(implementation_path)
                    self.relationship_map[implementation_path]["tested_by"].append(doc_id)
        
        # Infer documentation relationships
        for doc_id in self.doc_registry:
            if doc_id.startswith('docs/'):
                # This is documentation
                # Try to find what it documents
                documented_paths = self._infer_documented_subjects(doc_id)
                for path in documented_paths:
                    self.relationship_map[doc_id]["documents"].append(path)
                    self.relationship_map[path]["documented_by"].append(doc_id)
                    
        # Infer implementation relationships for prompt modules
        for doc_id in self.doc_registry:
            if doc_id.startswith(('prompt-library/', 'modules/')):
                # This is a prompt module
                implementation_paths = self._infer_prompt_implementations(doc_id)
                for path in implementation_paths:
                    self.relationship_map[doc_id]["implemented_by"].append(path)
                    self.relationship_map[path]["implements"].append(doc_id)
    
    def _infer_tested_implementation(self, test_path: str) -> Optional[str]:
        """Infer which implementation a test file is testing."""
        # Common patterns:
        # 1. tests/dir/test_file.py -> src/dir/file.py
        # 2. tests/test_file.py -> src/file.py
        
        if test_path.startswith('tests/'):
            potential_src_path = test_path.replace('tests/', 'src/')
            potential_src_path = potential_src_path.replace('test_', '')
            
            # Check if this path exists in our registry
            if potential_src_path in self.doc_registry:
                return potential_src_path
            
            # Try other variations
            path_parts = Path(potential_src_path).parts
            if len(path_parts) > 2:
                # Try removing a directory level
                alt_path = str(Path('src') / Path(*path_parts[2:]))
                if alt_path in self.doc_registry:
                    return alt_path
        
        return None
    
    def _infer_documented_subjects(self, doc_path: str) -> List[str]:
        """Infer which files a documentation file documents."""
        # Extract potential subjects from filename
        doc_filename = Path(doc_path).stem.lower()
        
        # Look for files with matching names
        subjects = []
        for potential_subject in self.doc_registry:
            if potential_subject == doc_path:
                continue  # Skip self
                
            subject_filename = Path(potential_subject).stem.lower()
            
            # Check for filename match
            if subject_filename in doc_filename or doc_filename in subject_filename:
                subjects.append(potential_subject)
                
            # If it's an API doc, look for potential implementations
            if 'api' in doc_filename and potential_subject.startswith('src/'):
                subjects.append(potential_subject)
                
        return subjects
    
    def _infer_prompt_implementations(self, prompt_path: str) -> List[str]:
        """Infer which files implement a prompt module."""
        # Get prompt metadata to look for clues
        prompt_metadata = self.doc_registry.get(prompt_path, {})
        prompt_name = prompt_metadata.get("front_matter", {}).get("name", "")
        
        if not prompt_name:
            return []
            
        # Extract core name without Module_ prefix
        if prompt_name.startswith("Module_"):
            core_name = prompt_name[7:].lower()
        else:
            core_name = prompt_name.lower()
            
        # Look for files that might implement this module
        implementations = []
        for potential_impl in self.doc_registry:
            if potential_impl.startswith('src/'):
                file_stem = Path(potential_impl).stem.lower()
                
                # Check for name match
                if core_name in file_stem or file_stem in core_name:
                    implementations.append(potential_impl)
                    
        return implementations
    
    def _annotate_taxonomy_layers(self) -> None:
        """Add taxonomy layer information to document registry."""
        taxonomy_layers = self.config.get("taxonomy_layers", [])
        
        for doc_id in self.doc_registry:
            layer_assigned = False
            
            for layer in taxonomy_layers:
                layer_name = layer["name"]
                layer_paths = layer["paths"]
                
                for path_prefix in layer_paths:
                    if doc_id == path_prefix or doc_id.startswith(path_prefix):
                        self.doc_registry[doc_id]["taxonomy_layer"] = layer_name
                        layer_assigned = True
                        break
                        
                if layer_assigned:
                    break
                    
            if not layer_assigned:
                self.doc_registry[doc_id]["taxonomy_layer"] = "unknown"
    
    def save_results(self, output_dir: str) -> None:
        """
        Save the processing results to output files.
        
        Args:
            output_dir: Directory to save the output files
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save document registry
        with open(output_path / "document_registry.json", 'w') as f:
            json.dump(self.doc_registry, f, indent=2)
            
        # Save relationship map
        with open(output_path / "relationship_map.json", 'w') as f:
            json.dump(self.relationship_map, f, indent=2)
            
        logger.info(f"Results saved to {output_dir}")
    
    def process_and_save(self, output_dir: str) -> None:
        """
        Process the repository and save results.
        
        Args:
            output_dir: Directory to save the output files
        """
        self.process_repository()
        self.save_results(output_dir)


def main():
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description="Process documentation and extract metadata")
    parser.add_argument("--base-path", default=".", help="Base path of the repository")
    parser.add_argument("--config", default="docs/nlu/schemas/processor_config.yaml", 
                        help="Path to configuration file")
    parser.add_argument("--output-dir", default="docs/nlu", 
                        help="Directory to save the output files")
    parser.add_argument("--mode", choices=["full", "relationships"], default="full",
                        help="Processing mode")
    
    args = parser.parse_args()
    
    processor = DocumentProcessor(args.base_path, args.config)
    
    if args.mode == "full":
        processor.process_and_save(args.output_dir)
    elif args.mode == "relationships":
        # Assume document registry already exists
        registry_path = Path(args.output_dir) / "document_registry.json"
        if registry_path.exists():
            with open(registry_path, 'r') as f:
                processor.doc_registry = json.load(f)
            processor._build_relationships()
            processor.save_results(args.output_dir)
        else:
            logger.error(f"Document registry not found at {registry_path}")
            return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
