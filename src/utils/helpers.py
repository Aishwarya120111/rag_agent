import re
from typing import List, Dict, Any
import os

def clean_text(text: str) -> str:
    """Basic text cleaning utility."""
    return text.strip().replace('\n', ' ')

def validate_question(question: str) -> bool:
    """Validate if a question is appropriate for the RAG system."""
    if not question or len(question.strip()) < 2:
        return False
    
    # Allow single-word greetings and common small talk
    question_lower = question.strip().lower()
    single_word_greetings = ['hi', 'hello', 'hey', 'bye', 'goodbye', 'thanks', 'thank you']
    
    # If it's a single word, check if it's a valid greeting
    words = question.strip().split()
    if len(words) == 1 and question_lower in single_word_greetings:
        return True
    
    # For other cases, require at least 2 words
    if len(words) < 2:
        return False
    
    return True

def format_response(response: str) -> str:
    """Format the response for better readability."""
    # Remove extra whitespace but preserve line breaks
    response = re.sub(r'[ \t]+', ' ', response)
    
    # Ensure proper spacing around punctuation
    response = re.sub(r'\s+([.,!?])', r'\1', response)
    
    # Ensure bullet points and numbered lists are properly formatted
    response = re.sub(r'•\s*', '• ', response)
    response = re.sub(r'(\d+\.)\s*', r'\1 ', response)
    
    return response.strip()

def extract_keywords(text: str) -> List[str]:
    """Extract potential keywords from text."""
    # Remove common stop words and extract meaningful words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
    
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    
    return list(set(keywords))

def get_file_info(filepath: str) -> Dict[str, Any]:
    """Get information about a file."""
    if not os.path.exists(filepath):
        return {}
    
    stat = os.stat(filepath)
    return {
        'filename': os.path.basename(filepath),
        'size': stat.st_size,
        'modified': stat.st_mtime,
        'extension': os.path.splitext(filepath)[1]
    }

def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text to a maximum length while preserving word boundaries."""
    if len(text) <= max_length:
        return text
    
    truncated = text[:max_length]
    last_space = truncated.rfind(' ')
    
    if last_space > max_length * 0.8:  # If we can find a space in the last 20%
        return truncated[:last_space] + "..."
    else:
        return truncated + "..."