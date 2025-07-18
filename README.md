# 🤖 RAG AI Agent

A powerful Retrieval-Augmented Generation (RAG) AI agent that provides intelligent responses based on your knowledge base documents. This agent combines the power of large language models with semantic search to deliver accurate, context-aware answers.

## ✨ Features

- **📚 Document Processing**: Automatically processes and chunks documents for efficient retrieval
- **🔍 Semantic Search**: Uses advanced embeddings to find the most relevant document chunks
- **🤖 AI-Powered Responses**: Generates intelligent responses using OpenAI's GPT models
- **💬 Interactive Chat Interface**: Modern Streamlit-based chat interface with conversation history
- **📊 Real-time Statistics**: Monitor system performance and document statistics
- **🎨 Beautiful UI**: Clean, responsive design with intuitive user experience
- **🔧 Configurable**: Easy configuration through environment variables

## 🏗️ Architecture

The RAG agent consists of several key components:

1. **Document Retriever** (`src/rag/retriever.py`): Handles document loading, chunking, and semantic search
2. **AI Agent** (`src/rag/agent.py`): Manages LLM interactions and response generation
3. **Frontend** (`src/frontend/streamlit_app.py`): Modern web interface built with Streamlit
4. **Utilities** (`src/utils/helpers.py`): Helper functions for text processing and validation

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Virtual environment (recommended)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd rag_agent
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   # Copy the example config file
   cp config.env.example .env
   
   # Edit .env and add your OpenAI API key
   OPENAI_API_KEY=your_actual_api_key_here
   ```

5. **Add your documents**:
   - Place your `.txt` files in the `documents/` folder
   - The system will automatically process them on startup

6. **Run the application**:
   ```bash
   streamlit run src/frontend/streamlit_app.py
   ```

7. **Open your browser** and navigate to `http://localhost:8501`

## 📁 Project Structure

```
rag_agent/
├── documents/                 # Knowledge base documents
│   ├── ai_ethics.txt
│   └── machine_learning_basics.txt
├── src/
│   ├── rag/                   # RAG system components
│   │   ├── retriever.py       # Document retrieval and search
│   │   └── agent.py          # AI agent and response generation
│   ├── frontend/              # User interface
│   │   └── streamlit_app.py   # Streamlit web application
│   └── utils/                 # Utility functions
│       └── helpers.py         # Text processing and validation
├── venv/                      # Virtual environment
├── requirements.txt           # Python dependencies
├── config.env.example         # Environment variables template
└── README.md                  # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Model Configuration
DEFAULT_MODEL=gpt-3.5-turbo
TEMPERATURE=0.7

# Document Processing Configuration
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Retrieval Configuration
TOP_K_RESULTS=3
```

### Supported Document Formats

Currently supports:
- `.txt` files (UTF-8 encoded)

## 💡 Usage

### Basic Usage

1. **Start the application** using the command above
2. **Load components** by clicking the "Load Components" button
3. **Ask questions** in the chat interface
4. **View sources** by expanding the "Sources" section in responses

### Example Questions

- "What are the key principles of AI ethics?"
- "Explain the different types of machine learning"
- "How does bias affect AI systems?"
- "What are the best practices for ML development?"

### Features

- **Conversation History**: All chat messages are preserved during the session
- **Source Attribution**: View the specific documents used to generate responses
- **Quick Actions**: Pre-defined buttons for common questions
- **System Statistics**: Monitor document counts and system performance
- **Clear Chat**: Reset conversation history

## 🛠️ Development

### Adding New Features

1. **Document Processing**: Extend `DocumentRetriever` to support more file formats
2. **Response Generation**: Modify `RAGAgent` to use different LLM providers
3. **UI Enhancements**: Customize the Streamlit interface in `streamlit_app.py`
4. **Utilities**: Add new helper functions in `helpers.py`

### Testing

```bash
# Run the application in development mode
streamlit run src/frontend/streamlit_app.py --server.port 8501
```

### Dependencies

Key dependencies include:
- `streamlit`: Web interface framework
- `langchain`: LLM framework and utilities
- `langchain-openai`: OpenAI integration
- `sentence-transformers`: Text embeddings
- `faiss-cpu`: Vector similarity search
- `python-dotenv`: Environment variable management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT models
- Streamlit for the excellent web framework
- LangChain for the RAG framework
- Sentence Transformers for text embeddings
- FAISS for efficient similarity search

## 🆘 Support

If you encounter any issues:

1. Check that all dependencies are installed correctly
2. Verify your OpenAI API key is valid
3. Ensure your documents are in the correct format
4. Check the console for error messages

For additional help, please open an issue on the repository.

---

**Happy chatting with your RAG AI Agent! 🤖✨** 