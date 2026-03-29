# RAG Resume Scorer Application

A FastAPI-based Resume Scoring System using Retrieval-Augmented Generation (RAG) with OpenAI API.

## Features

- **RAG-based Analysis**: Retrieves relevant resume sections for comparison
- **OpenAI Integration**: Uses GPT-3.5-turbo for intelligent scoring
- **Multi-format Support**: Handles PDF, DOCX, and TXT files
- **Detailed Feedback**: Provides score, matching skills, gaps analysis
- **FastAPI Framework**: Modern, fast web framework with automatic documentation

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure OpenAI API Key

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key_here
```

Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)

### 3. Run the Application

```bash
cd backend
python main.py
```

Or use uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### 1. Analyze with File Upload

**POST** `/api/analyze`

Upload resume and job description files for analysis.

```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "resume=@resume.pdf" \
  -F "jd=@job_description.pdf"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "score": 85,
    "matching_skills": ["Python", "FastAPI", "Machine Learning"],
    "gaps": ["Kubernetes", "AWS"],
    "assessment": "Strong candidate with relevant experience...",
    "rag_context_used": true
  }
}
```

### 2. Analyze with Text Input

**POST** `/api/analyze-text`

Submit resume and JD as plain text.

```bash
curl -X POST "http://localhost:8000/api/analyze-text" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Your resume content...",
    "jd_text": "Your job description..."
  }'
```

### 3. Health Check

**GET** `/api/health`

```bash
curl "http://localhost:8000/api/health"
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration management
├── routes.py              # API routes
├── services_parser.py     # File parsing (PDF, DOCX, TXT)
├── services_embeddings.py # OpenAI embeddings
├── services_rag.py        # RAG retrieval logic
└── services_scorer.py     # Resume scoring logic
```

## How It Works

1. **Parsing**: Resume and JD are parsed from files or text
2. **Requirement Extraction**: Key requirements extracted from JD using LLM
3. **Indexing**: Resume is chunked and embedded using OpenAI embeddings
4. **Retrieval**: Relevant resume sections retrieved for each requirement
5. **Scoring**: LLM generates intelligent score and analysis using retrieved context

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: Model to use (default: gpt-3.5-turbo)
- `EMBEDDING_MODEL`: Embedding model (default: text-embedding-3-small)

## Cost Optimization

The RAG approach optimizes API costs by:
- Chunking documents to process only relevant sections
- Using small embedding model (text-embedding-3-small)
- Limiting context window inputs to necessary information

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200`: Successful analysis
- `400`: Invalid input (empty files/text)
- `500`: Server error during processing

## Future Enhancements

- [ ] Support for more file formats (Excel, PowerPoint)
- [ ] Caching of embeddings for repeated analyses
- [ ] Batch processing of multiple resumes
- [ ] Custom scoring templates
- [ ] Resume feedback generation
- [ ] Interview question generation

## License

Open source
