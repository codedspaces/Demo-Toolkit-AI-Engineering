#!/usr/bin/env python3
"""
AI Toolkit RAG System

A complete Retrieval-Augmented Generation system for querying the AI Engineering Toolkit
knowledge base. This system allows users to ask questions about AI tools, frameworks,
and best practices.

Features:
- Vector-based similarity search
- LLM-powered response generation
- Tool recommendation system
- Context-aware conversations

Usage:
    python ai_toolkit_rag.py --query "What are the best LLM inference tools?"
"""

import os
import sys
import argparse
import json
import pickle
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import openai
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
import requests
from sentence_transformers import SentenceTransformer
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ToolInfo:
    """Data class for AI tool information"""
    name: str
    description: str
    category: str
    url: str
    github_stars: Optional[int] = None
    use_cases: List[str] = None
    pros: List[str] = None
    cons: List[str] = None

class AIToolkitKnowledgeBase:
    """Knowledge base of AI tools and frameworks"""
    
    def __init__(self):
        self.tools = self._load_toolkit_data()
    
    def _load_toolkit_data(self) -> List[ToolInfo]:
        """Load AI toolkit data from various sources"""
        tools = []
        
        # LLM Tools
        llm_tools = [
            ToolInfo(
                name="vLLM",
                description="High-throughput and memory-efficient inference and serving engine for LLMs",
                category="LLM Inference",
                url="https://github.com/vllm-project/vllm",
                github_stars=15000,
                use_cases=["High-throughput inference", "Model serving", "Batch processing"],
                pros=["Excellent performance", "Memory efficient", "Easy to use"],
                cons=["GPU memory requirements", "Limited model support"]
            ),
            ToolInfo(
                name="LangChain",
                description="Framework for developing applications powered by large language models",
                category="LLM Framework",
                url="https://github.com/langchain-ai/langchain",
                github_stars=75000,
                use_cases=["LLM applications", "RAG systems", "AI agents"],
                pros=["Comprehensive framework", "Great documentation", "Active community"],
                cons=["Can be complex", "Frequent API changes"]
            ),
            ToolInfo(
                name="Ollama",
                description="Run large language models locally",
                category="Local Inference",
                url="https://ollama.ai",
                use_cases=["Local deployment", "Privacy-focused applications", "Development"],
                pros=["Easy local deployment", "Privacy", "No API costs"],
                cons=["Hardware requirements", "Limited performance"]
            ),
            ToolInfo(
                name="Unsloth",
                description="2x faster LLM fine-tuning with less memory",
                category="Fine-tuning",
                url="https://github.com/unslothai/unsloth",
                github_stars=8000,
                use_cases=["Model fine-tuning", "Custom model training", "Memory optimization"],
                pros=["Memory efficient", "Fast training", "Easy to use"],
                cons=["Limited model support", "Beta software"]
            )
        ]
        
        # Vector Databases
        vector_dbs = [
            ToolInfo(
                name="Chroma",
                description="Open-source embedding database for building AI applications",
                category="Vector Database",
                url="https://github.com/chroma-core/chroma",
                github_stars=12000,
                use_cases=["RAG systems", "Semantic search", "Embeddings storage"],
                pros=["Easy to use", "Open source", "Good documentation"],
                cons=["Performance limitations", "Limited enterprise features"]
            ),
            ToolInfo(
                name="Pinecone",
                description="Vector database for ML applications",
                category="Vector Database", 
                url="https://www.pinecone.io",
                use_cases=["Production RAG", "Semantic search", "Recommendation systems"],
                pros=["Excellent performance", "Managed service", "Scalable"],
                cons=["Cost", "Vendor lock-in"]
            )
        ]
        
        # MLOps Tools
        mlops_tools = [
            ToolInfo(
                name="MLflow",
                description="ML lifecycle management platform",
                category="MLOps",
                url="https://github.com/mlflow/mlflow",
                github_stars=16000,
                use_cases=["Experiment tracking", "Model registry", "Model deployment"],
                pros=["Comprehensive platform", "Open source", "Language agnostic"],
                cons=["Setup complexity", "UI limitations"]
            ),
            ToolInfo(
                name="Weights & Biases",
                description="ML experiment tracking and visualization",
                category="MLOps",
                url="https://wandb.ai",
                use_cases=["Experiment tracking", "Model monitoring", "Collaboration"],
                pros=["Excellent UI", "Great collaboration features", "Comprehensive tracking"],
                cons=["Cost for teams", "Cloud dependency"]
            )
        ]
        
        tools.extend(llm_tools)
        tools.extend(vector_dbs)
        tools.extend(mlops_tools)
        
        return tools
    
    def get_tools_by_category(self, category: str) -> List[ToolInfo]:
        """Get tools filtered by category"""
        return [tool for tool in self.tools if tool.category.lower() == category.lower()]
    
    def search_tools(self, query: str) -> List[ToolInfo]:
        """Search tools by name or description"""
        query_lower = query.lower()
        return [
            tool for tool in self.tools 
            if query_lower in tool.name.lower() or query_lower in tool.description.lower()
        ]

class VectorStore:
    """Vector store for semantic search using ChromaDB"""
    
    def __init__(self, collection_name: str = "ai_toolkit"):
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./chromadb"
        ))
        self.collection_name = collection_name
        self.collection = None
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    def create_collection(self, tools: List[ToolInfo]):
        """Create and populate vector collection"""
        try:
            # Delete existing collection if it exists
            try:
                self.client.delete_collection(self.collection_name)
            except:
                pass
            
            # Create new collection
            self.collection = self.client.create_collection(self.collection_name)
            
            # Prepare documents
            documents = []
            metadatas = []
            ids = []
            
            for i, tool in enumerate(tools):
                # Create comprehensive document text
                doc_text = f"""
                Tool: {tool.name}
                Category: {tool.category}
                Description: {tool.description}
                Use Cases: {', '.join(tool.use_cases or [])}
                Pros: {', '.join(tool.pros or [])}
                Cons: {', '.join(tool.cons or [])}
                """
                
                documents.append(doc_text.strip())
                metadatas.append({
                    "name": tool.name,
                    "category": tool.category,
                    "url": tool.url,
                    "github_stars": tool.github_stars or 0
                })
                ids.append(f"tool_{i}")
            
            # Add to collection
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Created collection with {len(documents)} tools")
            
        except Exception as e:
            logger.error(f"Error creating collection: {str(e)}")
            raise
    
    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search for relevant tools"""
        if not self.collection:
            self.collection = self.client.get_collection(self.collection_name)
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # Format results
            formatted_results = []
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    'document': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching collection: {str(e)}")
            return []

class RAGGenerator:
    """RAG-based response generator"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = openai.OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
    
    def generate_response(self, query: str, context_docs: List[Dict], 
                         conversation_history: List[Dict] = None) -> str:
        """Generate response using RAG approach"""
        
        # Prepare context from retrieved documents
        context = "\n\n".join([
            f"Tool: {doc['metadata']['name']}\n"
            f"Category: {doc['metadata']['category']}\n" 
            f"Details: {doc['document']}"
            for doc in context_docs
        ])
        
        # Prepare conversation history
        messages = []
        if conversation_history:
            messages.extend(conversation_history)
        
        # System prompt
        system_prompt = """
        You are an AI Engineering expert assistant. Your role is to help users find and understand 
        AI tools, frameworks, and best practices. Use the provided context to give accurate, 
        helpful recommendations.
        
        Guidelines:
        - Provide specific tool recommendations based on user needs
        - Explain pros and cons of different options
        - Include practical usage advice
        - Suggest alternatives when appropriate
        - Be honest about limitations
        """
        
        # User prompt with context
        user_prompt = f"""
        User Query: {query}
        
        Relevant Tools and Information:
        {context}
        
        Please provide a comprehensive answer that addresses the user's query using the above information.
        Include specific tool recommendations, use cases, and any important considerations.
        """
        
        messages.extend([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                max_tokens=1000,
                temperature=0.3
            )
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I apologize, but I encountered an error generating a response. Please try again."

class AIToolkitRAG:
    """Main RAG system for AI Toolkit queries"""
    
    def __init__(self):
        self.kb = AIToolkitKnowledgeBase()
        self.vector_store = VectorStore()
        self.generator = RAGGenerator()
        self.conversation_history = []
        
        # Initialize vector store
        self._setup_vector_store()
    
    def _setup_vector_store(self):
        """Set up vector store with tool data"""
        logger.info("Setting up vector store...")
        self.vector_store.create_collection(self.kb.tools)
        logger.info("Vector store ready!")
    
    def query(self, question: str, include_history: bool = True) -> str:
        """Process a query and return response"""
        logger.info(f"Processing query: {question}")
        
        # Search for relevant tools
        relevant_docs = self.vector_store.search(question, n_results=5)
        
        # Generate response
        history = self.conversation_history if include_history else None
        response = self.generator.generate_response(question, relevant_docs, history)
        
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": question})
        self.conversation_history.append({"role": "assistant", "content": response})
        
        # Keep history manageable
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
        
        return response
    
    def get_tool_recommendations(self, category: str = None, use_case: str = None) -> List[ToolInfo]:
        """Get tool recommendations based on category or use case"""
        if category:
            return self.kb.get_tools_by_category(category)
        elif use_case:
            return self.kb.search_tools(use_case)
        else:
            return self.kb.tools
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")

def main():
    """Main function for command-line interface"""
    parser = argparse.ArgumentParser(description='AI Toolkit RAG System')
    parser.add_argument('--query', help='Query to process')
    parser.add_argument('--interactive', action='store_true', help='Start interactive mode')
    parser.add_argument('--category', help='Get tools by category')
    parser.add_argument('--setup', action='store_true', help='Setup vector store only')
    
    args = parser.parse_args()
    
    # Check for required environment variables
    if not os.getenv('OPENAI_API_KEY'):
        logger.error("OPENAI_API_KEY environment variable is required")
        sys.exit(1)
    
    try:
        # Initialize RAG system
        rag = AIToolkitRAG()
        
        if args.setup:
            logger.info("Vector store setup completed!")
            return
        
        if args.category:
            tools = rag.get_tool_recommendations(category=args.category)
            print(f"\n=== Tools in category: {args.category} ===")
            for tool in tools:
                print(f"\n{tool.name}: {tool.description}")
                print(f"URL: {tool.url}")
            return
        
        if args.query:
            response = rag.query(args.query)
            print(f"\nQuery: {args.query}")
            print(f"\nResponse:\n{response}")
        
        elif args.interactive:
            print("\n🤖 AI Toolkit RAG System - Interactive Mode")
            print("Ask questions about AI tools and frameworks!")
            print("Commands: 'clear' to clear history, 'quit' to exit\n")
            
            while True:
                try:
                    query = input("🔍 Your question: ").strip()
                    
                    if query.lower() in ['quit', 'exit', 'q']:
                        break
                    elif query.lower() == 'clear':
                        rag.clear_history()
                        print("✅ Conversation history cleared")
                        continue
                    elif not query:
                        continue
                    
                    response = rag.query(query)
                    print(f"\n🤖 Response:\n{response}\n")
                    print("-" * 60)
                    
                except KeyboardInterrupt:
                    print("\n\nGoodbye!")
                    break
                except Exception as e:
                    print(f"Error: {str(e)}")
        
        else:
            print("Please provide --query, --interactive, or --category option")
            parser.print_help()
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()