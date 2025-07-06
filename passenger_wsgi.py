#!/usr/bin/env python3
"""
Passenger WSGI application for FastAPI on cPanel Cloud Hosting
Optimized for production deployment with PostgreSQL support
"""

import sys
import os
from pathlib import Path

# Add project directory to Python path
project_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_dir))

# Environment configuration for cloud hosting
os.environ.setdefault('ENVIRONMENT', 'production')
os.environ.setdefault('DEBUG', 'false')

# Database configuration - Update with your PostgreSQL credentials
# Format: postgresql://username:password@localhost/database_name
# You can also use SQLite as fallback: sqlite:///./product_management.db
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./product_management.db')
os.environ['DATABASE_URL'] = DATABASE_URL

# Thread optimization for shared hosting
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['NUMEXPR_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'

def application(environ, start_response):
    """
    Passenger WSGI application entry point
    """
    try:
        # Import FastAPI app
        from product_management import app
        
        # Handle the WSGI request
        return app(environ, start_response)
        
    except ImportError as e:
        # Handle import errors gracefully
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        
        error_msg = f"""
FastAPI Import Error: {str(e)}

Troubleshooting Steps:
1. Check if FastAPI is installed: python3 -c "import fastapi"
2. Install missing packages: python3 -m pip install --user fastapi uvicorn pydantic
3. Check Python path: {sys.path}
4. Check working directory: {os.getcwd()}
5. Check project files: {list(project_dir.glob('*.py'))}

Python Version: {sys.version}
Project Directory: {project_dir}
Environment: {os.environ.get('ENVIRONMENT', 'not set')}
Database URL: {DATABASE_URL}
"""
        return [error_msg.encode('utf-8')]
        
    except Exception as e:
        # Handle other errors
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        
        error_msg = f"""
Application Error: {str(e)}

System Information:
- Python Version: {sys.version}
- Working Directory: {os.getcwd()}
- Project Directory: {project_dir}
- Python Path: {sys.path}
- Environment Variables: {dict(os.environ)}

Please check the error logs for more details.
"""
        return [error_msg.encode('utf-8')]

# For testing the WSGI application
if __name__ == '__main__':
    print("🧪 Testing Passenger WSGI Application")
    print(f"📁 Project Directory: {project_dir}")
    print(f"🐍 Python Version: {sys.version}")
    print(f"📋 Python Path: {sys.path}")
    print(f"🗄️  Database URL: {DATABASE_URL}")
    
    try:
        from product_management import app
        print("✅ FastAPI app imported successfully")
        print("✅ Passenger WSGI application ready")
        
        # Test basic functionality
        print("\n🔍 Testing app components...")
        
        # Check if app has the expected attributes
        if hasattr(app, 'routes'):
            print(f"✅ Found {len(app.routes)} routes")
        
        if hasattr(app, 'openapi'):
            print("✅ OpenAPI documentation available")
            
        print("\n🎉 All tests passed! Application is ready for deployment.")
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Install FastAPI: python3 -m pip install --user fastapi uvicorn pydantic")
        print("2. Check file exists: ls -la product_management.py")
        print("3. Test import: python3 -c 'import product_management'")
        
    except Exception as e:
        print(f"❌ Application error: {e}")
        print("\n🔧 Check your FastAPI application for errors")