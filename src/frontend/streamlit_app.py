# -*- coding: utf-8 -*-
import streamlit as st
import sys
import os
from datetime import datetime

# Add src directories to the path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../rag')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))

from retriever import DocumentRetriever
from agent import RAGAgent
from helpers import validate_question, format_response, truncate_text, extract_keywords

# Page configuration
st.set_page_config(
    page_title="RAG AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left-color: #9c27b0;
    }
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message only once
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hello! 👋 I'm your RAG AI Agent. I can help you with questions about your knowledge base documents, or we can just chat! What would you like to know?",
            "timestamp": datetime.now()
        })
    if "welcome_added" not in st.session_state:
        st.session_state.welcome_added = True
    if "retriever" not in st.session_state:
        st.session_state.retriever = None
    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "documents_loaded" not in st.session_state:
        st.session_state.documents_loaded = False

def load_components():
    """Load RAG components."""
    try:
        with st.spinner("Loading document retriever..."):
            st.session_state.retriever = DocumentRetriever()
        
        with st.spinner("Initializing AI agent..."):
            st.session_state.agent = RAGAgent()
        
        st.session_state.documents_loaded = True
        st.success("✅ Components loaded successfully!")
        
    except Exception as e:
        st.error(f"❌ Error loading components: {str(e)}")
        st.info("Please check your configuration and try again.")

def display_sidebar():
    """Display sidebar with system information and controls."""
    with st.sidebar:
        st.markdown('<div class="sidebar-header">🤖 RAG AI Agent</div>', unsafe_allow_html=True)
        
        # System status
        if st.session_state.documents_loaded:
            st.success("✅ System Ready")
            
            # Document summary - commented out as requested
            # doc_summary = st.session_state.retriever.get_document_summary()
            # st.markdown("### 📚 Knowledge Base")
            # for doc, chunks in doc_summary.items():
            #     st.write(f"• {doc}: {chunks} chunks")
            
            # Agent info
            agent_info = st.session_state.agent.get_agent_info()
            st.markdown("### 🤖 Agent Info")
            st.write(f"Model: {agent_info['model']}")
            st.write(f"Temperature: {agent_info['temperature']}")
            
        else:
            st.warning("⚠️ System Not Ready")
            if st.button("🔄 Load Components"):
                load_components()
        
        # Controls
        st.markdown("### ⚙️ Controls")
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.welcome_added = False
            st.rerun()
        
        if st.button("📊 Show Statistics"):
            show_statistics()

def show_statistics():
    """Show system statistics."""
    if not st.session_state.documents_loaded:
        st.warning("Please load components first.")
        return
    
    st.markdown("### 📊 System Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        doc_summary = st.session_state.retriever.get_document_summary()
        total_chunks = sum(doc_summary.values())
        st.metric("Total Chunks", total_chunks)
    
    with col2:
        st.metric("Documents", len(doc_summary))
    
    with col3:
        st.metric("Chat Messages", len(st.session_state.messages))

def display_chat_message(role: str, content: str, sources: list = None):
    """Display a chat message with proper styling."""
    if role == "user":
        st.chat_message("user").write(content)
    else:
        with st.chat_message("assistant"):
            st.write(content)
            if sources and len(sources) > 0:
                with st.expander("📚 Sources"):
                    for i, (filename, text, metadata) in enumerate(sources):
                        st.markdown(f"**Source {i+1}: {filename}**")
                        st.text(truncate_text(text, 300))

def process_user_input(user_input: str):
    """Process user input and generate response."""
    if not validate_question(user_input):
        st.warning("Please enter a valid question (at least 2 words).")
        return
    
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input, "timestamp": datetime.now()})
    
    # Retrieve relevant documents
    with st.spinner("🔍 Searching knowledge base..."):
        retrieved_docs = st.session_state.retriever.retrieve(user_input, top_k=3)
    
    # Generate response
    with st.spinner("🤖 Generating response..."):
        response = st.session_state.agent.generate_response(user_input, retrieved_docs)
        # Remove question repetition from response
        response = format_response(response)
        # Clean up response to remove question repetition
        if "Based on the information provided in the retrieved documents, here is a helpful response to the question" in response:
            # Extract the actual response part
            response = response.split(":", 1)[-1].strip()
            if response.startswith("'"):
                response = response[1:]
            if response.endswith("'"):
                response = response[:-1]
    
    # Add assistant message to chat
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response, 
        "sources": retrieved_docs,
        "timestamp": datetime.now()
    })

def main():
    """Main application function."""
    initialize_session_state()
    
    # Auto-load components on startup
    if not st.session_state.documents_loaded:
        load_components()
    
    # Header
    st.markdown('<div class="main-header">🤖 RAG AI Agent</div>', unsafe_allow_html=True)
    st.markdown("Ask me anything based on the knowledge base documents!")
    
    # Sidebar
    display_sidebar()
    
    # Main content area
    if not st.session_state.documents_loaded:
        st.info("👋 Loading system components...")
        st.rerun()
        return
    
    # Chat interface
    st.markdown("### 💬 Chat")
    
    # Display chat history
    for i, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            display_chat_message("user", message["content"])
        else:
            sources = message.get("sources", [])
            display_chat_message("assistant", message["content"], sources)
    
    # User input
    user_input = st.chat_input("Ask a question...")
    
    if user_input:
        process_user_input(user_input)
        st.rerun()
    
    # Quick action buttons - commented out as requested
    # st.markdown("### 💡 Quick Actions")
    # col1, col2, col3 = st.columns(3)
    
    # with col1:
    #     if st.button("❓ What is AI ethics?"):
    #         process_user_input("What are the key principles of AI ethics?")
    #         st.rerun()
    
    # with col2:
    #     if st.button("📚 Explain machine learning"):
    #         process_user_input("What are the main types of machine learning?")
    #         st.rerun()
    
    # with col3:
    #     if st.button("🔍 How does RAG work?"):
    #         process_user_input("How does retrieval augmented generation work?")
    #         st.rerun()

if __name__ == "__main__":
    main() 