from typing import List, Tuple

import json
import numpy as np
from openai import OpenAI

from .config import settings
from .embedder import embed_texts, cosine_similarity


def score_resumes_against_jd(
    resumes: List[Tuple[str, str]],
    jd_text: str,
) -> List[Tuple[str, float]]:
    """Return list of (resume_name, score_0_to_100)."""
    if not resumes or not jd_text.strip():
        return []

    resume_texts = [text for _, text in resumes]

    # Embed JD and resumes together for efficiency
    all_texts = [jd_text] + resume_texts
    embeddings = embed_texts(all_texts)
    jd_vec = embeddings[0:1]
    resume_vecs = embeddings[1:]

    sims = cosine_similarity(jd_vec, resume_vecs)[0]  # shape: (n_resumes,)

    # Convert cosine similarity (-1..1) to 0..100
    scores = ((sims + 1) / 2) * 100

    results: List[Tuple[str, float]] = []
    for (name, _), score in zip(resumes, scores):
        results.append((name, float(score)))
    # Sort by score descending
    results.sort(key=lambda x: x[1], reverse=True)
    return results


def _get_llm_client() -> OpenAI:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not set for LLM scoring.")
    return OpenAI(api_key=settings.openai_api_key)


def _llm_score_single_resume(jd_text: str, resume_text: str) -> float:
    """Ask an LLM to score one resume vs the JD (0–100)."""
    client = _get_llm_client()
    system_prompt = (
        "You are an expert technical recruiter. "
        "Given a job description and a candidate resume, you must assign a "
        "single numeric match score between 0 and 100 where 0 = not a fit "
        "and 100 = perfect fit. Return ONLY a JSON object with keys 'score' "
        "(number) and 'reason' (short string explanation)."
    )
    user_prompt = (
        "Job description:\n" + jd_text.strip() + "\n\n" +
        "Candidate resume:\n" + resume_text.strip()
    )

    response = client.chat.completions.create(
        model=settings.llm_model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    content = response.choices[0].message.content
    data = json.loads(content)
    score = float(data.get("score", 0.0))
    # Clamp to 0–100 just in case
    return max(0.0, min(100.0, score))


def llm_score_resumes_against_jd(
    resumes: List[Tuple[str, str]],
    jd_text: str,
) -> List[Tuple[str, float]]:
    """Use an LLM to score each resume vs JD and return (name, score).

    This is more expensive than cosine similarity but can capture
    nuanced semantic match.
    """
    if not resumes or not jd_text.strip():
        return []

    results: List[Tuple[str, float]] = []
    for name, text in resumes:
        score = _llm_score_single_resume(jd_text, text)
        results.append((name, score))

    results.sort(key=lambda x: x[1], reverse=True)
    return results
