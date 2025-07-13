#!/usr/bin/env python3
import os
import subprocess
import sys

def main():
    port = os.environ.get('PORT', '8000')
    cmd = [
        'uvicorn', 
        'app.main:app', 
        '--host', '0.0.0.0', 
        '--port', port
    ]
    
    print(f"Starting server on port {port}")
    subprocess.run(cmd)

if __name__ == '__main__':
    main() 