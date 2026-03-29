# Vercel Deployment Guide

## Quick Start

### Step 1: Prepare Your Repository
```bash
# Make sure all changes are committed
git add .
git commit -m "Add Vercel configuration"
git push origin main
```

### Step 2: Deploy to Vercel

#### Option A: Using Vercel CLI (Recommended)
```bash
# Install Vercel CLI globally
npm install -g vercel

# Log in to your Vercel account
vercel login

# Deploy from project root
cd c:\Users\91954\OneDrive\Desktop\Data_Science\RAG_Project
vercel

# Follow the prompts and answer:
# - Set project name: rag-resume-scorer (or your choice)
# - Skip creating monorepo structure (y/n): n
# - Root directory: . (current directory)
```

#### Option B: Connect GitHub to Vercel Dashboard
1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Select the repository: `your-username/Resume_Scorer`
5. Keep settings default (root directory: .)
6. Click Deploy

### Step 3: Set Environment Variables
In Vercel Dashboard:
1. Go to your project settings
2. Navigate to Environment Variables
3. Add the following:
   - **OPENAI_API_KEY**: Your OpenAI API key
   - **ENVIRONMENT**: `production`

### Step 4: Configure Frontend

The frontend static files should be served from the `/frontend` directory. Make sure:
- `frontend/index.html` exists
- All frontend assets are in the `frontend/` folder
- JavaScript files reference `/api/...` for backend calls

## Project Structure for Vercel

```
RAG_Project/
├── api/
│   └── index.py              # Vercel serverless function entry point
├── backend/
│   ├── main.py
│   ├── routes.py            # Your API routes
│   ├── services_*.py         # Backend services
│   └── ...
├── frontend/
│   ├── index.html           # Main HTML file
│   ├── styles.css
│   ├── script.js
│   └── ...
├── requirements.txt          # Python dependencies
├── vercel.json              # Vercel configuration
└── .vercelignore            # Files to exclude from deployment
```

## How It Works

1. **Vercel detects** `vercel.json` configuration
2. **Builds** Python environment using `requirements.txt`
3. **Deploys** FastAPI app as serverless function at `/api/index.py`
4. **Routes**:
   - Requests to `/api/*` → Go to FastAPI backend
   - Requests to `/*` → Serve frontend static files

## API Endpoints After Deployment

Once deployed, your API will be available at:
- `https://your-project-name.vercel.app/api/health` - Health check
- `https://your-project-name.vercel.app/api/analyze` - File upload analysis
- `https://your-project-name.vercel.app/api/analyze-text` - Text analysis

## Frontend JavaScript Configuration

Update your frontend scripts to use the deployed API:

**In `frontend/script.js`:**

```javascript
// For production (Vercel)
const API_BASE_URL = window.location.origin; // Uses same domain

// For local development
// const API_BASE_URL = 'http://localhost:8000';

// All API calls will use: ${API_BASE_URL}/api/...
```

## Troubleshooting

### Issue: 500 Internal Server Error
**Solution**: Check Vercel logs
```bash
vercel logs
```

### Issue: Module import errors
**Solution**: Ensure backend modules are properly structured
- Check `api/index.py` can import from `backend/` directory
- Verify all dependencies are in `requirements.txt`

### Issue: Frontend not loading
**Solution**: 
- Verify `frontend/index.html` exists
- Check that frontend files are in `/frontend` directory
- Ensure routes in `vercel.json` are correct

### Issue: CORS errors
**Solution**: CORS is already enabled in `api/index.py`
- If still getting errors, check browser console for specific origins

## Monitoring & Logs

View deployment logs:
```bash
vercel logs
```

View function logs in real-time:
```bash
vercel deployments
```

## Performance Tips

1. **Cold Starts**: Vercel serverless functions may have initial cold start delay. This is normal.
2. **Dependencies**: Keep `requirements.txt` minimal to reduce build time
3. **Cache**: Enable static caching in Vercel Dashboard for frontend files

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Connect repo to Vercel
3. ✅ Add environment variables
4. ✅ Monitor first deployment in Vercel Dashboard
5. ✅ Share your public URL with team

---

**Default Vercel URL**: `https://rag-resume-scorer.vercel.app` (replace with your project name)

For more info: https://vercel.com/docs/concepts/functions/serverless-functions/python
