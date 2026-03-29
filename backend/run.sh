#!/bin/bash
# Setup and run RAG Resume Scorer application

echo ""
echo "===================================="
echo "RAG Resume Scorer - Setup & Run"
echo "===================================="
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Please create a .env file with your OpenAI API key:"
    echo ""
    echo "OPENAI_API_KEY=your_api_key_here"
    echo ""
    read -p "Press enter to exit..."
    exit 1
fi

# Check if dependencies are installed
echo "Checking dependencies..."
pip list | grep -E "fastapi|uvicorn|openai" > /dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip install -r ../requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        read -p "Press enter to exit..."
        exit 1
    fi
fi

echo ""
echo "✓ Dependencies installed"
echo ""

# Run the application
echo "Starting RAG Resume Scorer..."
echo ""
echo "Server will be available at: http://localhost:8000"
echo "Documentation at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py
