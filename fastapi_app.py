from io import BytesIO
from typing import List, Optional

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pypdf import PdfReader

from src.scorer import llm_score_resumes_against_jd

app = FastAPI(title="Resume Scoring API")

# Allow React dev server (localhost:5173) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


def _read_text_from_upload(upload: UploadFile) -> str:
    raw = upload.file.read()
    if upload.filename.lower().endswith(".txt"):
        return raw.decode("utf-8", errors="ignore")
    if upload.filename.lower().endswith(".pdf"):
        reader = PdfReader(BytesIO(raw))
        texts = []
        for page in reader.pages:
            texts.append(page.extract_text() or "")
        return "\n".join(texts)
    return ""


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "results": None, "jd_name": None, "error": None},
    )


@app.post("/score", response_class=HTMLResponse)
async def score(
    request: Request,
    jd: UploadFile = File(...),
    resumes: List[UploadFile] = File(...),
    top_k: Optional[int] = Form(10),
) -> HTMLResponse:
    error: Optional[str] = None

    try:
        jd_text = _read_text_from_upload(jd)
        if not jd_text.strip():
            error = "Could not read text from JD file. Only PDF/TXT are supported."
    except Exception as exc:  # noqa: BLE001
        error = f"Failed to read JD file: {exc}"
        jd_text = ""

    resume_docs = []
    if not error:
        for up in resumes:
            try:
                text = _read_text_from_upload(up)
            except Exception as exc:  # noqa: BLE001
                error = f"Failed to read resume {up.filename}: {exc}"
                resume_docs = []
                break
            if text.strip():
                resume_docs.append((up.filename, text))

    results = None
    if not error and resume_docs:
        try:
            results = llm_score_resumes_against_jd(resume_docs, jd_text)
        except Exception as exc:  # noqa: BLE001
            error = f"Scoring failed: {exc}"

    if results and top_k is not None:
        results = results[: max(1, top_k)]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "results": results,
            "jd_name": jd.filename if jd else None,
            "error": error,
        },
    )


@app.post("/api/score", response_class=JSONResponse)
async def api_score(
    jd: UploadFile = File(...),
    resumes: List[UploadFile] = File(...),
    top_k: Optional[int] = Form(10),
) -> JSONResponse:
    """JSON API for React frontend.

    Accepts one JD file and multiple resume files, returns scores as JSON.
    """

    error: Optional[str] = None

    try:
        jd_text = _read_text_from_upload(jd)
        if not jd_text.strip():
            error = "Could not read text from JD file. Only PDF/TXT are supported."
    except Exception as exc:  # noqa: BLE001
        error = f"Failed to read JD file: {exc}"
        jd_text = ""

    resume_docs = []
    if not error:
        for up in resumes:
            try:
                text = _read_text_from_upload(up)
            except Exception as exc:  # noqa: BLE001
                error = f"Failed to read resume {up.filename}: {exc}"
                resume_docs = []
                break
            if text.strip():
                resume_docs.append((up.filename, text))

    results = []
    if not error and resume_docs:
        try:
            scored = llm_score_resumes_against_jd(resume_docs, jd_text)
            if top_k is not None:
                scored = scored[: max(1, top_k)]
            results = [
                {"name": name, "score": float(score)} for name, score in scored
            ]
        except Exception as exc:  # noqa: BLE001
            error = f"Scoring failed: {exc}"

    return JSONResponse(
        {
            "jd_name": jd.filename if jd else None,
            "results": results,
            "error": error,
        }
    )
