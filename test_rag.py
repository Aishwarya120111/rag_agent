#!/usr/bin/env python3
"""
Simple test script for the RAG AI Agent.
This script tests the core functionality without the Streamlit UI.
"""

import os
import sys
from dotenv import load_dotenv

# Add src directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src/rag'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'src/utils'))

from retriever import DocumentRetriever
from agent import RAGAgent
from helpers import validate_question, format_response

def test_document_loading():
    """Test document loading and processing."""
    print("🔍 Testing document loading...")
    
    try:
        retriever = DocumentRetriever()
        doc_summary = retriever.get_document_summary()
        
        print(f"✅ Successfully loaded {len(doc_summary)} documents:")
        for doc, chunks in doc_summary.items():
            print(f"   - {doc}: {chunks} chunks")
        
        return retriever
    except Exception as e:
        print(f"❌ Error loading documents: {e}")
        return None

def test_retrieval(retriever):
    """Test document retrieval."""
    print("\n🔍 Testing document retrieval...")
    
    test_queries = [
        "What is AI ethics?",
        "Explain machine learning types",
        "How does bias affect AI?",
        "What are the best practices for ML?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        try:
            results = retriever.retrieve(query, top_k=2)
            print(f"Found {len(results)} relevant chunks:")
            for i, (filename, text, metadata) in enumerate(results):
                print(f"   {i+1}. {filename} (chunk {metadata['chunk_id']})")
                print(f"      Preview: {text[:100]}...")
        except Exception as e:
            print(f"❌ Error retrieving documents: {e}")

def test_agent_response(retriever):
    """Test AI agent response generation."""
    print("\n🤖 Testing AI agent response generation...")
    
    # Check if OpenAI API key is available
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key or api_key == "your_openai_api_key_here":
        print("⚠️  OpenAI API key not configured. Skipping agent test.")
        print("   Please set your OPENAI_API_KEY in the .env file")
        return None
    
    try:
        agent = RAGAgent()
        print("✅ AI agent initialized successfully")
        
        # Test a simple query
        test_query = "What are the key principles of AI ethics?"
        print(f"\nTesting query: {test_query}")
        
        retrieved_docs = retriever.retrieve(test_query, top_k=2)
        response = agent.generate_response(test_query, retrieved_docs)
        
        print("Response:")
        print("-" * 50)
        print(response)
        print("-" * 50)
        
        return agent
    except Exception as e:
        print(f"❌ Error with AI agent: {e}")
        return None

def test_helpers():
    """Test utility functions."""
    print("\n🔧 Testing utility functions...")
    
    # Test question validation
    test_questions = [
        "What is AI?",
        "Hi",
        "",
        "This is a valid question with multiple words"
    ]
    
    for question in test_questions:
        is_valid = validate_question(question)
        print(f"Question: '{question}' -> Valid: {is_valid}")
    
    # Test text formatting
    test_text = "This   has   extra   spaces   and   punctuation  ."
    formatted = format_response(test_text)
    print(f"\nOriginal: '{test_text}'")
    print(f"Formatted: '{formatted}'")

def main():
    """Main test function."""
    print("🚀 Starting RAG AI Agent Tests")
    print("=" * 50)
    
    # Test document loading
    retriever = test_document_loading()
    if not retriever:
        print("❌ Document loading failed. Exiting.")
        return
    
    # Test retrieval
    test_retrieval(retriever)
    
    # Test agent
    agent = test_agent_response(retriever)
    
    # Test helpers
    test_helpers()
    
    print("\n" + "=" * 50)
    if agent:
        print("✅ All tests completed successfully!")
        print("🎉 Your RAG AI Agent is ready to use!")
    else:
        print("⚠️  Tests completed with warnings.")
        print("   Some features may not work without proper API configuration.")
    
    print("\nTo run the full application:")
    print("streamlit run src/frontend/streamlit_app.py")

if __name__ == "__main__":
    main() 