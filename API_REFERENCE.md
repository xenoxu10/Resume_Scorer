# RAG Resume Scorer - API Reference

## Server Information

**Base URL**: `http://localhost:8000`

**Documentation**: 
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Endpoints

### 1. Root Endpoint

**GET** `/`

Returns API information and available endpoints.

**Response** (200 OK):
```json
{
  "message": "RAG Resume Scorer API",
  "version": "1.0.0",
  "docs": "/docs",
  "endpoints": {
    "analyze": "/api/analyze (POST with files)",
    "analyze-text": "/api/analyze-text (POST with text)",
    "health": "/api/health (GET)"
  }
}
```

---

### 2. Analyze Resume with File Upload

**POST** `/api/analyze`

Analyze a resume against a job description by uploading files.

**Content-Type**: `multipart/form-data`

**Parameters**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| resume | File | Yes | Resume file (PDF, DOCX, or TXT) |
| jd | File | Yes | Job Description file (PDF, DOCX, or TXT) |

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "resume=@john_doe_resume.pdf" \
  -F "jd=@senior_developer_jd.pdf"
```

**Python Example**:
```python
import requests

files = {
    'resume': open('resume.pdf', 'rb'),
    'jd': open('job_description.pdf', 'rb')
}

response = requests.post(
    'http://localhost:8000/api/analyze',
    files=files
)

result = response.json()
print(f"Score: {result['data']['score']}")
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "score": 85,
    "matching_skills": [
      "Python",
      "FastAPI",
      "Docker",
      "REST API Development"
    ],
    "gaps": [
      "Kubernetes",
      "AWS Lambda",
      "CI/CD Pipeline Implementation"
    ],
    "assessment": "Strong candidate with relevant backend development experience. Would benefit from cloud platform expertise, particularly AWS and containerization at scale.",
    "rag_context_used": true
  }
}
```

**Error Responses**:

```json
{
  "detail": "Resume file is empty"
}
```
Status: 400 Bad Request

```json
{
  "detail": "Job description file is empty"
}
```
Status: 400 Bad Request

```json
{
  "detail": "Error processing files: [error details]"
}
```
Status: 500 Internal Server Error

---

### 3. Analyze Resume with Text Input

**POST** `/api/analyze-text`

Analyze resume and job description provided as plain text.

**Content-Type**: `application/json`

**Request Body**:
```json
{
  "resume_text": "string (resume content)",
  "jd_text": "string (job description content)"
}
```

**Parameters**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| resume_text | String | Yes | Resume content as plain text (min 50 chars) |
| jd_text | String | Yes | Job description as plain text (min 50 chars) |

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/analyze-text" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "John Doe\nSoftware Engineer\nSkills: Python, FastAPI, Docker",
    "jd_text": "Senior Python Developer\nRequired: Python, FastAPI, Docker"
  }'
```

**Python Example**:
```python
import requests

resume_text = """
John Doe
Senior Software Engineer

About:
Experienced Python developer with 5+ years of experience
developing microservices and REST APIs.

Skills:
- Python, FastAPI, Flask
- Docker, Kubernetes
- PostgreSQL, MongoDB
- AWS, GCP
"""

jd_text = """
Senior Python Developer Position

Requirements:
- 5+ years Python development
- FastAPI or similar framework experience
- Docker and container knowledge
- Cloud platform (AWS/GCP) experience
- RESTful API design experience
"""

response = requests.post(
    'http://localhost:8000/api/analyze-text',
    json={
        'resume_text': resume_text,
        'jd_text': jd_text
    }
)

result = response.json()
print(result['data'])
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "score": 88,
    "matching_skills": [
      "Python",
      "FastAPI",
      "Docker",
      "REST API Development",
      "Cloud Platforms"
    ],
    "gaps": [
      "Kubernetes orchestration",
      "Advanced cloud deployment"
    ],
    "assessment": "Excellent match. Candidate demonstrates strong Python skills and directly relevant experience with FastAPI and Docker. All core requirements met.",
    "rag_context_used": true
  }
}
```

**Error Responses**:

```json
{
  "detail": "Resume text is empty"
}
```
Status: 400 Bad Request

```json
{
  "detail": "Job description text is empty"
}
```
Status: 400 Bad Request

---

### 4. Health Check

**GET** `/api/health`

Check if the API is running and healthy.

**Response** (200 OK):
```json
{
  "status": "healthy",
  "service": "RAG Resume Scorer"
}
```

**cURL Example**:
```bash
curl "http://localhost:8000/api/health"
```

---

## Response Structure

All successful responses follow this structure:

```json
{
  "success": boolean,
  "data": {
    "score": integer (0-100),
    "matching_skills": [
      "skill1",
      "skill2",
      "..."
    ],
    "gaps": [
      "gap1",
      "gap2",
      "..."
    ],
    "assessment": "string",
    "rag_context_used": boolean
  }
}
```

### Score Scale

- **90-100**: Excellent match - Highly qualified candidate
- **75-89**: Good match - Well-qualified candidate
- **60-74**: Moderate match - Meets most requirements
- **40-59**: Partial match - Missing some key skills
- **0-39**: Poor match - Lacks critical requirements

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Indicates if request was successful |
| score | integer | Match score from 0-100 |
| matching_skills | array | Skills that match JD requirements |
| gaps | array | Skills/experience missing from resume |
| assessment | string | AI-generated summary assessment |
| rag_context_used | boolean | Whether RAG retrieval found relevant content |

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Request processed successfully |
| 400 | Bad Request | Empty file or invalid input |
| 500 | Server Error | Processing error (check OpenAI API key) |

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Errors

**"ModuleNotFoundError: No module named 'openai'"**
- Solution: Run `pip install openai`

**"OPENAI_API_KEY not found"**
- Solution: Add key to `backend/.env` file

**"Connection refused"**
- Solution: Make sure app is running with `python main.py`

**"Invalid API key"**
- Solution: Check key at https://platform.openai.com/api-keys

---

## Rate Limiting & Costs

### OpenAI API Costs (Approximate)

- **GPT-3.5-turbo**: ~$0.002 per 1K input tokens
- **text-embedding-3-small**: ~$0.00002 per 1K tokens

Typical analysis: **$0.01 - $0.05 per resume**

### Optimization Tips

1. Use smaller models for demos
2. Enable response caching
3. Batch similar analyses
4. Monitor usage: https://platform.openai.com/account/usage

---

## Authentication

Currently, the API has **no authentication**. For production:

1. Add API key requirement
2. Implement JWT tokens
3. Use OAuth2
4. Add rate limiting per user

---

## Examples

### Example 1: Basic Score Check

```python
import requests

response = requests.post('http://localhost:8000/api/analyze-text', json={
    'resume_text': 'Python, FastAPI, Docker',
    'jd_text': 'Python, FastAPI, Docker required'
})

if response.status_code == 200:
    score = response.json()['data']['score']
    print(f"Match Score: {score}%")
```

### Example 2: Batch Processing

```python
import os
import requests

resume_files = [f for f in os.listdir('resumes') if f.endswith('.pdf')]
jd_file = 'job_descriptions/senior_dev.pdf'

results = []
for resume in resume_files:
    files = {
        'resume': open(f'resumes/{resume}', 'rb'),
        'jd': open(jd_file, 'rb')
    }
    response = requests.post('http://localhost:8000/api/analyze', files=files)
    results.append({
        'resume': resume,
        'score': response.json()['data']['score']
    })

# Sort by score
results.sort(key=lambda x: x['score'], reverse=True)
for r in results:
    print(f"{r['resume']}: {r['score']}")
```

### Example 3: Integration with Web App

```javascript
// JavaScript/React example
async function scoreResume(formData) {
  const response = await fetch('http://localhost:8000/api/analyze', {
    method: 'POST',
    body: formData // FormData with resume and jd files
  });
  
  const result = await response.json();
  return result.data;
}
```

---

## Supported File Formats

| Format | Extension | Supported |
|--------|-----------|-----------|
| PDF | .pdf | ✓ |
| Word Document | .docx | ✓ |
| Plain Text | .txt | ✓ |
| Rich Text | .rtf | ✗ |
| Excel | .xlsx | ✗ |
| Image | .png, .jpg | ✗ |

---

## Configuration

### Environment Variables

Set in `backend/.env`:

```
OPENAI_API_KEY=sk-xxxx...          # Your OpenAI API key
OPENAI_MODEL=gpt-3.5-turbo         # Model to use (gpt-4 for better quality)
EMBEDDING_MODEL=text-embedding-3-small  # Embedding model
```

### Changing Models

Edit `backend/config.py`:

```python
openai_model = "gpt-4"  # Better quality, higher cost
embedding_model = "text-embedding-3-large"  # Better embeddings
```

---

## Troubleshooting API Issues

### Check API Status
```bash
curl http://localhost:8000/api/health
```

### View Live Logs
```bash
python main.py  # Shows print statements and errors
```

### Test with Sample Data
```bash
python example_usage.py
```

### Debug OpenAI Issues
```python
from openai import OpenAI
client = OpenAI(api_key="your-key")
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=["test"]
)
print(response)
```

---

## Versioning

Current Version: **1.0.0**

Future versions may change endpoint structure or response format.

---

## Support & Documentation

- **Full Docs**: See [README.md](README.md)
- **Quick Start**: See [QUICKSTART.md](QUICKSTART.md)
- **Setup Guide**: See [SETUP_COMPLETE.md](SETUP_COMPLETE.md)
- **OpenAI Docs**: https://platform.openai.com/docs

---

**Last Updated**: March 29, 2024
