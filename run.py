#!/usr/bin/env python3
"""
RAG AI Agent Launcher
Provides options to run the application or test the system.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_environment():
    """Check if the environment is properly set up."""
    print("🔍 Checking environment...")
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Virtual environment not detected. It's recommended to use one.")
    
    # Check if requirements are installed
    try:
        import streamlit
        import langchain
        import sentence_transformers
        import faiss
        print("✅ Core dependencies are installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    # Check if documents exist
    docs_path = Path("documents")
    if not docs_path.exists() or not list(docs_path.glob("*.txt")):
        print("⚠️  No documents found in documents/ folder")
        print("   The system will work but won't have any knowledge base")
    else:
        print("✅ Documents found")
    
    # Check if .env file exists
    env_path = Path(".env")
    if not env_path.exists():
        print("⚠️  .env file not found")
        print("   Please copy config.env.example to .env and add your OpenAI API key")
    else:
        print("✅ .env file found")
    
    return True

def run_app():
    """Run the Streamlit application."""
    print("🚀 Starting RAG AI Agent...")
    app_path = Path("src/frontend/streamlit_app.py")
    
    if not app_path.exists():
        print(f"❌ Application file not found: {app_path}")
        return
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(app_path), "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def run_tests():
    """Run the test script."""
    print("🧪 Running system tests...")
    test_path = Path("test_rag.py")
    
    if not test_path.exists():
        print(f"❌ Test file not found: {test_path}")
        return
    
    try:
        subprocess.run([sys.executable, str(test_path)])
    except Exception as e:
        print(f"❌ Error running tests: {e}")

def show_menu():
    """Show the main menu."""
    print("\n" + "=" * 50)
    print("🤖 RAG AI Agent Launcher")
    print("=" * 50)
    print("1. 🚀 Run Application")
    print("2. 🧪 Run Tests")
    print("3. 🔍 Check Environment")
    print("4. 📚 Show Help")
    print("5. 🚪 Exit")
    print("=" * 50)

def show_help():
    """Show help information."""
    print("\n📚 RAG AI Agent Help")
    print("-" * 30)
    print("This is a Retrieval-Augmented Generation AI agent that can answer")
    print("questions based on your knowledge base documents.")
    print("\nSetup:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Copy config.env.example to .env and add your OpenAI API key")
    print("3. Add .txt documents to the documents/ folder")
    print("4. Run the application")
    print("\nUsage:")
    print("- Run the app and ask questions in the chat interface")
    print("- View source documents used for each response")
    print("- Monitor system statistics in the sidebar")
    print("\nFor more information, see README.md")

def main():
    """Main launcher function."""
    while True:
        show_menu()
        
        try:
            choice = input("\nSelect an option (1-5): ").strip()
            
            if choice == "1":
                if check_environment():
                    run_app()
                else:
                    print("❌ Environment check failed. Please fix the issues above.")
            
            elif choice == "2":
                run_tests()
            
            elif choice == "3":
                check_environment()
            
            elif choice == "4":
                show_help()
            
            elif choice == "5":
                print("👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid option. Please select 1-5.")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 