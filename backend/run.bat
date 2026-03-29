@echo off
REM Setup and run RAG Resume Scorer application

echo.
echo ====================================
echo RAG Resume Scorer - Setup & Run
echo ====================================
echo.

REM Check if .env exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please create a .env file with your OpenAI API key:
    echo.
    echo OPENAI_API_KEY=your_api_key_here
    echo.
    pause
    exit /b 1
)

REM Check if dependencies are installed
echo Checking dependencies...
pip list | findstr "fastapi uvicorn openai" > nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r ..\requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo ✓ Dependencies installed
echo.

REM Run the application
echo Starting RAG Resume Scorer...
echo.
echo Server will be available at: http://localhost:8000
echo Documentation at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py

pause
