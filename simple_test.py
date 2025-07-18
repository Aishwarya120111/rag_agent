#!/usr/bin/env python3
"""
Simple test to check for null bytes and basic imports.
"""

import os
import sys

print("🔍 Testing basic imports...")

try:
    import sentence_transformers
    print("✅ sentence_transformers imported successfully")
except Exception as e:
    print(f"❌ Error importing sentence_transformers: {e}")

try:
    import faiss
    print("✅ faiss imported successfully")
except Exception as e:
    print(f"❌ Error importing faiss: {e}")

try:
    import langchain
    print("✅ langchain imported successfully")
except Exception as e:
    print(f"❌ Error importing langchain: {e}")

try:
    from dotenv import load_dotenv
    print("✅ python-dotenv imported successfully")
except Exception as e:
    print(f"❌ Error importing python-dotenv: {e}")

print("\n🔍 Testing file paths...")
src_rag_path = os.path.join(os.path.dirname(__file__), 'src/rag')
src_utils_path = os.path.join(os.path.dirname(__file__), 'src/utils')

print(f"RAG path: {src_rag_path}")
print(f"Utils path: {src_utils_path}")
print(f"RAG path exists: {os.path.exists(src_rag_path)}")
print(f"Utils path exists: {os.path.exists(src_utils_path)}")

print("\n🔍 Testing document loading...")
documents_path = os.path.join(os.path.dirname(__file__), 'documents')
print(f"Documents path: {documents_path}")
print(f"Documents path exists: {os.path.exists(documents_path)}")

if os.path.exists(documents_path):
    files = os.listdir(documents_path)
    print(f"Files in documents: {files}")

print("\n✅ Basic test completed!") 