from typing import List

import numpy as np
from openai import OpenAI

from .config import settings


def get_client() -> OpenAI:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")
    return OpenAI(api_key=settings.openai_api_key)


def embed_texts(texts: List[str]) -> np.ndarray:
    client = get_client()
    response = client.embeddings.create(
        model=settings.embedding_model,
        input=texts,
    )
    vectors = [item.embedding for item in response.data]
    return np.array(vectors, dtype="float32")


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a_norm = a / (np.linalg.norm(a, axis=1, keepdims=True) + 1e-10)
    b_norm = b / (np.linalg.norm(b, axis=1, keepdims=True) + 1e-10)
    return np.dot(a_norm, b_norm.T)
