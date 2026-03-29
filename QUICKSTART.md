# RAG Resume Scorer - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### Step 1: Get OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create account
3. Click "Create new secret key"
4. Copy your API key

### Step 2: Configure Environment
Edit `backend/.env`:
```
OPENAI_API_KEY=sk-xxx...  # Replace with your actual key
```

### Step 3: Install & Run

**Windows:**
```bash
cd backend
python -m pip install -r ../requirements.txt
python main.py
```

**macOS/Linux:**
```bash
cd backend
pip install -r ../requirements.txt
python main.py
```

## 📝 Using the Application

### Option 1: Web Interface (Recommended)
1. Open http://localhost:8000/docs
2. Click "Try it out" on `/api/analyze`
3. Upload resume and job description files
4. Click "Execute"

### Option 2: Command Line (cURL)
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "resume=@your_resume.pdf" \
  -F "jd=@job_description.pdf"
```

### Option 3: Python Script
```python
import requests

with open('resume.pdf', 'rb') as r, open('jd.pdf', 'rb') as j:
    files = {'resume': r, 'jd': j}
    response = requests.post('http://localhost:8000/api/analyze', files=files)
    print(response.json())
```

## 🧪 Test the Setup
```bash
cd backend
python test_app.py
```

## 📊 API Response Example
```json
{
  "success": true,
  "data": {
    "score": 85,
    "matching_skills": [
      "Python",
      "FastAPI",
      "Docker"
    ],
    "gaps": [
      "Kubernetes",
      "AWS Lambda"
    ],
    "assessment": "Strong candidate with relevant experience in backend development...",
    "rag_context_used": true
  }
}
```

## 🔧 Configuration

Edit `backend/config.py` to change:
- `openai_model`: Change from "gpt-3.5-turbo" to "gpt-4" (costs more)
- `embedding_model`: Different embedding models available

## 📚 API Documentation

**Auto-generated docs available at:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## ⚠️ Troubleshooting

### "ModuleNotFoundError: No module named 'openai'"
```bash
pip install openai
```

### "Error: OPENAI_API_KEY not found"
Make sure `.env` file exists in `backend/` folder with valid key

### "Connection refused"
Make sure server is running:
```bash
python main.py
```

### Out of credits/Invalid API key
Visit https://platform.openai.com/account/billing/overview to check account status

## 💡 How RAG Works

1. **Parse** - Extract text from resume and JD
2. **Extract Requirements** - AI identifies JD requirements
3. **Chunk & Embed** - Break resume into chunks and create embeddings
4. **Retrieve** - Find most relevant resume sections (RAG)
5. **Score** - AI scores based on retrieved context

This approach:
✓ Reduces API costs by limiting context
✓ Provides better reasoning (uses relevant sections)
✓ Gives more accurate scores

## 📈 Next Steps

1. ✓ Set up API key
2. ✓ Run the application
3. ✓ Test with your resume
4. → Integrate into your workflow
5. → Add batch processing
6. → Deploy to production

## 🤝 Support

For issues:
1. Check the README.md
2. Review error messages carefully
3. Ensure .env file is in `backend/` folder
4. Check API key is valid at OpenAI dashboard

---

**Happy scoring!** 🎉
