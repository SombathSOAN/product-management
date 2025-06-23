#!/usr/bin/env python3
"""
Comprehensive deployment status checker for Railway
"""

import requests
import time
from datetime import datetime

# Possible Railway URLs to test
POSSIBLE_URLS = [
    "https://product-management-production.up.railway.app",
    "https://web-production.up.railway.app", 
    "https://product-management-production-f7083ae4.up.railway.app",
    "https://web-production-f7083ae4.up.railway.app"
]

def test_url(url):
    """Test a single URL"""
    try:
        print(f"Testing: {url}")
        response = requests.get(f"{url}/health", timeout=10)
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            print(f"  ✅ SUCCESS: {response.json()}")
            return True
        else:
            print(f"  ❌ Response: {response.text[:200]}...")
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Connection error: {e}")
    return False

def main():
    print("=" * 60)
    print("RAILWAY DEPLOYMENT STATUS CHECKER")
    print("=" * 60)
    print(f"Check time: {datetime.now()}")
    print()
    
    success_found = False
    
    for url in POSSIBLE_URLS:
        if test_url(url):
            success_found = True
            print(f"\n🎉 WORKING URL FOUND: {url}")
            break
        print()
    
    if not success_found:
        print("🚨 No working URLs found. Possible issues:")
        print("1. Deployment is still in progress")
        print("2. Application failed to start")
        print("3. URL has changed")
        print("4. Railway service is down")
        print("\nRecommendations:")
        print("- Check Railway dashboard for deployment logs")
        print("- Verify the correct service URL")
        print("- Check if deployment is still building")

if __name__ == "__main__":
    main()