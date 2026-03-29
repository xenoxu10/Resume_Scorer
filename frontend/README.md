# RAG Resume Scorer - Web Frontend

A modern, responsive web interface for the RAG Resume Scorer API.

## Features

✨ **Modern UI**
- Beautiful gradient design
- Smooth animations
- Responsive layout (mobile-friendly)
- Dark mode ready

📁 **Easy File Upload**
- Drag-and-drop support
- Support for PDF, DOCX, TXT files
- Clear visual feedback

📊 **Detailed Results Display**
- Visual score display (0-100)
- Color-coded interpretation
- Matching skills list
- Skills gap analysis
- AI-generated assessment

📝 **Text Input Option**
- Paste resume and JD as text
- Useful for quick testing
- No file upload required

📥 **Download Reports**
- Export analysis as HTML report
- Formatted and ready to share
- Printable format

## Files

```
frontend/
├── index.html          # Main HTML page
├── styles.css          # Styling (Tailwind-inspired)
├── script.js           # Frontend logic & API calls
├── server.py           # Simple Python HTTP server
└── README.md           # This file
```

## Getting Started

### Option 1: Python HTTP Server (Recommended)

```bash
# Make sure you're in the frontend directory
cd frontend

# Run the server
python server.py
```

The frontend will open automatically at `http://localhost:3000`

### Option 2: Use Any HTTP Server

```bash
# Using Python 3
python -m http.server 3000

# Using Node.js
npx http-server -p 3000

# Using PHP
php -S localhost:3000
```

### Option 3: Direct File Access

Simply open `index.html` in your web browser (limited functionality without a server)

## Usage

### 1. Start the Backend

Make sure the FastAPI backend is running:

```bash
cd backend
python main.py
```

Backend will be available at: `http://localhost:8000`

### 2. Start the Frontend

In a separate terminal:

```bash
cd frontend
python server.py
```

Frontend will open at: `http://localhost:3000`

### 3. Analyze a Resume

1. **Upload Files**
   - Click on the upload area or select files
   - Choose resume file (PDF, DOCX, or TXT)
   - Choose job description file
   - Click "Analyze Resume"

2. **Or Paste Text**
   - Click "Or paste text directly"
   - Paste resume content
   - Paste job description
   - Click "Analyze Text"

3. **View Results**
   - See your match score (0-100)
   - Review matching skills in green
   - Check skills to develop in orange
   - Read AI-generated assessment
   - Download report if needed

## API Integration

The frontend communicates with the backend API:

### Endpoints Used

**POST** `/api/analyze`
- Upload resume and JD files
- Returns: Score, matching skills, gaps, assessment

**POST** `/api/analyze-text`
- Analyze plain text input
- Returns: Score, matching skills, gaps, assessment

**GET** `/api/health`
- Check API availability
- Returns: Status

### Configuration

The API base URL is hardcoded in `script.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

Change this if your backend runs on a different URL.

## Customization

### Change Colors

Edit `styles.css`:

```css
:root {
    --primary-color: #6366f1;      /* Purple */
    --secondary-color: #10b981;    /* Green */
    --danger-color: #ef4444;       /* Red */
    --warning-color: #f59e0b;      /* Orange */
}
```

### Change Port

Edit `server.py`:

```python
PORT = 3000  # Change this to your desired port
```

### Change API URL

Edit `script.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000/api';  // Change as needed
```

### Modify Appearance

All styling is in `styles.css`. The design is responsive and uses:
- CSS Grid & Flexbox
- CSS Custom Properties (variables)
- CSS Animations
- Font Awesome icons

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance

- **Bundle Size**: ~50KB (HTML + CSS + JS combined)
- **No Dependencies**: Pure vanilla JavaScript
- **Fast Load Time**: All assets load quickly
- **Optimized**: Minimal reflows and repaints

## Troubleshooting

### "Unable to connect to the API"

**Cause:** Backend is not running

**Solution:**
```bash
cd backend
python main.py
```

### Files not uploading

**Cause:** File size too large or format not supported

**Solution:**
- Use PDF, DOCX, or TXT files only
- Keep files under 10MB
- Check file doesn't have special characters in name

### Styling looks broken

**Cause:** CSS file not loading

**Solution:**
- Check that `styles.css` is in the same directory as `index.html`
- Clear browser cache (Ctrl+Shift+Delete)
- Do a hard refresh (Ctrl+Shift+R)

### Icons not showing

**Cause:** Font Awesome CDN not loading

**Solution:**
- Check your internet connection
- Wait a few seconds for CDN to load
- Icons are non-essential, analysis will work without them

### Results not appearing

**Cause:** API error or network issue

**Solution:**
- Open browser console (F12)
- Check for error messages
- Make sure API key is set in `.env`
- Verify API is responding at http://localhost:8000/docs

## Mobile Optimization

The frontend is fully responsive:

- Mobile: Single column layout
- Tablet: Optimized spacing
- Desktop: Full featured UI

All buttons and inputs are touch-friendly on mobile devices.

## Accessibility

The frontend includes:
- Semantic HTML5
- ARIA labels where needed
- Keyboard navigation support
- Good color contrast
- Focus states on interactive elements

## Security Notes

⚠️ **Current Security**: Minimal (development environment)

For production:
1. Add HTTPS
2. Implement CORS properly
3. Add authentication
4. Validate all inputs
5. Rate limit API calls
6. Store API keys securely

## Advanced Features

### Adding Authentication

Add JWT token handling in `script.js`:

```javascript
const token = localStorage.getItem('auth_token');
const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
};
```

### Caching Results

Add to `script.js`:

```javascript
const cache = new Map();
function getCachedResult(key) {
    return cache.get(key);
}
```

### Local Storage

Save last analysis:

```javascript
localStorage.setItem('lastAnalysis', JSON.stringify(result));
```

## Development

### File Structure

```
index.html   - HTML structure & semantic markup
styles.css   - All styling (3000+ lines)
script.js    - JavaScript logic & API calls
```

### Key JavaScript Functions

- `analyzeFiles()` - Handle file upload
- `analyzeText()` - Handle text input
- `displayResults()` - Show results
- `downloadReport()` - Generate HTML report
- `getScoreInterpretation()` - Score meaning

### Key CSS Classes

- `.card` - Content container
- `.btn-primary` - Primary button
- `.skill-tag` - Matching skill badge
- `.gap-tag` - Gap skill badge
- `.score-card` - Score display

## Next Steps

1. ✅ Frontend created
2. ✅ Backend API running
3. → Test with sample data
4. → Deploy to production
5. → Add authentication
6. → Create mobile app
7. → Add analytics

## Deployment

### Deploy to Netlify

```bash
# Build (nothing to build, it's static)
# Just upload the frontend folder

# Or use Netlify CLI:
npm install -g netlify-cli
netlify deploy --dir=frontend
```

### Deploy to GitHub Pages

```bash
# Push the frontend folder to gh-pages branch
git subtree push --prefix frontend origin gh-pages
```

### Deploy to AWS S3

```bash
aws s3 sync frontend/ s3://your-bucket-name/
```

### Deploy with Python

```bash
# Use server.py with Gunicorn for production
pip install gunicorn
gunicorn --workers=4 server:httpd
```

## Support

- Backend Docs: http://localhost:8000/docs
- API Reference: http://localhost:8000/redoc
- Backend README: ../README.md
- Setup Guide: ../SETUP_COMPLETE.md

## License

Open source

---

**Backend & Frontend working together to score your resume! 🚀**
