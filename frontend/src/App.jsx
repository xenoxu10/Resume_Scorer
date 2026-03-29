import React, { useState } from 'react';
import './style.css';

export function App() {
  const [jdFile, setJdFile] = useState(null);
  const [resumeFiles, setResumeFiles] = useState([]);
  const [topK, setTopK] = useState(10);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [results, setResults] = useState([]);
  const [jdName, setJdName] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResults([]);

    if (!jdFile) {
      setError('Please select a JD file.');
      return;
    }
    if (!resumeFiles.length) {
      setError('Please select at least one resume file.');
      return;
    }

    const formData = new FormData();
    formData.append('jd', jdFile);
    for (const file of resumeFiles) {
      formData.append('resumes', file);
    }
    formData.append('top_k', String(topK));

    setLoading(true);
    try {
      const resp = await fetch('http://localhost:8000/api/score', {
        method: 'POST',
        body: formData,
      });
      const data = await resp.json();
      if (!resp.ok || data.error) {
        setError(data.error || 'Request failed');
      } else {
        setResults(data.results || []);
        setJdName(data.jd_name || '');
      }
    } catch (err) {
      setError(String(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Resume Scoring (React + FastAPI)</h1>
      <form onSubmit={handleSubmit}>
        <div className="field">
          <label>Job Description (PDF/TXT)</label>
          <input
            type="file"
            accept=".pdf,.txt"
            onChange={(e) => setJdFile(e.target.files?.[0] || null)}
          />
        </div>
        <div className="field">
          <label>Resumes (PDF/TXT, multiple)</label>
          <input
            type="file"
            accept=".pdf,.txt"
            multiple
            onChange={(e) => setResumeFiles(Array.from(e.target.files || []))}
          />
        </div>
        <div className="field">
          <label>Top K results</label>
          <input
            type="number"
            min={1}
            max={100}
            value={topK}
            onChange={(e) => setTopK(Number(e.target.value) || 1)}
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Scoring...' : 'Score Resumes'}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {!!results.length && (
        <div className="results">
          <h2>Results {jdName && `for ${jdName}`}</h2>
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Resume</th>
                <th>Score</th>
              </tr>
            </thead>
            <tbody>
              {results.map((r, idx) => (
                <tr key={r.name + idx}>
                  <td>{idx + 1}</td>
                  <td>{r.name}</td>
                  <td>{r.score.toFixed(2)}/100</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
