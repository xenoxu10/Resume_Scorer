# 🚀 Running Backend & Frontend Together

Complete guide to running the RAG Resume Scorer with both backend API and web frontend.

## ⚡ Quick Start (5 minutes)

### Terminal 1: Start Backend

```bash
cd RAG_Project/backend
python main.py
```

You should see:
```
Uvicorn running on http://127.0.0.1:8000
```

### Terminal 2: Start Frontend

```bash
cd RAG_Project/frontend
python server.py
```

You should see:
```
✓ Server running at: http://localhost:3000
```

### 3. Open Browser

Visit: **http://localhost:3000**

---

## 📋 Detailed Setup

### Prerequisites

- Python 3.10+ installed
- Virtual environment activated
- Dependencies installed (`pip install -r requirements.txt`)
- OpenAI API key in `.env`

### Step 1: Verify Backend Setup

```bash
cd RAG_Project/backend

# Check if .env has API key
cat .env

# Should show:
# OPENAI_API_KEY=sk-xxxx...
```

If not set, edit `.env`:
```
OPENAI_API_KEY=your_actual_key_here
```

### Step 2: Start Backend

```bash
cd RAG_Project/backend
python main.py
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     Application startup complete
```

**Check it's working:**
Visit http://localhost:8000/docs in your browser
You should see the interactive API documentation

### Step 3: Start Frontend (New Terminal)

```bash
cd RAG_Project/frontend
python server.py
```

**Expected Output:**
```
====================================
RAG Resume Scorer - Frontend Server
====================================

✓ Server running at: http://localhost:3000
✓ Serving files from: C:\...\RAG_Project\frontend

✓ Make sure backend is running at: http://localhost:8000

Opening browser...
```

### Step 4: Use the Application

1. Open http://localhost:3000 in your browser
2. Upload resume and job description files
3. Click "Analyze Resume"
4. View results!

---

## 🖥️ Windows Setup

### Using Batch Scripts (Easiest)

**Terminal 1:**
```bash
cd RAG_Project\backend
run.bat
```

**Terminal 2:**
```bash
cd RAG_Project\frontend
run.bat
```

### Using PowerShell

**Terminal 1:**
```powershell
cd RAG_Project\backend
python main.py
```

**Terminal 2:**
```powershell
cd RAG_Project\frontend
python server.py
```

---

## 🍎 macOS Setup

### Using Shell Scripts

**Terminal 1:**
```bash
cd RAG_Project/backend
chmod +x run.sh
./run.sh
```

**Terminal 2:**
```bash
cd RAG_Project/frontend
chmod +x run.sh
./run.sh
```

### Using Terminal

**Terminal 1:**
```bash
cd RAG_Project/backend
python main.py
```

**Terminal 2:**
```bash
cd RAG_Project/frontend
python server.py
```

---

## 🐧 Linux Setup

**Terminal 1:**
```bash
cd RAG_Project/backend
python3 main.py
```

**Terminal 2:**
```bash
cd RAG_Project/frontend
python3 server.py
```

---

## 🌐 Access Points

Once both are running, you have:

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:3000 | Web UI for uploading and analyzing |
| **API** | http://localhost:8000 | Backend API endpoint |
| **API Docs** | http://localhost:8000/docs | Interactive Swagger documentation |
| **API Reference** | http://localhost:8000/redoc | Alternative API documentation |

---

## ✅ Checklist

Before starting, verify:

- [ ] Python 3.10+ installed (`python --version`)
- [ ] In correct directory
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip list | grep fastapi`)
- [ ] `.env` file has OpenAI API key
- [ ] Port 8000 is available (backend)
- [ ] Port 3000 is available (frontend)

---

## 🔍 Troubleshooting

### "Address already in use"

Port 8000 or 3000 is already taken

**Solution:**
```bash
# Find what's using port 8000
# Windows:
netstat -ano | findstr :8000

# macOS/Linux:
lsof -i :8000

# Kill the process or use a different port
```

### "OPENAI_API_KEY not found"

Backend can't find your API key

**Solution:**
1. Check `backend/.env` exists
2. Verify key is set: `OPENAI_API_KEY=sk-xxx`
3. Restart backend after changing `.env`

### "Unable to connect to API"

Frontend can't reach backend

**Possible causes:**
1. Backend not running (Terminal 1)
2. Backend on different port
3. API key error (check backend logs)

**Solution:**
1. Check backend Terminal 1 is still running
2. Look for errors in backend output
3. Try API docs: http://localhost:8000/docs

### "Files not uploading"

Files stuck on "Analyzing..."

**Possible causes:**
1. Large files
2. API key invalid
3. Network issue

**Solution:**
1. Try smaller files first
2. Verify API key in `.env`
3. Check internet connection
4. Look at frontend browser console (F12)

### "Score always 50"

Analysis seems incomplete

**Cause:** Often means API key issue or rate limiting

**Solution:**
1. Check API key validity at https://platform.openai.com/api-keys
2. Check usage at https://platform.openai.com/account/usage
3. Restart backend with valid key

---

## 📊 Architecture

```
                Frontend (Port 3000)
                    ↓
              [Upload Files/Text]
                    ↓
            ┌──────────────────────┐
            │  HTTP Request        │
            │  /api/analyze        │
            └──────────────────────┘
                    ↓
            Backend API (Port 8000)
                    ↓
        ┌────────────────────────────┐
        │ Parse Files                │
        │ Extract Requirements       │
        │ Create Embeddings (OpenAI) │
        │ Retrieve Relevant Sections │
        │ Score & Analyze (OpenAI)   │
        └────────────────────────────┘
                    ↓
            ┌──────────────────────┐
            │  HTTP Response       │
            │  JSON Result         │
            └──────────────────────┘
                    ↓
               Frontend
                    ↓
           [Display Results]
```

---

## 🛠️ Configuration

### Change Backend Port

Edit `backend/main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=9000)  # Change 8000 to 9000
```

Then update frontend `script.js`:
```javascript
const API_BASE_URL = 'http://localhost:9000/api';  // Changed port
```

### Change Frontend Port

Edit `frontend/server.py`:
```python
PORT = 4000  # Change from 3000
```

### Change Allowed Origins

For production, edit `backend/main.py`:
```python
allow_origins=[
    "http://localhost:3000",
    "https://yourdomain.com"
]
```

---

## 📈 Performance Tips

1. **Use smaller files** - Faster processing
2. **Browser dev tools** - Monitor network tab
3. **Watch logs** - Check backend output for errors
4. **Cache results** - Avoid duplicate analyses
5. **Batch processing** - Process multiple files together

---

## 🚀 Next Steps

After everything is working:

1. **Test thoroughly** - Try different resume/JD combinations
2. **Add authentication** - Secure the API
3. **Deploy backend** - AWS, Heroku, Azure, etc.
4. **Deploy frontend** - Netlify, GitHub Pages, AWS S3
5. **Add analytics** - Track usage and improvements
6. **Create mobile app** - React Native or Flutter

---

## 🔐 Security Checklist

For production deployment:

- [ ] Move API key to serverless secrets manager
- [ ] Enable HTTPS/TLS
- [ ] Add authentication to API
- [ ] Implement rate limiting
- [ ] Add CORS restrictions
- [ ] Enable logging and monitoring
- [ ] Set up error tracking
- [ ] Regular security audits

---

## 📞 Quick Help

**Backend won't start?**
```bash
# Check port is free
netstat -ano | findstr :8000

# Try different port
python main.py --port 9000
```

**Frontend won't load?**
```bash
# Clear cache
# Ctrl+Shift+Delete in browser

# Hard refresh
# Ctrl+Shift+R in browser
```

**API connection error?**
```bash
# Test API directly
curl http://localhost:8000/api/health

# Check firewall
# Windows: Check Windows Defender Firewall
```

---

## 📚 Documentation

- [Backend README](../backend/README.md) - API documentation
- [Frontend README](./README.md) - Frontend documentation
- [API Reference](../API_REFERENCE.md) - Complete API docs
- [Quick Reference](../QUICK_REFERENCE.md) - One-page guide

---

## 🎉 Ready to Use!

You now have a complete RAG Resume Scorer system running!

**Start here:**
1. Terminal 1: `python backend/main.py`
2. Terminal 2: `python frontend/server.py`
3. Browser: http://localhost:3000

**Enjoy analyzing resumes!** 🚀
