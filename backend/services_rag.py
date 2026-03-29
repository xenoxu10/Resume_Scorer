from typing import List, Dict, Tuple
try:
    from .services_embeddings import get_embeddings, chunk_text, cosine_similarity
except ImportError:
    from services_embeddings import get_embeddings, chunk_text, cosine_similarity


class RAGRetriever:
    """Retrieval-Augmented Generation for resume scoring"""
    
    def __init__(self, top_k: int = 5):
        self.top_k = top_k
        self.chunks: List[str] = []
        self.embeddings: List[List[float]] = []
    
    def index_document(self, text: str) -> None:
        """
        Index a document by chunking and embedding it
        
        Args:
            text: Document text to index
        """
        self.chunks = chunk_text(text, chunk_size=500, overlap=100)
        if self.chunks:
            self.embeddings = get_embeddings(self.chunks)
    
    def retrieve(self, query: str) -> List[str]:
        """
        Retrieve relevant chunks for a query
        
        Args:
            query: Query text
        
        Returns:
            Top-k relevant chunks
        """
        if not self.chunks or not self.embeddings:
            return []
        
        # Get query embedding
        query_embedding = get_embeddings([query])[0]
        
        # Calculate similarities
        similarities = []
        for i, embedding in enumerate(self.embeddings):
            similarity = cosine_similarity(query_embedding, embedding)
            similarities.append((similarity, i, self.chunks[i]))
        
        # Sort by similarity and return top-k
        similarities.sort(reverse=True, key=lambda x: x[0])
        retrieved_chunks = [item[2] for item in similarities[:self.top_k] if item[0] > 0.0]
        
        return retrieved_chunks


def extract_key_requirements(jd: str) -> Dict[str, List[str]]:
    """
    Extract key requirements from job description using RAG and LLM
    
    Args:
        jd: Job description text
    
    Returns:
        Dictionary of requirements by category
    """
    from openai import OpenAI
    from config import settings
    
    client = OpenAI(api_key=settings.openai_api_key)
    
    prompt = f"""Analyze the following Job Description and extract key requirements.
Categorize them into: Skills, Experience, Education, and Other Requirements.

Job Description:
{jd}

Return the response as JSON with these categories. Be concise."""
    
    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": "You are an expert recruiter analyzing job descriptions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=500
    )
    
    try:
        # Try to parse the response as JSON
        import json
        content = response.choices[0].message.content
        # Find JSON in the response
        start_idx = content.find('{')
        end_idx = content.rfind('}') + 1
        if start_idx != -1 and end_idx > start_idx:
            parsed = json.loads(content[start_idx:end_idx])
            # Ensure all values are lists
            result = {}
            for key, value in parsed.items():
                if isinstance(value, list):
                    result[key] = [str(v).strip() for v in value if v]
                else:
                    result[key] = [str(value).strip()] if value else []
            return result
    except Exception as e:
        print(f"Warning: Failed to parse requirements: {e}")
    
    return {
        "skills": [],
        "experience": [],
        "education": [],
        "other": []
    }
