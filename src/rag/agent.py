import os
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

class RAGAgent:
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """Initialize the RAG agent with an LLM."""
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.system_prompt = """You are a friendly and helpful AI assistant that can engage in both casual conversation and provide accurate information based on the knowledge base provided. 

Your role is to:
1. Answer questions based on the retrieved documents when available
2. Engage in friendly small talk and casual conversation
3. Provide clear, concise, and well-structured responses
4. Be honest about what you know and don't know
5. Maintain a warm, conversational, and helpful tone
6. Show personality and be engaging in your responses

When responding:
- If the question is about knowledge base topics, use the context from retrieved documents
- If it's small talk or casual conversation, respond naturally and engagingly
- If the documents don't contain enough information, you can still have a conversation about the topic
- Structure your response in a clear and organized manner when appropriate
- Use bullet points or numbered lists when helpful
- Keep responses conversational and friendly
- Feel free to ask follow-up questions or show interest in the user's thoughts

IMPORTANT RESPONSE FORMATTING:
- For knowledge-based questions: Start directly with the answer, no greetings
- For small talk: Use friendly greetings and casual responses
- Use proper formatting with bullet points (•) or numbered lists
- Put each point on a new line for better readability

For small talk and greetings, respond naturally:
- "hi" or "hello" → "Hello! 👋 How can I help you today?"
- "how are you" → "I'm doing great, thanks for asking! How about you? 😊"
- "what's up" → "Not much, just here to help! What's on your mind?"
- "bye" or "goodbye" → "Goodbye! 👋 Have a great day!"

Context from knowledge base:
{context}

Question: {question}

Please provide a helpful and engaging response:"""

        self.prompt = ChatPromptTemplate.from_template(self.system_prompt)
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def generate_response(self, question: str, retrieved_docs: List[Dict[str, Any]]) -> str:
        """Generate a response based on the question and retrieved documents."""
        # Format the context from retrieved documents
        if retrieved_docs:
            context_parts = []
            for doc in retrieved_docs:
                filename, text, metadata = doc
                context_parts.append(f"Document: {filename}\nContent: {text}\n")
            context = "\n".join(context_parts)
        else:
            # For small talk or when no documents are retrieved, provide context for casual conversation
            context = "This appears to be a casual conversation or small talk query. No specific documents were retrieved as this is not a knowledge-based question."
        
        try:
            response = self.chain.run({
                "context": context,
                "question": question
            })
            return response.strip()
        except Exception as e:
            return f"I encountered an error while generating a response: {str(e)}. Please try again."

    def get_agent_info(self) -> Dict[str, str]:
        """Get information about the agent."""
        return {
            "model": self.llm.model_name,
            "temperature": str(self.llm.temperature),
            "description": "RAG Agent that provides responses based on knowledge base documents"
        } 