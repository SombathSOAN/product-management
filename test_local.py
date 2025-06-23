#!/usr/bin/env python3
"""
Test script to verify the FastAPI application works locally
"""
import subprocess
import sys
import time
import requests
from threading import Thread

def test_local_server():
    """Test the application locally"""
    print("🧪 Testing FastAPI application locally...")
    
    # Start the server in background
    print("📡 Starting local server...")
    try:
        # Test if we can import the app
        from product_management import app
        print("✅ Successfully imported FastAPI app")
        
        # Start uvicorn server
        import uvicorn
        
        def run_server():
            uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
        
        server_thread = Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Wait for server to start
        time.sleep(3)
        
        # Test endpoints
        base_url = "http://127.0.0.1:8000"
        
        print(f"🔍 Testing endpoints at {base_url}")
        
        # Test root/docs
        try:
            response = requests.get(f"{base_url}/docs", timeout=5)
            print(f"📄 /docs endpoint: {response.status_code}")
        except Exception as e:
            print(f"❌ /docs failed: {e}")
        
        # Test products endpoint
        try:
            response = requests.get(f"{base_url}/products", timeout=5)
            print(f"📦 /products endpoint: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Products count: {len(data)}")
        except Exception as e:
            print(f"❌ /products failed: {e}")
        
        # Test debug endpoint
        try:
            response = requests.get(f"{base_url}/products/debug", timeout=5)
            print(f"🐛 /products/debug endpoint: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Debug info: {data}")
        except Exception as e:
            print(f"❌ /products/debug failed: {e}")
            
        print("\n✅ Local testing completed!")
        print("🚀 If local tests pass, the issue is with Railway deployment/DNS")
        
    except ImportError as e:
        print(f"❌ Failed to import app: {e}")
        return False
    except Exception as e:
        print(f"❌ Error running local test: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🔧 FastAPI Application Test")
    print("=" * 40)
    
    # Check if required packages are installed
    try:
        import fastapi
        import uvicorn
        import requests
        print("✅ Required packages are installed")
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("💡 Install with: pip install fastapi uvicorn requests")
        sys.exit(1)
    
    # Run local test
    success = test_local_server()
    
    if success:
        print("\n📋 Next Steps:")
        print("1. Check Railway dashboard for deployment status")
        print("2. Look for the correct Railway-generated URL (usually *.railway.app)")
        print("3. Verify custom domain DNS settings if using e-catalog-dhhe.com")
        print("4. Check Railway deployment logs for any errors")
    else:
        print("\n🔧 Fix local issues first, then redeploy to Railway")