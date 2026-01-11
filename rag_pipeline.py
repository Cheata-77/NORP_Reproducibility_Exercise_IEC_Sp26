from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
import re

class RAGPipeline:
    def __init__(self, texts):
        self.texts = texts
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = self.embedder.encode(texts, convert_to_tensor=True)
        
        # Use a simpler approach to avoid memory issues
        self.model_type = 'extraction'  # Use extraction instead of generation
        print("Using: keyword extraction (no data loss)")

    def query(self, question, top_k=5):  # Increase top_k to get more relevant chunks
        question_embedding = self.embedder.encode([question], convert_to_tensor=True)
        similarities = cosine_similarity(question_embedding.cpu(), self.embeddings.cpu())[0]
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        # Get all relevant chunks (no truncation)
        relevant_chunks = [self.texts[i] for i in top_indices]
        
        # Extract answer from relevant chunks without losing data
        answer = self._extract_answer_from_chunks(relevant_chunks, question)
        return answer

    def _extract_answer_from_chunks(self, chunks, question):
        """Extract answer from multiple chunks without data loss"""
        question_lower = question.lower()
        
        # Look for specific data patterns based on question
        if any(word in question_lower for word in ['count', 'number', 'how many']):
            return self._extract_counts(chunks, question)
        elif 'year' in question_lower or '2022' in question_lower:
            return self._extract_year_data(chunks, question)
        else:
            # Return the most relevant chunks as-is
            return f"Most relevant data found:\n\n" + "\n\n---\n\n".join(chunks[:3])

    def _extract_counts(self, chunks, question):
        """Extract count-related information"""
        results = []
        for chunk in chunks:
            if 'mortgage' in question.lower() and 'mortgage' in chunk.lower():
                results.append(f"Relevant data chunk:\n{chunk}")
        
        if results:
            return "\n\n---\n\n".join(results)
        else:
            return f"Found {len(chunks)} relevant data chunks, but no specific mortgage counts. Here's the most relevant data:\n\n{chunks[0] if chunks else 'No data found'}"

    def _extract_year_data(self, chunks, question):
        """Extract year-specific information"""
        year_chunks = []
        for chunk in chunks:
            if '2022' in chunk or 'year' in chunk.lower():
                year_chunks.append(chunk)
        
        if year_chunks:
            return f"Data for year 2022:\n\n" + "\n\n---\n\n".join(year_chunks)
        else:
            return f"Most relevant chunks (may contain year data):\n\n" + "\n\n---\n\n".join(chunks[:2])