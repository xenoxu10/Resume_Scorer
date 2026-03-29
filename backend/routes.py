from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Dict, Any, List
try:
    from .services_parser import parse_file
    from .services_scorer import score_resume_with_rag
    from .services_batch_scorer import score_multiple_resumes, get_candidate_comparison
except ImportError:
    from services_parser import parse_file
    from services_scorer import score_resume_with_rag
    from services_batch_scorer import score_multiple_resumes, get_candidate_comparison


router = APIRouter()


@router.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(..., description="Resume file (PDF, DOCX, or TXT)"),
    jd: UploadFile = File(..., description="Job Description file (PDF, DOCX, or TXT)")
) -> Dict[str, Any]:
    """
    Analyze resume against job description using RAG
    
    Args:
        resume: Resume file upload
        jd: Job description file upload
    
    Returns:
        Scoring result with detailed analysis
    """
    try:
        # Parse resume
        resume_content = await resume.read()
        resume_text = await parse_file(resume_content, resume.filename)
        
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Resume file is empty")
        
        # Parse job description
        jd_content = await jd.read()
        jd_text = await parse_file(jd_content, jd.filename)
        
        if not jd_text.strip():
            raise HTTPException(status_code=400, detail="Job description file is empty")
        
        # Score resume
        result = score_resume_with_rag(resume_text, jd_text)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": result
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing files: {str(e)}"
        )


@router.post("/analyze-text")
async def analyze_text(
    resume_text: str,
    jd_text: str
) -> Dict[str, Any]:
    """
    Analyze resume and JD provided as plain text
    
    Args:
        resume_text: Resume content as text
        jd_text: Job description content as text
    
    Returns:
        Scoring result with detailed analysis
    """
    try:
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Resume text is empty")
        
        if not jd_text.strip():
            raise HTTPException(status_code=400, detail="Job description text is empty")
        
        # Score resume
        result = score_resume_with_rag(resume_text, jd_text)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": result
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing text: {str(e)}"
        )


@router.post("/batch-analyze")
async def batch_analyze(
    resumes: List[UploadFile] = File(..., description="Resume files"),
    jd: UploadFile = File(..., description="Job Description file")
) -> Dict[str, Any]:
    """
    Analyze multiple resumes against a job description and rank them
    
    Args:
        resumes: List of resume files (PDF, DOCX, or TXT)
        jd: Job description file
    
    Returns:
        Ranked list of candidates with scores
    """
    try:
        if not resumes:
            raise HTTPException(status_code=400, detail="No resume files provided")
        
        if len(resumes) > 50:
            raise HTTPException(status_code=400, detail="Maximum 50 resumes allowed per batch")
        
        # Parse job description
        jd_content = await jd.read()
        jd_text = await parse_file(jd_content, jd.filename)
        
        if not jd_text.strip():
            raise HTTPException(status_code=400, detail="Job description file is empty")
        
        # Parse resumes
        resume_texts = {}
        for resume in resumes:
            try:
                resume_content = await resume.read()
                resume_text = await parse_file(resume_content, resume.filename)
                
                if resume_text.strip():
                    # Use filename without extension as candidate name
                    candidate_name = resume.filename.rsplit('.', 1)[0]
                    resume_texts[candidate_name] = resume_text
            except Exception as e:
                print(f"Error parsing resume {resume.filename}: {e}")
                continue
        
        if not resume_texts:
            raise HTTPException(status_code=400, detail="No valid resume files provided")
        
        # Score and rank resumes
        results = score_multiple_resumes(resume_texts, jd_text)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": results
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing batch: {str(e)}"
        )


@router.post("/batch-analyze-text")
async def batch_analyze_text(
    resumes: Dict[str, str],
    jd_text: str
) -> Dict[str, Any]:
    """
    Analyze multiple resumes provided as text and rank them
    
    Args:
        resumes: Dictionary of {candidate_name: resume_text}
        jd_text: Job description as text
    
    Returns:
        Ranked list of candidates with scores
    """
    try:
        if not resumes:
            raise HTTPException(status_code=400, detail="No resumes provided")
        
        if len(resumes) > 50:
            raise HTTPException(status_code=400, detail="Maximum 50 resumes allowed per batch")
        
        if not jd_text.strip():
            raise HTTPException(status_code=400, detail="Job description text is empty")
        
        # Validate resumes
        valid_resumes = {
            name: text for name, text in resumes.items() if text.strip()
        }
        
        if not valid_resumes:
            raise HTTPException(status_code=400, detail="No valid resume texts provided")
        
        # Score and rank resumes
        results = score_multiple_resumes(valid_resumes, jd_text)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": results
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing batch: {str(e)}"
        )


@router.post("/compare-candidates")
async def compare_candidates(
    candidate1_name: str,
    candidate2_name: str,
    candidate1_data: Dict[str, Any],
    candidate2_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Compare two candidates
    
    Args:
        candidate1_name: Name of first candidate
        candidate2_name: Name of second candidate
        candidate1_data: Score data of first candidate
        candidate2_data: Score data of second candidate
    
    Returns:
        Comparison analysis
    """
    try:
        candidate1_data["name"] = candidate1_name
        candidate2_data["name"] = candidate2_name
        
        comparison = get_candidate_comparison(candidate1_data, candidate2_data)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": comparison
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error comparing candidates: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "service": "RAG Resume Scorer"}
    )
