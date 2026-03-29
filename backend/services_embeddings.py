from openai import OpenAI
try:
    from .config import settings
except ImportError:
    from config import settings
from typing import List, Dict
import json


client = OpenAI(api_key=settings.openai_api_key)


def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Get embeddings from OpenAI API
    
    Args:
        texts: List of texts to embed
    
    Returns:
        List of embedding vectors
    """
    response = client.embeddings.create(
        model=settings.embedding_model,
        input=texts
    )
    return [item.embedding for item in response.data]


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """
    Split text into overlapping chunks
    
    Args:
        text: Text to chunk
        chunk_size: Size of each chunk
        overlap: Overlap between chunks
    
    Returns:
        List of text chunks
    """
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0
    
    for word in words:
        current_chunk.append(word)
        current_size += len(word) + 1
        
        if current_size >= chunk_size:
            chunks.append(" ".join(current_chunk))
            # Keep last few words for overlap
            overlap_words = max(1, len(current_chunk) // 4)
            current_chunk = current_chunk[-overlap_words:]
            current_size = sum(len(w) for w in current_chunk) + overlap_words
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors"""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = sum(a * a for a in vec1) ** 0.5
    magnitude2 = sum(b * b for b in vec2) ** 0.5
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)
