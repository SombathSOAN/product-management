#!/usr/bin/env python3
"""
Production-ready server runner for Product Management API
Optimized for stability and performance
"""

import os
import sys
import subprocess
import socket
from pathlib import Path

def is_port_available(port, host='0.0.0.0'):
    """Check if a port is available"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, int(port)))
            return True
    except OSError:
        return False

def find_available_port(start_port=8001, host='0.0.0.0'):
    """Find the next available port starting from start_port"""
    port = start_port
    while port < start_port + 100:  # Try up to 100 ports
        if is_port_available(port, host):
            return str(port)
        port += 1
    raise RuntimeError(f"No available ports found starting from {start_port}")

def main():
    """Run the server with optimized settings"""
    
    # Set environment variables for thread optimization
    os.environ['OPENBLAS_NUM_THREADS'] = '1'
    os.environ['MKL_NUM_THREADS'] = '1'
    os.environ['NUMEXPR_NUM_THREADS'] = '1'
    os.environ['OMP_NUM_THREADS'] = '1'
    
    # Get port from environment or default
    requested_port = os.getenv('PORT', '8001')
    host = os.getenv('HOST', '0.0.0.0')
    
    # Check if requested port is available, if not find an alternative
    if is_port_available(requested_port, host):
        port = requested_port
        print(f"✅ Port {port} is available")
    else:
        print(f"⚠️  Port {requested_port} is already in use")
        port = find_available_port(int(requested_port), host)
        print(f"🔄 Using alternative port {port}")
    
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