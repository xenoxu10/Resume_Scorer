#!/usr/bin/env python3
"""
Simple HTTP Server for RAG Resume Scorer Frontend
Serves the frontend on http://localhost:3000
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

PORT = 3000
FRONTEND_DIR = Path(__file__).parent.absolute()

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)
    
    def end_headers(self):
        # Prevent caching to get latest files
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Customize log format
        print(f"[Frontend] {format % args}")

if __name__ == "__main__":
    os.chdir(FRONTEND_DIR)
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print("\n" + "="*60)
        print("RAG Resume Scorer - Frontend Server")
        print("="*60)
        print(f"\n✓ Server running at: http://localhost:{PORT}")
        print(f"✓ Serving files from: {FRONTEND_DIR}")
        print(f"\n✓ Make sure backend is running at: http://localhost:8000")
        print("\nPress Ctrl+C to stop the server\n")
        
        # Try to open in browser
        try:
            webbrowser.open(f'http://localhost:{PORT}')
            print("Opening browser...\n")
        except:
            pass
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")
