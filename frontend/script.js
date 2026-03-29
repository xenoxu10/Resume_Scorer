/* ==========================================
   RAG Resume Scorer - JavaScript
   ========================================== */

const API_BASE_URL = 'http://localhost:8000/api';

// DOM Elements
const uploadForm = document.getElementById('uploadForm');
const resumeFile = document.getElementById('resumeFile');
const jdFile = document.getElementById('jdFile');
const resumeFileName = document.getElementById('resumeFileName');
const jdFileName = document.getElementById('jdFileName');
const submitBtn = document.getElementById('submitBtn');
const errorMessage = document.getElementById('errorMessage');

const resultsSection = document.getElementById('resultsSection');
const loadingState = document.getElementById('loadingState');
const resultsContent = document.getElementById('resultsContent');

const scoreValue = document.getElementById('scoreValue');
const scoreTitle = document.getElementById('scoreTitle');
const scoreDescription = document.getElementById('scoreDescription');
const assessmentText = document.getElementById('assessmentText');
const matchingSkillsList = document.getElementById('matchingSkillsList');
const gapsList = document.getElementById('gapsList');

const downloadBtn = document.getElementById('downloadBtn');
const newAnalysisBtn = document.getElementById('newAnalysisBtn');

const toggleTextInputBtn = document.getElementById('toggleTextInput');
const textInputForm = document.getElementById('textInputForm');
const resumeText = document.getElementById('resumeText');
const jdText = document.getElementById('jdText');
const analyzeTextBtn = document.getElementById('analyzeTextBtn');
const textErrorMessage = document.getElementById('textErrorMessage');

let currentResult = null;

// ==========================================
// Event Listeners
// ==========================================

// File input change handlers
resumeFile.addEventListener('change', (e) => {
    const fileName = e.target.files[0]?.name;
    resumeFileName.textContent = fileName ? `✓ ${fileName}` : '';
});

jdFile.addEventListener('change', (e) => {
    const fileName = e.target.files[0]?.name;
    jdFileName.textContent = fileName ? `✓ ${fileName}` : '';
});

// Form submission
uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!resumeFile.files[0]) {
        showError('Please select a resume file');
        return;
    }
    
    if (!jdFile.files[0]) {
        showError('Please select a job description file');
        return;
    }
    
    await analyzeFiles(resumeFile.files[0], jdFile.files[0]);
});

// Text input toggle
toggleTextInputBtn.addEventListener('click', () => {
    textInputForm.classList.toggle('show');
});

// Analyze text button
analyzeTextBtn.addEventListener('click', async () => {
    if (!resumeText.value.trim()) {
        showTextError('Please enter resume text');
        return;
    }
    
    if (!jdText.value.trim()) {
        showTextError('Please enter job description text');
        return;
    }
    
    await analyzeText(resumeText.value, jdText.value);
});

// Download button
downloadBtn.addEventListener('click', downloadReport);

// New analysis button
newAnalysisBtn.addEventListener('click', resetForm);

// ==========================================
// API Calls
// ==========================================

async function analyzeFiles(resumeFileObj, jdFileObj) {
    try {
        clearErrors();
        submitBtn.disabled = true;
        
        const formData = new FormData();
        formData.append('resume', resumeFileObj);
        formData.append('jd', jdFileObj);
        
        showLoading();
        
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Analysis failed');
        }
        
        const data = await response.json();
        currentResult = data.data;
        displayResults(data.data);
        
    } catch (error) {
        showError(`Error: ${error.message}`);
        hideLoading();
    } finally {
        submitBtn.disabled = false;
    }
}

async function analyzeText(resumeTextValue, jdTextValue) {
    try {
        clearTextErrors();
        analyzeTextBtn.disabled = true;
        
        showLoading();
        
        const response = await fetch(`${API_BASE_URL}/analyze-text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                resume_text: resumeTextValue,
                jd_text: jdTextValue
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Analysis failed');
        }
        
        const data = await response.json();
        currentResult = data.data;
        displayResults(data.data);
        
    } catch (error) {
        showTextError(`Error: ${error.message}`);
        hideLoading();
    } finally {
        analyzeTextBtn.disabled = false;
    }
}

// ==========================================
// Display Results
// ==========================================

function displayResults(result) {
    hideLoading();
    
    const score = result.score || 0;
    const assessment = result.assessment || 'Assessment complete';
    const matchingSkills = result.matching_skills || [];
    const gaps = result.gaps || [];
    
    // Update score
    scoreValue.textContent = score;
    
    // Update score interpretation
    const { title, description } = getScoreInterpretation(score);
    scoreTitle.textContent = title;
    scoreDescription.textContent = description;
    
    // Update assessment
    assessmentText.textContent = assessment;
    
    // Update matching skills
    matchingSkillsList.innerHTML = matchingSkills
        .slice(0, 10)
        .map(skill => `<div class="skill-tag">${escapeHtml(skill)}</div>`)
        .join('');
    
    if (matchingSkills.length === 0) {
        matchingSkillsList.innerHTML = '<p style="color: var(--text-light); margin: 0;">No matching skills found</p>';
    }
    
    // Update gaps
    gapsList.innerHTML = gaps
        .slice(0, 10)
        .map(gap => `<div class="gap-tag">${escapeHtml(gap)}</div>`)
        .join('');
    
    if (gaps.length === 0) {
        gapsList.innerHTML = '<p style="color: var(--text-light); margin: 0;">No significant gaps found</p>';
    }
    
    resultsContent.classList.remove('hidden');
}

function getScoreInterpretation(score) {
    if (score >= 90) {
        return {
            title: '🎉 Perfect Match!',
            description: 'Your resume excellently matches the job description. You\'re an ideal candidate!'
        };
    } else if (score >= 75) {
        return {
            title: '✨ Great Match!',
            description: 'Your resume is well-aligned with the job requirements. Consider addressing the gaps.'
        };
    } else if (score >= 60) {
        return {
            title: '👍 Good Match',
            description: 'Your resume covers most requirements. Focus on developing the missing skills.'
        };
    } else if (score >= 40) {
        return {
            title: '⚠️ Partial Match',
            description: 'Your resume meets some requirements. Consider gaining more relevant experience.'
        };
    } else {
        return {
            title: '📚 Building Your Path',
            description: 'Your resume needs significant alignment. Consider acquiring the key skills listed.'
        };
    }
}

function showLoading() {
    resultsSection.classList.remove('hidden');
    loadingState.classList.remove('hidden');
    resultsContent.classList.add('hidden');
    window.scrollTo(0, resultsSection.offsetTop - 100);
}

function hideLoading() {
    loadingState.classList.add('hidden');
}

// ==========================================
// Download Report
// ==========================================

function downloadReport() {
    if (!currentResult) return;
    
    const reportHTML = generateReportHTML(currentResult);
    const blob = new Blob([reportHTML], { type: 'text/html' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `resume-analysis-${Date.now()}.html`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

function generateReportHTML(result) {
    const score = result.score || 0;
    const assessment = result.assessment || '';
    const matchingSkills = result.matching_skills || [];
    const gaps = result.gaps || [];
    
    return `
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Resume Analysis Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; color: #333; }
            h1 { color: #6366f1; border-bottom: 2px solid #6366f1; padding-bottom: 10px; }
            h2 { color: #764ba2; margin-top: 25px; }
            .score-box {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                margin: 20px 0;
            }
            .score-value { font-size: 48px; font-weight: bold; }
            .skills, .gaps { display: flex; flex-wrap: wrap; gap: 10px; margin: 15px 0; }
            .tag {
                display: inline-block;
                padding: 8px 14px;
                border-radius: 20px;
                font-size: 14px;
            }
            .skill-tag { background: #d1fae5; color: #065f46; }
            .gap-tag { background: #fef3c7; color: #92400e; }
            .assessment { 
                background: #f0f9ff; 
                border-left: 4px solid #0284c7; 
                padding: 15px; 
                margin: 20px 0;
            }
            footer { 
                margin-top: 40px; 
                padding-top: 20px; 
                border-top: 1px solid #ddd; 
                font-size: 12px; 
                color: #666; 
            }
        </style>
    </head>
    <body>
        <h1>Resume Analysis Report</h1>
        
        <div class="score-box">
            <div class="score-value">${score}</div>
            <div>Match Score / 100</div>
        </div>
        
        <h2>Overall Assessment</h2>
        <div class="assessment">${assessment}</div>
        
        <h2>Matching Skills (${matchingSkills.length})</h2>
        <div class="skills">
            ${matchingSkills.map(skill => `<span class="tag skill-tag">${skill}</span>`).join('')}
        </div>
        
        <h2>Skills to Develop (${gaps.length})</h2>
        <div class="gaps">
            ${gaps.map(gap => `<span class="tag gap-tag">${gap}</span>`).join('')}
        </div>
        
        <footer>
            <p>Generated by RAG Resume Scorer on ${new Date().toLocaleString()}</p>
            <p>This report was automatically generated based on AI analysis.</p>
        </footer>
    </body>
    </html>
    `;
}

// ==========================================
// Form Management
// ==========================================

function resetForm() {
    uploadForm.reset();
    resumeFileName.textContent = '';
    jdFileName.textContent = '';
    resumeText.value = '';
    jdText.value = '';
    resultsSection.classList.add('hidden');
    clearErrors();
    clearTextErrors();
    window.scrollTo(0, 0);
}

// ==========================================
// Error Handling
// ==========================================

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
    console.error('Error:', message);
}

function showTextError(message) {
    textErrorMessage.textContent = message;
    textErrorMessage.classList.remove('hidden');
    console.error('Error:', message);
}

function clearErrors() {
    errorMessage.textContent = '';
    errorMessage.classList.add('hidden');
}

function clearTextErrors() {
    textErrorMessage.textContent = '';
    textErrorMessage.classList.add('hidden');
}

// ==========================================
// Utilities
// ==========================================

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ==========================================
// Batch Analysis
// ==========================================

// Batch DOM Elements
const toggleBatchMode = document.getElementById('toggleBatchMode');
const batchForm = document.getElementById('batchForm');
const batchResumesFile = document.getElementById('batchResumesFile');
const batchJdFile = document.getElementById('batchJdFile');
const batchResumesFileName = document.getElementById('batchResumesFileName');
const batchJdFileName = document.getElementById('batchJdFileName');
const batchSubmitBtn = document.getElementById('batchSubmitBtn');
const batchErrorMessage = document.getElementById('batchErrorMessage');
const batchResultsSection = document.getElementById('batchResultsSection');
const batchResultsContent = document.getElementById('batchResultsContent');
const rankingsTableBody = document.getElementById('rankingsTableBody');
const topCandidateContent = document.getElementById('topCandidateContent');
const newBatchAnalysisBtn = document.getElementById('newBatchAnalysisBtn');

// Batch mode toggle
if (toggleBatchMode) {
    toggleBatchMode.addEventListener('click', () => {
        const singleUploadSection = document.querySelector('.upload-section:has(#uploadForm)');
        const textInputSection = document.querySelector('.text-input-section');
        
        // Toggle visibility
        if (batchForm.classList.contains('hidden')) {
            // Show batch mode
            if (singleUploadSection) singleUploadSection.style.display = 'none';
            if (textInputSection) textInputSection.style.display = 'none';
            batchForm.classList.remove('hidden');
            toggleBatchMode.innerHTML = '<i class="fas fa-exchange-alt"></i> Switch to Single Analysis';
        } else {
            // Show single mode
            if (singleUploadSection) singleUploadSection.style.display = 'block';
            if (textInputSection) textInputSection.style.display = 'block';
            batchForm.classList.add('hidden');
            toggleBatchMode.innerHTML = '<i class="fas fa-layer-group"></i> Switch to Batch Analysis (Multiple Resumes)';
            clearBatchErrors();
        }
        
        window.scrollTo(0, 0);
    });
}

// Batch file input handlers
if (batchResumesFile) {
    batchResumesFile.addEventListener('change', (e) => {
        const count = e.target.files.length;
        if (batchResumesFileName) {
            if (count > 0) {
                const fileNames = Array.from(e.target.files)
                    .map(f => f.name)
                    .join(', ');
                batchResumesFileName.innerHTML = `<i class="fas fa-check" style="color: var(--secondary-color);"></i> ${count} file(s) selected: ${fileNames}`;
            } else {
                batchResumesFileName.innerHTML = '';
            }
        }
    });
}

if (batchJdFile) {
    batchJdFile.addEventListener('change', (e) => {
        const fileName = e.target.files[0]?.name;
        if (batchJdFileName) {
            batchJdFileName.textContent = fileName ? `✓ ${fileName}` : '';
        }
    });
}

// Batch form submission
if (batchForm) {
    batchForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (!batchResumesFile.files.length) {
            showBatchError('Please select at least one resume file');
            return;
        }
        
        if (!batchJdFile.files[0]) {
            showBatchError('Please select a job description file');
            return;
        }
        
        await analyzeBatch(Array.from(batchResumesFile.files), batchJdFile.files[0]);
    });
}

// Batch new analysis button
if (newBatchAnalysisBtn) {
    newBatchAnalysisBtn.addEventListener('click', resetBatchForm);
}

// Batch download report button
const downloadBatchReportBtn = document.getElementById('downloadBatchReportBtn');
if (downloadBatchReportBtn) {
    downloadBatchReportBtn.addEventListener('click', downloadBatchReport);
}

// Batch file analyze function
async function analyzeBatch(resumeFiles, jdFile) {
    try {
        clearBatchErrors();
        batchSubmitBtn.disabled = true;
        
        const formData = new FormData();
        
        // Append all resume files
        resumeFiles.forEach((file, index) => {
            formData.append(`resumes`, file);
        });
        
        formData.append('jd', jdFile);
        
        showBatchLoading();
        
        const response = await fetch(`${API_BASE_URL}/batch-analyze`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Batch analysis failed');
        }
        
        const data = await response.json();
        displayBatchResults(data.data);
        
    } catch (error) {
        showBatchError(`Error: ${error.message}`);
        hideBatchLoading();
    } finally {
        batchSubmitBtn.disabled = false;
    }
}

// Display batch results
function displayBatchResults(result) {
    hideBatchLoading();
    
    const candidates = result.candidates || [];
    
    if (candidates.length === 0) {
        showBatchError('No candidates to display');
        return;
    }
    
    // Sort by score descending
    candidates.sort((a, b) => b.score - a.score);
    
    // Add rank to each candidate
    candidates.forEach((candidate, index) => {
        candidate.rank = index + 1;
    });
    
    // Calculate summary statistics
    const scores = candidates.map(c => c.score);
    const totalCandidates = candidates.length;
    const averageScore = Math.round(scores.reduce((a, b) => a + b, 0) / totalCandidates);
    const highestScore = Math.max(...scores);
    const lowestScore = Math.min(...scores);
    
    // Calculate score distribution (0-20, 20-40, 40-60, 60-80, 80-100)
    const distributions = [
        { range: '0-20', min: 0, max: 20, color: '#ef4444' },
        { range: '20-40', min: 20, max: 40, color: '#f97316' },
        { range: '40-60', min: 40, max: 60, color: '#eab308' },
        { range: '60-80', min: 60, max: 80, color: '#84cc16' },
        { range: '80-100', min: 80, max: 100, color: '#10b981' }
    ];
    
    const distributionCounts = distributions.map(dist => ({
        ...dist,
        count: scores.filter(s => s >= dist.min && s < dist.max).length
    }));
    
    // Display summary
    const totalCandidatesEl = document.getElementById('totalCandidates');
    const averageScoreEl = document.getElementById('averageScore');
    const highestScoreEl = document.getElementById('highestScore');
    const lowestScoreEl = document.getElementById('lowestScore');
    
    if (totalCandidatesEl) totalCandidatesEl.textContent = totalCandidates;
    if (averageScoreEl) averageScoreEl.textContent = averageScore;
    if (highestScoreEl) highestScoreEl.textContent = highestScore;
    if (lowestScoreEl) lowestScoreEl.textContent = lowestScore;
    
    // Display score distribution
    const scoreDistributionEl = document.getElementById('scoreDistribution');
    if (scoreDistributionEl) {
        scoreDistributionEl.innerHTML = distributionCounts.map(dist => `
            <div class="distribution-item">
                <div class="distribution-label">${dist.range}</div>
                <div class="distribution-bar" style="background: linear-gradient(90deg, ${dist.color}, ${dist.color}cc);" data-percentage="${Math.round((dist.count / totalCandidates) * 100)}%"></div>
                <div class="distribution-count">${dist.count}</div>
            </div>
        `).join('');
    }
    
    // Display all candidate scores
    const allCandidatesScoresEl = document.getElementById('allCandidatesScores');
    if (allCandidatesScoresEl) {
        allCandidatesScoresEl.innerHTML = candidates.map((candidate, index) => {
            const scorePercentage = candidate.score;
            const interpretation = getScoreInterpretation(candidate.score);
            return `
                <div class="candidate-score-item">
                    <div class="score-item-header">
                        <div style="display: flex; align-items: center; flex: 1;">
                            <div class="score-item-rank">${candidate.rank}</div>
                            <div class="score-item-name">${escapeHtml(candidate.name || candidate.candidate_name)}</div>
                        </div>
                        <div class="score-item-score">${candidate.score}</div>
                    </div>
                    <div class="score-meter">
                        <div class="score-meter-fill" style="width: ${scorePercentage}%"></div>
                    </div>
                    <div class="score-item-interpretation">${interpretation.title}</div>
                </div>
            `;
        }).join('');
    }
    
    // Display top candidate
    if (topCandidateContent) {
        const topCandidate = candidates[0];
        topCandidateContent.innerHTML = `
            <div class="top-candidate-info">
                <div class="info-item">
                    <div class="info-label">Resume File</div>
                    <div class="info-value">${escapeHtml(topCandidate.name || topCandidate.candidate_name)}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Match Score</div>
                    <div class="info-value" style="color: var(--secondary-color);">${topCandidate.score}/100</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Assessment</div>
                    <div class="info-value" style="color: var(--secondary-color); font-size: 14px;">
                        ${getScoreInterpretation(topCandidate.score).title}
                    </div>
                </div>
            </div>
        `;
    }
    
    // Display rankings table
    if (rankingsTableBody) {
        rankingsTableBody.innerHTML = candidates.map((candidate, index) => `
            <tr>
                <td>
                    <span class="rank-badge ${getRankClass(index)}">${candidate.rank}</span>
                </td>
                <td>
                    <span class="candidate-name">${escapeHtml(candidate.name || candidate.candidate_name)}</span>
                </td>
                <td>
                    <span class="score-badge">${candidate.score}</span>
                </td>
                <td>
                    <span style="font-size: 14px; color: var(--text-light);">
                        ${getScoreInterpretation(candidate.score).title}
                    </span>
                </td>
                <td>
                    <div class="candidate-actions">
                        <button class="action-btn" onclick="window.resumeScorer.viewCandidateDetails('${index}')">
                            <i class="fas fa-eye"></i> Details
                        </button>
                        <button class="action-btn" onclick="window.resumeScorer.downloadCandidateReport('${index}', '${escapeHtml(candidate.name || candidate.candidate_name).replace(/'/g, "\\'")}')">
                            <i class="fas fa-download"></i> Report
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
    }
    
    // Show results section and content
    if (batchResultsSection) {
        batchResultsSection.classList.remove('hidden');
    }
    if (batchResultsContent) {
        batchResultsContent.classList.remove('hidden');
    }
    
    // Hide loading if shown
    const batchLoadingState = document.getElementById('batchLoadingState');
    if (batchLoadingState) {
        batchLoadingState.classList.add('hidden');
    }
    
    window.scrollTo(0, batchResultsSection.offsetTop - 100);
    
    // Store candidates for later use
    window.batchCandidates = candidates;
    
    // Log batch info for verification
    console.log(`✓ Batch Analysis Complete:`, {
        totalCandidates: totalCandidates,
        resumes: candidates.map(c => c.name || c.candidate_name),
        scores: candidates.map(c => c.score),
        averageScore: averageScore,
        highestScore: highestScore,
        lowestScore: lowestScore
    });
}

function getRankClass(index) {
    if (index === 0) return 'first';
    if (index === 1) return 'second';
    if (index === 2) return 'third';
    return '';
}

function showBatchLoading() {
    const batchLoadingState = document.getElementById('batchLoadingState');
    if (batchResultsSection) {
        batchResultsSection.classList.remove('hidden');
    }
    if (batchLoadingState) {
        batchLoadingState.classList.remove('hidden');
    }
    if (batchResultsContent) {
        batchResultsContent.classList.add('hidden');
    }
    window.scrollTo(0, batchResultsSection.offsetTop - 100);
}

function hideBatchLoading() {
    const batchLoadingState = document.getElementById('batchLoadingState');
    if (batchLoadingState) {
        batchLoadingState.classList.add('hidden');
    }
}

function resetBatchForm() {
    if (batchForm) {
        batchForm.reset();
    }
    if (batchResumesFileName) {
        batchResumesFileName.innerHTML = '';
    }
    if (batchJdFileName) {
        batchJdFileName.textContent = '';
    }
    if (batchResultsSection) {
        batchResultsSection.classList.add('hidden');
    }
    clearBatchErrors();
    window.scrollTo(0, 0);
}

function showBatchError(message) {
    if (batchErrorMessage) {
        batchErrorMessage.textContent = message;
        batchErrorMessage.classList.remove('hidden');
        console.error('Batch Error:', message);
    }
}

function clearBatchErrors() {
    if (batchErrorMessage) {
        batchErrorMessage.textContent = '';
        batchErrorMessage.classList.add('hidden');
    }
}

function viewCandidateDetails(index) {
    const candidate = window.batchCandidates[index];
    if (!candidate) return;
    
    // Create detailed view modal
    const candidateName = candidate.name || candidate.candidate_name;
    const detailsHTML = `
<div class="candidate-details-modal">
    <div class="modal-content">
        <div class="modal-header">
            <h2><i class="fas fa-file-alt"></i> #${candidate.rank} - ${escapeHtml(candidateName)}</h2>
            <button class="modal-close" onclick="document.querySelector('.candidate-details-modal').remove()">&times;</button>
        </div>
        
        <div class="modal-body">
            <div class="detail-section">
                <div class="detail-label">Match Score</div>
                <div class="detail-value score-value">${candidate.score}<span style="font-size: 14px; color: var(--text-light); margin-left: 8px;"> / 100</span></div>
            </div>
            
            <div class="detail-section">
                <div class="detail-label">Assessment</div>
                <div class="detail-value assessment-text">${escapeHtml(candidate.assessment)}</div>
            </div>
            
            <div class="detail-section">
                <div class="detail-label">✓ Matching Skills (${(candidate.matching_skills || []).length})</div>
                <div class="skills-container">
                    ${(candidate.matching_skills || []).length > 0 ? (candidate.matching_skills || []).map(skill => `<span class="skill-tag">${escapeHtml(skill)}</span>`).join('') : '<p style="color: var(--text-light); margin: 0;">No matching skills found</p>'}
                </div>
            </div>
            
            <div class="detail-section">
                <div class="detail-label">⚠ Skills to Develop (${(candidate.gaps || []).length})</div>
                <div class="skills-container">
                    ${(candidate.gaps || []).length > 0 ? (candidate.gaps || []).map(gap => `<span class="gap-tag">${escapeHtml(gap)}</span>`).join('') : '<p style="color: var(--text-light); margin: 0;">No significant gaps found</p>'}
                </div>
            </div>
        </div>
        
        <div class="modal-footer">
            <button class="btn btn-secondary" onclick="document.querySelector('.candidate-details-modal').remove()">Close</button>
            <button class="btn btn-primary" onclick="window.resumeScorer.downloadCandidateReport('${index}', '${escapeHtml(candidateName).replace(/'/g, "\\'")}'); document.querySelector('.candidate-details-modal').remove();"><i class="fas fa-download"></i> Download Report</button>
        </div>
    </div>
</div>
    `;
    
    const modal = document.createElement('div');
    modal.innerHTML = detailsHTML;
    document.body.appendChild(modal);
}

function downloadCandidateReport(index, candidateName) {
    const candidate = window.batchCandidates[index];
    if (!candidate) return;
    
    const reportHTML = `
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Candidate Analysis - ${candidateName}</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; color: #333; }
            h1 { color: #6366f1; border-bottom: 2px solid #6366f1; padding-bottom: 10px; }
            h2 { color: #764ba2; margin-top: 25px; }
            .score-box {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                margin: 20px 0;
            }
            .score-value { font-size: 48px; font-weight: bold; }
            .skills, .gaps { display: flex; flex-wrap: wrap; gap: 10px; margin: 15px 0; }
            .tag {
                display: inline-block;
                padding: 8px 14px;
                border-radius: 20px;
                font-size: 14px;
            }
            .skill-tag { background: #d1fae5; color: #065f46; }
            .gap-tag { background: #fef3c7; color: #92400e; }
            .rank-badge {
                display: inline-block;
                width: 40px;
                height: 40px;
                line-height: 40px;
                text-align: center;
                border-radius: 50%;
                background: #6366f1;
                color: white;
                font-weight: bold;
                margin-right: 10px;
            }
            .assessment { 
                background: #f0f9ff; 
                border-left: 4px solid #0284c7; 
                padding: 15px; 
                margin: 20px 0;
            }
            footer { 
                margin-top: 40px; 
                padding-top: 20px; 
                border-top: 1px solid #ddd; 
                font-size: 12px; 
                color: #666; 
            }
        </style>
    </head>
    <body>
        <div style="text-align: center;">
            <span class="rank-badge">#${candidate.rank}</span>
            <h1>${candidateName}</h1>
        </div>
        
        <div class="score-box">
            <div class="score-value">${candidate.score}</div>
            <div>Match Score / 100</div>
        </div>
        
        <h2>Overall Assessment</h2>
        <div class="assessment">${candidate.assessment || 'Assessment complete'}</div>
        
        <h2>Matching Skills (${(candidate.matching_skills || []).length})</h2>
        <div class="skills">
            ${(candidate.matching_skills || []).map(skill => `<span class="tag skill-tag">${skill}</span>`).join('')}
        </div>
        
        <h2>Skills to Develop (${(candidate.gaps || []).length})</h2>
        <div class="gaps">
            ${(candidate.gaps || []).map(gap => `<span class="tag gap-tag">${gap}</span>`).join('')}
        </div>
        
        <footer>
            <p>Generated by RAG Resume Scorer on ${new Date().toLocaleString()}</p>
            <p>This report was automatically generated based on AI analysis.</p>
        </footer>
    </body>
    </html>
    `;
    
    const blob = new Blob([reportHTML], { type: 'text/html' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `candidate-${candidateName.replace(/\s+/g, '-')}-${Date.now()}.html`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

// ==========================================
// Health Check
// ==========================================

async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (!response.ok) {
            console.warn('API health check failed');
        }
    } catch (error) {
        console.warn('Unable to connect to API. Make sure the backend is running:', error);
        showError('Unable to connect to the API. Please start the backend server at http://localhost:8000');
    }
}

function downloadBatchReport() {
    if (!window.batchCandidates || window.batchCandidates.length === 0) {
        return;
    }
    
    const candidates = window.batchCandidates;
    const scores = candidates.map(c => c.score);
    const totalCandidates = candidates.length;
    const averageScore = Math.round(scores.reduce((a, b) => a + b, 0) / totalCandidates);
    const highestScore = Math.max(...scores);
    const lowestScore = Math.min(...scores);
    
    const reportHTML = `
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Batch Resume Analysis Report</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; color: #333; background: #f5f5f5; }
            .container { max-width: 1000px; margin: 0 auto; background: white; padding: 40px; }
            h1 { color: #6366f1; border-bottom: 3px solid #6366f1; padding-bottom: 15px; margin: 0 0 30px 0; font-size: 28px; }
            h2 { color: #764ba2; margin-top: 30px; margin-bottom: 15px; border-bottom: 1px solid #e0e0e0; padding-bottom: 8px; font-size: 20px; }
            h3 { color: #333; margin-top: 20px; margin-bottom: 10px; font-size: 16px; }
            .summary-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 30px; }
            .summary-box { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; }
            .summary-label { font-size: 12px; opacity: 0.9; text-transform: uppercase; margin-bottom: 8px; }
            .summary-value { font-size: 32px; font-weight: bold; }
            .candidates-table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            .candidates-table th { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px; text-align: left; font-weight: 600; border: 1px solid #ddd; }
            .candidates-table td { padding: 12px; border: 1px solid #ddd; }
            .candidates-table tbody tr:nth-child(even) { background: #f9f9f9; }
            .candidates-table tbody tr:hover { background: #f0f0f0; }
            .rank-badge { display: inline-block; width: 28px; height: 28px; line-height: 28px; text-align: center; border-radius: 50%; background: #6366f1; color: white; font-weight: bold; font-size: 12px; }
            .score-high { color: #10b981; font-weight: bold; }
            .score-medium { color: #f59e0b; font-weight: bold; }
            .score-low { color: #ef4444; font-weight: bold; }
            .candidate-name { font-weight: 500; word-break: break-word; }
            .assessment { font-size: 13px; color: #666; }
            .distribution-table { width: 100%; margin: 20px 0; }
            .distribution-row { display: flex; align-items: center; margin-bottom: 12px; }
            .distribution-label { min-width: 80px; font-weight: 500; }
            .distribution-bar { flex: 1; height: 24px; background: linear-gradient(90deg, #667eea, #764ba2); border-radius: 4px; margin: 0 15px; position: relative; }
            .distribution-count { min-width: 40px; text-align: right; font-weight: 600; }
            .candidate-detail { background: #f9f9f9; padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #6366f1; }
            .candidate-detail h4 { margin: 0 0 10px 0; color: #333; font-size: 14px; }
            .detail-item { margin: 8px 0; font-size: 13px; }
            .detail-label { font-weight: 600; color: #666; }
            .detail-value { color: #333; }
            footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666; text-align: center; }
            .timestamp { color: #999; font-size: 11px; margin-top: 10px; }
            @media print {
                body { background: white; }
                .container { box-shadow: none; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Batch Resume Analysis Report</h1>
            
            <h2>Summary Statistics</h2>
            <div class="summary-grid">
                <div class="summary-box">
                    <div class="summary-label">Total Candidates</div>
                    <div class="summary-value">${totalCandidates}</div>
                </div>
                <div class="summary-box">
                    <div class="summary-label">Average Score</div>
                    <div class="summary-value">${averageScore}</div>
                </div>
                <div class="summary-box">
                    <div class="summary-label">Highest Score</div>
                    <div class="summary-value">${highestScore}</div>
                </div>
                <div class="summary-box">
                    <div class="summary-label">Lowest Score</div>
                    <div class="summary-value">${lowestScore}</div>
                </div>
            </div>
            
            <h2>All Candidates Rankings</h2>
            <table class="candidates-table">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Resume File</th>
                        <th>Score</th>
                        <th>Assessment</th>
                    </tr>
                </thead>
                <tbody>
                    ${candidates.map((candidate, index) => {
                        const scoreClass = candidate.score >= 80 ? 'score-high' : candidate.score >= 60 ? 'score-medium' : 'score-low';
                        const interpretation = getScoreInterpretation(candidate.score);
                        return `
                            <tr>
                                <td><span class="rank-badge">${candidate.rank}</span></td>
                                <td class="candidate-name">${escapeHtml(candidate.name || candidate.candidate_name)}</td>
                                <td class="${scoreClass}">${candidate.score}/100</td>
                                <td class="assessment">${interpretation.title}</td>
                            </tr>
                        `;
                    }).join('')}
                </tbody>
            </table>
            
            <h2>Detailed Candidate Analysis</h2>
            ${candidates.map((candidate, index) => `
                <div class="candidate-detail">
                    <h4>#${candidate.rank} - ${escapeHtml(candidate.name || candidate.candidate_name)}</h4>
                    <div class="detail-item">
                        <span class="detail-label">Score:</span>
                        <span class="detail-value">${candidate.score}/100</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Assessment:</span>
                        <span class="detail-value">${getScoreInterpretation(candidate.score).title}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Summary:</span>
                        <span class="detail-value">${escapeHtml(candidate.assessment)}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Matching Skills (${(candidate.matching_skills || []).length}):</span>
                        <span class="detail-value">${(candidate.matching_skills || []).join(', ') || 'None'}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Skills to Develop (${(candidate.gaps || []).length}):</span>
                        <span class="detail-value">${(candidate.gaps || []).join(', ') || 'None'}</span>
                    </div>
                </div>
            `).join('')}
            
            <footer>
                <p style="margin: 0;">Generated by RAG Resume Scorer</p>
                <p class="timestamp">${new Date().toLocaleString()}</p>
                <p style="margin: 10px 0 0 0; font-size: 11px;">This report was automatically generated based on AI analysis of ${totalCandidates} resume(s).</p>
            </footer>
        </div>
    </body>
    </html>
    `;
    
    const blob = new Blob([reportHTML], { type: 'text/html' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `batch-resume-analysis-${Date.now()}.html`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

// Run health check on load
document.addEventListener('DOMContentLoaded', checkAPIHealth);

// ==========================================
// Export Functions
// ==========================================

window.resumeScorer = {
    analyzeFiles,
    analyzeText,
    resetForm,
    downloadReport,
    analyzeBatch,
    resetBatchForm,
    viewCandidateDetails,
    downloadCandidateReport
};
