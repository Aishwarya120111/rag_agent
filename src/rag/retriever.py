import os
import re
from typing import List, Tuple, Dict
from sentence_transformers import SentenceTransformer
import faiss
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken

DOCUMENTS_PATH = os.path.join(os.path.dirname(__file__), '../../documents')
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

class DocumentRetriever:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        self.documents, self.chunks, self.chunk_texts = self.load_and_process_documents()
        self.index = self.create_index(self.chunk_texts)

    def load_and_process_documents(self) -> Tuple[List[str], List[Dict], List[str]]:
        """Load documents and split them into chunks."""
        documents = []
        chunks = []
        chunk_texts = []
        
        for fname in os.listdir(DOCUMENTS_PATH):
            fpath = os.path.join(DOCUMENTS_PATH, fname)
            if fname.endswith('.txt'):
                with open(fpath, 'r', encoding='utf-8') as f:
                    text = f.read()
                    
                # Split text into chunks
                text_chunks = self.text_splitter.split_text(text)
                
                for i, chunk in enumerate(text_chunks):
                    documents.append(fname)
                    chunks.append({
                        'filename': fname,
                        'chunk_id': i,
                        'start_char': text.find(chunk),
                        'end_char': text.find(chunk) + len(chunk)
                    })
                    chunk_texts.append(chunk)
        
        return documents, chunks, chunk_texts

    def create_index(self, texts: List[str]):
        """Create FAISS index from text embeddings."""
        if not texts:
            return None
        
        embeddings = self.model.encode(texts)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        return index

    def is_small_talk(self, query: str) -> bool:
        """Detect if the query is small talk or casual conversation."""
        small_talk_patterns = [
            r'\b(hi|hello|hey|good morning|good afternoon|good evening)\b',
            r'\bhow are you\b',
            r'\bhow\'s it going\b',
            r'\bwhat\'s up\b',
            r'\bhow do you do\b',
            r'\bthanks? you\b',
            r'\bthank you\b',
            r'\bbye|goodbye|see you\b',
            r'\bweather\b',
            r'\bweekend\b',
            r'\bhobby|hobbies\b',
            r'\bweekend plans\b',
            r'\bday\b.*\bgoing\b',
            r'\bnice to meet you\b',
            r'\bpleasure\b',
            r'\bgood\b.*\bday\b',
            r'\bhave a good\b',
            r'\btake care\b'
        ]
        
        query_lower = query.lower()
        for pattern in small_talk_patterns:
            if re.search(pattern, query_lower):
                return True
        return False

    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[str, str, Dict]]:
        """Retrieve relevant document chunks for a query."""
        if not self.index or not self.chunk_texts:
            return []
        
        # For small talk, return empty results to let the agent handle it conversationally
        if self.is_small_talk(query):
            return []
        
        query_emb = self.model.encode([query])
        D, I = self.index.search(query_emb, top_k)
        
        results = []
        for i, (distance, idx) in enumerate(zip(D[0], I[0])):
            if idx < len(self.chunk_texts):
                results.append((
                    self.documents[idx],
                    self.chunk_texts[idx],
                    self.chunks[idx]
                ))
        
        return results

    def get_document_summary(self) -> Dict[str, int]:
        """Get summary of loaded documents."""
        doc_counts = {}
        for doc in self.documents:
            doc_counts[doc] = doc_counts.get(doc, 0) + 1
        return doc_counts 