#!/bin/bash

# Start RAG Resume Scorer Frontend

echo ""
echo "====================================="
echo "RAG Resume Scorer - Frontend Server"
echo "====================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7+ and try again"
    read -p "Press enter to exit..."
    exit 1
fi

echo "Starting frontend server on port 3000..."
echo ""
echo "Available at: http://localhost:3000"
echo "API at: http://localhost:8000"
echo ""
echo "Make sure the backend is running!"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python3 server.py
