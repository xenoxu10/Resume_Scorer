# RAG Resume Scorer - Setup Complete ✓

## What Was Created

A complete RAG-based resume scoring application using FastAPI and OpenAI API.

### Project Structure
```
RAG_Project/
├── backend/
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Configuration management
│   ├── routes.py                  # API endpoints
│   ├── services_parser.py         # PDF/DOCX/TXT parsing
│   ├── services_embeddings.py     # OpenAI embeddings
│   ├── services_rag.py            # RAG retriever logic
│   ├── services_scorer.py         # Resume scoring
│   ├── test_app.py                # Test suite
│   ├── example_usage.py           # Usage examples
│   ├── .env                       # Environment variables (needs API key)
│   ├── run.bat                    # Windows startup script
│   └── run.sh                     # Unix startup script
├── requirements.txt               # Python dependencies
├── README.md                      # Full documentation
└── QUICKSTART.md                  # Quick start guide
```

## ⚠️ IMPORTANT: Add Your OpenAI API Key

### Step 1: Get API Key
1. Go to https://platform.openai.com/api-keys
2. Sign in or create account
3. Create new secret key
4. Copy the key

### Step 2: Add to .env File
Edit `backend/.env`:
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

Replace `sk-xxxxxxxxxxxxxxxxxxxx` with your actual key.

**IMPORTANT:** 
- Do NOT commit .env to git (it's in .gitignore)
- Keep your API key secret
- Check your usage at https://platform.openai.com/account/billing/overview

## 🚀 Getting Started

### Option 1: Windows
```bash
cd backend
python main.py
```

Or double-click: `run.bat`

### Option 2: macOS/Linux
```bash
cd backend
python main.py
```

Or run: `./run.sh`

### Option 3: Using Uvicorn Directly
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🌐 Access the Application

Once running, open your browser:
- **Main API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)

## 📝 Using the API

### Method 1: Web Interface (Recommended)
1. Go to http://localhost:8000/docs
2. Click on `/api/analyze` endpoint
3. Click "Try it out"
4. Upload your resume and job description
5. Click "Execute"
6. See detailed scoring results

### Method 2: cURL Command
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "resume=@resume.pdf" \
  -F "jd=@job_description.pdf"
```

### Method 3: Python Script
```python
import requests

resume_path = "resume.pdf"
jd_path = "job_description.pdf"

with open(resume_path, 'rb') as r, open(jd_path, 'rb') as j:
    files = {'resume': r, 'jd': j}
    response = requests.post(
        'http://localhost:8000/api/analyze',
        files=files
    )
    print(response.json())
```

## 📊 Example Response
```json
{
  "success": true,
  "data": {
    "score": 82,
    "matching_skills": [
      "Python",
      "FastAPI",
      "Docker",
      "REST APIs"
    ],
    "gaps": [
      "Kubernetes",
      "AWS Lambda",
      "CI/CD Pipelines"
    ],
    "assessment": "Strong candidate with solid Python and framework experience. Would benefit from cloud platform expertise.",
    "rag_context_used": true
  }
}
```

## 🧪 Test the Application

```bash
cd backend
python test_app.py
```

This will test:
- File parsing
- OpenAI embeddings
- RAG retriever
- API health check

## 📚 Key Features

✓ **RAG-based Analysis** - Retrieves relevant resume sections for better accuracy
✓ **OpenAI Integration** - Uses GPT-3.5-turbo for intelligent scoring
✓ **Multi-format Support** - Handles PDF, DOCX, and TXT files
✓ **Detailed Feedback** - Provides score, matching skills, gaps analysis
✓ **Auto Documentation** - Built-in Swagger and ReDoc docs
✓ **Easy Integration** - RESTful API with clear endpoints

## 🔧 How It Works

1. **Parse Files**: Extract text from resume and job description
2. **Extract Requirements**: AI identifies key JD requirements
3. **Chunk & Embed**: Break resume into chunks and create OpenAI embeddings
4. **Retrieve**: Find most relevant resume sections (RAG)
5. **Score**: AI analyzes and scores based on retrieved context

This approach:
- Reduces API costs by limiting context window
- Provides better reasoning with relevant sections
- Generates more accurate scores

## 💡 Configuration

Edit `backend/config.py` to customize:
```python
openai_model = "gpt-4"  # For better quality (higher cost)
embedding_model = "text-embedding-3-large"  # For better embeddings
```

## ⚡ API Endpoints

### POST /api/analyze
Upload resume and job description files
- **Content-Type**: multipart/form-data
- **Parameters**: 
  - resume: Resume file (PDF, DOCX, TXT)
  - jd: Job description file (PDF, DOCX, TXT)

### POST /api/analyze-text
Analyze using plain text input
- **Content-Type**: application/json
- **Parameters**:
  - resume_text: Resume as string
  - jd_text: Job description as string

### GET /api/health
Health check endpoint

## 🐛 Troubleshooting

### ImportError: No module named 'openai'
```bash
pip install openai
```

### OPENAI_API_KEY not found
- Ensure `.env` file is in `backend/` folder
- Check the key is set correctly
- Restart the application

### "Connection refused" on http://localhost:8000
- Make sure the server is running: `python main.py`
- Check if another service is using port 8000

### API Rate Limit
- Check your OpenAI quota: https://platform.openai.com/account/billing/overview
- Consider implementing request throttling

### Out of Credits
- Visit https://platform.openai.com/account/billing/overview
- Add payment method and set usage limits

## 📈 Next Steps

1. ✅ Install dependencies
2. ✅ Add OpenAI API key to `.env`
3. ✅ Run the application
4. → Test with sample resumes and JDs
5. → Integrate into your workflow
6. → Deploy to production (AWS, Azure, etc.)
7. → Add batch processing
8. → Create custom scoring templates

## 🚀 Production Deployment

For deploying to production:

**Docker**:
```dockerfile
FROM python:3.10
WORKDIR /app
COPY backend .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Environment Setup**:
- Use AWS Secrets Manager or similar for API key
- Set up logging and monitoring
- Implement rate limiting
- Add authentication to endpoints

## 📞 Support

- Check [README.md](README.md) for detailed documentation
- Review [QUICKSTART.md](QUICKSTART.md) for quick reference
- Check OpenAI API status: https://status.openai.com/

## ✨ Features Ready for Development

- ✓ Resume parsing (PDF, DOCX, TXT)
- ✓ Job description analysis
- ✓ RAG-based retrieval
- ✓ OpenAI-powered scoring
- ✓ RESTful API
- ⏳ Batch processing (coming soon)
- ⏳ Resume feedback generation (coming soon)
- ⏳ Interview question generation (coming soon)

---

**Your RAG Resume Scorer is ready to use! 🎉**

Add your OpenAI API key to `.env` and start scoring resumes!
