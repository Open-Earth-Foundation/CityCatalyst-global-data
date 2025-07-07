#!/usr/bin/env python3
"""
Token Calculator for Vector Database Content

This script calculates the total number of tokens for all documents 
that are loaded into the ChromaDB vector store. It uses the same 
text processing pipeline as the vectorstore creation process.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import tiktoken
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.config_loader import ConfigLoader


class TokenCalculator:
    """Calculate tokens for vector database content."""
    
    def __init__(self):
        """Initialize the token calculator."""
        self.embeddings_model = ConfigLoader.get_embeddings_model()
        self.encoding = self._get_encoding()
        
        # Use same text splitter settings as vectorstore creation
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200,
            is_separator_regex=False,
        )
        
    def _get_encoding(self) -> tiktoken.Encoding:
        """Get the appropriate tokenizer encoding for the embeddings model."""
        # Map embeddings models to their tokenizer encodings
        model_encodings = {
            "text-embedding-3-large": "cl100k_base",
            "text-embedding-3-small": "cl100k_base", 
            "text-embedding-ada-002": "cl100k_base",
            "text-embedding-3": "cl100k_base"
        }
        
        # Get encoding name, default to cl100k_base for OpenAI models
        encoding_name = model_encodings.get(self.embeddings_model, "cl100k_base")
        
        try:
            return tiktoken.get_encoding(encoding_name)
        except Exception as e:
            print(f"Warning: Could not load encoding {encoding_name}, using cl100k_base")
            return tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in a text string."""
        return len(self.encoding.encode(text))
    
    def load_and_split_documents(self, file_path: str) -> List[Any]:
        """Load and split documents using the same method as vectorstore creation."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        print(f"Loading PDF: {file_path}")
        
        # Load PDF file (same as vectorstore_creation.py)
        loader = PyPDFLoader(file_path)
        
        # Split PDF using text splitter (same settings as vectorstore_creation.py)
        pages = loader.load_and_split(self.text_splitter)
        
        print(f"Document split into {len(pages)} chunks")
        return pages
    
    def calculate_total_tokens(self, file_path: str) -> Dict[str, Any]:
        """Calculate total tokens for all documents."""
        print("=" * 60)
        print("🔢 TOKEN CALCULATION FOR VECTOR DATABASE")
        print("=" * 60)
        
        # Load and split documents
        documents = self.load_and_split_documents(file_path)
        
        # Calculate tokens for each chunk
        chunk_tokens = []
        total_tokens = 0
        
        print("\nCalculating tokens for each chunk...")
        
        for i, doc in enumerate(documents):
            tokens = self.count_tokens(doc.page_content)
            chunk_tokens.append(tokens)
            total_tokens += tokens
            
            if (i + 1) % 50 == 0:  # Progress update every 50 chunks
                print(f"Processed {i + 1}/{len(documents)} chunks...")
        
        # Calculate statistics
        avg_tokens = total_tokens / len(documents) if documents else 0
        max_tokens = max(chunk_tokens) if chunk_tokens else 0
        min_tokens = min(chunk_tokens) if chunk_tokens else 0
        
        # Cost estimation (approximate, based on OpenAI pricing)
        cost_per_1k_tokens = 0.0001  # $0.0001 per 1K tokens for text-embedding-3-large
        estimated_cost = (total_tokens / 1000) * cost_per_1k_tokens
        
        results = {
            "file_path": file_path,
            "embeddings_model": self.embeddings_model,
            "total_chunks": len(documents),
            "total_tokens": total_tokens,
            "average_tokens_per_chunk": round(avg_tokens, 2),
            "max_tokens_per_chunk": max_tokens,
            "min_tokens_per_chunk": min_tokens,
            "estimated_embedding_cost": round(estimated_cost, 4),
            "chunk_size_setting": 2000,
            "chunk_overlap_setting": 200
        }
        
        return results
    
    def print_results(self, results: Dict[str, Any]):
        """Print formatted results."""
        print("\n" + "=" * 60)
        print("📊 RESULTS")
        print("=" * 60)
        
        print(f"📄 File: {Path(results['file_path']).name}")
        print(f"🤖 Embeddings Model: {results['embeddings_model']}")
        print(f"📑 Total Chunks: {results['total_chunks']:,}")
        print(f"🎯 Total Tokens: {results['total_tokens']:,}")
        print(f"📈 Average Tokens/Chunk: {results['average_tokens_per_chunk']:,}")
        print(f"📊 Token Range: {results['min_tokens_per_chunk']:,} - {results['max_tokens_per_chunk']:,}")
        print(f"💰 Estimated Embedding Cost: ${results['estimated_embedding_cost']}")
        
        print(f"\n⚙️ Settings:")
        print(f"   Chunk Size: {results['chunk_size_setting']:,}")
        print(f"   Chunk Overlap: {results['chunk_overlap_setting']:,}")
        
        # Memory usage estimation
        avg_chars_per_token = 4  # Rough estimate
        estimated_memory_mb = (results['total_tokens'] * avg_chars_per_token) / (1024 * 1024)
        print(f"   Estimated Memory Usage: ~{estimated_memory_mb:.1f} MB")
        
        print("\n" + "=" * 60)
    
    def save_results(self, results: Dict[str, Any], output_file: str = "token_analysis.json"):
        """Save results to a JSON file."""
        import json
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to: {output_file}")


def main():
    """Main function to calculate tokens for vector database content."""
    try:
        # Initialize calculator
        calculator = TokenCalculator()
        
        # Default file path (same as used in vectorstore_creation.py)
        default_file_path = "./files/GPC_Full_MASTER_RW_v7.pdf"
        
        # Check if file exists
        if not os.path.exists(default_file_path):
            print(f"❌ Error: File not found at {default_file_path}")
            print("Please ensure the GPC_Full_MASTER_RW_v7.pdf file is in the ./files/ directory")
            sys.exit(1)
        
        # Calculate tokens
        results = calculator.calculate_total_tokens(default_file_path)
        
        # Print results
        calculator.print_results(results)
        
        # Save results
        calculator.save_results(results)
        
        print("✅ Token calculation completed successfully!")
        
    except FileNotFoundError as e:
        print(f"❌ File Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 