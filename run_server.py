#!/usr/bin/env python3
"""
Production-ready server runner for Product Management API
Optimized for stability and performance
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Run the server with optimized settings"""
    
    # Set environment variables for thread optimization
    os.environ['OPENBLAS_NUM_THREADS'] = '1'
    os.environ['MKL_NUM_THREADS'] = '1'
    os.environ['NUMEXPR_NUM_THREADS'] = '1'
    os.environ['OMP_NUM_THREADS'] = '1'
    
    # Get port from environment or default
    port = os.getenv('PORT', '8001')
    host = os.getenv('HOST', '0.0.0.0')
    
    # Check if we should use Gunicorn (production) or Uvicorn (development)
    use_gunicorn = os.getenv('USE_GUNICORN', 'false').lower() == 'true'
    
    if use_gunicorn:
        print("🚀 Starting server with Gunicorn (Production Mode)")
        cmd = [
            'gunicorn',
            '--config', 'gunicorn.conf.py',
            'product_management:app'
        ]
    else:
        print("🔧 Starting server with Uvicorn (Development Mode)")
        print("💡 For production, set USE_GUNICORN=true")
        cmd = [
            'uvicorn',
            'product_management:app',
            '--host', host,
            '--port', port,
            '--workers', '1',  # Single worker to prevent thread explosion
            '--access-log',
            '--log-level', 'info'
        ]
    
    print(f"📡 Server will be available at http://{host}:{port}")
    print("🔧 Thread optimization: ENABLED")
    print("🗄️  Database pool: OPTIMIZED (1-5 connections)")
    print("⚡ Ready to serve requests!")
    print("-" * 50)
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Server command not found. Please install uvicorn or gunicorn:")
        print("   pip install uvicorn gunicorn")
        sys.exit(1)

if __name__ == "__main__":
    main()