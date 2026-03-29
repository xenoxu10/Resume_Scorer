@echo off
REM Start RAG Resume Scorer Frontend

echo.
echo =====================================
echo RAG Resume Scorer - Frontend Server
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

echo Starting frontend server on port 3000...
echo.
echo Available at: http://localhost:3000
echo API at: http://localhost:8000
echo.
echo Make sure the backend is running!
echo.
echo Press Ctrl+C to stop
echo.

python server.py

pause
