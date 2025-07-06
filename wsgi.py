#!/usr/bin/env python3
"""
WSGI adapter for FastAPI on shared hosting
Compatible with cPanel and most shared hosting providers
"""

import sys
import os
from pathlib import Path

# Add project directory to Python path
project_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_dir))

# Set environment variables for shared hosting
os.environ.setdefault('ENVIRONMENT', 'production')
os.environ.setdefault('DATABASE_URL', 'sqlite:///./product_management.db')

try:
    # Import FastAPI app
    from product_management import app
    
    # Create WSGI application
    def application(environ, start_response):
        """WSGI application entry point"""
        
        # Handle WSGI environment
        from fastapi.middleware.wsgi import WSGIMiddleware
        
        # Create WSGI middleware
        wsgi_app = WSGIMiddleware(app)
        
        # Call the WSGI app
        return wsgi_app(environ, start_response)
        
except ImportError as e:
    # Fallback error handler
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        error_msg = f"Import Error: {str(e)}\nPython Path: {sys.path}\nWorking Directory: {os.getcwd()}"
        return [error_msg.encode('utf-8')]

except Exception as e:
    # General error handler
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        error_msg = f"Application Error: {str(e)}\nPython Version: {sys.version}"
        return [error_msg.encode('utf-8')]

# For testing
if __name__ == '__main__':
    print("WSGI Application Test")
    print(f"Project Directory: {project_dir}")
    print(f"Python Path: {sys.path}")
    try:
        from product_management import app
        print("✅ FastAPI app imported successfully")
    except Exception as e:
        print(f"❌ Import failed: {e}")