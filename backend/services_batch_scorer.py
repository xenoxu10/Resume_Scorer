from typing import Dict, Any, List
from openai import OpenAI
try:
    from .config import settings
    from .services_rag import RAGRetriever, extract_key_requirements
except ImportError:
    from config import settings
    from services_rag import RAGRetriever, extract_key_requirements


client = OpenAI(api_key=settings.openai_api_key)


def score_resume_with_rag(resume_text: str, jd_text: str) -> Dict[str, Any]:
    """
    Score resume against job description using RAG and OpenAI
    
    Args:
        resume_text: Resume content
        jd_text: Job description content
    
    Returns:
        Scoring result with score, analysis, and matching details
    """
    # Extract key requirements from JD
    jd_requirements = extract_key_requirements(jd_text)
    
    # Index resume for retrieval
    retriever = RAGRetriever(top_k=5)
    retriever.index_document(resume_text)
    
    # Build RAG context by extracting relevant resume sections
    relevant_resume_sections = []
    for category, requirements in jd_requirements.items():
        # Ensure requirements is a list
        if not isinstance(requirements, list):
            requirements = [str(requirements)] if requirements else []
        
        # Get top 3 from each category
        for requirement in requirements[:3]:
            requirement_str = str(requirement).strip()
            if requirement_str:  # Only process non-empty requirements
                relevant_sections = retriever.retrieve(requirement_str)
                relevant_resume_sections.extend(relevant_sections)
    
    # Remove duplicates while preserving order
    unique_sections = []
    seen = set()
    for section in relevant_resume_sections:
        if section not in seen:
            unique_sections.append(section)
            seen.add(section)
    
    rag_context = "\n".join(unique_sections[:5])  # Top 5 most relevant sections
    
    # Generate score and analysis using OpenAI
    prompt = f"""You are an ATS (Applicant Tracking System) and resume scoring expert.
Analyze the following resume against the job description and provide a detailed score (0-100).

JOB DESCRIPTION:
{jd_text[:2000]}

RELEVANT RESUME SECTIONS (from RAG retrieval):
{rag_context if rag_context else resume_text[:1500]}

FULL RESUME (for context):
{resume_text[:3000]}

Based on this analysis, provide:
1. A score from 0-100
2. Key matching skills
3. Gaps or missing requirements
4. a brief overall assessment

Format your response as JSON with keys: score, matching_skills, gaps, assessment"""

    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {
                "role": "system",
                "content": "You are an expert ATS system that accurately scores resumes against job descriptions. Return valid JSON."
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=800
    )
    
    result_text = response.choices[0].message.content
    
    # Parse response
    try:
        import json
        # Extract JSON from response
        start_idx = result_text.find('{')
        end_idx = result_text.rfind('}') + 1
        if start_idx != -1 and end_idx > start_idx:
            result = json.loads(result_text[start_idx:end_idx])
        else:
            result = {"score": 50, "assessment": result_text}
    except Exception as e:
        print(f"Warning: Failed to parse response: {e}")
        result = {"score": 50, "assessment": result_text}
    
    # Ensure score is an integer
    if isinstance(result.get("score"), str):
        try:
            result["score"] = int(float(result["score"]))
        except:
            result["score"] = 50
    
    result["score"] = max(0, min(100, int(result.get("score", 50))))
    
    # Ensure matching_skills and gaps are lists of strings
    matching_skills = result.get("matching_skills", [])
    if not isinstance(matching_skills, list):
        matching_skills = [str(matching_skills)] if matching_skills else []
    matching_skills = [str(s).strip() for s in matching_skills if s]
    
    gaps = result.get("gaps", [])
    if not isinstance(gaps, list):
        gaps = [str(gaps)] if gaps else []
    gaps = [str(g).strip() for g in gaps if g]
    
    return {
        "score": result.get("score", 50),
        "matching_skills": matching_skills,
        "gaps": gaps,
        "assessment": str(result.get("assessment", "Assessment complete")).strip(),
        "rag_context_used": len(unique_sections) > 0
    }


def score_multiple_resumes(resume_texts: Dict[str, str], jd_text: str) -> Dict[str, Any]:
    """
    Score multiple resumes against a job description and rank them
    
    Args:
        resume_texts: Dictionary of {candidate_name: resume_content}
        jd_text: Job description content
    
    Returns:
        Ranked list of candidates with scores and analysis
    """
    if not resume_texts:
        return {"candidates": [], "total": 0}
    
    candidates_scores = []
    
    # Score each resume
    for candidate_name, resume_text in resume_texts.items():
        try:
            score_result = score_resume_with_rag(resume_text, jd_text)
            candidates_scores.append({
                "name": candidate_name,
                "score": score_result["score"],
                "matching_skills": score_result["matching_skills"],
                "gaps": score_result["gaps"],
                "assessment": score_result["assessment"]
            })
        except Exception as e:
            print(f"Error scoring {candidate_name}: {e}")
            candidates_scores.append({
                "name": candidate_name,
                "score": 0,
                "matching_skills": [],
                "gaps": [],
                "assessment": f"Error: {str(e)}"
            })
    
    # Sort by score (descending)
    candidates_scores.sort(key=lambda x: x["score"], reverse=True)
    
    # Add ranking
    for idx, candidate in enumerate(candidates_scores, 1):
        candidate["rank"] = idx
    
    return {
        "candidates": candidates_scores,
        "total": len(candidates_scores),
        "top_candidate": candidates_scores[0] if candidates_scores else None
    }


def get_candidate_comparison(candidate1: Dict[str, Any], candidate2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compare two candidates
    
    Args:
        candidate1: First candidate data
        candidate2: Second candidate data
    
    Returns:
        Comparison analysis
    """
    return {
        "candidate1": candidate1["name"],
        "candidate2": candidate2["name"],
        "score_difference": candidate1["score"] - candidate2["score"],
        "better_candidate": candidate1["name"] if candidate1["score"] > candidate2["score"] else candidate2["name"],
        "candidate1_unique_skills": list(set(candidate1["matching_skills"]) - set(candidate2["matching_skills"])),
        "candidate2_unique_skills": list(set(candidate2["matching_skills"]) - set(candidate1["matching_skills"])),
        "shared_skills": list(set(candidate1["matching_skills"]) & set(candidate2["matching_skills"]))
    }
